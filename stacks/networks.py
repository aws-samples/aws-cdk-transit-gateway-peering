from aws_cdk import core
import aws_cdk.aws_ec2 as ec2

class Network(core.Stack):

    def __init__(self, scope: core.Construct, id: str, cidr_range: str, tgw_asn: int, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # VPC Creation
        self.vpc = ec2.Vpc(self,
            f"{kwargs['env']['region']}-vpc",
            max_azs=1,
            cidr=cidr_range,
            # configuration will create 1 subnet in a single AZ.
            subnet_configuration=[ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.ISOLATED,
                    name="Isolated",
                    cidr_mask=25
                    )
            ]
        )

        # Transit Gateway creation
        self.tgw = ec2.CfnTransitGateway(
            self,
            id=f"TGW-{kwargs['env']['region']}",
            amazon_side_asn=tgw_asn,
            auto_accept_shared_attachments="enable",
            default_route_table_association="enable",
            default_route_table_propagation="enable",
            tags=[core.CfnTag(key='Name', value=f"tgw-{kwargs['env']['region']}")]
        )

        # Transit Gateway attachment to the VPC
        self.tgw_attachment = ec2.CfnTransitGatewayAttachment(
            self,
            id=f"tgw-vpc-{kwargs['env']['region']}",
            transit_gateway_id=self.tgw.ref,
            vpc_id=self.vpc.vpc_id,
            subnet_ids=[subnet.subnet_id for subnet in self.vpc.isolated_subnets],
            tags=[core.CfnTag(key='Name', value=f"tgw-{self.vpc.vpc_id}-attachment")]
        )

        # VPC Endpoint creation for SSM (3 Endpoints needed)
        ec2.InterfaceVpcEndpoint(
            self,
            "VPCe - SSM",
            service=ec2.InterfaceVpcEndpointService(
                core.Fn.sub("com.amazonaws.${AWS::Region}.ssm")
            ),
            private_dns_enabled=True,
            vpc=self.vpc,
        )

        ec2.InterfaceVpcEndpoint(
            self,
            "VPCe - EC2 Messages",
            service=ec2.InterfaceVpcEndpointService(
                core.Fn.sub("com.amazonaws.${AWS::Region}.ec2messages")
            ),
            private_dns_enabled=True,
            vpc=self.vpc,
        )

        ec2.InterfaceVpcEndpoint(
            self,
            "VPCe - SSM Messages",
            service=ec2.InterfaceVpcEndpointService(
                core.Fn.sub("com.amazonaws.${AWS::Region}.ssmmessages")
            ),
            private_dns_enabled=True,
            vpc=self.vpc,
        )
