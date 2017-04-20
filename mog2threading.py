import cv2
import datetime
import threading
import subprocess
import time

def save_file():
    fileName = threading.current_thread().getName() + ".mp4"

    cap = cv2.VideoCapture('mall.mp4')

    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    height, width = int(cap.get(4)), int(cap.get(3))
    out = cv2.VideoWriter(fileName, fourcc, 28.0, (width, height))
    timeout = time.time() + 5
    while time.time() < timeout:
        ret, frame = cap.read()
        if ret == True:
            out.write(frame)
#Initialize
vid = cv2.VideoCapture("mall.mp4")
bgsub = cv2.createBackgroundSubtractorMOG2()


while vid.isOpened():

    #read frames, apply mask
    ret, frame = vid.read()
    bgmask = bgsub.apply(frame)


    #Use the mask to find contours

    th = cv2.threshold(bgmask.copy(), 244, 255, cv2.THRESH_BINARY)[1]
    dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
    feed, contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    count = 0
    for c in contours:
        if cv2.contourArea(c) > 1400:

            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
            count += 1
            capture = True
    txt = "Count: " + str(count)
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = cv2.putText(frame, txt, (250, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)



    # show the mask and the feed with rectangles
    cv2.imshow("Frame", bgmask)
    cv2.imshow("thresh", th)
    cv2.imshow("text", text)
    cv2.imshow("detection", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    if key == ord("s"):
        file = "./%s.png" % datetime.datetime.now().strftime("%d-%m-%y--%H-%M-%S")
        cv2.imwrite(file, frame)

vid.release()
cv2.destroyAllWindows()

if capture == True:
    thread = threading.Thread(target=save_file, name='mall2')
    thread.start()