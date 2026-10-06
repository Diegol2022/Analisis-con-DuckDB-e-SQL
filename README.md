# DuckDB Weather Analysis

Este proyecto analiza un conjunto de datos meteorológicos de Reino Unido usando DuckDB para ejecutar consultas SQL directamente sobre un archivo CSV. El programa permite explorar la estructura del dataset, resumir registros por década, calcular promedios mensuales y detectar días con condiciones climáticas extremas.

## Descripción del proyecto

El script principal, `main.py`, conecta DuckDB en memoria y carga el archivo `Data/uk_climate.csv` mediante `read_csv_auto()`. A partir de ese punto, ejecuta varias consultas SQL para responder preguntas clave sobre el clima registrado:

- Ver una vista previa del dataset
- Contar registros válidos por década
- Identificar temperaturas nulas o faltantes
- Calcular promedios mensuales de temperatura y precipitación
- Detectar días con calor extremo o lluvias intensas
- Obtener los máximos históricos por estación del año

> **Nota:** la carpeta de datos se llama `Data` (con mayúscula). En Linux y macOS las rutas distinguen mayúsculas de minúsculas, por lo que `main.py` usa exactamente `Data/uk_climate.csv`.

## Dataset

El dataset contiene **23.376 observaciones diarias** entre el 1 de enero de 1961 y el 31 de diciembre de 2024 (64 años), sin valores nulos en ninguna columna. Los valores corresponden a promedios diarios para el Reino Unido. Incluye campos como:

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
git clone [<url-del-repositorio>](https://github.com/Diegol2022/Analisis-con-DuckDB-e-SQL)
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

### 5. Máximos históricos por estación

Agrupa los registros con `GROUP BY season` y calcula, para cada estación del año:

- temperatura máxima y mínima registrada
- precipitación diaria máxima
- velocidad máxima del viento
- cantidad de registros

```sql
SELECT 
    season AS estacion,
    ROUND(MAX(temp), 2) AS temp_maxima,
    ROUND(MIN(temp), 2) AS temp_minima,
    ROUND(MAX(precipitation), 2) AS precipitacion_maxima,
    ROUND(MAX(wind_speed), 2) AS viento_maximo,
    COUNT(*) AS total_registros
FROM read_csv_auto('Data/uk_climate.csv')
GROUP BY season
ORDER BY temp_maxima DESC;
```

## Hallazgos analíticos

### Calidad de los datos

- Las 23.376 filas tienen temperatura válida: la consulta 1 reporta **0 temperaturas nulas** en todas las décadas.
- Las décadas completas tienen 3.652 o 3.653 registros (según los años bisiestos). La década de 1960 tiene 3.287 porque empieza en 1961, y la de 2020 tiene 1.827 porque llega hasta 2024.

### Ciclo anual (consulta 2)

- **Julio** es el mes más cálido (14,65 °C promedio) y **enero** el más frío (3,37 °C).
- La lluvia está repartida durante todo el año, pero es mayor en otoño e invierno: **octubre** es el mes más lluvioso (8,07 mm/día) y **abril** el más seco (5,87 mm/día).

### Días extremos (consulta 3)

- **Ningún día supera los 30 °C**. La temperatura máxima del dataset es 23,59 °C, porque se trata de promedios diarios de todo el país y no de máximas de una estación meteorológica. Por eso la categoría "Calor Extremo" nunca aparece.
- Hay **1.037 días con lluvia intensa** (más de 20 mm). La cantidad por década pasa de 102 en los años 60 a valores entre 160 y 181 desde los 80.

### Máximos por estación (consulta 4)

| Estación | Temp. máxima (°C) | Temp. mínima (°C) | Precipitación máxima (mm) | Viento máximo |
|---|---|---|---|---|
| Verano (summer) | 23,59 | 6,28 | 57,29 | 7,85 |
| Otoño (autumn) | 19,63 | -2,63 | 49,57 | 9,46 |
| Primavera (spring) | 17,95 | -3,41 | 36,97 | 9,37 |
| Invierno (winter) | 12,30 | -7,21 | 49,35 | 9,92 |

- El día más caluroso del registro fue el **19/07/2022** (23,59 °C), durante la ola de calor de ese verano.
- Los récords de temperatura de las cuatro estaciones son posteriores a 2015: invierno (19/12/2015), primavera (26/05/2017), verano (19/07/2022) y otoño (09/09/2023).
- La mayor lluvia diaria ocurrió en verano (**10/08/2004**, 57,29 mm), aunque el verano no es la estación más lluviosa en promedio. Las tormentas estivales son menos frecuentes pero más intensas.
- El invierno concentra los vientos más fuertes y las temperaturas más bajas.

### Tendencia de largo plazo

La temperatura promedio pasa de **7,96 °C en los años 60** a **9,55 °C en los 2020**, un aumento de alrededor de 1,6 °C. Este cálculo no forma parte de `main.py`, pero se obtiene con un `AVG(temp)` agrupado por `decade`.

## Tiempos de respuesta

Cada consulta mide su tiempo de ejecución con `time.time()` y lo muestra en consola. Estos son los tiempos obtenidos en una ejecución local (Windows, Python 3.10). Los valores pueden variar según el equipo.

| Consulta | Descripción | Tiempo (ms) |
|---|---|---|
| 1 | Registros válidos por década | 78,30 |
| 2 | Promedios mensuales | 74,80 |
| 3 | Días climáticos extremos | 77,30 |
| 4 | Máximos históricos por estación | 96,25 |

| | **Total** | **326,65** |

Todas las consultas se resuelven en menos de 100 ms sobre las 23.376 filas, con un promedio de unos 82 ms. DuckDB lee el CSV directamente, sin necesidad de cargarlo antes en una base de datos ni de crear tablas.

Cada consulta vuelve a leer el CSV con `read_csv_auto()`, así que la mayor parte del tiempo medido corresponde a la lectura y detección de tipos del archivo, no al cálculo en sí. Eso explica que consultas de distinta complejidad tarden casi lo mismo. La consulta 4 fue la más lenta en esta ejecución, posiblemente porque calcula cinco agregaciones por grupo, aunque con una sola medición la diferencia puede deberse también a variaciones normales del equipo. Si se necesitara más velocidad, se podría cargar el CSV una sola vez en una tabla en memoria (`CREATE TABLE clima AS SELECT * FROM read_csv_auto(...)`) y consultar esa tabla.

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
