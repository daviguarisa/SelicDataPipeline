WITH copom_clean AS (
    SELECT
        reuniao_index, 
        reuniao_num,
        reuniao_ano,
        reuniao_data,
        vigencia_inicio,
        vigencia_fim,
        meta_selic,
        taxa_selic_pct,
        taxa_selic_aa
    FROM read_parquet('data/silver/copom.parquet')
)
SELECT * FROM copom_clean;