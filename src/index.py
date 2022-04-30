import cv2 as cv
import numpy as np


def nothing(x):
    pass


def setup() -> None:
    cv.namedWindow('Webcam')
    cv.namedWindow('ChromaKeyControlWindow')
    cv.createTrackbar('HMin', 'ChromaKeyControlWindow', 0, 179, nothing)
    cv.createTrackbar('HMax', 'ChromaKeyControlWindow', 0, 179, nothing)
    cv.createTrackbar('SMin', 'ChromaKeyControlWindow', 0, 255, nothing)
    cv.createTrackbar('SMax', 'ChromaKeyControlWindow', 0, 255, nothing)
    cv.createTrackbar('VMin', 'ChromaKeyControlWindow', 0, 255, nothing)
    cv.createTrackbar('VMax', 'ChromaKeyControlWindow', 0, 255, nothing)

    cv.setTrackbarPos('HMax', 'ChromaKeyControlWindow', 179)
    cv.setTrackbarPos('SMax', 'ChromaKeyControlWindow', 255)
    cv.setTrackbarPos('VMax', 'ChromaKeyControlWindow', 255)


if __name__ == '__main__':
    cap = cv.VideoCapture(2)
    setup()
    while True:
        _, image = cap.read()
        hMin = cv.getTrackbarPos('HMin', 'ChromaKeyControlWindow')
        sMin = cv.getTrackbarPos('SMin', 'ChromaKeyControlWindow')
        vMin = cv.getTrackbarPos('VMin', 'ChromaKeyControlWindow')
        hMax = cv.getTrackbarPos('HMax', 'ChromaKeyControlWindow')
        sMax = cv.getTrackbarPos('SMax', 'ChromaKeyControlWindow')
        vMax = cv.getTrackbarPos('VMax', 'ChromaKeyControlWindow')

        lower = np.array([hMin, sMin, vMin])
        upper = np.array([hMax, sMax, vMax])

        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, lower, upper)
        result = cv.bitwise_and(image, image, mask=mask)

        imf = cv.resize(result, (1920, 1080))
        mask = cv.resize(mask, (1920, 1080))

        background_image = cv.imread('images/room.png')
        background_image = cv.cvtColor(background_image, cv.COLOR_BGR2RGB)

        background_image[mask != 0] = [0, 0, 0]

        final_image = imf + background_image
        final_image = cv.resize(final_image, (1280, 720))

        cv.imshow('Webcam', final_image)

        if cv.waitKey(10) & 0xFF == ord('q'):
            break

    cv.destroyAllWindows()
