#!/usr/bin/env bash

echo "Démarrage de Hadoop HDFS..."

hdfs --daemon start namenode
hdfs --daemon start datanode

echo
echo "Processus Java actifs :"
jps

echo
echo "Interface web : http://localhost:9870"
