## Pulumi

Pulumi is an open source infrastructure as code tool for creating, deploying, and managing cloud infrastructure.

The language chosen to write the code is python.

In order to setup and manage an environment, it is necessary to follow this steps.

  1. Download pulumi : https://www.pulumi.com/docs/get-started/aws/install-pulumi/
    `curl -fsSL https://get.pulumi.com | sh`
  2. AWS CLI needs to be in place: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html   
  3. Set the AWS profile to be used in current terminal  with export *AWS_PROFILE = <your_profile>*, of the default AWS configuration is in place there is no need.
  4. Download this repository.
  5. This repository is already a pulumi project. No need to create a new one.
  6. Make sure to setup the environment `python3 -m venv venv`.
  7. Activate it `source venv/bin/activate`.
  8. And install the requirements `pip3 install -r requirements.txt`.
  5. pulumi login --cloud-url s3://<back_end_s3_bucket>
  9. Pulumi works with a password `export PULUMI_CONFIG_PASSPHRASE="PASSWORD"`
  10. Select or create the stack to use `pulumi stack init` or `pulumi stack select us-west-2`
  11. After installation the following command should work `pulumi refresh`, or `pulumi up`. Where the later is to create.


 Pulumi is not syntax based but pure integrated code, there for, some normal practices in infrastructure as code don't seem to be integrated. Included Output handling or variable interpolation across stacks. This was created coding it and manged in a similar way as a regular IaC.

The infrastructure consists of the following modules. Each module is a class that contains definitions for creation of the resources and the related AWS requirements for it to work. Some have methods that facilitate the integration with other modules or specific scenarios.