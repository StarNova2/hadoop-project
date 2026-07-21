import os
import matplotlib
# ⚠️ Obligatoire : Configurer le backend SANS interface graphique AVANT d'importer pyplot
matplotlib.use('Agg') 

import matplotlib.pyplot as plt
from pyspark.sql import SparkSession
import seaborn as sns

os.environ['HADOOP_CONF_DIR'] = '/usr/local/hadoop/etc/hadoop'

def init_spark_and_plot():
    spark = SparkSession.builder \
        .appName("ESGI_Hadoop_Project_Parsing") \
        .master("local[*]") \
        .config("spark.sql.warehouse.dir", "hdfs://localhost:9000/user/hive/warehouse") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    print(f"✅ Spark initialisé ! Version : {spark.version}")

    # Créer un dossier pour stocker les graphiques si nécessaire
    output_dir = "plots"
    os.makedirs(output_dir, exist_ok=True)

    try:
        print("📊 Chargement des données...")
        df = spark.read.csv("/home/letort/datasets/gaming_mental_health/gaming_mental_health.csv", header=True, inferSchema=True)

        # 1. Répartition par Genre
        print("📸 Génération du graphique : Genre...")
        gender_counts = df.groupBy("gender").count().toPandas()
        plt.figure()
        plt.pie(gender_counts["count"], labels=gender_counts["gender"], autopct="%1.1f%%")
        plt.title("Répartition par Genre")
        plt.savefig(f"{output_dir}/1_repartition_genre.png") # <-- Sauvegarde en PNG
        plt.close()

        # 2. Répartition par Âge
        print("📸 Génération du graphique : Âge...")
        age_df = df.select("age").toPandas()
        plt.figure()
        sns.histplot(data=age_df, x="age", kde=True, bins=15)
        plt.title("Distribution des Âges")
        plt.savefig(f"{output_dir}/2_distribution_age.png")
        plt.close()

        # 3. Qualité du sommeil vs Heures de jeu
        print("📸 Génération du graphique : Sommeil vs Jeu (Bar)...")
        df_pandas_bar = df.groupBy("sleep_quality").avg("daily_gaming_hours").toPandas()
        plt.figure()
        sns.barplot(x="sleep_quality", y="avg(daily_gaming_hours)", data=df_pandas_bar)
        plt.title("Moyenne des heures de jeu par qualité de sommeil")
        plt.savefig(f"{output_dir}/3_sommeil_vs_jeu_bar.png")
        plt.close()

        # 4. Boxplot Habitudes vs Qualité du sommeil
        print("📸 Génération du graphique : Sommeil vs Jeu (Box)...")
        df_pandas_box = df.select("sleep_quality", "daily_gaming_hours").toPandas()
        plt.figure()
        sns.boxplot(data=df_pandas_box, x="daily_gaming_hours", y="sleep_quality")
        plt.title("Impact des heures de jeu sur la qualité du sommeil")
        plt.savefig(f"{output_dir}/4_sommeil_vs_jeu_box.png")
        plt.close()

        # 5. Scatter plot (Heures de jeu vs Temps de sommeil)
        print("📸 Génération du graphique : Scatter plot...")
        df_pandas_scatter = df.select("daily_gaming_hours", "sleep_hours").toPandas()
        plt.figure()
        sns.scatterplot(data=df_pandas_scatter, x="daily_gaming_hours", y="sleep_hours")
        plt.title("Relation heures de jeu et temps de sommeil")
        plt.savefig(f"{output_dir}/5_heures_vs_temps_sommeil.png")
        plt.close()

        # 6. Distribution des dépenses mensuelles
        print("📸 Génération du graphique : Dépenses...")
        df_pandas_hist = df.select("monthly_game_spending_usd").toPandas()
        plt.figure()
        sns.histplot(data=df_pandas_hist, x="monthly_game_spending_usd", kde=True)
        plt.title("Distribution des dépenses mensuelles ($)")
        plt.savefig(f"{output_dir}/6_distribution_depenses.png")
        plt.close()

        print("📸 Génération du graphique : Risque d'addiction (Camembert)...")
        

        risk_counts = df.groupBy("gaming_addiction_risk_level").count().toPandas().set_index("gaming_addiction_risk_level")
        risk_counts.plot.pie(y="count", autopct='%1.1f%%', legend=False)
        plt.title("Répartition des utilisateurs par niveau de risque d'addiction")
        plt.savefig(f"{output_dir}/X_repartition_risque_addiction.png")
        plt.close()


        print(f"🎉 Terminé ! Tous les graphiques ont été sauvegardés dans le dossier '{output_dir}/'")

    finally:
        print("🔌 Fermeture de la session Spark...")
        spark.stop()

if __name__ == "__main__":
    init_spark_and_plot()