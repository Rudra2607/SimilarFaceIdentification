import cv2 
import os
import datetime
# from __future__ import print_function,unicode_literals

# from imgix import UrlBuilder

import json

import boto3

from botocore.exceptions import NoCredentialsError

ACCESS_KEY = 'AKIA3XQ6MOP5NIQD5J7Q'
SECRET_KEY = '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'

face_detection = ""
face_comparing = ""
faceset_initialise = ""
face_search = ""
face_landmarks=""
dense_facial_landmarks=""
face_attributes=""
beauty_score_and_emotion_recognition=""

from facepplib import FacePP,exceptions


def check(img1,img2):
    # img1 = upload_to_aws('/frames/face1.jpg','iamdngproject','face1.jpg')
    api_key = 'xQLsTmMyqp1L2MIt7M3l0h-cQiy0Dwhl'
    api_secret = 'TyBSGw8NBEP9Tbhv_JbQM18mIlorY6-D'
    try:
        app_ = FacePP(api_key=api_key,api_secret = api_secret)
        funcs = [
            face_detection,
            solve,
            faceset_initialise,
            face_search,
            face_landmarks,
            dense_facial_landmarks,
            face_attributes,
            beauty_score_and_emotion_recognition]
        return solve(app_,img1,img2)
    except exceptions.BaseFacePPError as e:
        print(e)


def solve(app,img1,img2):
    # img_url1 = img1
    # img_url2 = img2
    cmp_ = app.compare.get(image_url1=img1,image_url2=img2)

    if cmp_.confidence>=70:
        # print('Same')
        return 'Same'
    else:
        return 'Not Same'
        # print('Not Same')

frame = cv2.imread('nihi.jpg')
hc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
faces = hc.detectMultiScale(gray,1.3,5)
for (x,y,w,h) in faces:
    fimg = frame[y:y+h,x:x+w]
    cv2.imwrite('fff/fac.jpg',fimg)
    # count+=1
flag=False
ans = -1
l=[]
for file in os.listdir('faces'):
    l.append(file[4:])
y = 'https://iamdngproject.s3.ap-south-1.amazonaws.com/fc.jpg'
for i in l:
    x = 'https://iamdngproject.s3.ap-south-1.amazonaws.com/f'+i
    # y = 'https://iamdngproject.s3.ap-south-1.amazonaws.com/fc.jpg'
    if check(x,y) == 'Same':
        flag=True
        ans=i[2:]
        break
if flag==True:
    print('Face found at Face '+(ans))
else:
    print('Face not found')

