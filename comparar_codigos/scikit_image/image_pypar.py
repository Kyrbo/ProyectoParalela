import numpy as np
import time
import ray
from skimage.util import invert
from skimage.feature import hessian_matrix, hessian_matrix_eigvals
from skimage._shared.utils import check_nD
from skimage._shared._warnings import warn
from skimage.filters import frangi
from pyinstrument import Profiler

ray.init()

def _check_sigmas(sigmas):
    sigmas = np.atleast_1d(sigmas)
    if np.any(sigmas <= 0):
        raise ValueError("All sigmas must be > 0")
    return sigmas

@ray.remote
def frangi_parallel_func_0(sigma, cval, mode, image):
    H_elems = hessian_matrix(image, sigma=sigma, order='rc', mode=mode, cval=cval)
    lambdas = hessian_matrix_eigvals(H_elems)
    return lambdas

def _supported_float_type(dtype):
    # Retorna float64 o float32 según el tipo original
    if np.issubdtype(dtype, np.float32):
        return np.float32
    else:
        return np.float64

def _divide_nonzero(a, b):
    with np.errstate(divide='ignore', invalid='ignore'):
        c = np.true_divide(a, b)
        c[~np.isfinite(c)] = 0  # -inf inf NaN se ponen a 0
    return c

def frangi_ray(image, sigmas=range(1, 10, 2), scale_range=None, scale_step=None,
               alpha=0.5, beta=0.5, gamma=15, black_ridges=True,
               mode='reflect', cval=0):
    if scale_range is not None and scale_step is not None:
        warn('Use keyword parameter `sigmas` instead of `scale_range` and `scale_step` which will be removed.', stacklevel=2)
        sigmas = np.arange(scale_range[0], scale_range[1], scale_step)

    check_nD(image, [2, 3])
    sigmas = _check_sigmas(sigmas)
    alpha_sq = 2 * alpha ** 2
    beta_sq = 2 * beta ** 2
    gamma_sq = 2 * gamma ** 2
    ndim = image.ndim

    if black_ridges:
        image = invert(image)

    float_dtype = _supported_float_type(image.dtype)
    filtered_array = np.zeros((sigmas.shape + image.shape), dtype=float_dtype)
    lambdas_array = np.zeros_like(filtered_array, dtype=float_dtype)

    remote_list_0 = [
        frangi_parallel_func_0.remote(sigma, cval, mode, image)
        for sigma in sigmas
    ]
    remote_list_0 = ray.get(remote_list_0)

    for i, lambdas in enumerate(remote_list_0):
        lambda1, *rest = lambdas
        r_a = np.inf if ndim == 2 else (_divide_nonzero(*rest) ** 2)
        lambdas_array[i] = np.max(rest, axis=0)
        filtered_raw = (np.abs(np.multiply.reduce(rest)) ** (1 / len(rest)))
        r_g = sum([lambda1 ** 2] + [l ** 2 for l in rest])
        r_b = (_divide_nonzero(lambda1, filtered_raw) ** 2)

        filtered_array[i] = (
            (1 - np.exp(-r_a / alpha_sq)) *
            np.exp(-r_b / beta_sq) *
            (1 - np.exp(-r_g / gamma_sq))
        )
    filtered_array[lambdas_array > 0] = 0
    return np.max(filtered_array, axis=0)


if __name__ == '__main__':
    # Crear imagen aleatoria
    N = 2000
    np.random.seed(1)
    image = np.random.uniform(size=(N, N), low=0.0, high=1.0)

  

    ray.shutdown()

