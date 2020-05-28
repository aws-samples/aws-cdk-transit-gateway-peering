import boto3

client = boto3.client('ec2', region_name='us-east-1')

query = client.describe_transit_gateways(
    Filters=[
        {
            'Name': 'state',
            'Values': [
                'available',
            ]
        }
    ]
)

tgw_us_east_1=(query['TransitGateways'][0]['TransitGatewayId'])
account_id=(query['TransitGateways'][0]['OwnerId'])

client = boto3.client('ec2', region_name='eu-west-1')

query = client.describe_transit_gateways(
    Filters=[
        {
            'Name': 'state',
            'Values': [
                'available',
            ]
        }
    ]
)

tgw_eu_west_1=(query['TransitGateways'][0]['TransitGatewayId'])

response = client.create_transit_gateway_peering_attachment(
    TransitGatewayId=(tgw_eu_west_1),
    PeerTransitGatewayId=(tgw_us_east_1),
    PeerAccountId=(account_id),
    PeerRegion='us-east-1'
)