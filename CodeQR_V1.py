"""
Code qui genere un code QR avec l'information qu'on veut d'encoder dedans.
"""
import qrcode
import numpy as np
# data to encode
data = "ceci est un test"
# instantiate QRCode object
qr = qrcode.QRCode(version=1, box_size=10, border=1)
# add data to the QR code
qr.add_data(data)
# compile the data into a QR code array
qr.make()
# print the image shape
print("The shape of the QR image:", np.array(qr.get_matrix()).shape)
# transfer the array into an actual image
img = qr.make_image(fill_color="black", back_color="white")
# save it to a file
img.save("necrons.png")