from PIL import Image
import os

# Chemin vers le dossier contenant les images PNG
dossier_source = 'dataset_kahoot/images'

# Créer un dossier de sortie (optionnel)
dossier_sortie = os.path.join(dossier_source, 'jpg')
os.makedirs(dossier_sortie, exist_ok=True)

# Parcours de tous les fichiers du dossier
for nom_fichier in os.listdir(dossier_source):
    if nom_fichier.lower().endswith('.png'):
        chemin_complet = os.path.join(dossier_source, nom_fichier)
        with Image.open(chemin_complet) as img:
            # Convertir en mode RGB si nécessaire
            rgb_img = img.convert('RGB')
            # Construire le nom de sortie
            nom_sans_extension = os.path.splitext(nom_fichier)[0]
            chemin_sortie = os.path.join(dossier_sortie, nom_sans_extension + '.jpg')
            # Sauvegarde en JPEG
            rgb_img.save(chemin_sortie, 'JPEG')
            print(f'Converti : {nom_fichier} -> {chemin_sortie}')
