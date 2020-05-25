import os
from cv2 import cv2

directory = 'detect_test4'
parent_dir = '/Users/vanneswijaya/Python/KyraAbsen'
path = os.path.join(parent_dir, directory)
os.mkdir(path)

face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

img = cv2.imread('screenshot4.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.1, 4)

z = 1
width = 1000
height = 1000

for (x, y, w, h) in faces:
    crop = img[y:y+h, x:x+w]
    resized = cv2.resize(crop, (width, height))
    cv2.imwrite(f'{directory}/detected_resized{z}.png', resized)
    z += 1


 
