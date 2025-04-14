from model import pipeline_gbr, df
import pandas as pd
import numpy as np

# Função 1: Gerar previsão de demanda para um dia específico
def gerar_previsao(data_previsao: str, modelo, salvar_csv=True):
    data_ref = pd.to_datetime(data_previsao)
    produtos_unicos = df[["produto", "categoria"]].drop_duplicates().reset_index(drop=True)
    base_previsao = produtos_unicos.copy()
    base_previsao["mes"] = data_ref.month
    base_previsao["dia_semana"] = data_ref.day_name()
    precos_medio = df.groupby("produto")["preco_unitario"].mean().reset_index()
    base_previsao = base_previsao.merge(precos_medio, on="produto", how="left")
    previsoes = modelo.predict(base_previsao)
    resultado = base_previsao.copy()
    resultado["data_previsao"] = data_ref.date()
    resultado["previsao"] = np.round(previsoes).astype(int)

    df_resultado = resultado[["data_previsao", "produto", "categoria", "mes", "dia_semana", "preco_unitario", "previsao"]]
    
    if salvar_csv:
        nome_arquivo = f"data/previsao_demanda_{data_previsao}.csv".replace(":", "-")
        df_resultado.to_csv(nome_arquivo, index=False)
        print(f"Previsão salva em: {nome_arquivo}")
    
    return df_resultado


# Função 2: Gerar alerta de reposição com base em limites por categoria
def gerar_alerta_reposicao(df_previsao, salvar_csv=True):
    limites_categoria = {
        "Hortifruti": 80,
        "Bebidas": 120,
        "Mercearia": 100,
        "Padaria": 70,
        "Laticínios": 90,
        "Higiene": 60,
        "Limpeza": 60,
        "Carnes": 130
    }
    df_alerta = df_previsao.copy()
    df_alerta["limite_reposicao"] = df_alerta["categoria"].map(limites_categoria)
    df_alerta["alerta_reposicao"] = df_alerta["previsao"] > df_alerta["limite_reposicao"]

    if salvar_csv:
        nome_arquivo = f"data/previsao_alerta_{df_alerta['data_previsao'].iloc[0]}.csv"
        df_alerta.to_csv(nome_arquivo, index=False)
        print(f"Arquivo com alertas salvo em: {nome_arquivo}")

    return df_alerta

# Executar exemplo para 2024-01-02
df_prev = gerar_previsao("2024-01-02", pipeline_gbr)
df_alertas = gerar_alerta_reposicao(df_prev)


# Exemplo de uso:
if __name__ == "__main__":
    # Gerar previsão para uma data
    df_previsao = gerar_previsao("2024-01-02", pipeline_gbr)

    # Gerar alertas com base nessa previsão
    df_alerta = gerar_alerta_reposicao(df_previsao)
