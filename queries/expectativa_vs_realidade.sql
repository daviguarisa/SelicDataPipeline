WITH copom_base AS (
    SELECT 
        reuniao_index,
        reuniao_ano,
        reuniao_num,
        reuniao_data,
        meta_selic AS realidade_selic
    FROM gold.copom
),

focus_janelas AS (
    SELECT 
        c.reuniao_index,
        c.reuniao_ano,
        c.reuniao_num,
        c.reuniao_data,
        c.realidade_selic,
        
        -- Expectativa 1 Mês Antes
        (SELECT f.media 
         FROM gold.focus f 
         WHERE f.reuniao_ano = c.reuniao_ano 
           AND f.reuniao_num = c.reuniao_num 
           AND f.data <= c.reuniao_data - INTERVAL '1 month'
         ORDER BY f.data DESC LIMIT 1) AS exp_1m_antes,
         
        -- Expectativa 3 Meses Antes
        (SELECT f.media 
         FROM gold.focus f 
         WHERE f.reuniao_ano = c.reuniao_ano 
           AND f.reuniao_num = c.reuniao_num 
           AND f.data <= c.reuniao_data - INTERVAL '3 months'
         ORDER BY f.data DESC LIMIT 1) AS exp_3m_antes,

        -- Expectativa 6 Meses Antes
        (SELECT f.media 
         FROM gold.focus f 
         WHERE f.reuniao_ano = c.reuniao_ano 
           AND f.reuniao_num = c.reuniao_num 
           AND f.data <= c.reuniao_data - INTERVAL '6 months'
         ORDER BY f.data DESC LIMIT 1) AS exp_6m_antes,

        -- Expectativa 12 Meses Antes
        (SELECT f.media 
         FROM gold.focus f 
         WHERE f.reuniao_ano = c.reuniao_ano 
           AND f.reuniao_num = c.reuniao_num 
           AND f.data <= c.reuniao_data - INTERVAL '12 months'
         ORDER BY f.data DESC LIMIT 1) AS exp_12m_antes

    FROM copom_base c
)

SELECT 
    reuniao_index,
    reuniao_ano,
    reuniao_num,
    reuniao_data,
    realidade_selic,
    exp_1m_antes,
    exp_3m_antes,
    exp_6m_antes,
    exp_12m_antes,
    -- Métricas de Erro (Expectativa - Realidade)
    ROUND(exp_1m_antes - realidade_selic, 2) AS erro_1m,
    ROUND(exp_3m_antes - realidade_selic, 2) AS erro_3m,
    ROUND(exp_6m_antes - realidade_selic, 2) AS erro_6m,
    ROUND(exp_12m_antes - realidade_selic, 2) AS erro_12m
FROM focus_janelas
ORDER BY reuniao_data DESC;