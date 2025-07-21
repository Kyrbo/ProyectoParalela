from seaborn_original import analizar_por_especie
from seaborn_pypar import analizar_por_especie_ray
from comparar_tiempo import comparar_rendimiento
from comparar_pylint import comparar_calidad

if __name__ == '__main__':
    comparar_rendimiento(analizar_por_especie,analizar_por_especie_ray)

    comparar_calidad('seaborn_original.py', 'seaborn_pypar.py')
