import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
from calibration_utils import calibrate_camera, undistort
from binarization_utils import binarize

def trapesium_ori(h, w):
    node_a = 0
    node_b = 546
    node_c = 732
    node_d = w
    h_trap = 460
    b_trap = h-10
    return node_a, node_b, node_c, node_d, h_trap, b_trap

def trapesium_v1(h, w):
    pengurang = int(w//20)
    node_a = int(150)
    node_b = int(w/2-pengurang+20)
    node_c = int(w/2+pengurang+110)
    node_d = w-50
    h_trap = int(390)
    b_trap = h-50
    return node_a, node_b, node_c, node_d, h_trap, b_trap

def trapesium_custom(h, w):
    pengurang = int(w//12)
    node_a = int(150)
    node_b = int(w/2-pengurang+50)
    node_c = int(w/2+pengurang+20)
    node_d = w-50
    h_trap = int(510)
    b_trap = h-80
    return node_a, node_b, node_c, node_d, h_trap, b_trap

def birdeye(img, verbose):
    """
    Apply perspective transform to input frame to get the bird's eye view.
    :param img: input color frame
    :param verbose: if True, show the transformation result
    :return: warped image, and both forward and backward transformation matrices
    """
    h, w = img.shape[:2]
    
    # ROI Original
    # node_a, node_b, node_c, node_d, h_trap, b_trap = trapesium_ori(h, w)

    # ROI Variation
    node_a, node_b, node_c, node_d, h_trap, b_trap = trapesium_custom(h, w)

    src = np.float32([[node_d, b_trap],    # br
                      [node_a, b_trap],    # bl
                      [node_b, h_trap],   # tl
                      [node_c, h_trap]])  # tr
    dst = np.float32([[w, h],       # br
                      [0, h],       # bl
                      [0, 0],       # tl
                      [w, 0]])      # tr
    
    # Menggaris trapesium pada gambar input biar terlihat ROI nya
    cv2.line(img,(node_a,b_trap),(node_b,h_trap),(0,255,0),3) # Sisi A
    cv2.line(img,(node_b,h_trap),(node_c,h_trap),(0,255,0),3) # Sisi node B-C
    cv2.line(img,(node_c,h_trap),(node_d,b_trap),(0,255,0),3) # Sisi turun

    M = cv2.getPerspectiveTransform(src, dst)
    Minv = cv2.getPerspectiveTransform(dst, src)
    warped = cv2.warpPerspective(img, M, (w, h), flags=cv2.INTER_LINEAR)

    if verbose:
        f, axarray = plt.subplots(1, 2)
        f.set_facecolor('white')
        axarray[0].set_title('Before perspective transform')
        axarray[0].imshow(img, cmap='gray')
        
        for point in src:
            axarray[0].plot(*point, '.')
        axarray[1].set_title('After perspective transform')
        axarray[1].imshow(warped, cmap='gray')
        for point in dst:
            axarray[1].plot(*point, '.')
        for axis in axarray:
            axis.set_axis_off()
        plt.show()
    
    return warped, M, Minv


if __name__ == '__main__':
    ret, mtx, dist, rvecs, tvecs = calibrate_camera(calib_images_dir='camera_cal')

    # show result on test images for 1 folder
    # for test_img in glob.glob('test_images/*.jpg'):
    #     img = cv2.imread(test_img)
    #     img_undistorted = undistort(img, mtx, dist, verbose=False)
    #     img_binary = binarize(img_undistorted, verbose=False)
    #     img_birdeye, M, Minv = birdeye(cv2.cvtColor(img_undistorted, cv2.COLOR_BGR2RGB), verbose=True)

    # show result for 1 file
    img = cv2.imread('test_images/drive8b.png')
    img_undistorted = undistort(img, mtx, dist, verbose=False)
    img_binary = binarize(img_undistorted, verbose=False)
    img_birdeye, M, Minv = birdeye(cv2.cvtColor(img_undistorted, cv2.COLOR_BGR2RGB), verbose=True)  