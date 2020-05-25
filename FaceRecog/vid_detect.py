import os
from cv2 import cv2

frame_dir = 'frames_saved3'
detect_dir = 'frames_detected3'
parent_dir = '/Users/vanneswijaya/Python/KyraAbsen'
path1 = os.path.join(parent_dir, frame_dir)
path2 = os.path.join(parent_dir, detect_dir)
os.mkdir(path1)
os.mkdir(path2)

cap = cv2.VideoCapture('vid.mp4')

time_skips = 1800000

count = 1

cap.set(cv2.CAP_PROP_POS_MSEC, 60000)

while True:
    try:
        success, image = cap.read()
        cv2.imwrite(f'{frame_dir}/frame{count}.jpg', image)  
        cap.set(cv2.CAP_PROP_POS_MSEC,(count*time_skips))      
        count += 1
    except:
        break

print('FRAMES SAVED')

face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
a = 1

while True:
    try:
        img = cv2.imread(f'{frame_dir}/frame{a}.jpg')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        z = 1
        width = 1000
        height = 1000

        for (x, y, w, h) in faces:
            crop = img[y-50:y+h+50, x-50:x+w+50]
            resized = cv2.resize(crop, (width, height))
            cv2.imwrite(f'{detect_dir}/frame{a}_detected{z}.jpg', resized)
            z += 1

        a += 1
    except:
        break

print ('FRAMES DETECTED')