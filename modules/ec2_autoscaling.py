import pulumi
import pulumi_aws as aws
from modules.common import *

class AUTOSCALING(pulumi.ComponentResource):
    """
    Create an autoscaling group of EC2 instances.
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

    def Create(self, Image_Id, InstanceSize, KeyName, Role, VpcId, SubnetIds, UserData="", DesiredCapacity=0, MaxSize=3, MinSize=0, IngressPolicy=None, EgressPolicy=None):

        instance_profile = aws.iam.InstanceProfile(
            "InstanceProfile-{}".format(self.stack_name),
            path = "/",
            role = Role
        )

        default_rule = [
            { 'protocol': 'tcp', 'from_port': 0, 'to_port': 65535, 'cidr_blocks': ["0.0.0.0/0"] },
            { 'protocol': 'udp', 'from_port': 0, 'to_port': 65535, 'cidr_blocks': ["0.0.0.0/0"] }
        ]
        securityGroup = aws.ec2.SecurityGroup(
            "SecurityGroup-{}".format(self.stack_name),
            description = "AutoScalingEc2SecurityGroup-{}".format(self.stack_name),
            name = "AutoScalingEc2SecurityGroup-{}".format(self.stack_name),
            vpc_id = VpcId,
            ingress = default_rule if IngressPolicy is None else IngressPolicy,
            egress = default_rule if EgressPolicy is None else EgressPolicy,
            tags = {
                "Name": "AutoScalingEc2SecurityGroup-{}".format(self.stack_name)
            }
        )
        self.output.put("SecurityGroup", securityGroup)

        launch_config = aws.ec2.LaunchConfiguration(
            "LaunchConfiguration-{}".format(self.stack_name),
            name_prefix="LaunchConfiguration-{}".format(self.stack_name),
            image_id=Image_Id,
            instance_type=InstanceSize,
            iam_instance_profile=instance_profile,
            security_groups=[securityGroup.id],
            key_name=KeyName,
            user_data=UserData,
            root_block_device= {
                'deleteOnTermination': 'true',
                'volumeType': 'gp2',
                'volume_size': 60
            }
        )
        self.output.put("LaunchConfiguration", launch_config)

        autoscaling_group = aws.autoscaling.Group(
            "AutoScalingGroup-{}".format(self.stack_name),
            vpc_zone_identifiers=SubnetIds,
            desired_capacity=DesiredCapacity,
            max_size=MaxSize,
            min_size=MinSize,
            default_cooldown=300,
            launch_configuration=launch_config.id,
            tags = [
                {
                    "Key": "Name",
                    "Value": "-{}".format(self.stack_name),
                    "propagateAtLaunch": True
                }
            ]
        )
        self.output.put("AutoScalingGroup", autoscaling_group)

        scaling_down_policy = aws.autoscaling.Policy(
            "AutoScalingPolicyDown-{}".format(self.stack_name),
            policy_type="StepScaling",
            adjustment_type="ChangeInCapacity",
            autoscaling_group_name=autoscaling_group.name,
            step_adjustments=[
                {
                    "scaling_adjustment" : -1,
                    "metricIntervalLowerBound" : 0
                }
            ],
        )

        scaling_up_policy = aws.autoscaling.Policy(
            "AutoScalingPolicyUp-{}".format(self.stack_name),
            policy_type="StepScaling",
            adjustment_type="ChangeInCapacity",
            autoscaling_group_name=autoscaling_group.name,
            step_adjustments=[
                {
                    "scaling_adjustment" : 1,
                    "metricIntervalLowerBound" : 0,
                    "metricIntervalUpperBound" : 500
                },
                {
                    "scaling_adjustment" : 2,
                    "metricIntervalLowerBound" : 500
                }
            ],
        )
