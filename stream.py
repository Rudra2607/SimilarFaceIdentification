import streamlit as st
import os
import boto3
from moviepy.editor import *
import cv2
from botocore.exceptions import NoCredentialsError
import json
import shutil
import datetime
from facepplib import FacePP,exceptions
# os.makedirs('fff')
ACCESS_KEY = 'AKIA3XQ6MOP5NIQD5J7Q'
SECRET_KEY = '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'
download_folder_path = 'videos'
frames_path = 'frames'
faces_path = 'faces'
check_path = 'fff'
vid = ''
img = ''
# Set the page title

face_detection = ""
face_comparing = ""
faceset_initialise = ""
face_search = ""
face_landmarks=""
dense_facial_landmarks=""
face_attributes=""
beauty_score_and_emotion_recognition=""



def checkkk(img1,img2):
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
        pass



def solve(app,img1,img2):
    # img_url1 = img1
    # img_url2 = img2
    cmp_ = app.compare.get(image_url1=img1,image_url2=img2)

    if cmp_.confidence>=70:
        # print('Same')
        return True
    else:
        return False
    


def get_file_url(bucket_name,access_key, secret_key,file_name):
    # Create a new session with your AWS credentials
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

    # Create an S3 client using the session
    s3_client = session.client('s3')

    # Generate the URL for the file
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': file_name},
        # ExpiresIn=360000  # URL expiration time in seconds (optional)
    )

    return url

def solve(bucket_name,access_key, secret_key):
    # Create a new session with your AWS credentials
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

    # Create an S3 client using the session
    s3_client = session.client('s3')

    # List the objects in the bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name)

    # Check if the bucket has objects
    if 'Contents' in response:
        # Count the number of objects
        file_count = len(response['Contents'])
        return file_count
    else:
        return 0


def get_files(bucket_name,access_key, secret_key):
    # Create a new session with your AWS credentials
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

    # Create an S3 client using the session
    s3_client = session.client('s3')

    # List the objects in the bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name)

    # Check if the bucket has objects
    if 'Contents' in response:
        # Count the number of objects
        files = [obj['Key'] for obj in response['Contents']]
        return files
    else:
        return []

st.set_page_config(page_title="Video Uploader")

# Add a file uploader to the page
uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])
import streamlit as st
cam=''
options = ["CAM 1", "CAM 2", "CAM 3"]
selected_option = st.radio("Choose an option", options)

# Do something based on the selected option
if selected_option == "CAM 1":
    # st.write("You selected Option 1")
    cam = 'feeed1'
elif selected_option == "CAM 2":
    # st.write("You selected Option 2")
    cam = 'feeed2'
elif selected_option == "CAM 3":
    cam = 'feeed3'
else:
    pass
    # st.write("You selected Option 3")

