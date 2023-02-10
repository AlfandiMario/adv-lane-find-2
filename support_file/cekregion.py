import cv2
import matplotlib.pyplot as plt
import numpy as np

path = '7_test.mp4'

cap = cv2.VideoCapture(path)

while True:
     _, image = cap.read()

     frame = np.copy(image)

     h, w = frame.shape[:2]
    
     pengurang = int(w//14)
     node_b = int(w/2-pengurang)
     node_c = int(w/2+pengurang)
     h_trap = int(6/10*h)

     cv2.line(frame,(0,int(h)-int(10)),(node_b,h_trap),(0,255,0),3) # Sisi A
     cv2.line(frame,(node_b,h_trap),(node_c,h_trap,),(0,255,0),3) # Sisi node B-C
     cv2.line(frame,(node_c,h_trap),(int(w),int(h)-int(10)),(0,255,0),3) # Sisi turun

     cv2.imshow("Result", frame)
     
     # cv2.imshow(image)
     plt.imshow(frame)
     plt.show()

     if cv2.waitKey(1) & 0xFF == 27:
            print("Escape hit, closing...")
            break

cap.release()
cv2.destroyAllWindows()