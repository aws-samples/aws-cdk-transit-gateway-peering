import boto3

client = boto3.client('ec2', region_name='us-east-1')

query = client.describe_transit_gateway_peering_attachments(
    Filters=[
        {
            'Name': 'state',
            'Values': [
                'pendingAcceptance',
            ]
        }
    ]
)

attachment_id=(query['TransitGatewayPeeringAttachments'][0]['TransitGatewayAttachmentId'])

response = client.accept_transit_gateway_peering_attachment(
    TransitGatewayAttachmentId=(attachment_id),
)