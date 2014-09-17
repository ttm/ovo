import cv2

cap = cv2.VideoCapture(0)
sift = cv2.SIFT()

# Sets camera to 320x240
ret = cap.set(3,320)
ret = cap.set(4,240)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # SIFT
    kp = sift.detect(gray,None)

    img = cv2.drawKeypoints(gray,kp)

    # Display the resulting frame
    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()