# If a file was uploaded
if uploaded_file is not None:
    vid = uploaded_file.name[:-4]
    # Display the file name and type
    st.write(f"Uploading file: {uploaded_file.name} ({uploaded_file.type})")

    # Play the uploaded video
    st.video(uploaded_file)

    download_button = st.download_button(
        label="Process",
        data=uploaded_file.getvalue(),
        file_name=uploaded_file.name,
        mime=uploaded_file.type
    )
    if download_button:
        if not os.path.exists(download_folder_path):
            os.makedirs(download_folder_path)

        # Save the uploaded file to the download folder
        with open(os.path.join(download_folder_path, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        clip = VideoFileClip(os.path.join('videos',uploaded_file.name))
        duration = clip.duration
        st.write(duration,"seconds")
        # st.write(uploaded_file.name[::-1])
        f_path = os.path.join(frames_path,uploaded_file.name[:-4])
        os.makedirs(f_path)
        fc_path = os.path.join(faces_path,uploaded_file.name[:-4])
        os.makedirs(fc_path)
        count=1
        for i in range(1,int(duration)+1):
            x = 'frame'+str(i)+'.jpg'
            y = os.path.join(f_path,x)
            clip.save_frame(y, t = i)
            frame = clip.get_frame(i)
            hc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = hc.detectMultiScale(gray,1.3,5)
            for (x,y,w,h) in faces:
                r = 'face'+str(count)+'_'+str(i)+'.jpg'
                ms = os.path.join(fc_path,r)
                fimg = frame[y:y+h,x:x+w]
                cv2.imwrite(ms,fimg)
                count+=1
        def upload_to_aws(local_file, bucket, s3_file):
            s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)

            try:
                s3.upload_file(local_file, bucket, s3_file)
            # print("Upload Successful")
                return 'https://'+bucket+'.s3.ap-south-1.amazonaws.com/'+s3_file
            except FileNotFoundError:
                print("The file was not found")
                return False
            except NoCredentialsError:
                print("Credentials not available")
                return False
        count=1
        no_of_files=1
        l = []
        for file in os.listdir(fc_path):
            no_of_files+=1
            l.append(file)
        for i in l:
            x = os.path.join(fc_path,i)
            fc=uploaded_file.name[:-4]
            f = upload_to_aws(x,cam,'fc'+i[4:])
        # s3 = boto3.client('s3')

        # bucket_name = uploaded_file.name[:-4]

        # s3.create_bucket(Bucket=bucket_name)
        # import boto3
    # import json

    # Set the name of the bucket and the policy

        st.success("Processed successfully!")

uploaded_file = st.file_uploader("Choose a Image file", type=[".png", ".jpeg", ".jpg"])
if uploaded_file is not None:
    # Display the file name and type
    st.write(f"Uploading file: {uploaded_file.name} ({uploaded_file.type})")
    img = uploaded_file.name[:-4]
    # Play the uploaded video
    st.image(uploaded_file)
    download_button = st.button("Process")
    def upload_to_aws(local_file, bucket,s3_file):
            s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
            try:
                s3.upload_file(local_file, bucket, s3_file)
            # print("Upload Successful")
                return 'https://'+bucket+'.s3.ap-south-1.amazonaws.com/'+s3_file
            except FileNotFoundError:
                print("The file was not found")
                return False
            except NoCredentialsError:
                print("Credentials not available")
                return False
    if download_button is not None:
        target = 'fff/'
        with open(target+uploaded_file.name,"wb") as f:
            shutil.copyfileobj(uploaded_file,f)
        f = upload_to_aws(target+uploaded_file.name,'searchh',uploaded_file.name[:-4]+'checkk.jpg')
st.success("Successful")

check = st.button('CHECK')
c1 = []
c2 = []
c3 = []
if check:
    if solve('feeed1',ACCESS_KEY,SECRET_KEY)==0:
        st.write('Camera 1 has no feed')
    else:
        st.write('No.of faces detected in Camera 1 feed are : '+str(solve('feeed1',ACCESS_KEY,SECRET_KEY)))
        c1 = get_files('feeed1',ACCESS_KEY,SECRET_KEY)
        st.write(c1)
    if solve('feeed2',ACCESS_KEY,SECRET_KEY)==0:
        st.write('Camera 2 has no feed')
    else:
        # pass
        st.write('No.of faces detected in Camera 2 feed are : '+str(solve('feeed2',ACCESS_KEY,SECRET_KEY)))
        c2 = get_files('feeed2',ACCESS_KEY,SECRET_KEY)
        st.write(c2)
    if solve('feeed3',ACCESS_KEY,SECRET_KEY)==0:
        st.write('Camera 3 has no feed')
    else:
        # pass
        st.write('No.of faces detected in Camera 3 feed are : '+str(solve('feeed3',ACCESS_KEY,SECRET_KEY)))
        c3 = get_files('feeed3',ACCESS_KEY,SECRET_KEY)
        st.write(c3)
clear = st.button("Clear")
if clear:
    shutil.rmtree(os.path.join('frames',vid))
    shutil.rmtree(os.path.join('faces',vid))
    shutil.rmtree('fff/')

tv1 = st.empty()
tv1.write("CAM 1 Output")

tv2 = st.empty()
tv2.write("CAM 2 Output")

tv3 = st.empty()
tv3.write("CAM 3 Output")

if st.button("CLICK HERE FOR THE OUTPUT"):
    c1 = get_files('feeed1',ACCESS_KEY,SECRET_KEY)
    tv1.write(c1)
    c2 = get_files('feeed2',ACCESS_KEY,SECRET_KEY)
    tv2.write(c2)
    c3 = get_files('feeed3',ACCESS_KEY,SECRET_KEY)
    tv3.write(c3)


if st.button('REVEAL'):
    def convert(seconds):
        time_delta = datetime.timedelta(seconds=seconds)
        datetime_obj = datetime.datetime(1, 1, 1) + time_delta
        hhmmss = datetime_obj.strftime('%H:%M:%S')

        return hhmmss

    face_detection = ""
    face_comparing = ""
    faceset_initialise = ""
    face_search = ""
    face_landmarks=""
    dense_facial_landmarks=""
    face_attributes=""
    beauty_score_and_emotion_recognition=""
    def solvee(bucket_name,access_key, secret_key):
    # Create a new session with your AWS credentials
        session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
        )

    # Create an S3 client using the session
        s3_client = session.client('s3')

    # List the objects in the bucket
        response = s3_client.list_objects_v2(Bucket=bucket_name)

    # Check if the bucket has objects
        if 'Contents' in response:
        # Count the number of objects
            file_count = len(response['Contents'])
            return file_count
        else:
            return 0
    def solve(app,img1,img2):
    # img_url1 = img1
    # img_url2 = img2
        cmp_ = app.compare.get(image_url1=img1,image_url2=img2)

        if cmp_.confidence>=70:
        # print('Same')
            return True
        else:
            return False
            
    def checkkk(img1,img2):
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
            pass



        

    cc = get_files('searchh',ACCESS_KEY,SECRET_KEY)

    y = 'https://'+'searchh'+'.s3.ap-south-1.amazonaws.com/'+cc[0]
    c1 = get_files('feeed1',ACCESS_KEY,SECRET_KEY)
    c2 = get_files('feeed2',ACCESS_KEY,SECRET_KEY)
    c3 = get_files('feeed3',ACCESS_KEY,SECRET_KEY)
    ch1 = []
    ch2 = []
    ch3 = []
    if solvee('feeed1',ACCESS_KEY,SECRET_KEY)==0:
        tv1.write('There is no feed in Cam 1')
    else:
        for i in c1:
        # x = get_file_url('feeed1',ACCESS_KEY,SECRET_KEY,i)
            x = 'https://'+'feeed1'+'.s3.ap-south-1.amazonaws.com/'+i
        # st.write(x)
        # st.write(x)
        # st.write(y)
        # st.write(checkkk(x,y))
        # st.write(checkkk(x,y))
    # for file in os.listdir(faces_path):
    #     f = os.path.join(faces_path,file)
    #     if os.path.isfile(f):
    #         os.remove(f)
    # for file in os.listdir(frames_path):
    #     f = os.path.join(frames_path,file)
    #     if os.path.isfile(f):
    #         os.remove(f)
    # for file in os.listdir(check_path):
    #     f = os.path.join(check_path,file)
    #     if os.path.isfile(f):
    #         os.remove(f)
        # ch1=[]
            if checkkk(x,y) is not None and checkkk(x,y)==True:
                ch1.append(i)
                break
        else:
            if ch1==[]:
                tv1.write('The Image is not found in Camera Feed 1')
            else:       
                x = ch1[0].index('_')
                fin = ch1[0][x+1:]
                inn = fin.index('.')
                fin = fin[:inn]
                # fin = int(fin)
                tv2.write(convert(int(fin)))
    if solvee('feeed2',ACCESS_KEY,SECRET_KEY)==0:
        tv2.write('There is no feed in Cam2')
    else:
        for i in c2:
            # x = get_file_url('feeed1',ACCESS_KEY,SECRET_KEY,i)
            x = 'https://'+'feeed2'+'.s3.ap-south-1.amazonaws.com/'+i
            # st.write(x)
            # st.write(x)
            # st.write(y)
            # st.write(checkkk(x,y))
            # st.write(checkkk(x,y))
        # for file in os.listdir(faces_path):
        #     f = os.path.join(faces_path,file)
        #     if os.path.isfile(f):
        #         os.remove(f)
        # for file in os.listdir(frames_path):
        #     f = os.path.join(frames_path,file)
        #     if os.path.isfile(f):
        #         os.remove(f)
        # for file in os.listdir(check_path):
        #     f = os.path.join(check_path,file)
        #     if os.path.isfile(f):
        #         os.remove(f)
            # ch1=[]
            if checkkk(x,y) is not None and checkkk(x,y)==True:
                ch2.append(i)
                break
        if ch2==[]:
            tv2.write('The Image is not found in Camera Feed 2')
        else:       
            x = ch2[0].index('_')
            fin = ch2[0][x+1:]
            inn = fin.index('.')
            fin = fin[:inn]
            # tv2.write(fin+' seconds...')
            # fin = int(fin)
            tv2.write(convert(int(fin)))
    if solvee('feeed3',ACCESS_KEY,SECRET_KEY)==0:
        tv3.write("There is no feed in CAM 3")
    else:
        for i in c3:
    #     # x = get_file_url('feeed1',ACCESS_KEY,SECRET_KEY,i)
            x = 'https://'+'feeed3'+'.s3.ap-south-1.amazonaws.com/'+i
    #     # st.write(x)
    #     # st.write(x)
    #     # st.write(y)
    #     # st.write(checkkk(x,y))
    #     # st.write(checkkk(x,y))
    # # for file in os.listdir(faces_path):
    # #     f = os.path.join(faces_path,file)
    # #     if os.path.isfile(f):
    # #         os.remove(f)
    # # for file in os.listdir(frames_path):
    # #     f = os.path.join(frames_path,file)
    # #     if os.path.isfile(f):
    # #         os.remove(f)
    # # for file in os.listdir(check_path):
    # #     f = os.path.join(check_path,file)
    # #     if os.path.isfile(f):
    # #         os.remove(f)
    #     # ch1=[]
            if checkkk(x,y) is not None and checkkk(x,y)==True:
                ch3.append(i)
                break
        if ch3==[]:
            tv3.write('The Image is not found in Camera Feed 3')
        else:       
            x = ch3[0].index('_')
            fin = ch3[0][x+1:]
            inn = fin.index('.')
            fin = fin[:inn]
            # fin = int(fin)
            tv3.write(convert(int(fin)))