Para probar Pypar asegurese de tener instalado:

python==3.8.10
astunparse==1.6.3


Si quiere probar `usage.py`, instale:

scikit-image==0.19.3


Para probar el resto de biblotecas ocupadas en este proyecto:

-Abre su consola de comandos con el ambiente de python 3.8.10

-Instale las herramientas usadas en el proyecto:
-Pylint
-Pyinstrument

usando el comando: "pip install pylint" 

Tambien asegurese de tener ray instalado:
pip install ray

-Dirijase a la carpeta "comparar_codigos"


-Elija una de las 7 bibliotecas usando su terminal. Ej: cd scikit_image

--IMPORTANTE--
-Aseguresse de tener las bibliotecas instaladas en su ambiente. en caso de no tenerlas corra el siguiente comando

pip install (nombre de la bibloteca)
Ejemplo: pip install trimesh

EXCEPCION
En caso de sklearn tiene que correr el siguiente comando:

pip install scikit-learn


-Dentro de la carpeta de la biblioteca elija, use el siguiente comando: "python comparar_(nombredelafuncion)" 
Por ejemplo en la carpeta scikit_image seria: "python comparar_image"
