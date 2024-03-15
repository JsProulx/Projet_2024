import cv2

# Vérifiez si OpenCV a été compilé avec CUDA
print(cv2.cuda.getCudaEnabledDeviceCount())

# Chargez une image
image = cv2.imread('image.jpg')

# Créez un objet de traitement d'images CUDA
gpu_image = cv2.cuda_GpuMat()
gpu_image.upload(image)

# Appliquez un filtre gaussien sur l'image GPU
gpu_blur = cv2.cuda.createGaussianFilter(gpu_image.type(), gpu_image.type(), (5, 5), 0)
gpu_blur.apply(gpu_image, gpu_image)

# Téléchargez l'image du GPU vers le CPU
result_image = gpu_image.download()

# Affichez l'image résultante
cv2.imshow('Result', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
