import subprocess
import json

def analizar_pylint(path):
    result = subprocess.run(
        ['pylint', path, '--output-format=json'],
        capture_output=True, text=True
    )
    if result.returncode == 32 or not result.stdout.strip():
        return {}
    try:
        issues = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f" No se pudo decodificar el JSON de Pylint en {path}")
        return {}
    
    resumen = {
        'errores': len([i for i in issues if i['type'] == 'error']),
        'warnings': len([i for i in issues if i['type'] == 'warning']),
        'refactor': len([i for i in issues if i['type'] == 'refactor']),
        'convenciones': len([i for i in issues if i['type'] == 'convention']),
        'total': len(issues)
    }
    return resumen


def comparar_calidad(original_file, paralelizado_file):
    print(f"\n Comparando calidad entre:\n- Original: {original_file}\n- Paralelizado: {paralelizado_file}")

    r1 = analizar_pylint(original_file)
    r2 = analizar_pylint(paralelizado_file)

    if not r1 or not r2:
        print("No se pudo analizar uno de los archivos.")
        return

    def mostrar(nombre, datos):
        print(f"\n {nombre}")
        for k, v in datos.items():
            print(f"  {k}: {v}")

    mostrar("Original", r1)
    mostrar("Paralelizado", r2)

    print("\n DIFERENCIAS:")
    for clave in r1:
        dif = r1[clave] - r2[clave]
        signo = "+" if dif > 0 else ""
        print(f"  {clave}: {signo}{dif} ( {'mejoró' if dif > 0 else 'empeoró' if dif < 0 else 'sin cambio'} )")

    total_dif = r1['total'] - r2['total']
    print(f"\n Resultado general: {'Mejoró ' if total_dif > 0 else 'Empeoró ' if total_dif < 0 else 'Sin cambio'}")

