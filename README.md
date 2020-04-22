## AWS Transit Gateway Peering CDK Solution

Creating a global network with AWS Transit Gateway Peering and CDK

[IN PROGRESS]

Pre-requisites: 
- an AWS account
- Installed and authenticated AWS CLI
- Installed Python
- Installed AWS CDK

Using your device’s command line, check out the Git repository to a local directory on your device:

`git clone git@github.com:aws-samples/aws-cdk-transit-gateway-peering.git`

or

`git clone https://github.com/aws-samples/aws-cdk-transit-gateway-peering.git`

To manually create a virtualenv on MacOS and Linux:

`python3 -m venv .env`

After the init process completes and the virtualenv is created, you can use the following step to activate your virtualenv.

`source .env/bin/activate`

If you are a Windows platform, you would activate the virtualenv like this:

`.env\Scripts\activate.bat`

Once the virtualenv is activated, you can install the required dependencies.

`pip install -r requirements.txt`

At this point you can now synthesize the CloudFormation template for this code.

`cdk synth`

To deploy the solution

`cdk deploy '*'`

## License

This library is licensed under the MIT-0 License. See the LICENSE file.