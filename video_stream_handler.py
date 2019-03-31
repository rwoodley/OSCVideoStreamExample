import time
import cv2
import numpy as np

# All Open CV references are confined to this file.

def stream_handler():
    cap = cv2.VideoCapture(0)
    # cap.set(3, 1920)
    # cap.set(4, 1080)

    frame_count = 0
    start_time = time.time()

    while (True):
        ret, frame = cap.read()
        # Our operations on the frame come here

        # result = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # result = cv2.Canny(frame, 10, 200)

        # cv2.imshow("Result", result)

        # fr = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # lower_red = np.array([30,150,50])
        # upper_red = np.array([255,255,180])
        # mask = cv2.inRange(hsv, lower_red, upper_red)
        # result = cv2.bitwise_and(frame,frame, mask= mask)

        # laplacian = cv2.Laplacian(frame,cv2.CV_64F)
        # sobelx = cv2.Sobel(frame,cv2.CV_64F,1,0,ksize=5)
        # sobely = cv2.Sobel(frame,cv2.CV_64F,0,1,ksize=5)
        #
        kernel = np.ones((5, 5), np.uint8)
        erosion = cv2.erode(frame, kernel, iterations=1)
        # gradient = cv2.morphologyEx(frame, cv2.MORPH_GRADIENT, kernel)
        result = cv2.cvtColor(erosion, cv2.COLOR_BGR2HSV)
        result2 = cv2.Canny(result, 1, 400)
        result3 = cv2.cvtColor(result2, cv2.COLOR_GRAY2BGR)
        result4 = cv2.bitwise_and(result, result3)
        # cv2.circle(result4,(447,63), 63, (0,255,0), -1)
        # cv2.circle(result4,(547,63), 63, (0,240,0), -1)

        blah = cv2.imencode('.jpg', result4)[1].tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + blah + b'\r\n')

        # Display the resulting frame
        # cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1
        elapsed_time = time.time() - start_time
        h, w, _ = frame.shape
        print("Wrote frame: {}, fps={}, in shape=({},{})"
              .format(frame_count, 1 / elapsed_time, w,h))
        start_time = time.time()
