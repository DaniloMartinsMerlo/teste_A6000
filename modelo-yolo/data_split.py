import random
import shutil
from pathlib import Path

# --- CONFIGURAÇÃO PARA SUA ESTRUTURA ---
BASE_DIR    = Path('.')               # assume que você executa data_split.py em modelo-yolo/
IMG_SRC_DIR = BASE_DIR / 'imgs_filtered'
LBL_SRC_DIR = BASE_DIR / 'labels1'

# proporções
TRAIN_PCT = 0.6
VAL_PCT   = 0.4

# extensões aceitas (case-insensitive)
IMG_EXTS = {'.jpg', '.jpeg', '.png', '.PNG'}

# --- CRIAÇÃO DAS PASTAS DE DESTINO ---
for split in ('train','val'):
    (IMG_SRC_DIR / split).mkdir(parents=True, exist_ok=True)
    (LBL_SRC_DIR / split).mkdir(parents=True, exist_ok=True)

# --- LISTAGEM E EMBARALHAMENTO ---
all_images = [p for p in IMG_SRC_DIR.iterdir() if p.suffix.lower() in IMG_EXTS]
random.seed(42)
random.shuffle(all_images)

n = len(all_images)
n_train = int(TRAIN_PCT * n)
n_val   = int(VAL_PCT   * n)  

splits = {
    'train': all_images[:n_train],
    'val':   all_images[n_train:n_train + n_val]
    }

# --- MOVENDO ARQUIVOS ---
for split, imgs in splits.items():
    img_dest = IMG_SRC_DIR / split
    lbl_dest = LBL_SRC_DIR / split

    for img_path in imgs:
        # move a imagem
        shutil.move(str(img_path), str(img_dest  / img_path.name))

        # move o label correspondente (mesmo nome, .txt)
        lbl_path = LBL_SRC_DIR / (img_path.stem + '.txt')
        if lbl_path.exists():
            shutil.move(str(lbl_path), str(lbl_dest / lbl_path.name))
        else:
            print(f'⚠️  Label não encontrado para {img_path.name}')

# --- RESUMO ---
print("Divisão concluída:")
for split in ('train','val'):
    n_img = len(list((IMG_SRC_DIR/split).iterdir()))
    print(f"  {split.capitalize():5s}: {n_img} imagens")
