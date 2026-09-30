import duckdb
import time

def main():
    # Conexión embebida en memoria
    con = duckdb.connect(database=':memory:')
    
    csv_file_path = 'data/uk_climate.csv'
    
    print("=== 1. Registro y Vista Previa del Dataset ===")
    # Consulta directa sobre el archivo CSV (Punto 4)
    df_preview = con.execute(f"""
        SELECT * 
        FROM read_csv_auto('{csv_file_path}') 
        LIMIT 5
    """).df()
    print(df_preview)
    print("\n" + "="*50 + "\n")

    # -------------------------------------------------------------
    # Consulta 1: Conteo y Limpieza (Filtrado de nulos)
    # -------------------------------------------------------------
    start_time = time.time()
    print("=== Consulta 1: Resumen de registros válidos por estación ===")
    q1 = con.execute(f"""
        SELECT 
            decade,
            COUNT(*) AS total_registros,
            COUNT(temp) AS registros_temperatura_valida,
            COUNT(*) - COUNT(temp) AS temperaturas_nulas
        FROM read_csv_auto('{csv_file_path}')
        GROUP BY decade
        ORDER BY total_registros DESC
    """).df()
    print(q1)
    print(f"Tiempo de ejecución: {(time.time() - start_time) * 1000:.2f} ms\n")

    # -------------------------------------------------------------
    # Consulta 2: Promedios Mensuales (Agregación)
    # -------------------------------------------------------------
    start_time = time.time()
    print("=== Consulta 2: Promedio mensual de temperatura y precipitación ===")
    q2 = con.execute(f"""
        SELECT 
            month AS mes,
            ROUND(AVG(temp), 2) AS temp_promedio,
            ROUND(AVG(precipitation), 2) AS precipitacion_total
        FROM read_csv_auto('{csv_file_path}')
        WHERE temp IS NOT NULL
        GROUP BY month
        ORDER BY month ASC
    """).df()
    print(q2)
    print(f"Tiempo de ejecución: {(time.time() - start_time) * 1000:.2f} ms\n")

    # -------------------------------------------------------------
    # Consulta 3: Filtrado Complejo y Máximos Históricos
    # -------------------------------------------------------------
    start_time = time.time()
    print("=== Consulta 3: Días de clima extremo (Temp > 30°C o Precipitación > 20mm) ===")
    q3 = con.execute(f"""
        SELECT 
            decade,
            date,
            temp,
            precipitation,
            CASE 
                WHEN temp > 30 AND precipitation > 20 THEN 'Ola de Calor y Tormenta'
                WHEN temp > 30 THEN 'Calor Extremo'
                WHEN precipitation > 20 THEN 'Lluvia Intensa'
                ELSE 'Normal'
            END AS condicion_extrema
        FROM read_csv_auto('{csv_file_path}')
        WHERE temp > 30 OR precipitation > 20
        ORDER BY decade DESC, date ASC
        LIMIT 10
    """).df()
    print(q3)
    print(f"Tiempo de ejecución: {(time.time() - start_time) * 1000:.2f} ms\n")

if __name__ == "__main__":
    main()