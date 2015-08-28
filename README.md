This is a simiple python script that will allow you to use the Amazon KMS service in conjunction with AWS DynamoDB to store variables in encrypted form in a database that is easy to query and never has to store a key on disk.

# Prerequisites:
- Set up your Amazon environnment to already be ready for AWS API calls (e.g. add .aws directory or execute aws configure from CLI)
- Set up an AWS Dynamo DB with a hash key:  env-variable-name (type is String)
    
#Usage:
##Decrypt -
    usage: decrypt.py [-h] -p PARAMETER_KEY -t DDB_TABLE -k KMS_KEY

    Decrypts a KMS DynamoDB key
    
    optional arguments:
      -h, --help            show this help message and exit
      -p PARAMETER_KEY, --parameter_key PARAMETER_KEY
                            Name of Parameter in DynamoDB
      -t DDB_TABLE, --ddb_table DDB_TABLE
                            Name of existing DynamoDB Table to use in look-up
      -k KMS_KEY, --kms_key KMS_KEY
                            Name of AWS KMS Customer Master Key (ex: alias/test-
                            key)