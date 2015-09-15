#!/usr/bin/python3
import boto3
import datetime
from Crypto import Random
from Crypto.Cipher import AES
import argparse

#Pads the data to suit the AES-256 encryption requirements
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[0:-ord(str(s[-1]))]

#Used to decrypt locally on this machine using the key decrypted from KMS
def local_decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_ECB, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return unpad(plaintext.decode('ASCII'))

#Used to decrypt the data key pulled from DynamoDB
def decrypt_kms_data(encrypted_data):
    decrypted = kms.decrypt(CiphertextBlob=encrypted_data)
    return decrypted

#Pull data from DynamoDB
def read_from_ddb():
    response = ddb.get_item(
        TableName=ddb_table_name,
        Key={
            'env-variable-name': {
                'S': parameter_key
            }
        }
    )
    return response

#Pulls/Formats the data from DDB
def get_encrypted_parameter():
    returned_variable_dict = read_from_ddb()
    returned_db_value = returned_variable_dict['Item']['env-variable-enc-value']['B']
    returned_db_kms_encrypted_key = returned_variable_dict['Item']['env-variable-enc-kms-key']['B']
    kms_decrypted_key = decrypt_kms_data(returned_db_kms_encrypted_key)['Plaintext']
    
    final_value = local_decrypt(returned_db_value, kms_decrypted_key)
    return final_value

#primary method when executed directly
if __name__ == '__main__':
    #Check user input
    parser = argparse.ArgumentParser(description='Decrypts a KMS DynamoDB key')
    parser.add_argument('-k','--kms_key', help='Name of AWS KMS Customer Master Key (ex: alias/test-key)',required=True)
    parser.add_argument('-p','--parameter_key', help='Name of Parameter in DynamoDB',required=True)
    parser.add_argument('-r','--region', help='Name of AWS Region to use for both KMS and DynamoDB',required=False)
    parser.add_argument('-t','--ddb_table', help='Name of existing DynamoDB Table to use in look-up',required=True)
    args = parser.parse_args()
    
    #set up and configure AWS client variables
    #NOTE:  If args.region is empty, it'll still use the local .aws if you've configured the AWS CLI, for example.
    kms = boto3.client('kms', region_name=args.region)
    ddb = boto3.client('dynamodb', region_name=args.region)
    
    #Decrypt the value after validation
    boto_master_key_id = args.kms_key
    ddb_table_name = args.ddb_table
    parameter_key = args.parameter_key
    cleartext_value = get_encrypted_parameter()
    print(cleartext_value)