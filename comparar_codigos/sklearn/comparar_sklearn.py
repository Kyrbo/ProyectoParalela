from sklearn_original import ejecutar_sklearn
from sklearn_pypar import ejecutar_sklearn_ray
from comparar_tiempo import comparar_rendimiento
from comparar_pylint import comparar_calidad

if __name__ == '__main__':
    comparar_rendimiento(ejecutar_sklearn,ejecutar_sklearn_ray)

    comparar_calidad('sklearn_original.py', 'sklearn_pypar.py')
