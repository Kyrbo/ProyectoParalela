from pyinstrument import Profiler
import time

def comparar_rendimiento(func_original, func_parallel, *args, **kwargs):
    print("\n========== COMPARACIÓN DE RENDIMIENTO ==========")

    # --- Versión original ---
    print("\n Ejecutando versión ORIGINAL...")
    prof1 = Profiler()
    prof1.start()
    start1 = time.time()
    result1 = func_original(*args, **kwargs)
    end1 = time.time()
    prof1.stop()
    duracion_original = end1 - start1
    print(f"Tiempo ORIGINAL: {duracion_original:.4f} segundos")
    print(prof1.output_text(unicode=True, color=True))

    # --- Versión paralela ---
    print("\n Ejecutando versión PARALELA...")
    prof2 = Profiler()
    prof2.start()
    start2 = time.time()
    result2 = func_parallel(*args, **kwargs)
    end2 = time.time()
    prof2.stop()
    duracion_paralela = end2 - start2
    print(f" Tiempo PARALELA: {duracion_paralela:.4f} segundos")
    print(prof2.output_text(unicode=True, color=True))

    # --- Comparación ---
    mejora = ((duracion_original - duracion_paralela) / duracion_original) * 100
    print(f"\n Mejora estimada: {mejora:.2f}%")

    return result1, result2
