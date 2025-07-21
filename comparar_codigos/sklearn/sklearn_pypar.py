
import numpy as np
import ray
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def calcular_normas_parallel_func_0(remote_indices, X):
    resultados = []
    for i in remote_indices:
        resultados.append(np.linalg.norm(X[i]))
    return resultados

def ejecutar_sklearn_ray():
    digits = load_digits()
    X_train, X_test, y_train, y_test = train_test_split(
        digits.data, digits.target, random_state=42
    )

    pca = PCA(n_components=30)
    X_train_pca = pca.fit_transform(X_train)
    X_test_pca = pca.transform(X_test)

    if not ray.is_initialized():
        ray.init()


    indices = list(range(len(X_test_pca)))
    block_size = (len(indices) + 9) // 10
    bloques = [indices[i * block_size:(i + 1) * block_size] for i in range(10)]

 
    futures = [ray.remote(calcular_normas_parallel_func_0).remote(bloque, X_test_pca) for bloque in bloques]
    resultados_por_bloque = ray.get(futures)

   
    normas = [item for sublist in resultados_por_bloque for item in sublist]

    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train_pca, y_train)
    y_pred = clf.predict(X_test_pca)

    return accuracy_score(y_test, y_pred), normas
