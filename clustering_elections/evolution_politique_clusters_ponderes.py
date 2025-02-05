"""
Ce script analyse l'évolution des clusters politiques en utilisant des moyennes pondérées des résultats électoraux.
Modules importés:
- pandas: pour la manipulation des données
- os: pour la gestion des chemins de fichiers
- scipy.spatial.distance.euclidean: pour calculer la distance euclidienne entre les clusters
- itertools.product: pour générer des paires de clusters à comparer
Variables globales:
- DATA_DIR: chemin du répertoire contenant les fichiers de données
- CLUSTER_FILE: chemin du fichier contenant les données des clusters
- ELECTIONS_FILE: chemin du fichier contenant les données électorales
- REPORT_FILE: chemin du fichier où le rapport sera sauvegardé
- variables_votes: liste des colonnes électorales à analyser
- ponderation: colonne utilisée pour pondérer les moyennes
Fonctions:
- suivre_clusters_par_profil_pondere(df): analyse l'évolution des clusters en utilisant des moyennes pondérées des résultats électoraux et génère un rapport.
Étapes principales:
1. Chargement des fichiers de données des clusters et des votes.
2. Sélection des colonnes électorales disponibles dans les données.
3. Fusion des données des clusters avec les données de vote.
4. Analyse de l'évolution des clusters par année en utilisant des moyennes pondérées.
5. Génération et sauvegarde du rapport final.
Le rapport final est sauvegardé dans un fichier texte spécifié par REPORT_FILE.

"""
import pandas as pd
import os
from scipy.spatial.distance import euclidean
from itertools import product

# 📍 Chemin des fichiers
DATA_DIR = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data"
CLUSTER_FILE = os.path.join(DATA_DIR, "clusters_elections.csv")
ELECTIONS_FILE = os.path.join(DATA_DIR, "elections_fusionnees_cleaned_with_names.csv")
REPORT_FILE = os.path.join(DATA_DIR, "rapport_evolution_politique_clusters_pondere_corrige_final.txt")

# 📌 Chargement des fichiers
df_clusters = pd.read_csv(CLUSTER_FILE, sep=",", dtype={"codecommune": str})
df_votes = pd.read_csv(ELECTIONS_FILE, sep=",", dtype={"codecommune": str})

# 📌 Sélection des colonnes électorales à analyser
variables_votes = ["pvoteG", "pvoteCG", "pvoteC", "pvoteCD", "pvoteD"]
ponderation = "exprimes"  # Nombre de votes exprimés pour pondérer les moyennes

# 📌 Vérification des colonnes disponibles
votes_disponibles = [col for col in variables_votes if col in df_votes.columns]

# 📌 Fusionner les données des clusters avec les données de vote
df_merged = df_clusters.merge(df_votes[["codecommune", "année", ponderation] + votes_disponibles], on=["codecommune", "année"], how="left")

# 📌 Fonction pour analyser l’évolution des clusters en utilisant des moyennes pondérées
def suivre_clusters_par_profil_pondere(df):
    rapport = []
    
    for annee1, annee2 in zip(sorted(df["année"].unique())[:-1], sorted(df["année"].unique())[1:]):
        df_prev = df[df["année"] == annee1]
        df_next = df[df["année"] == annee2]

        # Calcul des moyennes pondérées des votes par cluster
        def weighted_mean(df_grouped, var):
            return (df_grouped[var] * df_grouped[ponderation]).sum() / df_grouped[ponderation].sum()

        # Exclure la colonne de regroupement et appliquer la fonction sur les autres colonnes uniquement
        stats_prev = df_prev.groupby("cluster_1er_tour")[votes_disponibles + [ponderation]].apply(
            lambda x: pd.Series({var: weighted_mean(x, var) for var in votes_disponibles})
        ).reset_index()

        stats_next = df_next.groupby("cluster_1er_tour")[votes_disponibles + [ponderation]].apply(
            lambda x: pd.Series({var: weighted_mean(x, var) for var in votes_disponibles})
        ).reset_index()

        # Associer les clusters d'une élection à l'autre en fonction de leur proximité électorale
        cluster_mapping = {}
        distances = []
        
        for cluster1, cluster2 in product(stats_prev["cluster_1er_tour"], stats_next["cluster_1er_tour"]):
            dist = euclidean(stats_prev.loc[stats_prev["cluster_1er_tour"] == cluster1, votes_disponibles].values[0], 
                             stats_next.loc[stats_next["cluster_1er_tour"] == cluster2, votes_disponibles].values[0])
            distances.append((cluster1, cluster2, dist))
        
        # Trier par distance pour faire correspondre les clusters les plus proches
        distances.sort(key=lambda x: x[2])
        
        matched_clusters = set()
        for cluster1, cluster2, dist in distances:
            if cluster1 not in cluster_mapping and cluster2 not in matched_clusters:
                cluster_mapping[cluster1] = cluster2
                matched_clusters.add(cluster2)

        rapport.append(f"\n📌 Correspondance des clusters entre {annee1} et {annee2} (moyennes pondérées) :")
        for cluster1, cluster2 in cluster_mapping.items():
            changements = stats_next.loc[stats_next["cluster_1er_tour"] == cluster2, votes_disponibles].values[0] - stats_prev.loc[stats_prev["cluster_1er_tour"] == cluster1, votes_disponibles].values[0]
            rapport.append(f"\n➡️ Cluster {cluster1} ({annee1}) ➝ Cluster {cluster2} ({annee2}) :")
            rapport.append(pd.Series(changements, index=votes_disponibles).to_string())

    return "\n".join(rapport)

# 📌 Génération du rapport
rapport_final = "📊 Suivi de l'évolution des clusters avec moyennes pondérées (Correction Définitive Pandas)\n"
rapport_final += "======================================\n\n"
rapport_final += suivre_clusters_par_profil_pondere(df_merged)

# 📌 Sauvegarde du rapport
with open(REPORT_FILE, "w", encoding="utf-8") as file:
    file.write(rapport_final)

print(f"✅ Rapport généré avec moyennes pondérées et correction complète des warnings : {REPORT_FILE}")
