import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
from scipy.spatial.distance import cosine
from scipy.stats import entropy

# 📂 Chargement des données
data_path = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/elections_socio_fusionnes.csv"
output_report = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/prediction_rolling_window_XGBOOST_deuxieme_tour.txt"

df = pd.read_csv(data_path, dtype={"codecommune": str, "année": int})

# 📌 Sélection des features pour le 2ᵉ tour (avec résultats du 1ᵉʳ tour)
features_2nd_tour = [
    'exprimesT2', 
    'revratio', 'pchom', 'pouvr', 'pcadr', 'pibratio',
    # Ajout des résultats du 1ᵉʳ tour
    'pvoteG', 'pvoteCG', 'pvoteC', 'pvoteCD', 'pvoteD', 'pvoteTG', 'pvoteTD',
    'pvoteTGratio', 'pvoteTDratio'
]
target_columns = ['pvoteT2_ED', 'pvoteT2_D', 'pvoteT2_CD', 'pvoteT2_C', 'pvoteT2_G']

# 📌 Définition des périodes d'entraînement et de test
years_train = [2002, 2007, 2012, 2017]
test_years = [2007, 2012, 2017, 2022]

# 📌 Fonction d'évaluation des métriques
def compute_metrics(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred, multioutput='uniform_average')
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)

    # Conversion en distributions de probabilités pour Cosine Similarity et KL Divergence
    y_true_prob = y_true / np.sum(y_true, axis=1, keepdims=True)
    y_pred_prob = y_pred / np.sum(y_pred, axis=1, keepdims=True)

    cosine_sim = np.mean([1 - cosine(y_true_prob[i], y_pred_prob[i]) for i in range(len(y_true))])
    kl_div = np.mean([entropy(y_true_prob[i], y_pred_prob[i]) for i in range(len(y_true))])

    return {"MAE": mae, "RMSE": rmse, "R²": r2, "Cosine Sim": cosine_sim, "KL Divergence": kl_div}

# 📌 Fonction d'entraînement et validation Rolling Window pour le 2ᵉ tour
def rolling_window_xgboost(df, features, target_columns, years_train, test_years):
    results = []

    for train_end, test_year in zip(years_train, test_years):
        print(f"\n🔄 **Rolling Window : Train jusqu'à {train_end}, Test sur {test_year}**")

        # Définition des jeux de données
        train = df[df["année"] <= train_end]
        test = df[df["année"] == test_year]

        X_train, y_train = train[features], train[target_columns]
        X_test, y_test = test[features], test[target_columns]

        # 📌 Définition et entraînement du modèle XGBoost
        model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=200, learning_rate=0.05, max_depth=8, reg_lambda=1)
        model.fit(X_train, y_train)

        # 📌 Prédictions et évaluation
        y_pred = model.predict(X_test)
        metrics = compute_metrics(y_test.values, y_pred)

        print(f"📉 MAE : {metrics['MAE']:.4f}, RMSE : {metrics['RMSE']:.4f}, R² : {metrics['R²']:.4f}")
        print(f"🔍 Cosine Similarity : {metrics['Cosine Sim']:.4f}, KL Divergence : {metrics['KL Divergence']:.4f}")

        results.append({
            "train_fin": train_end, "test": test_year,
            **metrics
        })

    return pd.DataFrame(results)

# 📌 Exécution du Rolling Window
df_results = rolling_window_xgboost(df, features_2nd_tour, target_columns, years_train, test_years)

# 📊 Génération du rapport
report = "\n📊 **Résultats Rolling Window - XGBoost Deuxième Tour (avec votes 1ᵉʳ tour)** 📊\n" + "-"*50 + "\n"
for _, row in df_results.iterrows():
    report += f"\n🔄 **Train jusqu'à {row['train_fin']}, Test sur {row['test']}**\n"
    report += f"📉 MAE : {row['MAE']:.4f}\n"
    report += f"📉 RMSE : {row['RMSE']:.4f}\n"
    report += f"📊 R² : {row['R²']:.4f}\n"
    report += f"🔍 Cosine Similarity : {row['Cosine Sim']:.4f}\n"
    report += f"🔍 KL Divergence : {row['KL Divergence']:.4f}\n"

# 📂 Sauvegarde du rapport
with open(output_report, "w", encoding="utf-8") as f:
    f.write(report)

print(report)
print(f"✅ Rapport sauvegardé dans : {output_report}")
