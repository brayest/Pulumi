import sys
import json
import pulumi
import pulumi_aws as aws

# To be able to import general modules
sys.path.append('../../')
from modules.vpc import *
from modules.common import *
