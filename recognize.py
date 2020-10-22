import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
import numpy as np
from skimage import data, color, io
from skimage.transform import rescale, resize
image = io.imread('image.png')
image = color.rgb2gray(image)
image_resized = resize(image, (28,28,1))


final = ((1-np.array(image_resized)))

# plt.imshow(final, cmap='gray')
# plt.savefig('books_read.png')
final = np.expand_dims(final, axis=0)
print(final.shape)

model = load_model("models/mnist_trained_99.h5")
answer = model.predict(final)
print(answer.argmax())