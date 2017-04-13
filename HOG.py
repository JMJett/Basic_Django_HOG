import cv2
import os
import datetime
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'DjangoCV.settings'
application = get_wsgi_application()

from Detection.models import Video

def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def draw_detections(img, rects, thickness=1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15 * w), int(0.05 * h)
        cv2.rectangle(img, (x + pad_w, y + pad_h), (x + w - pad_w, y + h - pad_h), (0, 255, 0), thickness)


if __name__ == '__main__':
    timeout = 0
    detected = False
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    cap = cv2.VideoCapture('mall.mp4')

    while timeout < 15:
        _, frame = cap.read()
        timeout += 1
        found, w = hog.detectMultiScale(frame, winStride=(8, 8), padding=(32, 32), scale=1.2)
        if(len(found != 0)):
            detected = True
        draw_detections(frame, found)
        cv2.imshow('feed', frame)
        ch = 0xFF & cv2.waitKey(1)

        if ch == ord("q"):
            break

        if ch == 27:
            break
    cv2.destroyAllWindows()

    if(detected):
        newvid = Video(filename="mall.mp4",timestamp=datetime.datetime.now(),human=True)
    else:
        newvid = Video(filename="mall.mp4",timestamp=datetime.datetime.now(),human=False)
    newvid.save()



