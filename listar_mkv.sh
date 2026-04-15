#!/usr/bin/env bash

set -euo pipefail

# Si no se pasa la ruta como argumento, la pide
if [ "${1:-}" != "" ]; then
    folder_path="$1"
else
    read -r -p "Introduce la ruta de la carpeta: " folder_path
fi

# Verifica que la carpeta exista
if [ ! -d "$folder_path" ]; then
    echo "Error: la carpeta no existe: $folder_path"
    exit 1
fi

# Guardar el .txt en la carpeta desde donde se ejecuta el script
output_file="$(pwd)/lista_mkv.txt"

# Crear la lista
find "$folder_path" -maxdepth 1 -type f \( -name '*.mkv' -o -name '*.MKV' \) -printf '%f\n' > "$output_file"

# Contar archivos y añadir el total al final
total_files=$(wc -l < "$output_file")
echo "Total de archivos .mkv/.MKV: $total_files" >> "$output_file"

echo "Lista creada en: $output_file"
