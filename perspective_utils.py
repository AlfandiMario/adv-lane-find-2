import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
from calibration_utils import calibrate_camera, undistort
from binarization_utils import binarize

def trapesium(h, w):
    # pengurang = int(w//20)
    # node_b = int(w/2-pengurang+20)
    # node_c = int(w/2+pengurang+80)
    # h_trap = int(500)

    # 3_test
    # pengurang = int(w//14)
    # node_b = int(w/2-pengurang)
    # node_c = int(w/2+pengurang)
    # h_trap = int(420)

    # 7_test
    pengurang = int(w//20)
    node_a = int(150)
    node_b = int(w/2-pengurang+20)
    node_c = int(w/2+pengurang+60)
    node_d = w-50
    h_trap = int(510)
    
    return node_a, node_b, node_c, node_d, h_trap

def birdeye(img, verbose=False):
    """
    Apply perspective transform to input frame to get the bird's eye view.
    :param img: input color frame
    :param verbose: if True, show the transformation result
    :return: warped image, and both forward and backward transformation matrices
    """
    h, w = img.shape[:2]

    node_a, node_b, node_c, node_d, h_trap = trapesium(h, w)

    src = np.float32([[node_d, h-50],    # br
                      [node_a, h-50],    # bl
                      [node_b, h_trap],   # tl
                      [node_c, h_trap]])  # tr
    dst = np.float32([[w, h],       # br
                      [0, h],       # bl
                      [0, 0],       # tl
                      [w, 0]])      # tr
    
    

    # src = np.float32([[w, h-10],    # br
    #                   [0, h-10],    # bl
    #                   [546, 460],   # tl
    #                   [732, 460]])  # tr
    # dst = np.float32([[w, h],       # br
    #                   [0, h],       # bl
    #                   [0, 0],       # tl
    #                   [w, 0]])      # tr

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

    # show result on test images
    for test_img in glob.glob('test_images/*.jpg'):

        img = cv2.imread(test_img)

        img_undistorted = undistort(img, mtx, dist, verbose=False)

        img_binary = binarize(img_undistorted, verbose=False)

        img_birdeye, M, Minv = birdeye(cv2.cvtColor(img_undistorted, cv2.COLOR_BGR2RGB), verbose=True)


