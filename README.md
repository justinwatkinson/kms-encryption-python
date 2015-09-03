This is a simiple python script that will allow you to use the Amazon KMS service in conjunction with AWS DynamoDB to store and retrieve variables in encrypted form in a database that is easy to query and never has to store a key on disk.

# Prerequisites:
- Set up your Amazon environnment to already be ready for AWS API calls (e.g. add .aws directory or execute aws configure from CLI)
- Set up an AWS Dynamo DB table with a hash key:  env-variable-name (type is String)
    
#Usage:
##Decrypt: 
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
                            
##Encrypt:
    usage: encrypt.py [-h] -p PARAMETER_KEY [-v PARAMETER_VALUE]
                  [-f PARAMETER_FILE] -t DDB_TABLE -k KMS_KEY

    Encrypts a KMS DynamoDB key
    
    optional arguments:
      -h, --help            show this help message and exit
      -p PARAMETER_KEY, --parameter_key PARAMETER_KEY
                            Name of Parameter to put into DynamoDB
      -v PARAMETER_VALUE, --parameter_value PARAMETER_VALUE
                            Value of Parameter to put into DynamoDB. One of this
                            or parameter_file required.
      -f PARAMETER_FILE, --parameter_file PARAMETER_FILE
                            Location of file you want to upload (e.g. SSL private
                            key). One of this or parameter_value required.
      -t DDB_TABLE, --ddb_table DDB_TABLE
                            Name of existing DynamoDB Table to use in look-up
      -k KMS_KEY, --kms_key KMS_KEY
                            Name of AWS KMS Customer Master Key (ex: alias/test-
                            key)