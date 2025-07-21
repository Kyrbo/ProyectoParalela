import numpy as np
from scipy.signal import convolve2d
from scipy.ndimage import gaussian_filter

def ejecutar_scipy(image, kernel):
    conv_image = convolve2d(image, kernel, mode='same')
    blurred_image = gaussian_filter(image, sigma=1)
    return conv_image + blurred_image