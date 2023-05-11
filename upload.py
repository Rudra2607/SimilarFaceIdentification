import json
import boto3
from botocore.exceptions import NoCredentialsError
import cv2 
import os
import datetime

ACCESS_KEY = 'AKIA3XQ6MOP5NIQD5J7Q'
SECRET_KEY = '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'

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        # print("Upload Successful")
        return 'https://iamdngproject.s3.ap-south-1.amazonaws.com/'+s3_file
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
count=1
no_of_files=1
l = []
for file in os.listdir('faces'):
    no_of_files+=1
    l.append(file)


for i in l:
    f = upload_to_aws('faces/'+i,'iamdngproject','f'+i[4:])
# for img in os.listdir('faces'):
#     x = os.path.join('faces',img)
#     f = upload_to_aws(x,'iamdngproject','faceee'+str(count)+'.jpg')
#     count+=1
# f = upload_to_aws('fff/fac.jpg','iamdngproject','fc.jpg')