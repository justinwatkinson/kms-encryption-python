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
#unpad = lambda s : s[0:-s[-1]]

'''
def pad(data):
    length = 16 - (len(data) % 16)
    data += bytes([length])*length
    return data

def unpad(data):
    data = data[:-data[-1]]
    return data
'''

#set up immutable variables
kms = boto3.client('kms')
ddb = boto3.client('dynamodb')

def local_decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_ECB, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return unpad(plaintext.decode('ASCII'))

def decrypt_kms_data(encrypted_data):
    #print('Start KMS Decrypt: ' + str(datetime.datetime.now()))
    decrypted = kms.decrypt(CiphertextBlob=encrypted_data)
    #print('End KMS Decrypt: ' + str(datetime.datetime.now()))
    #print('Decrypted Text: ',decrypted['Plaintext'])
    return decrypted

def read_from_ddb(env_var_name):
    response = ddb.get_item(
        TableName=ddb_table_name,
        Key={
            'env-variable-name': {
                'S': env_var_name
            }
        }
    )
    return response

def get_encrypted_parameter(p):
    #app.logger.info(p)
    returned_variable_dict = read_from_ddb(p)
    #app.logger.error(returned_variable_dict)
    returned_db_value = returned_variable_dict['Item']['env-variable-enc-value']['B']
    returned_db_kms_encrypted_key = returned_variable_dict['Item']['env-variable-enc-kms-key']['B']
    kms_decrypted_key = decrypt_kms_data(returned_db_kms_encrypted_key)['Plaintext']
    
    final_value = local_decrypt(returned_db_value, kms_decrypted_key)
    return final_value

#primary method when executed directly
if __name__ == '__main__':
    #Check user input
    parser = argparse.ArgumentParser(description='Decrypts a KMS DynamoDB key')
    parser.add_argument('-p','--parameter_key', help='Name of Parameter in DynamoDB',required=True)
    parser.add_argument('-t','--ddb_table', help='Name of existing DynamoDB Table to use in look-up',required=True)
    parser.add_argument('-k','--kms_key', help='Name of AWS KMS Customer Master Key (ex: alias/test-key)',required=True)
    args = parser.parse_args()
    
    #Decrypt the value after validation
    boto_master_key_id = args.kms_key
    ddb_table_name = args.ddb_table
    value = get_encrypted_parameter(args.parameter_key)
    print(value)