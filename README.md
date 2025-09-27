# UNIVERSIDAD EAFIT
# 2025-2
# PROFESOR: EDWIN MONTOYA – emontoya@eafit.edu.co

MLOps – ejemplo 2

Contexto: 3. Automatización del data pipeline

# Problema:

Se desea crear un script y automatización para la descarga de datos que se actualizan periódicamente de una API en Internet y ser almacenados como los datos crudos (raw) de un proyecto de ML. Se tienen los scripts de captura de datos y la automatización desde Github Actions. Si bien los datos actualizados vuelven al repositorio, la Automatización del podría llegar al DataLake o BD para las siguientes fases de preparación de datos, EDA o ingeniería de características.

Los datos son de la disponibilidad de celdas libres en diferentes parqueaderos de una ciudad, de tal manera que podamos realizar un modelo predictivo con días / horas de anticipación de hacia cual parqueadero dirigirse en caso de necesitar uno.

## Predicción de celdas libres en parqueaderos de Donostia (España)

Este ejemplo construye un pipeline de MLOps para un modelo que predice el número de celdas de parqueaderos en Donostia (españa).

Por ahora incluye la automatización de la extracción de datos.

### Automatización de extracción de datos con Github Actions

La ciudad de Donostia no provee datos históricos de celdas libres en parqueaderos. Es por ello, que debemos crear una extracción periódica para crear datos históricos.

La extracción se hace con el archivo: `extract_data.py` ubicado en la carpeta: `data_extraction`. 

`extract_data.py` hace llamados al endpoint donde los datos reciden, y los va agregando en el archivo: `data.csv` en la carpeta `data`. 

El archivo `data_extraction/update_data.sh` envia (push) los datos generados al Github. 

La ejecución de estos dos archivos es automatizados a través de `update_data.yml` ejecutado como un Github Action workflow, ejecutado cada 2 horas.

Datos Fuente: 

- https://www.donostia.eus/info/ciudadano/camaras_trafico.nsf/getParkings.xsp' 

Ingesta: 

- Crawler o robot en python (extract_data.py)
- Automatizado en ejecución cada hora, en github Actions

Almacenamiento:

- Queda almacenado en el repositorio github/data/data.csv

Procesamiento: 

- Ninguno para este ejemplo

Aplicación: 

- Ninguna para este ejemplo
 
## ETAPAS CICLO DE VIDA DATOS:

1.	Data source: API en Internet de parqueaderos libres en una ciudad
2.	Ingesta: Automática con Github Actions

    a.	PIPELINE PARA COLECTAR DATOS (.github/workflows/update_data.yml y data_extraction/update_data.sh)

    b.	Paso 1: configurar ambiente python3.9

    c.	Paso 2: ejecutar script: data_extraction/extract_data.py

    d.	Paso 3: enviar datos actualizados al mismo repo github en data/data.csv con el script: data_extraction/update_data.sh


3.	DATOS DE ENTRENAMIENTO – en repositorio github: data/data.csv
4.	ENTRENAMIENTO – sin especificar
5.	MODELOS ENVIADOS A GITHUB: sin especificar


### Consideración: generar API Token de github para permitir actualizar el repo:

* DEBE CONFIGURAR UNA VARIABLE DE AMBIENTE GH_TOKEN EN Github-Settings-> Developer Settings -> Personal access token - > Tokens

* LUEGO DENTRO DEL REPOSITORIO: Settings -> Secrets and variables -> Actions -> Secrets -> Environment secrets

* Adicionar el access token al script: .github/workflows/update_data.yml:

* git remote set-url origin https://x-access-token:${{ secrets.GH_TOKEN }}@github.com/edwinm67/mlops-ejemplo2.git


## TECNOLOGIAS:

LOCAL:
 
- Python 3.9
- Visual Studio Code
- Git

NUBE:

- Cuenta github
- Servicios:
    - Github Actions

## PROCEDIMIENTO:

1.	Clonar repo de clase:

- https://github.com/edwinm67/mlops-ejemplo2.git 

2.	Crear su propio repo ‘mlops-ejemplo2.git’ en su cuenta github y seguir trabajando en este para todos los cambios.

3.	Realizar los ajustes respectivos en su propio código, cada vez haga ‘git push’

4.	Revisar la ejecución de las acciones github

5.	Actualizar el repositorio local para verificar cambios en los datos y buen funcionamiento del crarler y automatización: 

    LOCAL: git pull

6.	documente todas las anteriores actividades

7.	entregar el lab



