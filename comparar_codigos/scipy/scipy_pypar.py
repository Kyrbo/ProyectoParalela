import numpy as np
from scipy.signal import convolve2d
from scipy.ndimage import gaussian_filter
import ray

def ejecutar_scipy_parallel_func_0(gaussian_filter, image):
    blurred_image = gaussian_filter(image, sigma=1)
    return (blurred_image,)

def ejecutar_scipy_parallel_func_1(convolve2d, kernel, image):
    conv_image = convolve2d(image, kernel, mode='same')
    return (conv_image,)

def ejecutar_scipy_ray(image, kernel):
    if not ray.is_initialized():
        ray.init()

    remote_tmp_0 = ray.remote(ejecutar_scipy_parallel_func_0).remote(gaussian_filter, image)
    remote_tmp_1 = ray.remote(ejecutar_scipy_parallel_func_1).remote(convolve2d, kernel, image)
    (blurred_image,) = ray.get(remote_tmp_0)
    (conv_image,) = ray.get(remote_tmp_1)
    return conv_image + blurred_image
