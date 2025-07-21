import numpy as np
import trimesh
import ray

def procesar_vertices_parallel_func_0(remote_list_0):
    rtLst = []
    mesh = trimesh.creation.icosphere(subdivisions=3, radius=1.0) 
    for loopIdx in range(len(remote_list_0)):
        (i,) = remote_list_0[loopIdx]
        v = mesh.vertices[i]
        expr_tmp_0 = np.linalg.norm(v)
        rtLst.append((expr_tmp_0, v))
    return rtLst

def procesar_vertices_ray(subdivisions=3):
    if not ray.is_initialized():
        ray.init()

    mesh = trimesh.creation.icosphere(subdivisions=subdivisions, radius=1.0)
    resultados = []

    remote_list_0 = [(i,) for i in range(len(mesh.vertices))]
    totalLength = len(remote_list_0)
    BlockLength = (totalLength // 10)
    while ((BlockLength * 10) < totalLength):
        BlockLength += 1

    
    remote_list_1 = [
        ray.remote(procesar_vertices_parallel_func_0).remote(remote_list_0[i * BlockLength:(i + 1) * BlockLength])
        for i in range(10)
    ]

    rmtTmp = ray.get(remote_list_1)
    remote_list_1 = [item for sublist in rmtTmp for item in sublist]

    for loop_idx_2 in range(len(mesh.vertices)):
        (i,) = remote_list_0[loop_idx_2]
        (expr_tmp_0, v) = remote_list_1[loop_idx_2]
        dist = expr_tmp_0
        resultados.append(dist)

    return resultados
