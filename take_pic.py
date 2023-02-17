import cv2
import matplotlib.pyplot as plt
import numpy as np

from perspective_utils import trapesium

cam = cv2.VideoCapture('drive 7.mp4')
cam.set(3, 1280)
cam.set(4, 720)


img_counter = 0

while True:
    ret, image = cam.read()
    if not ret:
        print("failed to grab frame")
        break

    frame = np.copy(image)

    h, w = frame.shape[:2]
    
    node_a, node_b, node_c, node_d, h_trap = trapesium(h, w)

    cv2.line(frame,(node_a,int(h)-int(50)),(node_b,h_trap),(0,255,0),3) # Sisi A
    cv2.line(frame,(node_b,h_trap),(node_c,h_trap),(0,255,0),3) # Sisi node B-C
    cv2.line(frame,(node_c,h_trap),(node_d,int(h)-int(50)),(0,255,0),3) # Sisi turun
    
    cv2.imshow("Result", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.jpg".format(img_counter)
        
        # Garis tidak difoto
        cv2.imwrite(img_name, image)
        
        # Garis ikut foto
        # cv2.imwrite(img_name, frame)
        
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()