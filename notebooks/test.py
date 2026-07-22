import os
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

    try:
        df_spark = spark.read.csv("/home/letort/datasets/gaming_mental_health/part-00000-c5eca9e6-5393-4d27-bb31-0d72a0573949-c000.csv", header=True, inferSchema=True)
        df = df_spark.toPandas()

        def show_fig(title):
            plt.title(title)
            plt.tight_layout()
            plt.show()

        # Graphiques
        plt.figure()
        df['gender'].value_counts().plot.pie(autopct="%1.1f%%")
        plt.ylabel("") # Masque le libellé de l'axe Y pour clarifier le camembert
        show_fig("Répartition par Genre")

        plt.figure()
        sns.histplot(data=df, x="age", kde=True, bins=15)
        show_fig("Distribution des Âges")

        plt.figure()
        sns.barplot(data=df, x="sleep_quality", y="daily_gaming_hours", errorbar=None)
        show_fig("Moyenne des heures de jeu par qualité de sommeil")

        plt.figure()
        sns.boxplot(data=df, x="daily_gaming_hours", y="sleep_quality")
        show_fig("Impact des heures de jeu sur la qualité du sommeil")

        plt.figure()
        sns.scatterplot(data=df, x="daily_gaming_hours", y="sleep_hours")
        show_fig("Relation heures de jeu et temps de sommeil")

        plt.figure()
        sns.histplot(data=df, x="monthly_game_spending_usd", kde=True)
        show_fig("Distribution des dépenses mensuelles ($)")

        plt.figure()
        df['gaming_addiction_risk_level'].value_counts().plot.pie(autopct="%1.1f%%")
        plt.ylabel("")
        show_fig("Niveau de risque d'addiction")

        print("🎉 Tous les graphiques ont été affichés !")

    finally:
        spark.stop()

if __name__ == "__main__":
    init_spark_and_plot()
