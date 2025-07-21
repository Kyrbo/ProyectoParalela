from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

def ejecutar_sklearn():
    digits = load_digits()
    X_train, X_test, y_train, y_test = train_test_split(
        digits.data, digits.target, random_state=42
    )

    pca = PCA(n_components=30)
    X_train_pca = pca.fit_transform(X_train)
    X_test_pca = pca.transform(X_test)

 
    normas = []
    for i in range(len(X_test_pca)):
        norma = np.linalg.norm(X_test_pca[i])
        normas.append(norma)

    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train_pca, y_train)
    y_pred = clf.predict(X_test_pca)

    return accuracy_score(y_test, y_pred), normas
