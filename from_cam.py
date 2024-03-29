import cv2
import matplotlib.pyplot as plt
import numpy as np
from playsound import playsound
from time import sleep
import time
import multiprocessing

from calibration_utils import calibrate_camera, undistort
from binarization_utils import binarize
from perspective_utils import birdeye, trapesium_custom, trapesium_v1, trapesium_ori
from line_utils import get_fits_by_sliding_windows, draw_back_onto_the_road, Line, get_fits_by_previous_fits
from globals import xm_per_pix, time_window


processed_frames = 0                    # counter of frames processed (when processing video)
line_lt = Line(buffer_len=time_window)  # line on the left of the lane
line_rt = Line(buffer_len=time_window)  # line on the right of the lane

# Menyatukan gambar untuk hasil akhir
def prepare_out_blend_frame(blend_on_road, img_binary, img_birdeye, img_fit, line_lt, line_rt, offset_meter):
    """
    Prepare the final pretty pretty output blend, given all intermediate pipeline images

    :param blend_on_road: color image of lane blend onto the road
    :param img_binary: thresholded binary image
    :param img_birdeye: bird's eye view of the thresholded binary image
    :param img_fit: bird's eye view with detected lane-lines highlighted
    :param line_lt: detected left lane-line
    :param line_rt: detected right lane-line
    :param offset_meter: offset from the center of the lane
    :return: pretty blend with all images and stuff stitched
    """
    h, w = blend_on_road.shape[:2]

    # thumb_ratio = 0.2
    thumb_ratio = 0.15
    thumb_h, thumb_w = int(thumb_ratio * h), int(thumb_ratio * w)

    off_x, off_y = 20, 15

    # add a gray rectangle to highlight the upper area
    mask = blend_on_road.copy()
    mask = cv2.rectangle(mask, pt1=(0, 0), pt2=(w, thumb_h+2*off_y), color=(0, 0, 0), thickness=cv2.FILLED)
    blend_on_road = cv2.addWeighted(src1=mask, alpha=0.2, src2=blend_on_road, beta=0.8, gamma=0)

    # add thumbnail of binary image
    thumb_binary = cv2.resize(img_binary, dsize=(thumb_w, thumb_h))
    thumb_binary = np.dstack([thumb_binary, thumb_binary, thumb_binary]) * 255
    blend_on_road[off_y:thumb_h+off_y, off_x:off_x+thumb_w, :] = thumb_binary

    # add thumbnail of bird's eye view
    thumb_birdeye = cv2.resize(img_birdeye, dsize=(thumb_w, thumb_h))
    thumb_birdeye = np.dstack([thumb_birdeye, thumb_birdeye, thumb_birdeye]) * 255
    blend_on_road[off_y:thumb_h+off_y, 2*off_x+thumb_w:2*(off_x+thumb_w), :] = thumb_birdeye

    # add thumbnail of bird's eye view (lane-line highlighted)
    thumb_img_fit = cv2.resize(img_fit, dsize=(thumb_w, thumb_h))
    blend_on_road[off_y:thumb_h+off_y, 3*off_x+2*thumb_w:3*(off_x+thumb_w), :] = thumb_img_fit

    # add text (curvature and offset info) on the upper right of the blend
    mean_curvature_meter = np.mean([line_lt.curvature_meter, line_rt.curvature_meter])
    font = cv2.FONT_HERSHEY_SIMPLEX
    # cv2.putText(blend_on_road, 'Curvature radius: {:.02f}m'.format(mean_curvature_meter), (860, 60), font, 0.9, (255, 255, 255), 2, cv2.LINE_AA)
    # cv2.putText(blend_on_road, 'Offset from center: {:.02f}m'.format(offset_meter), (860, 130), font, 0.9, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(blend_on_road, 'Offset from center: {:.02f}m'.format(offset_meter), (800, 40), font, 0.9, (255, 255, 255), 2, cv2.LINE_AA)

    return blend_on_road


def compute_offset_from_center(line_lt, line_rt, frame_width):
    """
    Compute offset from center of the inferred lane.
    The offset from the lane center can be computed under the hypothesis that the camera is fixed
    and mounted in the midpoint of the car roof. In this case, we can approximate the car's deviation
    from the lane center as the distance between the center of the image and the midpoint at the bottom
    of the image of the two lane-lines detected.

    :param line_lt: detected left lane-line
    :param line_rt: detected right lane-line
    :param frame_width: width of the undistorted frame
    :return: inferred offset
    """
    if line_lt.detected and line_rt.detected:
        line_lt_bottom = np.mean(line_lt.all_x[line_lt.all_y > 0.95 * line_lt.all_y.max()])
        line_rt_bottom = np.mean(line_rt.all_x[line_rt.all_y > 0.95 * line_rt.all_y.max()])
        lane_width = line_rt_bottom - line_lt_bottom
        midpoint = frame_width / 2
        offset_pix = abs((line_lt_bottom + lane_width / 2) - midpoint)
        offset_meter = xm_per_pix * offset_pix
    else:
        offset_meter = -1
    return offset_meter


