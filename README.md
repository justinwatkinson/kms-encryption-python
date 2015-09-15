This is a simiple python script that will allow you to use the Amazon KMS service in conjunction with AWS DynamoDB to store and retrieve variables in encrypted form in a database that is easy to query and never has to store a key on disk.

# Prerequisites:
- Set up your Amazon environnment to already be ready for AWS API calls (e.g. add .aws directory or execute aws configure from CLI)
- Set up an AWS Dynamo DB table with a hash key:  env-variable-name (type is String)
    
#Usage:
##Decrypt: 
    usage: decrypt.py [-h] -k KMS_KEY -p PARAMETER_KEY [-r REGION] -t DDB_TABLE
    
    Decrypts a KMS DynamoDB key
    
    optional arguments:
      -h, --help            show this help message and exit
      -k KMS_KEY, --kms_key KMS_KEY
                            Name of AWS KMS Customer Master Key (ex: alias/test-
                            key)
      -p PARAMETER_KEY, --parameter_key PARAMETER_KEY
                            Name of Parameter in DynamoDB
      -r REGION, --region REGION
                            Name of AWS Region to use for both KMS and DynamoDB
      -t DDB_TABLE, --ddb_table DDB_TABLE
                            Name of existing DynamoDB Table to use in look-up
                            
##Encrypt:
    usage: encrypt.py [-h] [-f PARAMETER_FILE] -k KMS_KEY -p PARAMETER_KEY
                      [-r REGION] -t DDB_TABLE [-v PARAMETER_VALUE]
    
    Encrypts a KMS DynamoDB key
    
    optional arguments:
      -h, --help            show this help message and exit
      -f PARAMETER_FILE, --parameter_file PARAMETER_FILE
                            Location of file you want to upload (e.g. SSL private
                            key). One of this or parameter_value required.
      -k KMS_KEY, --kms_key KMS_KEY
                            Name of AWS KMS Customer Master Key (ex: alias/test-
                            key)
      -p PARAMETER_KEY, --parameter_key PARAMETER_KEY
                            Name of Parameter to put into DynamoDB
      -r REGION, --region REGION
                            Name of AWS Region to use for both KMS and DynamoDB
      -t DDB_TABLE, --ddb_table DDB_TABLE
                            Name of existing DynamoDB Table to use in look-up
      -v PARAMETER_VALUE, --parameter_value PARAMETER_VALUE
                            Value of Parameter to put into DynamoDB. One of this
                            or parameter_file required.