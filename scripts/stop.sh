#!/usr/bin/env bash

echo "Arrêt de Hadoop HDFS..."

hdfs --daemon stop datanode
hdfs --daemon stop namenode

echo
echo "Processus Java restants :"
jps