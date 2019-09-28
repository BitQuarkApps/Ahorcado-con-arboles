# Juego del ahorcado


## Creación del entorno virtual

Es necesario virtualenv (python3)

Para instalar virtualenv con python3

```bash
pip3 install virtualenv
```

Para generar el virtualenv

```bash
virtualenv venv
```

Activar el virtualenv

```bash
source venv/bin/activate
```

## Instalación

Una vez activado el entorno virtual se deben de instalar desde cero las dependecias.
Para instalar las dependencias del proyecto ejecute el siguiente comando:

```bash
pip install -r requirements.txt
```

## Ejecutar el programa

```bash
python arbol.py
```

Generará una imagen llamada "arbol.png" en el directorio raíz.

## Desactivar el entorno virtual

```bash
deactivate venv
```