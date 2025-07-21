from skimage.filters import frangi  # original
# Prepara el input
from skimage.data import camera
from skimage.color import rgb2gray
import numpy as np

image = camera()
if image.ndim == 3:
    image = rgb2gray(image)

# Ejecuta comparación


if __name__ == '__main__':

     # prepare input for DynamicParallelizer
    import numpy as np
    N = 2000
    np.random.seed(1)
    image = np.random.uniform(size=(N, N), low=0.0, high=1.0)
    
    # code to run the target function
    code = 'frangi(image)'

    from pypar import DynamicParallelizer

    #discover parallelisms        
    parallelizer = DynamicParallelizer(
        code=code, 
        glbs=globals(),
        lcls=locals())
      

    # print the parallelism report
    from pypar import print_parallelizables
    print_parallelizables(parallelizer)

   # auto-rewrite target function into parallelized version
    from pypar import print_rewrite
    
    print_rewrite(parallelizer, 0)