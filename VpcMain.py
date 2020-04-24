#!/usr/bin/python

from VpcCreation import VpcCreation
from VgwCreation import VgwCreation
from IgwCreation import IgwCreation

class VpcMain:
    
    def __init__(self, requestId, requestType, accountName, network, cidr):
        print("Defining the Variables")
        self.requestId = requestId
        self.requestType = requestType
        self.accountName = accountName
        self.network = network
        self.cidr = cidr
        self.vpcId = ""

#def main():
print("hello")
results = VpcMain("REQ12345", "createvpcvgw", "TestAccount", "network", "10.1.1.0/24")
print(results.accountName)
if "default" in results.requestType:
    vpc_id = VpcCreation.createVpc(results)
elif "vgw" in results.requestType:
    vpc_id = VpcCreation.createVpc(results)
    results.vpcId = vpc_id
    VgwCreation.createVgw(results)
elif "igw" in results.requestType:
    vpc_id = VpcCreation.createVpc(results)
    IgwCreation.createIgw((results))