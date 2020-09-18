import pulumi
import pulumi_aws as aws
from modules.common import *

class VPC(pulumi.ComponentResource):
    """
    Create VPC with a specified number of subnets.
    """
    def __init__(self, name, environment, type, ops = None):
        super().__init__('pkg:index:VPC', Name, None, opts)
        self.name = name
        self.environment = environment
        self.type = type
        self.stack_name = "{}-{}-{}".format(name, environment, type)
        self.output = MapCreate()

    def Get(self, outputName=None):
        if outputName is not None:
            return self.output.get(outputName)
        else:
            return self.output

    def CreateBaseVpc(self, AvailabilityZones, CidrBlock, PublicSubnetsCidrs, InternetAccess=True):

        # Basic VPC Settings
        vpc = aws.ec2.Vpc(
            "Vpc-{}".format(self.stack_name),
            cidr_block =  CidrBlock,
            instance_tenancy = "default",
            enable_dns_support = True,
            enable_dns_hostnames = True,
            tags = {
                "Name": "VPC-{}".format(self.stack_name)
            },
        )
        self.output.put("Vpc", vpc)

        if InternetAccess:
            internetGw = aws.ec2.InternetGateway(
                "InternetGateway-{}".format(self.stack_name),
                vpc_id = vpc.id,
                tags = {
                    "Name": "IGW-{}".format(self.stack_name)
                }
            )
            self.output.put("InternetGateway", internetGw)

        dhcpOptions = aws.ec2.VpcDhcpOptions(
            "VpcDhcpOptions-{}".format(self.stack_name),
            domain_name = "advinow.int",
            domain_name_servers = ["AmazonProvidedDNS"],
            tags = {
                "Name": "VpcDhcpOptions-{}".format(self.stack_name)
            }
        )

        vpcOptionsAssociation = aws.ec2.VpcDhcpOptionsAssociation(
            "VpcDhcpOptionsAssociation-{}".format(self.stack_name),
            dhcp_options_id = dhcpOptions.id,
            vpc_id = vpc.id
        )

        # Default Public Routing
        if InternetAccess:
            publicRouteTable = aws.ec2.RouteTable(
                "PublicRouteTable-{}".format(self.stack_name),
                vpc_id = vpc.id,
                tags = {
                    "Name": "PublicRouteTable-{}".format(self.stack_name)
                }
            )
            self.output.put("PublicRouteTable", publicRouteTable)


            aws.ec2.Route(
                "PublicRoute-{}".format(self.stack_name),
                route_table_id = publicRouteTable.id,
                destination_cidr_block = "0.0.0.0/0",
                gateway_id = internetGw.id
            )

            # Create Public Subnets, Elastic IPs, NatGateways, and Route Associations
            for i in range(0, len(AvailabilityZones)):
                eip = aws.ec2.Eip(
                    "Eip-{}-{}".format(self.stack_name, AvailabilityZones[i]),
                    vpc = True,
                    tags = {
                        "Name": "Eip-{}-{}".format(self.stack_name, AvailabilityZones[i])
                    }
                )
                self.output.put("NatEip-{}".format(AvailabilityZones[i]), eip)

                subnet = aws.ec2.Subnet(
                    "PublicSubnet-{}-{}".format(self.stack_name, AvailabilityZones[i]),
                    vpc_id = vpc.id,
                    availability_zone = AvailabilityZones[i],
                    map_public_ip_on_launch = True,
                    cidr_block = PublicSubnetsCidrs[i],
                    tags = {
                        "Name": "PublicSubnet-{}".format(self.stack_name)
                    }
                )
                self.output.put("PublicSubnet-{}".format(AvailabilityZones[i]), subnet)

                nat = aws.ec2.NatGateway(
                    "NatGateway-{}-{}".format(self.stack_name, AvailabilityZones[i]),
                    subnet_id = subnet.id,
                    allocation_id = eip.id,
                    tags = {
                        "Name": "NatGateway-{}-{}".format(self.stack_name, i)
                    }
                )
                self.output.put("NatGateway-{}".format(AvailabilityZones[i]), nat)

                aws.ec2.RouteTableAssociation(
                    "PublicRouteTableAssociation-{}-{}".format(self.stack_name, AvailabilityZones[i]),
                    subnet_id = subnet.id,
                    route_table_id = publicRouteTable.id
                )

    def CreatePrivateSubnet(self, AvailabilityZone, SubnetsCidr, Type, Number, InternetAccess=True):
        privateSubnet = aws.ec2.Subnet(
            "PrivateSubnet-{}-{}-{}".format(self.stack_name, Type, Number),
            vpc_id = self.output.get('Vpc').id,
            availability_zone = AvailabilityZone,
            cidr_block = SubnetsCidr,
            tags = {
                "Name": "PrivateSubnet-{}-{}-{}".format(self.stack_name, Type, Number)
            }
        )
        self.output.put("PrivateSubnet-{}-{}".format(Type, AvailabilityZone), privateSubnet)

        privateRouteTable = aws.ec2.RouteTable(
            "PrivateRouteTable-{}-{}-{}".format(self.stack_name, Type, Number),
            vpc_id = self.output.get('Vpc').id,
            tags = {
                "Name": "PrivateRouteTable-{}-{}-{}".format(self.stack_name, Type, Number)
            }
        )
        self.output.put("PrivateRouteTable-{}-{}".format(Type, AvailabilityZone), privateRouteTable)

        routeTableAssociation = aws.ec2.RouteTableAssociation(
            "PrivateRouteTableAssociation-{}-{}-{}".format(self.stack_name, Type, Number),
            subnet_id = privateSubnet.id,
            route_table_id = privateRouteTable.id
        )

        if InternetAccess:
            route = aws.ec2.Route(
                "PrivateRoute-{}-{}-{}".format(self.stack_name, Type,Number),
                route_table_id = privateRouteTable.id,
                destination_cidr_block = "0.0.0.0/0",
                nat_gateway_id = self.output.get("NatGateway-{}".format(AvailabilityZone)).id,
            )
