""""
Ce script analyse les tendances de vote par cluster pour le premier tour des élections en utilisant des moyennes pondérées. 
Il charge les données électorales, calcule les moyennes pondérées des votes pour chaque cluster et année, 
et génère des graphiques pour visualiser l'évolution des votes par cluster.
Fonctionnalités :
- Chargement des données électorales à partir d'un fichier CSV.
- Sélection des colonnes électorales pertinentes.
- Calcul des moyennes pondérées des votes par cluster et année.
- Création de sous-graphiques pour chaque tendance de vote (Gauche, Centre, Droite).
- Affichage des graphiques avec des titres, légendes et grilles.
Bibliothèques utilisées :
- pandas : pour la manipulation des données.
- matplotlib.pyplot : pour la création des graphiques.
- seaborn : pour l'amélioration de l'esthétique des graphiques.
- os : pour la gestion des chemins de fichiers.
Variables :
- DATA_DIR : Chemin du répertoire contenant les données électorales.
- ELECTIONS_FILE : Chemin complet du fichier CSV des élections.
- df_votes : DataFrame contenant les données électorales chargées.
- variables_votes : Dictionnaire des colonnes électorales sélectionnées et leurs titres.
- ponderation : Colonne utilisée pour le calcul des moyennes pondérées.
- df_trends : DataFrame contenant les moyennes pondérées des votes par cluster et année.

"""


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 📍 Chemin du fichier des élections
DATA_DIR = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data"
ELECTIONS_FILE = os.path.join(DATA_DIR, "elections_fusionnees_tracking_1er_tour.csv")

# 📌 Chargement du fichier
df_votes = pd.read_csv(ELECTIONS_FILE, sep=",", dtype={"codecommune": str})

# 📌 Sélection des colonnes électorales
variables_votes = {
    "pvoteG": "Vote Gauche",
    "pvoteC": "Vote Centre",
    "pvoteD": "Vote Droite"
}
ponderation = "exprimes"  # Poids basé sur les votes exprimés

# 📌 Calcul des moyennes pondérées des votes par cluster et année
def weighted_mean(df_grouped, var):
    return (df_grouped[var] * df_grouped[ponderation]).sum() / df_grouped[ponderation].sum()

df_trends = df_votes.groupby(["année", "cluster_corrige_1er_tour"], as_index=False, group_keys=False).apply(
    lambda x: pd.Series({var: weighted_mean(x, var) for var in variables_votes.keys()})
)

# 📌 Création des sous-graphiques pour chaque tendance
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharex=True, sharey=True)

for ax, (var, title) in zip(axes, variables_votes.items()):
    sns.lineplot(data=df_trends, x="année", y=var, hue="cluster_corrige_1er_tour", marker="o", ax=ax, palette="tab10")
    ax.set_title(title)
    ax.set_xlabel("Année")
    ax.set_ylabel("Pourcentage moyen du vote")
    ax.legend(title="Cluster", loc="upper right")
    ax.grid(True)

# 📌 Ajustement des espaces entre les graphiques
plt.suptitle("Évolution des votes par cluster (moyennes pondérées)", fontsize=16)
plt.tight_layout()
plt.show()
