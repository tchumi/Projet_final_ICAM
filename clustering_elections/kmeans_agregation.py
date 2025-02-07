"""
Ce script effectue un clustering des résultats électoraux en utilisant l'algorithme K-Means.
Fonctionnalités principales :
- Chargement des données électorales à partir d'un fichier CSV.
- Sélection et standardisation des variables électorales pour le 1er et le 2nd tour.
- Détermination du nombre optimal de clusters à l'aide de la méthode du coude.
- Application de l'algorithme K-Means pour chaque année d'élection.
- Stockage des résultats des clusters et fusion avec les données originales.
- Sauvegarde des résultats finaux dans un fichier CSV.
Bibliothèques utilisées :
- pandas : pour la manipulation des données.
- os : pour la gestion des chemins de fichiers.
- matplotlib.pyplot et seaborn : pour la visualisation des données.
- sklearn.cluster et sklearn.preprocessing : pour le clustering et la standardisation des données.
- yellowbrick.cluster : pour la visualisation du nombre optimal de clusters.
Variables :
- DATA_DIR : chemin du répertoire contenant les données.
- INPUT_FILE : chemin du fichier CSV d'entrée contenant les données électorales.
- OUTPUT_FILE : chemin du fichier CSV de sortie pour sauvegarder les résultats des clusters.
- variables_1er_tour : liste des variables électorales pour le 1er tour.
- variables_2nd_tour : liste des variables électorales pour le 2nd tour.
- scaler : instance de StandardScaler pour la standardisation des données.
- clusters_results : liste pour stocker les résultats des clusters pour chaque année.
Étapes principales :
1. Chargement des données électorales.
2. Boucle sur chaque année d'élection pour effectuer le clustering.
3. Standardisation des variables électorales.
4. Détermination du nombre optimal de clusters pour le 1er et le 2nd tour.
5. Application de l'algorithme K-Means et stockage des résultats.
6. Fusion des résultats des clusters avec les données originales.
7. Sauvegarde des résultats finaux dans un fichier CSV.

"""


import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from yellowbrick.cluster import KElbowVisualizer

# 📍 Chemins des fichiers
DATA_DIR = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data"
INPUT_FILE = os.path.join(DATA_DIR, "elections_fusionnees_cleaned_with_names.csv")
OUTPUT_FILE = os.path.join(DATA_DIR, "elections_fusionnees_cleaned_with_names_clusters.csv")

# 📌 Chargement des données
df = pd.read_csv(INPUT_FILE, sep=",", dtype={"codecommune": str})

# 📌 Sélection des variables électorales pour clustering
variables_1er_tour = ["pvoteG", "pvoteCG", "pvoteC", "pvoteCD", "pvoteD", "pvoteTG", "pvoteTD"]
variables_2nd_tour = ["pvoteT2_ED", "pvoteT2_D", "pvoteT2_CD", "pvoteT2_C", "pvoteT2_G"]

# 📌 Standardisation des données
scaler = StandardScaler()

# 📌 Dictionnaire pour stocker les résultats des clusters
clusters_results = []

# 📌 Boucle sur chaque élection
for year in df["année"].unique():
    print(f"🔄 Clustering pour l'élection de {year}...")
    
    # 📌 Sélection des données de l’année
    df_year = df[df["année"] == year].copy()
    
    # 📌 Standardisation des variables électorales
    X_1er_tour = scaler.fit_transform(df_year[variables_1er_tour])
    X_2nd_tour = scaler.fit_transform(df_year[variables_2nd_tour])

    # 📌 Trouver le nombre optimal de clusters avec la méthode du coude
    elbow_1er = KElbowVisualizer(KMeans(n_init=10), k=(2, 10))
    elbow_1er.fit(X_1er_tour)
    k_1er = elbow_1er.elbow_value_
    
    elbow_2nd = KElbowVisualizer(KMeans(n_init=10), k=(2, 10))
    elbow_2nd.fit(X_2nd_tour)
    k_2nd = elbow_2nd.elbow_value_

    # 📌 Appliquer K-Means avec le nombre optimal de clusters
    kmeans_1er = KMeans(n_clusters=k_1er, n_init=10, random_state=42).fit(X_1er_tour)
    kmeans_2nd = KMeans(n_clusters=k_2nd, n_init=10, random_state=42).fit(X_2nd_tour)

    # 📌 Stocker les clusters trouvés
    df_year["cluster_1er_tour"] = kmeans_1er.labels_
    df_year["cluster_2nd_tour"] = kmeans_2nd.labels_

    clusters_results.append(df_year[["codecommune", "année", "cluster_1er_tour", "cluster_2nd_tour"]])

# 📌 Fusion des résultats des clusters
df_clusters = pd.concat(clusters_results, ignore_index=True)

# 📌 Fusion avec les données originales
df_final = df.merge(df_clusters, on=["codecommune", "année"], how="left")

# 📌 Sauvegarde du fichier final
df_final.to_csv(OUTPUT_FILE, index=False)

print(f"✅ Clustering terminé ! Fichier final sauvegardé sous {OUTPUT_FILE}")
