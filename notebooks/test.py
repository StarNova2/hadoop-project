import os
import matplotlib.pyplot as plt
import seaborn as sns
from pyspark.sql import SparkSession

os.environ['HADOOP_CONF_DIR'] = '/usr/local/hadoop/etc/hadoop'

spark = SparkSession.builder \
    .appName("ESGI_Hadoop_Project_Parsing") \
    .master("local[*]") \
    .config("spark.sql.warehouse.dir", "hdfs://localhost:9000/user/hive/warehouse") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

csv_path = "/home/letort/datasets/gaming_mental_health/part-00000-c5eca9e6-5393-4d27-bb31-0d72a0573949-c000.csv"
df_spark = spark.read.csv(csv_path, header=True, inferSchema=True)
df = df_spark.toPandas()

plt.figure()
df['gender'].value_counts().plot.pie(autopct="%1.1f%%")
plt.ylabel("")
plt.title("Répartition par Genre")
plt.tight_layout()
plt.show()

plt.figure()
sns.histplot(data=df, x="age", kde=True, bins=15)
plt.title("Distribution des Âges")
plt.tight_layout()
plt.show()

plt.figure()
sns.barplot(data=df, x="sleep_quality", y="daily_gaming_hours", errorbar=None)
plt.title("Moyenne des heures de jeu par qualité de sommeil")
plt.tight_layout()
plt.show()

plt.figure()
sns.boxplot(data=df, x="daily_gaming_hours", y="sleep_quality")
plt.title("Impact des heures de jeu sur la qualité du sommeil")
plt.tight_layout()
plt.show()

plt.figure()
sns.scatterplot(data=df, x="daily_gaming_hours", y="sleep_hours")
plt.title("Relation heures de jeu et temps de sommeil")
plt.tight_layout()
plt.show()

plt.figure()
sns.histplot(data=df, x="monthly_game_spending_usd", kde=True)
plt.title("Distribution des dépenses mensuelles ($)")
plt.tight_layout()
plt.show()

plt.figure()
df['gaming_addiction_risk_level'].value_counts().plot.pie(autopct="%1.1f%%")
plt.ylabel("")
plt.title("Niveau de risque d'addiction")
plt.tight_layout()
plt.show()

spark.stop()
print("Affichage des graphiques terminé.")
