from aws_cdk import (core,
    aws_ec2 as ec2,
    aws_iam as iam,
)

class Ec2(core.Stack):

    def __init__(self, scope: core.Construct, id: str, network_stack: core.Stack, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create ServiceRole for EC2 instances; enable SSM usage
        ec2_instance_role = iam.Role(self, "Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")],
            description="This is a custom role for assuming the SSM role"
        )

        # Create security group
        ec2_sg = ec2.SecurityGroup(
            self,
            id='test-ec2-instance-sg',
            vpc=network_stack.vpc
        )

        # Create Ingress rule to allow ping
        ec2_sg.add_ingress_rule(
            ec2.Peer.ipv4('172.16.0.0/16'),
            ec2.Port.all_icmp()
        )

        # Create Instance
        ec2.Instance(self, 'Instance',
            role=ec2_instance_role,
            vpc=network_stack.vpc,
            instance_type=ec2.InstanceType.of(
                instance_class=ec2.InstanceClass.BURSTABLE3_AMD,
                instance_size=ec2.InstanceSize.NANO,
            ),
            machine_image=ec2.AmazonLinuxImage(
              generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            ),
            security_group=ec2_sg
        )

        # Set the default route on the subnets to the TGW
        for subnet in network_stack.vpc.isolated_subnets:
            ec2.CfnRoute(
                self,
                id='vpc-route-all-tgw',
                route_table_id=subnet.route_table.route_table_id,
                destination_cidr_block='0.0.0.0/0',
                transit_gateway_id=network_stack.tgw.ref
            )
