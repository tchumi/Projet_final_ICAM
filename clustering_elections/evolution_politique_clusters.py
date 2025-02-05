import pandas as pd
import os
from scipy.spatial.distance import euclidean
from itertools import product

# 📍 Chemin des fichiers
DATA_DIR = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data"
CLUSTER_FILE = os.path.join(DATA_DIR, "clusters_elections.csv")
ELECTIONS_FILE = os.path.join(DATA_DIR, "elections_fusionnees_cleaned_with_names.csv")
REPORT_FILE = os.path.join(DATA_DIR, "rapport_evolution_politique_clusters_corrige.txt")

# 📌 Chargement des fichiers
df_clusters = pd.read_csv(CLUSTER_FILE, sep=",", dtype={"codecommune": str})
df_votes = pd.read_csv(ELECTIONS_FILE, sep=",", dtype={"codecommune": str})

# 📌 Sélection des colonnes électorales à analyser
variables_votes = ["pvoteG", "pvoteCG", "pvoteC", "pvoteCD", "pvoteD"]

# 📌 Vérification des colonnes disponibles
votes_disponibles = [col for col in variables_votes if col in df_votes.columns]

# 📌 Fusionner les données des clusters avec les données de vote
df_merged = df_clusters.merge(df_votes[["codecommune", "année"] + votes_disponibles], on=["codecommune", "année"], how="left")

# 📌 Fonction pour analyser l’évolution des clusters en suivant leur profil électoral
def suivre_clusters_par_profil(df):
    rapport = []
    
    for annee1, annee2 in zip(sorted(df["année"].unique())[:-1], sorted(df["année"].unique())[1:]):
        df_prev = df[df["année"] == annee1].groupby("cluster_1er_tour")[votes_disponibles].mean()
        df_next = df[df["année"] == annee2].groupby("cluster_1er_tour")[votes_disponibles].mean()

        # Associer les clusters d'une élection à l'autre en fonction de leur proximité électorale
        cluster_mapping = {}
        distances = []
        
        for cluster1, cluster2 in product(df_prev.index, df_next.index):
            dist = euclidean(df_prev.loc[cluster1], df_next.loc[cluster2])
            distances.append((cluster1, cluster2, dist))
        
        # Trier par distance pour faire correspondre les clusters les plus proches
        distances.sort(key=lambda x: x[2])
        
        matched_clusters = set()
        for cluster1, cluster2, dist in distances:
            if cluster1 not in cluster_mapping and cluster2 not in matched_clusters:
                cluster_mapping[cluster1] = cluster2
                matched_clusters.add(cluster2)

        rapport.append(f"\n📌 Correspondance des clusters entre {annee1} et {annee2} :")
        for cluster1, cluster2 in cluster_mapping.items():
            changements = df_next.loc[cluster2] - df_prev.loc[cluster1]
            rapport.append(f"\n➡️ Cluster {cluster1} ({annee1}) ➝ Cluster {cluster2} ({annee2}) :")
            rapport.append(changements.to_string())

    return "\n".join(rapport)

# 📌 Génération du rapport
rapport_final = "📊 Suivi de l'évolution des clusters par profil électoral\n"
rapport_final += "======================================\n\n"
rapport_final += suivre_clusters_par_profil(df_merged)

# 📌 Sauvegarde du rapport
with open(REPORT_FILE, "w", encoding="utf-8") as file:
    file.write(rapport_final)

print(f"✅ Rapport généré : {REPORT_FILE}")
