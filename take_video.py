import cv2
import numpy as np

from perspective_utils import trapesium

judul = 'drive 8.mp4'

cap= cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

width= int(1280)
height= int(720)

out = 'out_drive8.mp4'

writer= cv2.VideoWriter(out, cv2.VideoWriter_fourcc('m','p','4','v'), 20, (width,height))


while True:
    ret,image= cap.read()

    frame = np.copy(image)

    h, w = frame.shape[:2]
    
    node_a, node_b, node_c, node_d, h_trap = trapesium(h, w)

    cv2.line(frame,(node_a,int(h)-int(50)),(node_b,h_trap),(0,255,0),3) # Sisi A
    cv2.line(frame,(node_b,h_trap),(node_c,h_trap),(0,255,0),3) # Sisi node B-C
    cv2.line(frame,(node_c,h_trap),(node_d,int(h)-int(50)),(0,255,0),3) # Sisi turun

    cv2.imshow('Result', frame)

    writer.write(frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break
        

cap.release()
writer.release()
cv2.destroyAllWindows()