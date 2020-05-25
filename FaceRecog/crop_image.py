from cv2 import cv2

img = cv2.imread('screenshot.png')

y = 1
for x in range (0,2):
    for z in range (0,3):
        imgCropped = img[180+(270*x):450+(270*x), 0+(480*z):480+(480*z)]
        cv2.imwrite(f'manualcrop/cropped{y}.png', imgCropped)
        y += 1

cv2.waitKey(0)