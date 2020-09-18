import sys
import json
import pulumi
import pulumi_aws as aws

# To be able to import general modules
sys.path.append('../../')
from modules.vpc import *
from modules.common import *
from modules.ec2_autoscaling import *

# Load Parameters
config = pulumi.Config()

# Global Parameters
StackName = config.require('StackName')
Environment = config.require('Environment')
KeyName = config.require('KeyName')

# Network
CidrBlock = config.require('CidrBlock')
AvailabilityZones = []
for i in config.require_object("AvailabilityZones"):
    AvailabilityZones.append(i)
PublicSubnetsCidrs = []
for i in config.require_object("PublicSubnetsCidrs"):
    PublicSubnetsCidrs.append(i)
PrivateSubnetsCidr = []
for i in config.require_object("PrivateSubnetsCidr"):
    PrivateSubnetsCidr.append(i)

# Compute
Ec2AMI = config.require('Ec2AMI')
Ec2Size = config.require('Ec2Size')
KeyName = config.require('KeyName')
Ec2Role = config.require('Ec2Role')
AutoScalingDesiredCapacity = config.require('AutoScalingDesiredCapacity')

###################
# Create Base VPC
###################
vpc = VPC("{}-network".format(StackName), Environment, "Apps")
vpc.CreateBaseVpc(AvailabilityZones, CidrBlock, PublicSubnetsCidrs, InternetAccess=True)

# Create Private Subnets and Collect Public and Private IDs
PrivateSubnetsIds = []
PublicSubnetsIds = []
for i in range(0, len(AvailabilityZones)):
    vpc.CreatePrivateSubnet(AvailabilityZones[i], PrivateSubnetsCidr[i], "k8", i, InternetAccess=True)
    PrivateSubnetsIds.append(vpc.Get("PrivateSubnet-k8-{}".format(AvailabilityZones[i])).id)
    PublicSubnetsIds.append(vpc.Get("PublicSubnet-{}".format(AvailabilityZones[i])).id)

##################
# Auto Scaling
##################
autoscaling = AUTOSCALING("{}-compute".format(StackName), Environment, "Apps")
autoscaling.Create(
    Image_Id = Ec2AMI,
    InstanceSize = Ec2Size,
    KeyName = KeyName,
    Role = Ec2Role,
    VpcId = vpc.Get('Vpc').id,
    SubnetIds = PrivateSubnetsIds,
    DesiredCapacity=AutoScalingDesiredCapacity
)
