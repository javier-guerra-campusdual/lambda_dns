#!/bin/bash

# Directorio actual
CURRENT_DIR=$(pwd)
LAMBDA_DIR="src/lambda/dns_updater"
TERRAFORM_DIR="infrastructure/terraform"

# Crear directorio temporal
echo "Creando directorio temporal..."
TEMP_DIR=$(mktemp -d)
cp -r $LAMBDA_DIR/* $TEMP_DIR/

# Instalar dependencias
echo "Instalando dependencias..."
cd $TEMP_DIR
pip install -r requirements.txt -t .
cd $CURRENT_DIR

# Crear zip
echo "Creando archivo zip..."
cd $TEMP_DIR
zip -r $CURRENT_DIR/$TERRAFORM_DIR/lambda.zip ./*
cd $CURRENT_DIR

# Limpiar
echo "Limpiando archivos temporales..."
rm -rf $TEMP_DIR

echo "Archivo lambda.zip creado en $TERRAFORM_DIR"