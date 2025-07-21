from propagate_original import propagate
from propagate_pypar import propagate_parallel
from comparar_tiempo import comparar_rendimiento
from comparar_pylint import comparar_calidad
from comparar_pylint import comparar_calidad
from comparar_tiempo import comparar_rendimiento
import warnings


# DummyTypeInfer: contiene .warnings para usarse con catch_warnings
class DummyTypeInfer:
    def __init__(self):
        self.warnings = warnings


# DummyConstraint: simula una función con atributo .loc y que recibe typeinfer
class DummyConstraint:
    def __init__(self, name):
        self.loc = type('Loc', (object,), {'filename': 'dummy.py', 'line': 1})()

    def __call__(self, typeinfer):
        # Código falso que simula trabajo
        for _ in range(10000):
            pass


# DummySelf: contiene una lista de constraints como espera propagate()
class DummySelf:
    def __init__(self):
        self.constraints = [DummyConstraint(f"c{i}") for i in range(10000)]



# Crear instancias
obj = DummySelf()
typeinfer = DummyTypeInfer()

# Envolver las funciones para pasarlas a comparar_rendimiento()
original = lambda: propagate(obj, typeinfer)
paralela = lambda: propagate_parallel(obj, typeinfer)

# Ejecutar comparaciones
comparar_rendimiento(original, paralela)
comparar_calidad("propagate_original.py", "propagate_parallel.py")
