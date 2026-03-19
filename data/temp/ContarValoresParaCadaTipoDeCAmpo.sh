#!/bin/bash

# Definir el archivo origen
FILE="ObesityDataSet.csv"

# Bucle para recorrer las 17 columnas
for i in {1..17}; do
    # 1. Extraer el nombre del campo (Fila 1, Columna i)
    # head -n 1 toma la primera línea, cut extrae la columna i
    CAMPO=$(head -n 1 "$FILE" | cut -d ',' -f $i)
    
    # 2. Informar en consola el proceso
    echo "Procesando Campo $i: $CAMPO"
    
    # 3. Ejecutar el conteo y guardarlo en el archivo dinámico
    # tail -n +2 omite la cabecera para no contar el nombre del campo como un valor
    tail -n +2 "$FILE" | cut -d ',' -f $i | sort | uniq -c > "${FILE%.*}.$CAMPO.csv"
done