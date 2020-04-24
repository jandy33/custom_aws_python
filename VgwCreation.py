#!/usr/bin/python

import boto3

class VgwCreation:

    def __init__(self, requestId, accountName, vpcId):
        print("Defining the Variables")
        self.accountName = accountName
        self.requestId = requestId
        self.vpcId = vpcId

    def createVgw(self):
        print('Entering createVgw method')
        #Creating the resources needed to create the VGW
        ec2 = boto3.resource('ec2')
         
        #Creating the necessary code to create the Virtual Gateway
        vgw_options = boto3.client('ec2')
        response = vgw_options.create_vpn_gateway(
                AvailabilityZone = 'us-east-1',
                Type = 'ipsec.1',
                AmazonSideAsn = 65001
            )
        for vgw_results in response.values():
            if 'VpnGatewayId' in vgw_results:
                vgw_id = vgw_results['VpnGatewayId']

        vgw_options.attach_vpn_gateway(VpcId = self.vpcId, VpnGatewayId = vgw_id)
        ec2.create_tags(Resources=[vgw_id], Tags=[{"Key": "Name", "Value" : self.accountName}])
        ec2.create_tags(Resources=[vgw_id], Tags=[{"Key": "Request Id", "Value": self.requestId}])

        #Creating the necessary code to create the Customer Gateway
    	#Creating the first CGW
        cgw_client = boto3.client('ec2')
        
        cgw_count = 0
        cgw_array = []
        response = cgw_client.describe_customer_gateways()
        for header, info in response.items():
            if 'CustomerGateway' in header:
                for id in info:
                    if 'CustomerGatewayId' in id:
                        cgw_array.append(id.get('CustomerGatewayId'))
                        cgw_count += 1

        if len(cgw_array) != 2:
            cgw_count = 0
            cgw_array = []
  
            response = cgw_client.create_customer_gateway(
                    BgpAsn = 65011,
                    PublicIp = '1.1.1.0',
                    Type = 'ipsec.1'
                )
            for cgw_results in response.values():
                if 'CustomerGatewayId' in cgw_results:
                    cgw_id = cgw_results['CustomerGatewayId']
                    cgw_array.append(cgw_results['CustomerGatewayId'])
    
            ec2.create_tags(Resources=[cgw_id], Tags=[{"Key": "Name", "Value" : self.accountName}])
            ec2.create_tags(Resources=[cgw_id], Tags=[{"Key": "Request Id", "Value": self.requestId}])
    
    	    #Creating the second CGW
            cgw_count += 1
            response = cgw_client.create_customer_gateway(
                    BgpAsn = 65011,
                    PublicIp = '1.1.2.0',
                    Type = 'ipsec.1'
                )
            for cgw_results in response.values():
                if 'CustomerGatewayId' in cgw_results:
                    cgw_id = cgw_results['CustomerGatewayId']
                    cgw_array.append(cgw_results['CustomerGatewayId'])
    
            ec2.create_tags(Resources=[cgw_id], Tags=[{"Key": "Name", "Value" : self.accountName}])
            ec2.create_tags(Resources=[cgw_id], Tags=[{"Key": "Request Id", "Value": self.requestId}])
        
        #Creating the necessary code to create the Virtual Private Network
        #Creating the first VPN to match the first CGW
        vpn_options = boto3.client('ec2')
        response = vpn_options.create_vpn_connection(
                CustomerGatewayId = cgw_array[0], 
                Type = 'ipsec.1',
                VpnGatewayId = vgw_id
            )
        for vpn_results in response.values():
            if 'VpnConnectionId' in vpn_results:
                vpn_id = vpn_results['VpnConnectionId']

        ec2.create_tags(Resources=[vpn_id], Tags=[{"Key": "Name", "Value" : self.accountName}])
        ec2.create_tags(Resources=[vpn_id], Tags=[{"Key": "Request Id", "Value": self.requestId}])

        #Creating the second VPN to match the second CGW
        response = vpn_options.create_vpn_connection(
                CustomerGatewayId = cgw_array[1],
                Type = 'ipsec.1',
                VpnGatewayId = vgw_id
            )
        for vpn_results in response.values():
            if 'VpnConnectionId' in vpn_results:
              vpn_id = vpn_results['VpnConnectionId']

        ec2.create_tags(Resources=[vpn_id], Tags=[{"Key": "Name", "Value" : self.accountName}])
        ec2.create_tags(Resources=[vpn_id], Tags=[{"Key": "Request Id", "Value": self.requestId}])
