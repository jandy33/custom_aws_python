#!/usr/bin/python

import boto3

class IgwCreation:

    def __init__(self, requestId, accountName,vpcId):
        print("Defining the Variables")
        self.accountName = accountName
        self.requestId = requestId
        self.vpcId = vpcId

    def createIgw(self):
        print('Entering createIgw method')
        #Creating the resources needed to create the IGW
        ec2 = boto3.resource('ec2')
        igw = ec2.create_internet_gateway()
        
        #Creating the clien need to attach the IGW to the VPC
        igw_client = boto3.client('ec2')
        response = igw_client.attach_internet_gateway(
                DryRun = False,
                InternetGatewayId = igw.id, 
                VpcId = self.vpcId
            )
        
        ec2.create_tags(Resources=[igw.id], Tags=[{"Key": "Name", "Value" : self.accountName}])
        ec2.create_tags(Resources=[igw.id], Tags=[{"Key": "Request Id", "Value": self.requestId}])
        