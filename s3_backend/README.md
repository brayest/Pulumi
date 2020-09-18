# Pulumi AWS S3 backend bucket.

1. Download Pulumi: curl -fsSL https://get.pulumi.com | sh
2. AWS CLI needs to be in place: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html
3. Set the AWS profile to be used in current terminal  with export *AWS_PROFILE = profile*, of the desired AWS configuration.
4. Download this repository.
5. This repository is already a pulumi project. No need to create a new one.
6. Make sure to setup the environment `python3 -m venv venv`.
7. Activate it `source venv/bin/activate`.
8. And install the requirements `pip3 install -r requirements.txt`.
9. Just for the backend bucket creation use a local backend `pulumi login --local`
10. Execute `pulumi up` and the bucket will be created.
11. Set a password for the local pulumi backend, later you can set the ENV variable `export PULUMI_CONFIG_PASSPHRASE="PASSWORD"`.
12. Depending on how you name the stack, modify the pulumi YAML that was generated when creating the stack. 
