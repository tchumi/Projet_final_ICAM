"""
Ce script analyse les poids relatifs des clusters de communes au fil des élections en France.
Fonctionnalités :
1. Chargement des données de clusters et des résultats des élections.
2. Fusion des données pour récupérer les votes exprimés par commune et par année.
3. Calcul des poids relatifs des clusters en termes de nombre de communes et de votes exprimés.
4. Sauvegarde des résultats dans un fichier CSV.
5. Visualisation des tendances des poids relatifs des clusters au fil des années.
Bibliothèques utilisées :
- pandas : pour la manipulation des données.
- os : pour la gestion des chemins de fichiers.
- matplotlib.pyplot : pour la visualisation des données.
- seaborn : pour la création de graphiques.
Variables :
- DATA_DIR : chemin du répertoire contenant les fichiers de données.
- CLUSTER_FILE : chemin du fichier CSV contenant les données de clusters.
- ELECTIONS_FILE : chemin du fichier CSV contenant les résultats des élections.
- df_clusters : DataFrame contenant les données de clusters.
- df_votes : DataFrame contenant les résultats des élections.
- df_merged : DataFrame fusionnée contenant les données de clusters et les votes exprimés.
- df_weights : DataFrame contenant les poids relatifs des clusters.
Sortie :
- Un fichier CSV contenant les poids relatifs des clusters.
- Des graphiques montrant l'évolution des poids relatifs des clusters en termes de pourcentage de communes et de votes exprimés.

"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# 📍 Chemin des fichiers
DATA_DIR = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data"
CLUSTER_FILE = os.path.join(DATA_DIR, "clusters_elections.csv")
ELECTIONS_FILE = os.path.join(DATA_DIR, "elections_fusionnees_cleaned_with_names.csv")

# 📌 Chargement des fichiers
df_clusters = pd.read_csv(CLUSTER_FILE, sep=",", dtype={"codecommune": str})
df_votes = pd.read_csv(ELECTIONS_FILE, sep=",", dtype={"codecommune": str})

# 📌 Fusion avec les votes pour récupérer les votes exprimés
df_merged = df_clusters.merge(df_votes[["codecommune", "année", "exprimes"]], 
                              on=["codecommune", "année"], how="left")

# 📌 Calcul des poids relatifs des clusters
df_weights = df_merged.groupby(["année", "cluster_1er_tour"]).agg(
    nb_communes=("codecommune", "count"),
    total_votes=("exprimes", "sum")
).reset_index()

# ✅ **Correction : réindexation après l'opération groupby().apply()**
df_weights["pct_communes"] = df_weights.groupby("année")["nb_communes"].apply(lambda x: x / x.sum() * 100).reset_index(drop=True)
df_weights["pct_votes"] = df_weights.groupby("année")["total_votes"].apply(lambda x: x / x.sum() * 100).reset_index(drop=True)

# 📌 Affichage du tableau
# Sauvegarde du tableau dans un fichier CSV
output_file = os.path.join(DATA_DIR, "poids_relatif_clusters.csv")
df_weights.to_csv(output_file, index=False)
print(f"✅ Résultats enregistrés dans : {output_file}")

# Affichage des 10 premières lignes en console pour vérification
print(df_weights.head(10))

# 📌 Visualisation des tendances
fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharex=True)

# 📊 Évolution du % de communes par cluster
sns.lineplot(data=df_weights, x="année", y="pct_communes", hue="cluster_1er_tour", marker="o", ax=axes[0], palette="tab10")
axes[0].set_title("Évolution du % de communes par cluster")
axes[0].set_ylabel("Pourcentage des communes")
axes[0].set_xlabel("Année")
axes[0].legend(title="Cluster")

# 📊 Évolution du % de votes exprimés par cluster
sns.lineplot(data=df_weights, x="année", y="pct_votes", hue="cluster_1er_tour", marker="o", ax=axes[1], palette="tab10")
axes[1].set_title("Évolution du % des votes exprimés par cluster")
axes[1].set_ylabel("Pourcentage des votes exprimés")
axes[1].set_xlabel("Année")
axes[1].legend(title="Cluster")

# 📌 Ajustement et affichage
plt.suptitle("Poids relatif des clusters au fil des élections", fontsize=14)
plt.tight_layout()
plt.show()
