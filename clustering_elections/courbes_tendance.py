import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 📍 Chemin du fichier des clusters
DATA_DIR = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data"
CLUSTER_FILE = os.path.join(DATA_DIR, "clusters_elections.csv")
ELECTIONS_FILE = os.path.join(DATA_DIR, "elections_fusionnees_cleaned_with_names.csv")

# 📌 Chargement des fichiers
df_clusters = pd.read_csv(CLUSTER_FILE, sep=",", dtype={"codecommune": str})
df_votes = pd.read_csv(ELECTIONS_FILE, sep=",", dtype={"codecommune": str})

# 📌 Sélection des colonnes électorales
variables_votes = {
    "pvoteG": "Vote Gauche",
    "pvoteC": "Vote Centre",
    "pvoteD": "Vote Droite"
}
ponderation = "exprimes"  # Poids basé sur les votes exprimés

# 📌 Fusionner les clusters avec les données de vote
df_merged = df_clusters.merge(df_votes[["codecommune", "année", ponderation] + list(variables_votes.keys())], 
                              on=["codecommune", "année"], how="left")

# 📌 Calcul des moyennes pondérées des votes par cluster et année
def weighted_mean(df_grouped, var):
    return (df_grouped[var] * df_grouped[ponderation]).sum() / df_grouped[ponderation].sum()

df_trends = df_merged.groupby(["année", "cluster_1er_tour"], as_index=False, group_keys=False).apply(
    lambda x: pd.Series({var: weighted_mean(x, var) for var in variables_votes.keys()})
)

# 📌 Création des sous-graphiques pour chaque tendance
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharex=True, sharey=True)

for ax, (var, title) in zip(axes, variables_votes.items()):
    sns.lineplot(data=df_trends, x="année", y=var, hue="cluster_1er_tour", marker="o", ax=ax, palette="tab10")
    ax.set_title(title)
    ax.set_xlabel("Année")
    ax.set_ylabel("Pourcentage moyen du vote")
    ax.legend(title="Cluster", loc="upper right")
    ax.grid(True)

# 📌 Ajustement des espaces entre les graphiques
plt.suptitle("Évolution des votes par cluster (moyennes pondérées)", fontsize=16)
plt.tight_layout()
plt.show()
