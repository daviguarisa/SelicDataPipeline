from pathlib import Path
import marimo

__generated_with = "0.24.2"
app = marimo.App()


@app.cell
def _():
    from pathlib import Path

    import duckdb
    import marimo as mo
    import plotly.graph_objects as go

    return Path, duckdb, go, mo


@app.cell
def _(Path, duckdb):
    DB_PATH = Path(__file__).resolve().parent.parent / "datalake.db"
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    df_raw = conn.sql("SELECT * FROM gold.expectativa_vs_realidade").df()
    conn.close()
    return DB_PATH, df_raw


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
def _(df_raw, go, mo, toggle_janela):
    opcoes_janela = {
        "1 Mês Antes": ("exp_1m_antes", "erro_1m"),
        "3 Meses Antes": ("exp_3m_antes", "erro_3m"),
        "6 Meses Antes": ("exp_6m_antes", "erro_6m"),
        "12 Meses Antes": ("exp_12m_antes", "erro_12m"),
    }

    janela_selecionada = toggle_janela.value

    df = df_raw[df_raw["reuniao_ano"] >= 2022].sort_values(
        "reuniao_data", ascending=True
    )

    col_exp, col_erro = opcoes_janela[janela_selecionada]

    mae = df[col_erro].abs().mean()
    bias = df[col_erro].mean()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["reuniao_data"],
            y=df["realidade_selic"],
            mode="lines+markers",
            name="Realidade (COPOM)",
            line=dict(color="#EF553B", width=2.5),
            hovertemplate="Data: %{x}<br>Selic Real: %{y:.2f}%<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["reuniao_data"],
            y=df[col_exp],
            mode="lines+markers",
            name=f"Expectativa ({janela_selecionada})",
            line=dict(color="#636EFA", width=2, dash="dash"),
            hovertemplate="Data: %{x}<br>Expectativa: %{y:.2f}%<extra></extra>",
        )
    )

    fig.update_layout(
        title={
            "text": f"<b>Focus vs COPOM (2022+) — {janela_selecionada}</b><br><sup>MAE (Erro Médio Absoluto): {mae:.2f} p.p. | Viés Médio: {bias:.2f} p.p.</sup>",
            "x": 0.0,
            "xanchor": "left",
            "y": 0.96,
        },
        xaxis_title="Data da Reunião do COPOM",
        yaxis_title="Taxa Selic (% a.a.)",
        template="plotly_white",
        hovermode="x unified",
        legend=dict(
            orientation="h", yanchor="bottom", y=1.12, xanchor="right", x=1
        ),
        margin=dict(l=40, r=40, t=110, b=40),
        height=520,
    )

    header = mo.md("## Comparando Expectativas do Focus com a Realidade da Selic")
    mo.vstack([header, toggle_janela, mo.ui.plotly(fig)])


if __name__ == "__main__":
    app.run()