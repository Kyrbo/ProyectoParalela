from skimage.filters.ridges import frangi
from skimage._shared.utils import check_nD, _supported_float_type
from skimage.feature import hessian_matrix_eigvals, hessian_matrix
import numpy as np

def frangi_ray(image, sigmas=range(1, 10, 2), scale_range=None, scale_step=None, alpha=0.5, beta=0.5, gamma=None, black_ridges=True, mode='reflect', cval=0):
   
    if ((scale_range is not None) and (scale_step is not None)):
        warn('Use keyword parameter `sigmas` instead of `scale_range` and `scale_range` which will be removed in version 0.17.', stacklevel=2)
        sigmas = np.arange(scale_range[0], scale_range[1], scale_step)
    check_nD(image, [2, 3])
    image = image.astype(_supported_float_type(image.dtype), copy=False)
    if (not black_ridges):
        image = (- image)
    filtered_max = np.zeros_like(image)
    for (loop_idx_1, sigma) in enumerate(sigmas):
        eigvals = hessian_matrix_eigvals(hessian_matrix(image, sigma, mode=mode, cval=cval, use_gaussian_derivatives=True))
        eigvals = np.take_along_axis(eigvals, abs(eigvals).argsort(0), 0)
        lambda1 = eigvals[0]
        s = np.sqrt((eigvals ** 2).sum(0))
        gamma = (s.max() / 2)
        gamma = 1
        if (gamma == 0):
            gamma = 1
        if (gamma is None):
            gamma = (s.max() / 2)
            if (gamma == 0):
                gamma = 1
    return filtered_max