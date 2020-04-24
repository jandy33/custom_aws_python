#!/usr/bin/python

import boto3
import boto
import json
import array

domain_name = "ec2.internal"
domain_name_server = "1.1.1.0,1.1.2.0"

class VpcCreation:

    def __init__(self,requestId, requestType, accountName, network, cidr):
        print("Defining the Variables")
        self.requestId = requestId
        self.requestType = requestType
        self.accountName = accountName
        self.network = network
        self.cidr = cidr

    def createVpc(self):
        print('Entering createVpc method')
        ec2 = boto3.resource('ec2', region_name="us-east-1")
        vpc = ec2.create_vpc(CidrBlock=self.cidr)

        #Going to wait for the VPC to be created before adding any details
        vpc.wait_until_available()

        #Adding options to enable DNS Support
        if "default" in self.requestType:
            print("No Gateway Vpc")
        elif "vgw" in self.requestType:
            ec2Client = boto3.client('ec2')
            ec2Client.modify_vpc_tenancy(VpcId = vpc.id,  InstanceTenancy='default', DryRun=False)
            ec2Client.modify_vpc_attribute(VpcId = vpc.id, EnableDnsSupport = { 'Value': True })
            ec2Client.modify_vpc_attribute(VpcId = vpc.id, EnableDnsHostnames = { 'Value': True })

        #Adding tags of account name and request id to the tags
        vpc.create_tags(Tags=[{"Key": "Name", "Value" : self.accountName}])
        vpc.create_tags(Tags=[{"Key": "Request Id", "Value": self.requestId}])

        #Now set the DHCP options if available
        dhcp_options = boto3.client('ec2')
        response = dhcp_options.create_dhcp_options(
                DhcpConfigurations=[{'Key': 'domain-name', 'Values': [domain_name]},
                                    {'Key': 'domain-name-servers' , 'Values': [domain_name_server]} ]
            )
        for dhcp_results in response.values():
            if 'DhcpOptionsId' in dhcp_results:
               dhcp_options_id = dhcp_results['DhcpOptionsId']
        
        #Now going to associate the dhcp option to the VPC
        dhcp_options.associate_dhcp_options(DhcpOptionsId = dhcp_options_id, VpcId = vpc.id)
        
        #Now going to create tags associate to the dhcp option
        dhcp_options.create_tags(Resources=[dhcp_options_id], Tags=[{"Key": "Name", "Value" : self.accountName}])
        dhcp_options.create_tags(Resources=[dhcp_options_id], Tags=[{"Key": "Request Id", "Value": self.requestId}])
        
        print("\nCreate VPC for ",self.accountName)
        return vpc.id
