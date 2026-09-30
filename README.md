# DuckDB Weather Analysis

Este proyecto analiza un conjunto de datos meteorológicos de Reino Unido usando DuckDB para ejecutar consultas SQL directamente sobre un archivo CSV. El programa permite explorar la estructura del dataset, resumir registros por década, calcular promedios mensuales y detectar días con condiciones climáticas extremas.

## Descripción del proyecto

El script principal, `main.py`, conecta DuckDB en memoria y carga el archivo `Data/uk_climate.csv` mediante `read_csv_auto()`. A partir de ese punto, ejecuta varias consultas SQL para responder preguntas clave sobre el clima registrado:

- Ver una vista previa del dataset
- Contar registros válidos por década y estación
- Identificar temperaturas nulas o faltantes
- Calcular promedios mensuales de temperatura y precipitación
- Detectar días con calor extremo o lluvias intensas

## Dataset

El dataset contiene observaciones diarias con campos como:

- `date`
- `decade`
- `year`
- `season`
- `month`
- `day`
- `day_of_year`
- `temp`
- `wind_speed`
- `precipitation`
- `surface_runoff`
- `dewpoint_temp`

## Requisitos

Necesitas Python 3 y las siguientes dependencias:

- `duckdb`
- `pandas`

## Instalación

1. Clona el repositorio:

```bash
git clone <url-del-repositorio>
cd duckdb-weather-analysis
```

2. Crea un entorno virtual (opcional pero recomendado):

```bash
python -m venv venv
venv\Scripts\activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

Desde la raíz del proyecto:

```bash
python main.py
```

Al ejecutarse, el programa mostrará en consola una serie de tablas con los resultados de las consultas SQL.

## Consultas incluidas

### 1. Registro y vista previa del dataset

Muestra los primeros 5 registros para comprobar la estructura del CSV y validar el formato de los datos.

### 2. Conteo y limpieza por década

Calcula:

- número total de registros por década
- cantidad de valores de temperatura válidos
- número de temperaturas nulas

### 3. Promedios mensuales

Agrupa por mes y calcula:

- temperatura promedio
- precipitación promedio

### 4. Días climáticos extremos

Filtra registros con:

- temperatura superior a 30°C
- precipitación superior a 20 mm

y los clasifica según el tipo de fenómeno climático.

## Estructura del proyecto

```text
duckdb-weather-analysis/
├── Data/
│   └── uk_climate.csv
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Tecnologías utilizadas

- Python
- DuckDB
- Pandas
- SQL para análisis de datos

## Objetivo

Este programa sirve como ejemplo práctico de análisis de datos con SQL embebido, ideal para aprender a:

- leer archivos CSV con DuckDB
- ejecutar consultas analíticas en memoria
- generar resúmenes y filtros de datos
- trabajar con series temporales meteorológicas

## Autor

Proyecto desarrollado como ejercicio de análisis de datos y consulta SQL sobre datos climáticos.
