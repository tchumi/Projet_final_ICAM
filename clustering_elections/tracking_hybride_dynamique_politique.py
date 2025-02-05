import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 📍 Chargement des données
DATA_FILE = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/elections_fusionnees_tracking_1er_tour.csv"
df = pd.read_csv(DATA_FILE, sep=",", dtype={"codecommune": str})

# 📌 Sélection des variables pour l'analyse
variables_votes = ["pvoteG", "pvoteCG", "pvoteC", "pvoteCD", "pvoteD"]

# 📌 Définition d'une palette de couleurs du rouge (Gauche) au bleu (Droite)
custom_palette = {"pvoteG": "#d73027", "pvoteCG": "#fc8d59", "pvoteC": "#fee090", "pvoteCD": "#91bfdb", "pvoteD": "#4575b4"}

# 📌 Calcul des moyennes pondérées des votes par cluster corrigé et par année
def weighted_mean(group, column):
    return (group[column] * group["exprimes"]).sum() / group["exprimes"].sum()

df_trends = df.groupby(["année", "cluster_corrige_1er_tour"], group_keys=False).apply(
    lambda x: pd.Series({var: weighted_mean(x, var) for var in variables_votes})
).reset_index()

# 📌 Identification des clusters de bascule
clusters_bascule = []
for cluster in df_trends["cluster_corrige_1er_tour"].unique():
    df_cluster = df_trends[df_trends["cluster_corrige_1er_tour"] == cluster].sort_values("année")
    df_cluster["dominant_tendance"] = df_cluster[variables_votes].idxmax(axis=1)
    changements = df_cluster["dominant_tendance"].nunique()
    if changements > 1:
        clusters_bascule.append(cluster)

# 📌 Visualisation des clusters de bascule
plt.figure(figsize=(12, 6))
for cluster in clusters_bascule:
    df_cluster = df_trends[df_trends["cluster_corrige_1er_tour"] == cluster]
    for var in variables_votes:
        sns.lineplot(data=df_cluster, x="année", y=var, label=f"Cluster {cluster} - {var}", color=custom_palette[var])
plt.title("Évolution des clusters de bascule")
plt.xlabel("Année")
plt.ylabel("Pourcentage des votes")
plt.legend()
plt.savefig("clusters_bascule.png")
plt.show()

# 📌 Sauvegarde des clusters de bascule
df_trends[df_trends["cluster_corrige_1er_tour"].isin(clusters_bascule)].to_csv("clusters_bascule.csv", index=False)

print("✅ Identification et analyse des clusters de bascule terminée.")
