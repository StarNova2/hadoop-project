#!/usr/bin/env bash

echo "=== Vérification des processus Hadoop ==="
jps

echo
echo "=== Contenu du dataset dans HDFS ==="
hdfs dfs -ls -h /projet/gaming_mental_health/input

echo
echo "=== Aperçu du CSV ==="
hdfs dfs -cat /projet/gaming_mental_health/input/gaming_mental_health.csv | head
