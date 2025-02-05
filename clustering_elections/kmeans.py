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
