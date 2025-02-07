import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_absolute_error

# 📂 Chargement des données
data_path = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/elections_socio_fusionnes.csv"
df = pd.read_csv(data_path, dtype={"codecommune": str, "année": int})

# 📌 Ajout des votes du 1ᵉʳ tour dans les features du 2ᵉ tour
features_2nd_tour = [
    'exprimesT2',
    'revratio', 'pchom', 'pouvr', 'pcadr', 'pibratio',
    # Ajout des résultats du 1er tour
    'pvoteG', 'pvoteCG', 'pvoteC', 'pvoteCD', 'pvoteD', 'pvoteTG', 'pvoteTD',
    'pvoteTGratio', 'pvoteTDratio'
]
target_columns = ['pvoteT2_ED', 'pvoteT2_D', 'pvoteT2_CD', 'pvoteT2_C', 'pvoteT2_G']

# 📌 Split Chronologique pour l’Entraînement
train = df[df["année"] <= 2012]
test = df[df["année"] == 2017]
validation = df[df["année"] == 2022]

# 📌 Fonction pour entraîner et évaluer XGBoost
def train_evaluate_xgboost(train, test, features):
    X_train, y_train = train[features], train[target_columns]
    X_test, y_test = test[features], test[target_columns]

    # Définition et entraînement du modèle XGBoost
    model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=100, learning_rate=0.1, max_depth=6)
    model.fit(X_train, y_train)

    # Prédictions et évaluation
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred, multioutput='uniform_average')
    
    return model, mae, y_pred

# 📌 Entraînement et Évaluation
print("🔍 Entraînement du modèle pour le 2ᵉ tour avec votes du 1ᵉʳ tour...")
model_2nd_tour, mae_2nd_tour, y_pred_test = train_evaluate_xgboost(train, test, features_2nd_tour)

# 📊 Affichage des résultats
print(f"📉 MAE pour le 2ᵉ tour (Test 2017) : {mae_2nd_tour:.4f}")

# ✅ Validation finale sur 2022
X_validation, y_validation = validation[features_2nd_tour], validation[target_columns]
y_pred_validation = model_2nd_tour.predict(X_validation)

mae_validation = mean_absolute_error(y_validation, y_pred_validation, multioutput='uniform_average')
print(f"📊 Validation Finale (2022) - MAE : {mae_validation:.4f}")

# ✅ Consolidation des résultats sur toute la France
df_results = pd.DataFrame(y_pred_validation, columns=target_columns)
df_results["année"] = validation["année"].values
df_results["exprimesT2"] = validation["exprimesT2"].values

# 📌 Calcul des résultats nationaux pondérés par le nombre de votes exprimés
df_results_national = df_results.copy()
for col in target_columns:
    df_results_national[col] = df_results_national[col] * df_results_national["exprimesT2"] / 100

df_national_summary = df_results_national.groupby("année")[target_columns].sum()

# 📊 Affichage des résultats nationaux
print("\n📊 Résultats consolidés sur la France :")
print(df_national_summary)

# ✅ Sauvegarde des résultats
result_path = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/resultats_nationaux_2nd_tour.csv"
df_national_summary.to_csv(result_path)
print(f"✅ Fichier des résultats nationaux sauvegardé : {result_path}")
