import cv2
import matplotlib.pyplot as plt

cam = cv2.VideoCapture(0)
cam.set(3, 1280)
cam.set(4, 720)


img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    
    # cv2.namedWindow("Resized_Window", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("Resized_Window", 1280, 720)
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
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()