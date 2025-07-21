from trimesh_original import procesar_vertices
from trimesh_pypar import procesar_vertices_ray
from comparar_tiempo import comparar_rendimiento
from comparar_pylint import comparar_calidad

if __name__ == '__main__':
   

    comparar_rendimiento(procesar_vertices,procesar_vertices_ray)
    
    comparar_calidad("trimesh_original.py", "trimesh_pypar.py")
