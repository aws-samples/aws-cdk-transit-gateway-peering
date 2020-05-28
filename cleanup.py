import boto3

client = boto3.client('ec2', region_name='us-east-1')

query = client.describe_transit_gateway_attachments(
    Filters=[
        {
            'Name': 'resource-type',
            'Values': [
                'peering',
            ]
        },
        {
            'Name': 'state',
            'Values': [
                'available',
            ]
        }
    ]
)

tgw_rt_id_us_east_1=(query['TransitGatewayAttachments'][0]['Association']['TransitGatewayRouteTableId'])

response = client.delete_transit_gateway_route(
    DestinationCidrBlock='172.16.1.0/24',
    TransitGatewayRouteTableId=(tgw_rt_id_us_east_1)
)

client = boto3.client('ec2', region_name='eu-west-1')

query = client.describe_transit_gateway_attachments(
    Filters=[
        {
            'Name': 'resource-type',
            'Values': [
                'peering',
            ]
        },
        {
            'Name': 'state',
            'Values': [
                'available',
            ]
        }
    ]
)

tgw_rt_id_eu_west_1=(query['TransitGatewayAttachments'][0]['Association']['TransitGatewayRouteTableId'])
tgw_attachment_id=(query['TransitGatewayAttachments'][0]['TransitGatewayAttachmentId'])

response = client.delete_transit_gateway_route(
    DestinationCidrBlock='172.16.0.0/24',
    TransitGatewayRouteTableId=(tgw_rt_id_eu_west_1)
)

response = client.delete_transit_gateway_peering_attachment(
    TransitGatewayAttachmentId=(tgw_attachment_id)
)