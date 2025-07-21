import seaborn as sns
import ray

def analizar_por_especie_parallel_func_0(grupos):
    resultados = []
    for grupo in grupos:
        resultado = grupo['sepal_length'].mean() + grupo['sepal_width'].std()
        resultados.append(resultado)
    return resultados

def analizar_por_especie_ray():
    df = sns.load_dataset('iris')
    grupos = [grupo for _, grupo in df.groupby('species')]

    if not ray.is_initialized():
        ray.init()

   
    futures = [ray.remote(analizar_por_especie_parallel_func_0).remote([grupo]) for grupo in grupos]
    resultados_por_grupo = ray.get(futures)

   
    resultados = [item for sublist in resultados_por_grupo for item in sublist]
    return resultados
