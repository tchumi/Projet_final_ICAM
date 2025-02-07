import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
from scipy.spatial.distance import cosine
from scipy.stats import entropy
from sklearn.preprocessing import StandardScaler  # 📌 Ajout de la normalisation

# 📂 Chargement des données
data_path = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/elections_socio_fusionnes.csv"
output_report = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/prediction_rolling_window_XGBOOST_premier_tour.txt"

df = pd.read_csv(data_path, dtype={"codecommune": str, "année": int})

# 📌 Sélection des features (sans clusters ni votes)
features_1er_tour = ['exprimes', 'revratio', 'pchom', 'pouvr', 'pcadr', 'pibratio']

# 📌 Sélection des cibles (votes à prédire)
target_columns = ['pvoteG', 'pvoteCG', 'pvoteC', 'pvoteCD', 'pvoteD']

# 📌 Définition des périodes d'entraînement et de test
years_train = [2002, 2007, 2012, 2017]
test_years = [2007, 2012, 2017, 2022]

# 📌 Vérification et alignement des features + targets pour éviter l'erreur KeyError
def align_features_and_targets(df, features, targets=None):
    """S'assure que les features (et targets si fournies) sont bien alignées et présentes"""
    missing_features = [col for col in features if col not in df.columns]
    if missing_features:
        print(f"⚠ Attention : Les features suivantes sont absentes et seront ignorées : {missing_features}")
        features = [col for col in features if col in df.columns]

    if targets:
        missing_targets = [col for col in targets if col not in df.columns]
        if missing_targets:
            print(f"⚠ Attention : Les cibles suivantes sont absentes et seront ignorées : {missing_targets}")
            targets = [col for col in targets if col in df.columns]
        return df[features], df[targets]
    
    return df[features]

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

# 📌 Fonction d'entraînement et validation Rolling Window pour le 1ᵉʳ tour
def rolling_window_xgboost(df, features, target_columns, years_train, test_years):
    results = []
    scaler = StandardScaler()

    for train_end, test_year in zip(years_train, test_years):
        print(f"\n🔄 **Rolling Window : Train jusqu'à {train_end}, Test sur {test_year}**")

        # 📌 Définition des jeux de données
        train = df[df["année"] <= train_end]
        test = df[df["année"] == test_year]

        X_train, y_train = align_features_and_targets(train, features, target_columns)
        X_test, y_test = align_features_and_targets(test, features, target_columns)

        # 📌 Normalisation Standard (Z-Score)
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # 📌 Définition et entraînement du modèle XGBoost avec hyperparamètres optimisés
        model = xgb.XGBRegressor(
            objective="reg:squarederror",
            n_estimators=500,
            learning_rate=0.03,
            max_depth=10,
            colsample_bytree=0.8,
            subsample=0.8,
            reg_lambda=10,
            reg_alpha=1,
            min_child_weight=5,
            gamma=1
        )
        model.fit(X_train_scaled, y_train)

        # 📌 Prédictions et évaluation
        y_pred = model.predict(X_test_scaled)

        # 📌 Correction des valeurs négatives avant normalisation
        y_pred = np.maximum(y_pred, 0)
        y_pred = (y_pred.T / y_pred.sum(axis=1)).T * 100

        metrics = compute_metrics(y_test.values, y_pred)

        print(f"📉 MAE : {metrics['MAE']:.4f}, RMSE : {metrics['RMSE']:.4f}, R² : {metrics['R²']:.4f}")
        print(f"🔍 Cosine Similarity : {metrics['Cosine Sim']:.4f}, KL Divergence : {metrics['KL Divergence']:.4f}")

        results.append({
            "train_fin": train_end, "test": test_year,
            **metrics
        })

    return pd.DataFrame(results)

# 📌 Exécution du Rolling Window
df_results = rolling_window_xgboost(df, features_1er_tour, target_columns, years_train, test_years)

# 📊 Génération du rapport
report = "\n📊 **Résultats Rolling Window - XGBoost Premier Tour (Normalisation + Paramètres Optimisés)** 📊\n" + "-"*50 + "\n"
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
