WITH focus_clean AS (
    SELECT 
        CAST(data AS DATE) AS data_referencia,
        indicador,
        mediana AS expectativa_mediana,
        minimo AS expectativa_minima,
        maximo AS expectativa_maxima
    FROM read_parquet('data/silver/focus.parquet')
    WHERE LOWER(indicador) LIKE '%selic%'
)
SELECT * FROM focus_clean;