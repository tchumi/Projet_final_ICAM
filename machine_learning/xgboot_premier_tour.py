import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# 📂 Chemin des données
data_path = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/elections_socio_fusionnes.csv"
df = pd.read_csv(data_path, dtype={"codecommune": str, "année": int})

# 📌 Sélection des colonnes pertinentes pour le modèle du 1er tour
features_base = [
    'exprimes', 'voteG', 'voteCG', 'voteC', 'voteCD', 'voteD', 'voteTG', 'voteTD',
    'voteGCG', 'voteDCD', 'pvoteG', 'pvoteCG', 'pvoteC', 'pvoteCD', 'pvoteD',
    'pvoteTG', 'pvoteTD', 'pvoteTGratio', 'pvoteTDratio',
    'revratio', 'pchom', 'pouvr', 'pcadr', 'pibratio'
]
features_with_clusters = features_base + ["cluster_corrige_1er_tour"] if "cluster_corrige_1er_tour" in df.columns else features_base
target_columns = ['pvoteG', 'pvoteCG', 'pvoteC', 'pvoteCD', 'pvoteD', 'pvoteTG', 'pvoteTD']  # Variables cibles

# 📌 Split Chronologique pour l’Entraînement
train = df[df["année"] <= 2012]
test = df[df["année"] == 2017]
validation = df[df["année"] == 2022]

# 📌 Fonction pour entraîner et évaluer un modèle XGBoost multivarié
def train_evaluate_xgboost(train, test, features):
    X_train, y_train = train[features], train[target_columns]
    X_test, y_test = test[features], test[target_columns]

    # Définition et entraînement du modèle XGBoost
    model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=100, learning_rate=0.1, max_depth=6)
    model.fit(X_train, y_train)

    # Prédictions et évaluation
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred, multioutput='uniform_average')
    
    return model, mae

# 📌 Expérimentation : Avec et Sans Clusters
print("🔍 Entraînement du modèle sans clusters...")
model_no_clusters, mae_no_clusters = train_evaluate_xgboost(train, test, features_base)

print("🔍 Entraînement du modèle avec clusters...")
model_with_clusters, mae_with_clusters = train_evaluate_xgboost(train, test, features_with_clusters)

# 📊 Comparaison des performances
print(f"📉 MAE Sans Clusters : {mae_no_clusters:.4f}")
print(f"📉 MAE Avec Clusters : {mae_with_clusters:.4f}")

# ✅ Sélection du meilleur modèle et évaluation finale sur 2022
best_model = model_with_clusters if mae_with_clusters < mae_no_clusters else model_no_clusters
X_validation, y_validation = validation[features_base], validation[target_columns]
y_pred_validation = best_model.predict(X_validation)
mae_validation = mean_absolute_error(y_validation, y_pred_validation, multioutput='uniform_average')

print(f"📊 Validation Finale (2022) - MAE : {mae_validation:.4f}")
