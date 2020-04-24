#!/usr/bin/python

import boto3
import ipaddr
import os

class VpcPeering:

    def __init__(self, requestId, from_accountName, from_vpcId, from_cidr, to_accountName, to_vpcId, to_cidr):
        print("Defining the Variables")
        self.requestId = requestId
        self.requester_accountName = from_accountName
        self.requester_vpcId = from_vpcId
        self.requester_cidr = from_cidr
        self.requester_accountId = 0
        self.accepter_accountName = to_accountName
        self.accepter_vpcId = to_vpcId
        self.accepter_cidr = to_cidr
        self.accepter_accountId = 0
        
    def createPeering(self):
        print("\nEntering vpc peering methond")
        ec2 = boto3.resource('ec2')

        #First thing we do is to check to see if the cidr's dont over lap each other
        results = self.overlappingCidr()
        if results:
            print("\nThe requestor account %s with the cidr address of %s seems to have over lapping cidr with acceptor account %s, cidr address %s " % (self.requester_accountName, self.requester_cidr, self.accepter_accountName, self.accepter_cidr))
            exit(1)

        requester_client = boto3.client('ec2')
        
        self.requester_accountId = boto3.client('sts').get_caller_identity()['Account']
        
        response = requester_client.create_vpc_peering_connection(
                DryRun = False,
                PeerOwnerId = self.requester_accountId,
                PeerVpcId = self.requester_vpcId,
                VpcId = self.accepter_vpcId,
                PeerRegion = 'us-east-1'
            )

        pcx_id = response['VpcPeeringConnection']['VpcPeeringConnectionId']
        ec2.create_tags(Resources=[pcx_id], Tags=[{"Key": "Name", "Value" : self.requester_accountName}])
        ec2.create_tags(Resources=[pcx_id], Tags=[{"Key": "Request Id", "Value": self.requestId}])

        #Allowing the accepter to accept the peering request
        accepter_client = boto3.client('ec2')
        target = accepter_client.accept_vpc_peering_connection(
                VpcPeeringConnectionId = pcx_id
            )
            
    def overlappingCidr(self):
        cidr1 = ipaddr.IPNetwork(self.requester_cidr)
        cidr2 = ipaddr.IPNetwork(self.accepter_cidr)
        
        response = cidr1.overlaps(cidr2)
        
        return response

requestId = 'REQ1111'
from_accountName = 'Jim Anderson'
from_vpcId = 'vpc-096fbc5d68b9b4686'
from_cidr = '192.168.10.0/24'
to_accountName = 'Jim Anderson'
to_vpcId = 'vpc-e05f4687'
to_cidr = '172.31.0.0/16'

response = VpcPeering(requestId, from_accountName, from_vpcId, from_cidr, to_accountName, to_vpcId, to_cidr)
print(response.accepter_accountName)
VpcPeering.createPeering(response)

