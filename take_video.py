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
    imshape = image.shape
    height = image.shape[0]
    width = image.shape[1]
    
    node_b= int(546)
    node_c= int(732)
    t_trap= int(460)

    # Positioning
    pos_x = int(width/2)
    pos_y = int(9/10*height)
    cv2.circle(image2, (pos_x, pos_y), radius=10, color=(0, 0, 255), thickness=-10)

    cv2.line(image2,(0,int(height)-int(10)),(node_b,t_trap),(0,0,255),3) # Sisi A
    cv2.line(image2,(node_b,t_trap),(node_c,t_trap,),(0,0,255),3) # Sisi node B-C
    cv2.line(image2,(node_c,t_trap),(int(width),int(height)-int(10)),(0,0,255),3) # Sisi turun

    result = cv2.addWeighted(image, 0.8, image2, 1, 0)

    cv2.imshow('Result', result)

    writer.write(image)

    if cv2.waitKey(1) & 0xFF == 27:
        break
        

cap.release()
writer.release()
cv2.destroyAllWindows()