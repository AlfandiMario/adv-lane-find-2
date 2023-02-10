import cv2
import matplotlib.pyplot as plt
import numpy as np

cam = cv2.VideoCapture(0)
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
    pengurang = int(150)
    node_b = int(w/2-pengurang)
    node_c = int(w/2+pengurang)
    h_trap = int(h/2)
    print(h,w,node_b,node_c)

    cv2.line(frame,(0,int(h)-int(10)),(node_b,h_trap),(0,255,0),3) # Sisi A
    cv2.line(frame,(node_b,h_trap),(node_c,h_trap,),(0,255,0),3) # Sisi node B-C
    cv2.line(frame,(node_c,h_trap),(int(w),int(h)-int(10)),(0,255,0),3) # Sisi turun
    
    cv2.imshow("Result", frame)
    # plt.imshow(cv2.cvtColor(frame, code=cv2.COLOR_BGR2RGB))
    # plt.show()

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