#!/bin/python
import boto3
import datetime
from Crypto import Random
from Crypto.Cipher import AES
import argparse

#Pads the data to suit the AES-256 encryption requirements
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[0:-ord(str(s[-1]))]

#set up AWS client variables
kms = boto3.client('kms')
ddb = boto3.client('dynamodb')

def local_encrypt(message, key, key_size=256):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_ECB, iv)
    return iv + cipher.encrypt(message)

def write_to_ddb(encrypted_value, encrypted_kms_key):
    ddb.put_item(
        TableName=ddb_table_name,
        Item={
            'env-variable-name': {
                'S': parameter_key
            },
            'env-variable-enc-value': {
                'B': encrypted_value
            },
            'env-variable-enc-kms-key': {
                'B': encrypted_kms_key
            }
        }
    )
    return

def encrypt_and_store():
    #Generate a key using KMS service
    data_key = kms.generate_data_key(KeyId=boto_master_key_id,KeySpec='AES_256') #I use the boto key's id
    encrypted_data_key = data_key['CiphertextBlob']
    plaintext_data_key = data_key['Plaintext']
    
    #encrypt data locally and write it to Dynamo
    encrypted_data = local_encrypt(parameter_value,plaintext_data_key)
    write_to_ddb(encrypted_data, encrypted_data_key)
    return

#primary method when executed directly
if __name__ == '__main__':
    #Check user input
    parser = argparse.ArgumentParser(description='Encrypts a KMS DynamoDB key')
    parser.add_argument('-p','--parameter_key', help='Name of Parameter to put into DynamoDB',required=True)
    parser.add_argument('-v','--parameter_value', help='Value of Parameter to put into DynamoDB',required=True)
    parser.add_argument('-t','--ddb_table', help='Name of existing DynamoDB Table to use in look-up',required=True)
    parser.add_argument('-k','--kms_key', help='Name of AWS KMS Customer Master Key (ex: alias/test-key)',required=True)
    args = parser.parse_args()
    
    #Decrypt the value after validation - sets global variables
    boto_master_key_id = args.kms_key
    ddb_table_name = args.ddb_table
    parameter_key = args.parameter_key
    parameter_value = args.parameter_value
    encrypt_and_store()
    