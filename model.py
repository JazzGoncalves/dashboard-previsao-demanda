
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.ensemble import GradientBoostingRegressor

# 1. Carregamento e preparação da base
df = pd.read_csv("data/demanda_supermercado_2023_2024.csv")
df["data"] = pd.to_datetime(df["data"])
df["ano"] = df["data"].dt.year
df["mes"] = df["data"].dt.month
df["dia_semana"] = df["data"].dt.day_name()

# 2. Features e target
features = ["produto", "categoria", "mes", "dia_semana", "preco_unitario"]
target = "quantidade_vendida"
X = df[features]
y = df[target]

# 3. Separação treino/teste
X_train = X[df["ano"] == 2023]
X_test = X[df["ano"] == 2024]
y_train = y[df["ano"] == 2023]
y_test = y[df["ano"] == 2024]

# 4. Pipeline de pré-processamento + modelo
preprocessor = ColumnTransformer([
    ("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), ["produto", "categoria", "dia_semana"])
], remainder="passthrough")

pipeline_gbr = Pipeline([
    ("preprocess", preprocessor),
    ("model", GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42))
])

# 5. Treinamento do modelo
pipeline_gbr.fit(X_train, y_train)

# 6. Exportar variáveis úteis
__all__ = ["pipeline_gbr", "df"]
