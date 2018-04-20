import numpy as np
import cv2

cap = cv2.VideoCapture('rtmp://192.168.43.49:1935/flash/11:admin:admin1')

while(True):
    ret, frame = cap.read()
    #output_rgb = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    #cv2.imshow('Video', output_rwgb)
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imwrite("frame.png",frame)


cap.release()
cv2.destroyAllWindows()
