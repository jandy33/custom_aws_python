#!/usr/bin/python

import boto3
from datetime import datetime

class VpcTransitGateway:

    def __init__(self, accountName, requestId):
        self.accountName = accountName
        self.requestId = requestId
        
    def createTransitGateway(self):
        print("\nEntering Transit Gateway method")
        tgw_client = boto3.client('ec2')
        response = tgw_client.create_transit_gateway(
                Description = "TestingCreation",
                Options={'AmazonSideAsn': 65412,
                        'AutoAcceptSharedAttachments': 'enable',
                        'DefaultRouteTableAssociation': 'enable',
                        'DefaultRouteTablePropagation': 'enable',
                        'VpnEcmpSupport': 'enable',
                        'DnsSupport': 'enable', 
                        'MulticastSupport': 'disable'
                    },
                TagSpecifications=[{
                    #'client-vpn-endpoint'|'customer-gateway'|'dedicated-host'|'dhcp-options'|'elastic-ip'|'fleet'|'fpga-image'|'host-reservation'|'image'|'instance'|'internet-gateway'|'key-pair'|'launch-template'|'natgateway'|'network-acl'|'network-interface'|'placement-group'|'reserved-instances'|'route-table'|'security-group'|'snapshot'|'spot-fleet-request'|'spot-instances-request'|'subnet'|'traffic-mirror-filter'|'traffic-mirror-session'|'traffic-mirror-target'|'transit-gateway'|'transit-gateway-attachment'|'transit-gateway-multicast-domain'|'transit-gateway-route-table'|'volume'|'vpc'|'vpc-peering-connection'|'vpn-connection'|'vpn-gateway'|'vpc-flow-log',    
                    'ResourceType': 'transit-gateway',
                    'Tags': [{'Key': 'Account Name','Value': self.accountName},
                             {"Key": 'Request Id', 'Value': self.requestId},
                             {'Key': 'Name', 'Value': 'TGW Creation'}],
                    }],DryRun=False
            )
            
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        
        #response.wait_until_available()
        
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
                
        tgw_id = response['TransitGateway']['TransitGatewayId']
        print(response)
        
requestId = 'REQ1111'
accountName = 'Jim Anderson'
response = VpcTransitGateway(accountName, requestId)
VpcTransitGateway.createTransitGateway(response)


