import cv2
import numpy as np

cap= cv2.VideoCapture(0)

cap.set(3, 1280)
cap.set(4, 720)

width= int(1280)
height= int(720)
judul = '3_out_video.mp4'

writer= cv2.VideoWriter(judul, cv2.VideoWriter_fourcc('m','p','4','v'), 20, (width,height))


while True:
    ret,image= cap.read()

    image2 = np.copy(image)

    # This time we are defining a four sided polygon to mask
    h, w = image2.shape[:2]
    pengurang = int(150)
    node_b = int(w/2-pengurang)
    node_c = int(w/2+pengurang)
    h_trap = int(h/2)
    print(h,w,node_b,node_c)


    cv2.line(image2,(0,int(h)-int(10)),(node_b,h_trap),(0,255,0),3) # Sisi A
    cv2.line(image2,(node_b,h_trap),(node_c,h_trap,),(0,255,0),3) # Sisi node B-C
    cv2.line(image2,(node_c,h_trap),(int(w),int(h)-int(10)),(0,255,0),3) # Sisi turun

    cv2.imshow('Result', image2)

    writer.write(image)

    if cv2.waitKey(1) & 0xFF == 27:
        break
        

cap.release()
writer.release()
cv2.destroyAllWindows()