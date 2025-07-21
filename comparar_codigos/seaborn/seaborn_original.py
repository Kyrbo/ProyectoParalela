import seaborn as sns
import pandas as pd

def analizar_por_especie():
    df = sns.load_dataset('iris')
    resultados = []
    for especie, grupo in df.groupby('species'):
        resultado = grupo['sepal_length'].mean() + grupo['sepal_width'].std()
        resultados.append(resultado)
    return resultados
