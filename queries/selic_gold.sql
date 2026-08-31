WITH selic_clean AS (
    SELECT 
        CAST(data AS DATE) AS data_referencia,
        selic_meta AS taxa_realizada
    FROM read_parquet('data/silver/selic.parquet')
)
SELECT * FROM selic_clean;