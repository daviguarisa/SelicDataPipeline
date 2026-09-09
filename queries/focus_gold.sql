WITH focus_clean AS (
    SELECT 
    indicador,
    data::DATE AS data,
    reuniao_num,
    reuniao_ano,
    media,
    mediana,
    desvio_padrao,
    minimo,
    maximo,
    numero_respondentes,
    base_calculo
    FROM read_parquet('data/silver/focus.parquet')
)
SELECT * FROM focus_clean;