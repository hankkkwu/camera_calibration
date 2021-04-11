import cv2

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=640,
    display_height=360,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

#cam = cv2.VideoCapture(0)
cam = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)

cv2.namedWindow("image_capture")

image_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab image")
        break
    cv2.imshow("image", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("escape, closing...")
        break
    elif k%256 == 99:
        # c pressed
        image_name = "img{}.jpg".format(image_counter)
        cv2.imwrite(image_name, frame)
        print("{} written!".format(image_name))
        image_counter += 1

cam.release()
cv2.destroyAllWindows()
