import numpy as np
import cv2 as cv
import glob
import pickle
import matplotlib.pyplot as plt

def camera_calibration():
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*8,3), np.float32)
    objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    images = glob.glob('./pairs/right_*.jpg')
    img_size = None
    for fname in images:
        img = cv.imread(fname)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img_size = gray.shape[::-1]
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, (8,6), None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)
            # Draw and display the corners
            cv.drawChessboardCorners(img, (8,6), corners2, ret)
            cv.imshow('img', img)
            cv.waitKey(500)
    cv.destroyAllWindows()

    # do camera clibration given object point and image points
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, img_size, None, None)

    # Save the camera calibration result for later use
    dist_pickle = {}
    dist_pickle["mtx"] = mtx
    dist_pickle["dist"] = dist
    pickle.dump(dist_pickle, open("right_cam_calibration.p", "wb"))

    return mtx, dist

if __name__ == '__main__':
    # for calibration
    # mtx, dist = camera_calibration()

    # read from saved pickle file
    dist_pickle = pickle.load(open("right_cam_calibration.p", "rb"))
    mtx = dist_pickle["mtx"]
    dist = dist_pickle["dist"]
    # print("mtx:",mtx)
    # print("dist:",dist)

    # refine the camera matrix based on a free scaling parameter using cv.getOptimalNewCameraMatrix().
    img = cv.imread('./pairs/right_12.jpg')
    h,  w = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

    # undistort the image
    dst = cv.undistort(img, mtx, dist, None, newcameramtx)    

    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]

    # visualize the difference between distorted and undistorted images
    """
    NOTE: the size of the original and undistored image are different!!
    """
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(20,10))
    ax1.imshow(img)
    ax1.set_title("original image", fontsize=30)
    ax2.imshow(dst)
    ax2.set_title("undistorted image", fontsize=30)

    plt.show()