def process_pipeline(frame, keep_state=True):
    """
    Apply whole lane detection pipeline to an input color frame.
    :param frame: input color frame
    :param keep_state: if True, lane-line state is conserved (this permits to average results)
    :return: output blend with detected lane overlaid
    """

    global line_lt, line_rt, processed_frames

    # undistort the image using coefficients found in calibration
    img_undistorted = undistort(frame, mtx, dist, verbose=False)

    # binarize the frame s.t. lane lines are highlighted as much as possible
    img_binary = binarize(img_undistorted, verbose=False)

    # compute perspective transform to obtain bird's eye view
    img_birdeye, M, Minv = birdeye(img_binary, verbose=False)

    # fit 2-degree polynomial curve onto lane lines found
    # if processed_frames > 0  and keep_state and line_lt.detected and line_rt.detected:
    #     line_lt, line_rt, img_fit = get_fits_by_previous_fits(img_birdeye, line_lt, line_rt, verbose=False)
    # else:
    #     line_lt, line_rt, img_fit = get_fits_by_sliding_windows(img_birdeye, line_lt, line_rt, n_windows=9, verbose=False)
    # line_lt, line_rt, img_fit = get_fits_by_sliding_windows(img_birdeye, line_lt, line_rt, n_windows=9, verbose=False)
    if keep_state and line_lt.detected and line_rt.detected:
        if processed_frames < 16:
            line_lt, line_rt, img_fit = get_fits_by_previous_fits(img_birdeye, line_lt, line_rt, verbose=False)
        else:
            line_lt, line_rt, img_fit = get_fits_by_sliding_windows(img_birdeye, line_lt, line_rt, n_windows=9, verbose=False)
            processed_frames = 0
    else:
        line_lt, line_rt, img_fit = get_fits_by_sliding_windows(img_birdeye, line_lt, line_rt, n_windows=9, verbose=False)

    # compute offset in meter from center of the lane
    offset_meter = compute_offset_from_center(line_lt, line_rt, frame_width=frame.shape[1])

    # draw the surface enclosed by lane lines back onto the original frame
    blend_on_road = draw_back_onto_the_road(img_undistorted, Minv, line_lt, line_rt, keep_state)

    # stitch on the top of final output images from different steps of the pipeline
    blend_output = prepare_out_blend_frame(blend_on_road, img_binary, img_birdeye, img_fit, line_lt, line_rt, offset_meter)
    # blend_output = prepare_out_blend_frame(img_undistorted, img_binary, img_birdeye, img_fit, line_lt, line_rt, offset_meter)

    processed_frames += 1

    return blend_output, offset_meter

def sound():
    playsound('warning.mp3')

if __name__ == '__main__':
    # first things first: calibrate the camera
    ret, mtx, dist, rvecs, tvecs = calibrate_camera(calib_images_dir='camera_cal')

    # Coba dari Video
    cam = cv2.VideoCapture('test_videos/9_test.mp4')

    # Coba dari live camera
    # cam = cv2.VideoCapture(0)

    # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    # Untuk alarm
    # subproses = multiprocessing.Process(target = sound)

    # Hitung FPS
    # Record waktu ketika frame terakhir diproses
    prev_frame_time = 0
    # Record waktu ketika frame saat ini diproses
    new_frame_time = 0
    # Record jumlah FPS keseluruhan
    sum_fps = 0
    sum_frame = 0

    if not cam.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        _, result= cam.read()

        if not _:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        result, offset = process_pipeline(result)

        # Hitung FPS
        font = cv2.FONT_HERSHEY_SIMPLEX  #font to apply on text
        new_frame_time = time.time() 
        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time
        fps = float(fps)
        fps = round(fps,2)
        cv2.putText(result, str(fps), (50, 50), font, 1, (0, 0, 255), 2) # add text on frame
        
        sum_frame +=1
        sum_fps += fps

        # Menyalakan alarm warning
        # if offset >= 0.5:
        #     # subproses.run()
        #     # subproses.join()
        #     playsound('warning.mp3')

        # Menggambar garis trapesium ROI
        # h, w = result.shape[:2]
        # # node_a, node_b, node_c, node_d, h_trap, b_trap = trapesium_v1(h, w)
        # node_a, node_b, node_c, node_d, h_trap, b_trap = trapesium_custom(h, w)
        # cv2.line(result,(node_a,b_trap),(node_b,h_trap),(0,255,0),3) # Sisi A
        # cv2.line(result,(node_b,h_trap),(node_c,h_trap),(0,255,0),3) # Sisi node B-C
        # cv2.line(result,(node_c,h_trap),(node_d,b_trap),(0,255,0),3) # Sisi turun

        cv2.imshow("Result", result)


        if cv2.waitKey(1) & 0xFF == 27:
            print("Escape hit, closing...")
            break

    cam.release()
    cv2.destroyAllWindows()
    print("Jumlah FPS : ",sum_fps)
    print("Jumlah Frame: ",sum_frame)
    avg_fps = sum_fps/sum_frame
    print("Avg FPS : ",avg_fps)