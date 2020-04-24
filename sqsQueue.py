#!/usr/bin/python

import boto3

class sqsQueue:

    def __init__(self):
        pass
    
    def get_queue_messages(self, queue_url):
        """
        """
        # Get the service resource for Simple Queue Service
        sqs = boto3.resource('sqs')

        # Get the queue from the database
        # Get the queue from AWS
        queue = sqs.get_queue_by_name(QueueName = 'JimQueue.fifo')

        #Storing the information into a dictionary
        customer_request = {}

        #Defined variable for the receipt handler
        receipt_handle = ''
        
        #Predefined the attributes that we are looking in the message body
        attributeNames = ['RequestId', 'RequestType', 'Network', 'AccountName']
        for attributeName in attributeNames:
            for message in queue.receive_messages(AttributeNames = ['All'], VisibilityTimeout=0,
                                                  WaitTimeSeconds=0, MessageAttributeNames = [attributeName]):
                receipt_handle = message.receipt_handle
                if attributeName in message.message_attributes:
                    print('\nFound attribute name = %s in message %s' % (attributeName, message.message_attributes))
                    customer_request.update({attributeName:message.message_attributes.get(attributeName).get('StringValue')})
                    print(customer_request)
                    
        # Insert into a database to include 
        # insert into cloud_request(request_id, request_type, network, account_name, status)
        #                  values(customer_request[RequestId], customer_request[RequestType], customer_request[Network],
        #                         customer_request[accountName], 'INPROGRESS' )
        # Delete message from queue
        #sqs.delete_message(queue_url='JimQueue',ReceiptHandle=receipt_handle)

        # return messages

    def get_fifo_queue(self,queue_url):
        # Get the service resource for Simple Queue Service
        sqs = boto3.resource('sqs')

        # Get the queue from the database
        # Get the queue from AWS
        queue = sqs.get_queue_by_name(QueueName = 'JimQueue.fifo')
        
        customer_request = {}
        #Predefined the attributes that we are looking in the message body
        attributeNames = ['RequestID', 'RequestType', 'Network', 'AccountName']
        for attributeName in attributeNames:
            for message in queue.receive_messages(AttributeNames=['All'],VisibilityTimeout=0,WaitTimeSeconds=0,MessageAttributeNames=[attributeName]):
                print(message.message_attributes)
                customer_request.update({attributeName:message.message_attributes.get(attributeName).get('StringValue')})
                print(customer_request)
            receipt_handle = message.receipt_handle
            print(receipt_handle)
            
queue_url = 'https://sqs.us-east-1.amazonaws.com/022984306546/JimQueue.fifo'
queue = sqsQueue()
#response = queue.get_queue_messages(queue_url)
response = queue.get_fifo_queue(queue_url)

