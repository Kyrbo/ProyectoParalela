import numpy as np
from skimage.filters import frangi
from pyinstrument import Profiler

if __name__ == '__main__':
    N = 1000
    np.random.seed(1)
    image = np.random.uniform(size=(N, N), low=0.0, high=1.0)

  
