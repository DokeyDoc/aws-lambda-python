import rembg
import numpy as np
import os
import boto3
from PIL import Image

# Configuration du bucket S3
BUCKET_NAME = "roivioli-buckett"  
OUTPUT_FILENAME = "output_image.png"  

# Charger l'image d'entrée
input_image = Image.open('img.jpg')

# Convertir l'image en tableau numpy
input_array = np.array(input_image)

# Appliquer la suppression d'arrière-plan avec rembg
output_array = rembg.remove(input_array)

# Créer une image PIL à partir du tableau de sortie
output_image = Image.fromarray(output_array)

# Définir le chemin de sortie
output_dir = "./img"
output_path = os.path.join(output_dir, OUTPUT_FILENAME)

# Vérifier si le dossier existe, sinon le créer
os.makedirs(output_dir, exist_ok=True)

# Sauvegarde de l'image traitée
output_image.save(output_path)
print(f"Image enregistrée localement : {output_path}")

# Initialiser le client S3
s3_client = boto3.client("s3")

# Uploader le fichier sur S3
try:
    s3_client.upload_file(output_path, BUCKET_NAME, OUTPUT_FILENAME)
    print(f"✅ Fichier uploadé sur S3 : s3://{BUCKET_NAME}/{OUTPUT_FILENAME}")
except Exception as e:
    print(f"❌ Erreur lors de l'upload sur S3 : {e}")
