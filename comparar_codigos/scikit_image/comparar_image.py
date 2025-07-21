from skimage.filters import frangi  # original
from image_pypar import frangi_ray  # versión paralelizada
from comparar_tiempo import comparar_rendimiento
from comparar_pylint import comparar_calidad


# Prepara el input
from skimage.data import camera
from skimage.color import rgb2gray
import numpy as np

image = camera()
if image.ndim == 3:
    image = rgb2gray(image)

# Ejecuta comparación


if __name__ == '__main__':

    #Le da tamaño N a frangi y frangi ray
    import numpy as np
    N = 2000 # aumentar o disminuir para probar distintos casos
    np.random.seed(1)
    image = np.random.uniform(size=(N, N), low=0.0, high=1.0)
    
    # code to run the target function
    code = 'frangi(image)'


      
comparar_rendimiento(frangi, frangi_ray,image)


comparar_calidad("image_original.py", "image_pypar.py")

