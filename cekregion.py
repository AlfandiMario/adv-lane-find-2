import cv2
import matplotlib.pyplot as plt
import numpy as np
import os

from perspective_utils import trapesium

path = 'drive 7.mp4'

cap = cv2.VideoCapture(path)

while True:
     _, image = cap.read()

     frame = np.copy(image)

     h, w = frame.shape[:2]
    
     node_a, node_b, node_c, node_d, h_trap = trapesium(h,w)

     # ROI 1
     cv2.line(frame,(node_a,int(h)-int(50)),(node_b,h_trap),(0,255,0),3) # Sisi A
     cv2.line(frame,(node_b,h_trap),(node_c,h_trap),(0,255,0),3) # Sisi node B-C
     cv2.line(frame,(node_c,h_trap),(node_d,int(h)-int(50)),(0,255,0),3) # Sisi turun

     # ROI 2 untuk perbandingan
     cv2.line(frame,(0,int(h)-int(10)),(536,500),(0,0,255),3) # Sisi A
     cv2.line(frame,(536,500),(732,500),(0,0,255),3) # Sisi node B-C
     cv2.line(frame,(732,500),(int(w),int(h)-int(10)),(0,0,255),3) # Sisi turun

     cv2.imshow("Result", frame)
     
     # cv2.imshow(image)
     plt.imshow(cv2.cvtColor(frame, code=cv2.COLOR_BGR2RGB))
     plt.show()

     if cv2.waitKey(1) & 0xFF == 27:
            print("Escape hit, closing...")
            break

cap.release()
cv2.destroyAllWindows()