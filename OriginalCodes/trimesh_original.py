import numpy as np
import trimesh

def procesar_vertices(subdivisions=3):
    mesh = trimesh.creation.icosphere(subdivisions=subdivisions, radius=1.0)
    resultados = []
    for i in range(len(mesh.vertices)):
        v = mesh.vertices[i]
        dist = np.linalg.norm(v)
        resultados.append(dist)
    return resultados
