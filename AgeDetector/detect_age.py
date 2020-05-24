import os
from cv2 import cv2

AGE_BUCKETS = ["(0-2)", "(4-6)", "(8-12)", "(15-20)", "(25-32)",
	"(38-43)", "(48-53)", "(60-100)"]

directory = input('Enter desired folder name: ')
askimg = input('Enter image filename that you want to detect: ')

parent_dir = '/Users/vanneswijaya/Python/OpenCV/AgeDetector'
path = os.path.join(parent_dir, directory)
os.mkdir(path)

face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

img = cv2.imread(askimg)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.1, 4)

z = 1
width = 900
height = 900

prototxtPath = 'age_detector/age_deploy.prototxt'
weightsPath = 'age_detector/age_net.caffemodel'
agenet = cv2.dnn.readNet(prototxtPath, weightsPath)

for (x, y, w, h) in faces:
    crop = img[y:y+h, x:x+w]
    resized = cv2.resize(crop, (width, height))

    blob = cv2.dnn.blobFromImage(resized, 1.0, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)
    agenet.setInput(blob)
    preds = agenet.forward()

    i = preds[0].argmax()
    age = AGE_BUCKETS[i]
    agepercent = preds[0][i]

    text = 'You look {:.0f}%'.format(agepercent*100)
    text2 = 'like a {} years old'.format(age)
    edited = cv2.putText(resized, text, (250, 500), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 8)
    edited2 = cv2.putText(edited, text2, (80, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 8)
    cv2.imwrite(f'{directory}/agedetected{z}.png', edited2)
    z += 1

