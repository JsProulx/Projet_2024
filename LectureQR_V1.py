import cv2
# read the QRCODE image
img = cv2.imread("necrons.png")

# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()

# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()

# The detectAndDecode() function takes an image as an input and decodes it 
# to return a tuple of 3 values: the data decoded from the QR code, the output 
# array of vertices of the found QR code quadrangle, and the output image containing 
# rectified and binarized QR code.
data, bbox, straight_qrcode = detector.detectAndDecode(img)

