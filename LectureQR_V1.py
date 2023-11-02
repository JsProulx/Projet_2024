import cv2
from pyzbar.pyzbar import decode
import numpy as np


# read the QRCODE image
img = cv2.imread('necrons.png')




#configuration de la capture video
capture = cv2.VideoCapture(1)
capture.set(3,640)      #resolution de l'image
capture.set(4,480)

while True:

    success,img = capture.read()    #succes = indicateure de reussite, img = image capture par la cam
    for barcode in decode(img):
        monData = barcode.data.decode('utf-8')
        print (monData)

        #pour faire le polygone autour du code qr
        points = np.array([barcode.polygon], np.int32)
        points = points.reshape((-1,1,2))
        cv2.polylines(img,[points],True,(255,0,255),5)
        points2 = barcode.rect
        cv2.putText(img, monData,(points2[0],points2[1]),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,0,255),2)

    cv2.imshow('Result',img)
    cv2.waitKey(1)

