import cv2
import numpy as np

if __name__ == "__main__":
    filename = "./test/images/black_0305_1024x1024@2x.jpg"
    src = cv2.imread(filename)
    src = cv2.resize(src, [400, 400])
    cv2.imshow('Step1: origin', src)

    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    retval, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    cv2.imshow('Step2: binary', binary)

    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    tmp = np.zeros(src.shape, np.uint8)
    res = cv2.drawContours(tmp, contours, -1, (250, 255, 255), 1)
    cv2.imshow("Allcontours", res)

    cnt = contours[8]
    tmp2 = np.zeros(src.shape, np.uint8)
    res2 = cv2.drawContours(tmp2, cnt, -1, (250, 255, 255), 2)
    cv2.imshow('cnt', res2)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
