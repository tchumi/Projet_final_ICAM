import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from scipy.spatial.distance import cosine
from scipy.stats import entropy
import numpy as np

# 📂 Chemin des données
data_path = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/elections_socio_fusionnes.csv"
output_report = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/prédiction_XGBOOST_premier_tour.txt"

df = pd.read_csv(data_path, dtype={"codecommune": str, "année": int})

# 📌 Sélection des features pour le premier tour (sans clusters ni votes)
features_base = ['exprimes', 'revratio', 'pchom', 'pouvr', 'pcadr', 'pibratio']

# 📌 Sélection des cibles pour le premier tour (votes à prédire)
target_columns = ['pvoteG', 'pvoteCG', 'pvoteC', 'pvoteCD', 'pvoteD']

# 📌 Split Chronologique pour l’Entraînement
train = df[df["année"] <= 2012]
test = df[df["année"] == 2017]
validation = df[df["année"] == 2022]

# 📌 Fonction pour entraîner et évaluer XGBoost pour le premier tour
def train_evaluate_xgboost(train, test, validation, features):
    X_train, y_train = train[features], train[target_columns]
    X_test, y_test = test[features], test[target_columns]
    X_validation, y_validation = validation[features], validation[target_columns]

    # Définition et entraînement du modèle XGBoost
    model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=100, learning_rate=0.1, max_depth=6)
    model.fit(X_train, y_train)

    # Prédictions et évaluation sur l'ensemble de test
    y_pred_test = model.predict(X_test)
    mae_test = mean_absolute_error(y_test, y_pred_test, multioutput='uniform_average')
    rmse_test = mean_squared_error(y_test, y_pred_test, squared=False)
    r2_test = r2_score(y_test, y_pred_test, multioutput='uniform_average')
    cosine_sim_test = 1 - cosine(y_test.values.flatten(), y_pred_test.flatten())
    kl_div_test = entropy(y_test.values.flatten(), y_pred_test.flatten())

    # Prédictions et évaluation sur l'ensemble de validation
    y_pred_validation = model.predict(X_validation)
    mae_validation = mean_absolute_error(y_validation, y_pred_validation, multioutput='uniform_average')
    rmse_validation = mean_squared_error(y_validation, y_pred_validation, squared=False)
    r2_validation = r2_score(y_validation, y_pred_validation, multioutput='uniform_average')
    cosine_sim_validation = 1 - cosine(y_validation.values.flatten(), y_pred_validation.flatten())
    kl_div_validation = entropy(y_validation.values.flatten(), y_pred_validation.flatten())

    return model, {
        'mae_test': mae_test,
        'rmse_test': rmse_test,
        'r2_test': r2_test,
        'cosine_sim_test': cosine_sim_test,
        'kl_div_test': kl_div_test,
        'mae_validation': mae_validation,
        'rmse_validation': rmse_validation,
        'r2_validation': r2_validation,
        'cosine_sim_validation': cosine_sim_validation,
        'kl_div_validation': kl_div_validation
    }

# 📌 Entraînement et Évaluation
print("🔍 Entraînement du modèle pour le premier tour...")
model_1st_tour, metrics = train_evaluate_xgboost(train, test, validation, features_base)

# 📊 Affichage des résultats
print(f"📉 MAE pour le premier tour (Test 2017) : {metrics['mae_test']:.4f}")
print(f"📉 RMSE pour le premier tour (Test 2017) : {metrics['rmse_test']:.4f}")
print(f"📉 R² pour le premier tour (Test 2017) : {metrics['r2_test']:.4f}")
print(f"📉 Cosine Similarity pour le premier tour (Test 2017) : {metrics['cosine_sim_test']:.4f}")
print(f"📉 KL Divergence pour le premier tour (Test 2017) : {metrics['kl_div_test']:.4f}")

print(f"📉 MAE pour le premier tour (Validation 2022) : {metrics['mae_validation']:.4f}")
print(f"📉 RMSE pour le premier tour (Validation 2022) : {metrics['rmse_validation']:.4f}")
print(f"📉 R² pour le premier tour (Validation 2022) : {metrics['r2_validation']:.4f}")
print(f"📉 Cosine Similarity pour le premier tour (Validation 2022) : {metrics['cosine_sim_validation']:.4f}")
print(f"📉 KL Divergence pour le premier tour (Validation 2022) : {metrics['kl_div_validation']:.4f}")

# 📌 Enregistrement des résultats dans un fichier
with open(output_report, 'w', encoding='utf-8') as f:
    f.write(f"📉 MAE pour le premier tour (Test 2017) : {metrics['mae_test']:.4f}\n")
    f.write(f"📉 RMSE pour le premier tour (Test 2017) : {metrics['rmse_test']:.4f}\n")
    f.write(f"📉 R² pour le premier tour (Test 2017) : {metrics['r2_test']:.4f}\n")
    f.write(f"📉 Cosine Similarity pour le premier tour (Test 2017) : {metrics['cosine_sim_test']:.4f}\n")
    f.write(f"📉 KL Divergence pour le premier tour (Test 2017) : {metrics['kl_div_test']:.4f}\n")
    f.write("\n")
    f.write(f"📉 MAE pour le premier tour (Validation 2022) : {metrics['mae_validation']:.4f}\n")
    f.write(f"📉 RMSE pour le premier tour (Validation 2022) : {metrics['rmse_validation']:.4f}\n")
    f.write(f"📉 R² pour le premier tour (Validation 2022) : {metrics['r2_validation']:.4f}\n")
    f.write(f"📉 Cosine Similarity pour le premier tour (Validation 2022) : {metrics['cosine_sim_validation']:.4f}\n")
    f.write(f"📉 KL Divergence pour le premier tour (Validation 2022) : {metrics['kl_div_validation']:.4f}\n")

print("\n✅ Rapport généré et enregistré dans 'prédiction_XGBOOST_premier_tour.txt'.")