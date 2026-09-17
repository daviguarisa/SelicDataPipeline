from pathlib import Path
import marimo

__generated_with = "0.24.2"
app = marimo.App()


@app.cell
def _():
    from pathlib import Path

    import duckdb
    import marimo as mo
    import pandas as pd
    import plotly.graph_objects as go

    return Path, duckdb, go, mo, pd


@app.cell
def _(Path, duckdb):
    DB_PATH = Path(__file__).resolve().parent.parent / "datalake.db"
    conn = duckdb.connect(str(DB_PATH), read_only=True)

    df_historico = conn.sql(
        "SELECT * FROM gold.expectativa_vs_realidade WHERE reuniao_ano >= 2022 ORDER BY reuniao_data ASC"
    ).df()

    ultima_reuniao = conn.sql("""
        SELECT reuniao_ano, reuniao_num, reuniao_data, meta_selic 
        FROM gold.copom 
        ORDER BY reuniao_data DESC LIMIT 1
    """).fetchone()

    conn.close()
    return DB_PATH, df_historico, ultima_reuniao


@app.cell
def _(pd, ultima_reuniao):
    u_ano, u_num, u_data, u_selic = ultima_reuniao

    if u_num >= 8:
        prox_num = 1
        prox_ano = u_ano + 1
    else:
        prox_num = u_num + 1
        prox_ano = u_ano

    prox_data = pd.to_datetime(u_data) + pd.Timedelta(days=45)
    return prox_ano, prox_data, prox_num, u_selic


@app.cell
def _(mo):
    toggle_janela = mo.ui.radio(
        options=[
            "1 Mês Antes",
            "3 Meses Antes",
            "6 Meses Antes",
            "12 Meses Antes",
        ],
        value="1 Mês Antes",
        label="<b>Janela:</b>",
        inline=True,
    )
    return (toggle_janela,)


@app.cell
def _(
    DB_PATH,
    df_historico,
    duckdb,
    go,
    mo,
    prox_ano,
    prox_data,
    prox_num,
    toggle_janela,
    u_selic,
):
    janela_selecionada = toggle_janela.value

    opcoes_janela = {
        "1 Mês Antes": ("exp_1m_antes", "erro_1m", 1),
        "3 Meses Antes": ("exp_3m_antes", "erro_3m", 3),
        "6 Meses Antes": ("exp_6m_antes", "erro_6m", 6),
        "12 Meses Antes": ("exp_12m_antes", "erro_12m", 12),
    }

    col_exp, col_erro, meses_janela = opcoes_janela[janela_selecionada]

    mae = df_historico[col_erro].abs().mean()
    vies = df_historico[col_erro].mean()

    conn_func = duckdb.connect(str(DB_PATH), read_only=True)

    q_focus_janela = f"""
        SELECT media FROM gold.focus 
        WHERE reuniao_ano = {prox_ano} AND reuniao_num = {prox_num}
          AND data <= '{prox_data.strftime("%Y-%m-%d")}'::DATE - INTERVAL '{meses_janela} months'
        ORDER BY data DESC LIMIT 1
    """
    res_focus = conn_func.sql(q_focus_janela).fetchone()

    if not res_focus:
        res_focus = conn_func.sql(f"""
            SELECT media FROM gold.focus 
            WHERE reuniao_ano = {prox_ano} AND reuniao_num = {prox_num}
            ORDER BY data ASC LIMIT 1
        """).fetchone()

    conn_func.close()

    focus_bruto = res_focus[0] if res_focus else u_selic
    predicao_ajustada = focus_bruto - vies

    limite_inf = predicao_ajustada - mae
    limite_sup = predicao_ajustada + mae

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df_historico["reuniao_data"],
            y=df_historico["realidade_selic"],
            mode="lines+markers",
            name="Realidade (COPOM)",
            line=dict(color="#EF553B", width=2.5),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df_historico["reuniao_data"],
            y=df_historico[col_exp],
            mode="lines+markers",
            name=f"Focus ({janela_selecionada})",
            line=dict(color="#636EFA", width=2, dash="dash"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[prox_data],
            y=[predicao_ajustada],
            mode="markers",
            name=f"Predição R{prox_num}/{prox_ano}",
            marker=dict(color="#111827", size=14, symbol="star"),
            error_y=dict(
                type="data",
                array=[mae],
                visible=True,
                color="#111827",
                thickness=2,
                width=6,
            ),
            hovertemplate=(
                f"<b>Predição R{prox_num}/{prox_ano} ({janela_selecionada})</b><br>"
                f"Focus Bruto: {focus_bruto:.2f}%<br>"
                f"<b>Estimativa Calibrada: %{{y:.2f}}%</b><br>"
                f"Intervalo Esperado: [{limite_inf:.2f}% a {limite_sup:.2f}%]<br>"
                f"Margem erro (±MAE): ±{mae:.2f} p.p.<extra></extra>"
            ),
        )
    )

    fig.add_annotation(
        x=prox_data,
        y=predicao_ajustada,
        text=f" <b>{predicao_ajustada:.2f}%</b><br><sub>[{limite_inf:.2f}% - {limite_sup:.2f}%]</sub>",
        showarrow=True,
        arrowhead=2,
        arrowcolor="#111827",
        ax=45,
        ay=-15,
        font=dict(color="#111827", size=12),
        align="left",
        bgcolor="rgba(255, 255, 255, 0.85)",
        bordercolor="#111827",
        borderwidth=1,
    )

    fig.update_layout(
        title={
            "text": f"<b>Focus vs COPOM — {janela_selecionada} + Predição R{prox_num}/{prox_ano}</b><br>"
            f"<sup>Focus Bruto: {focus_bruto:.2f}%  |  <b>Predição Calibrada: {predicao_ajustada:.2f}%</b>  "
            f"(Intervalo: {limite_inf:.2f}% a {limite_sup:.2f}% | MAE: ±{mae:.2f} p.p.)</sup>",
            "x": 0.0,
            "xanchor": "left",
            "y": 0.96,
        },
        xaxis_title="Data da Reunião",
        yaxis_title="Taxa Selic (% a.a.)",
        template="plotly_white",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.12,
            xanchor="right",
            x=1,
        ),
        margin=dict(l=40, r=60, t=110, b=40),
        height=520,
    )

    header = mo.md("## Predição da Taxa Selic com Base no Boletim Focus")
    mo.vstack([header, toggle_janela, mo.ui.plotly(fig)])


if __name__ == "__main__":
    app.run()