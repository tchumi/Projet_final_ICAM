import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_absolute_error

# 📂 Chargement des données
data_path = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/elections_socio_fusionnes.csv"
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

# 📌 Entraînement et Évaluation
print("🔍 Entraînement du modèle pour le premier tour...")
model_1st_tour, mae_1st_tour = train_evaluate_xgboost(train, test, features_base)

# 📊 Affichage des résultats
print(f"� MAE pour le premier tour (Test 2017) : {mae_1st_tour:.4f}")

# ✅ Validation finale sur 2022
X_validation, y_validation = validation[features_base], validation[target_columns]
y_pred_validation = model_1st_tour.predict(X_validation)
mae_validation = mean_absolute_error(y_validation, y_pred_validation, multioutput='uniform_average')

# � Affichage des résultats de validation
print(f"� MAE pour le premier tour (Validation 2022) : {mae_validation:.4f}")