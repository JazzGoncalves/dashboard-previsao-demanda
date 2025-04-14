import pandas as pd
import numpy as np
from datetime import datetime
from model import pipeline_gbr, df 
import matplotlib.pyplot as plt

from pipeline_previsao import gerar_previsao

# Previsões para os 7 primeiros dias de janeiro de 2024
datas_previsao = pd.date_range(start="2024-01-01", end="2024-01-07")

# Lista para armazenar as previsões
lista_previsoes = []

for data in datas_previsao:
    previsao = gerar_previsao(data.strftime("%Y-%m-%d"), pipeline_gbr, salvar_csv=False)
    lista_previsoes.append(previsao)

# Concatenação das previsões
df_previsoes_multidias = pd.concat(lista_previsoes).reset_index(drop=True)

# Formatação
df_reais = df[df["data"].isin(datas_previsao)][["data", "produto", "quantidade_vendida"]].copy()
df_reais.rename(columns={"data": "data_previsao", "quantidade_vendida": "real"}, inplace=True)

df_previsoes_multidias["data_previsao"] = pd.to_datetime(df_previsoes_multidias["data_previsao"])
df_reais["data_previsao"] = pd.to_datetime(df_reais["data_previsao"])

df_monitoramento = pd.merge(df_previsoes_multidias, df_reais, on=["data_previsao", "produto"], how="left")

# Calculo de erro absoluto
df_monitoramento["erro_absoluto"] = abs(df_monitoramento["previsao"] - df_monitoramento["real"])

# Exporte base de monitoramento
df_monitoramento.to_csv("data/monitoramento_jan2024.csv", index=False)
print("Arquivo 'monitoramento_jan2024.csv' salvo com sucesso!")

# Média do erro absoluto por dia
media_erro_por_dia = df_monitoramento.groupby("data_previsao")["erro_absoluto"].mean().round(2)
print("\nErro médio por dia:\n", media_erro_por_dia)

plt.figure(figsize=(10, 5))
plt.plot(media_erro_por_dia.index, media_erro_por_dia.values, marker='o')
plt.title("Erro médio absoluto por dia - Janeiro 2024")
plt.xlabel("Data")
plt.ylabel("Erro Absoluto Médio")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("data/erro_medio_por_dia_jan2024.png")
print("Gráfico salvo como 'data/erro_medio_por_dia_jan2024.png'")