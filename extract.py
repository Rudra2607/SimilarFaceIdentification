# Import everything needed to edit video clips
from moviepy.editor import *
import cv2
# loading video gfg
clip = VideoFileClip("Nihira.mp4")


# getting duration of the video
duration = clip.duration
# print(duration)
# saving a frame at 1 second
count=1
for i in range(1,int(duration)+1):
    clip.save_frame("frames/frame"+str(i)+".jpg", t = i)
    frame = clip.get_frame(i)
    hc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = hc.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in faces:
        fimg = frame[y:y+h,x:x+w]
        cv2.imwrite('faces/face'+str(count)+'_'+str(i)+'.jpg',fimg)
        count+=1
# # showing clip
# clip.ipython_display(width = 360)
frame = cv2.imread('nihi.jpg')
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
faces = hc.detectMultiScale(gray,1.3,5)
for (x,y,w,h) in faces:
    fimg = frame[y:y+h,x:x+w]
    cv2.imwrite('fff/fac.jpg',fimg)