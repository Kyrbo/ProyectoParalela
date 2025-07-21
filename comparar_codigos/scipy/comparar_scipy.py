from scipy_original import ejecutar_scipy       # función original
from scipy_pypar import ejecutar_scipy_ray      # función paralelizada
from comparar_tiempo import comparar_rendimiento
from comparar_pylint import comparar_calidad

import numpy as np


if __name__ == '__main__':
    N = 5000  # por ejemplo, matriz más grande
    np.random.seed(1)
    image = np.random.rand(N, N)
    kernel = np.array([[1, 0, -1],
                       [1, 0, -1],
                       [1, 0, -1]])

    comparar_rendimiento(
        lambda: ejecutar_scipy(image, kernel),
        lambda: ejecutar_scipy_ray(image, kernel)
    )
    
  
    
    # Compara calidad de código entre los archivos fuente
    comparar_calidad("scipy_original.py", "scipy_pypar.py")
