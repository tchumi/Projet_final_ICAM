"""
Ce script Streamlit permet de simuler les résultats du 1er tour des élections en utilisant un modèle XGBoost.
Fonctionnalités :
- Chargement des données électorales et socio-économiques.
- Entraînement d'un modèle XGBoost sur les données jusqu'à une année sélectionnée.
- Sauvegarde du modèle entraîné.
- Chargement d'un modèle pré-entraîné pour effectuer des simulations.
- Interface utilisateur pour ajuster les paramètres socio-économiques et simuler les résultats électoraux.
- Affichage des résultats réels et simulés sous forme de camemberts pour chaque cluster.
Bibliothèques utilisées :
- streamlit : pour créer l'interface utilisateur interactive.
- pandas : pour la manipulation des données.
- xgboost : pour l'entraînement et l'utilisation du modèle XGBoost.
- numpy : pour les opérations numériques.
- matplotlib : pour la visualisation des résultats.
- os : pour vérifier l'existence du fichier de modèle sauvegardé.
Variables principales :
- data_path : chemin vers le fichier CSV contenant les données originales.
- model_path : chemin vers le fichier de sauvegarde du modèle XGBoost.
- features_1er_tour : liste des caractéristiques utilisées pour l'entraînement du modèle.
- vote_columns : liste des colonnes représentant les votes pour chaque orientation politique.
- vote_labels : liste des étiquettes correspondant aux orientations politiques.
Interface utilisateur :
- Sélection de l'année d'entraînement.
- Bouton pour entraîner le modèle.
- Vérification de l'existence d'un modèle pré-entraîné.
- Sélection de l'année pour la simulation.
- Sliders pour ajuster les paramètres socio-économiques.
- Bouton pour lancer la simulation.
- Affichage des résultats sous forme de camemberts comparant les votes réels et simulés pour chaque cluster.

"""

import streamlit as st
import pandas as pd
import xgboost as xgb
import numpy as np
import matplotlib.pyplot as plt
import os

# 📂 Chargement des données originales
data_path = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/elections_socio_fusionnes.csv"
df = pd.read_csv(data_path, dtype={"codecommune": str, "année": int})

# 📂 Définition du chemin de sauvegarde du modèle
model_path = "C:/Users/Admin.local/Documents/Projet_final_data/XGBoost_model_1er_tour.json"


features_1er_tour = [
    'exprimes', 'revratio', 'pchom', 'pouvr', 'pcadr', 'pibratio'
]

vote_columns = ["pvoteG", "pvoteCG", "pvoteC", "pvoteCD", "pvoteD"]
vote_labels = ["Gauche", "Centre-Gauche", "Centre", "Centre-Droite", "Droite"]

# 🎛️ Interface Streamlit
st.title("Simulation des Résultats du 1ᵉʳ Tour avec XGBoost")

# 📌 Sélection de l’année d'entraînement
annee_train = st.selectbox("Jusqu'à quelle année entraîner le modèle ?", [2002, 2007, 2012])

# 📌 Bouton pour entraîner le modèle
if st.button("🚀 Entraîner le Modèle XGBoost"):
    st.write(f"📊 Entraînement du modèle sur les élections jusqu’en {annee_train}...")

    df_train = df[df["année"] <= annee_train]
    X_train, y_train = df_train[features_1er_tour], df_train[vote_columns]

    model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=100, learning_rate=0.1, max_depth=6)
    model.fit(X_train, y_train)

    model.save_model(model_path)
    st.success(f"✅ Modèle entraîné et sauvegardé dans : {model_path}")

# 📌 Vérifier si un modèle pré-entraîné existe
if os.path.exists(model_path):
    model = xgb.XGBRegressor()
    model.load_model(model_path)
    st.success("✅ Modèle chargé avec succès ! Vous pouvez faire une simulation.")

    # 📌 Sélection de l’année pour la simulation
    annee_simulee = st.selectbox("Choisissez une année pour la simulation :", [2017, 2022])

    # 📌 Filtrage des données pour la simulation
    df_simulation = df[df["année"] == annee_simulee].copy()

    # 📌 Ajout des sliders pour modifier les variables
    st.subheader("🎛️ Ajustez les paramètres pour simuler un scénario")

    exprimes_modif = st.slider("📊 Variation de la participation (%)", -30, 30, 0)
    revratio_modif = st.slider("💰 Variation du revenu moyen (%)", -100, 300, 0)
    pchom_modif = st.slider("📉 Variation du taux de chômage (%)", -100, 300, 0)
    pouv_modif = st.slider("📈 Variation du taux d’ouvriers (%)", -100, 300, 0)
    pcadr_modif = st.slider("👔 Variation du taux de cadres (%)", -100, 300, 0)
    pibratio_modif = st.slider("💵 Variation du PIB ratio (%)", -100, 300, 0)

    # 📌 Bouton pour lancer la simulation
    if st.button("🔄 Lancer la Simulation"):
        # 📌 Mise à jour du dataframe simulé avec les valeurs modifiées
        df_simulation["exprimes"] *= (1 + exprimes_modif / 100)
        df_simulation["revratio"] *= (1 + revratio_modif / 100)
        df_simulation["pchom"] *= (1 + pchom_modif / 100)
        df_simulation["pouvr"] *= (1 + pouv_modif / 100)
        df_simulation["pcadr"] *= (1 + pcadr_modif / 100)
        df_simulation["pibratio"] *= (1 + pibratio_modif / 100)

        # 📌 Prédiction avec XGBoost sur la simulation
        X_simulation = df_simulation[features_1er_tour]
        y_pred_simulation = model.predict(X_simulation)

        # 📌 Normalisation pour que la somme des votes fasse bien 100 %
        y_pred_simulation = (y_pred_simulation.T / y_pred_simulation.sum(axis=1)).T * 100

        # 📊 Comparaison des résultats par cluster
        clusters = df_simulation["cluster_corrige_1er_tour"].unique()
        fig, ax = plt.subplots(len(clusters), 2, figsize=(10, 5 * len(clusters)))

        for i, cluster in enumerate(clusters):
            df_cluster = df_simulation[df_simulation["cluster_corrige_1er_tour"] == cluster]
            y_pred_cluster = y_pred_simulation[df_simulation["cluster_corrige_1er_tour"] == cluster]
            
            # 📊 Agrégation des votes pondérée par exprimes
            votes_reels = (df_cluster[vote_columns].multiply(df_cluster["exprimes"], axis=0)).sum()
            votes_simules = (y_pred_cluster * df_cluster["exprimes"].values[:, np.newaxis]).sum(axis=0)
            
            # 📌 Camembert des résultats réels
            ax[i, 0].pie(votes_reels, labels=vote_labels, autopct='%1.1f%%', startangle=140)
            ax[i, 0].set_title(f"Cluster {cluster} - Réel")

            # 📌 Camembert des résultats simulés
            ax[i, 1].pie(votes_simules, labels=vote_labels, autopct='%1.1f%%', startangle=140)
            ax[i, 1].set_title(f"Cluster {cluster} - Simulé")

        # Affichage des graphiques
        st.pyplot(fig)
