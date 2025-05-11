import os
import random
import shutil
from pathlib import Path

# 🔧 À adapter si besoin
dataset_dir = Path("../dataset_kahoot/")  # ex: Path("dataset/")
images_dir = dataset_dir / "images"
labels_dir = dataset_dir / "labels"

# 📁 Dossiers de destination
for split in ["train", "val"]:
    (images_dir / split).mkdir(parents=True, exist_ok=True)
    (labels_dir / split).mkdir(parents=True, exist_ok=True)

# 🖼️ Liste des fichiers .jpg
image_files = [f for f in images_dir.glob("*.jpg")]
random.shuffle(image_files)

# 🔢 Split 80/20
split_idx = int(0.8 * len(image_files))
train_files = image_files[:split_idx]
val_files = image_files[split_idx:]

# 📦 Fonction de déplacement
def move_files(file_list, split):
    for img_path in file_list:
        txt_path = labels_dir / (img_path.stem + ".txt")
        
        if txt_path.exists():
            shutil.move(str(img_path), str(images_dir / split / img_path.name))
            shutil.move(str(txt_path), str(labels_dir / split / txt_path.name))
        else:
            print(f"[!] ⚠️ Pas d'annotation pour : {img_path.name}")

# 🚚 Déplacement
move_files(train_files, "train")
move_files(val_files, "val")

print("✅ Split terminé !")
