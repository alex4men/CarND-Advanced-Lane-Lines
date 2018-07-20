from matplotlib import image as mpimg
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np

img = np.array(Image.open('undist_test.jpg'))
plt.imshow(img)
plt.show()