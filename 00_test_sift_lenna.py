import cv2

img = cv2.imread('data/Lenna.jpg')

gray= cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

sift = cv2.SIFT()
kp = sift.detect(gray,None)

img=cv2.drawKeypoints(gray,kp)

cv2.imwrite('out/Lenna_sift.jpg',img)