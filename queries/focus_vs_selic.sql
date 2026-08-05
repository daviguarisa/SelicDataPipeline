WITH focus_clean AS (
    SELECT 
        CAST(data AS DATE) AS data_referencia,
        indicador,
        mediana AS expectativa_mediana,
        minimo AS expectativa_minima,
        maximo AS expectativa_maxima
    FROM read_parquet('data/silver/focus.parquet')
    WHERE LOWER(indicador) LIKE '%selic%'
),
selic_clean AS (
    SELECT 
        CAST(data AS DATE) AS data_referencia,
        selic_meta AS taxa_realizada
    FROM read_parquet('data/silver/selic.parquet')
)
SELECT 
    f.data_referencia,
    f.indicador,
    f.expectativa_mediana,
    f.expectativa_minima,
    f.expectativa_maxima,
    s.taxa_realizada,
    ROUND(f.expectativa_mediana - s.taxa_realizada, 4) AS erro_projecao
FROM focus_clean f
LEFT JOIN selic_clean s 
    ON f.data_referencia = s.data_referencia
ORDER BY f.data_referencia DESC;