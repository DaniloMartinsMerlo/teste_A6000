import os
import random
import shutil

# Configurações
pasta_dataset = 'labels_my-project-name_2025-05-15-05-46-00'
extensoes_imagem = ['.jpg', '.png']  # Adicione outras extensões se necessário
proporcao_70 = 0.7
proporcao_train = 0.8  # dos 70%

# Pastas de saída
saida_base = 'dataset'
pastas = {
    'train': os.path.join(saida_base, 'train'),
    'val': os.path.join(saida_base, 'val'),
}
for pasta in pastas.values():
    os.makedirs(pasta, exist_ok=True)

# Coleta todos os pares imagem + txt
arquivos = []
for arquivo in os.listdir(pasta_dataset):
    nome, ext = os.path.splitext(arquivo)
    if ext.lower() in extensoes_imagem:
        caminho_img = os.path.join(pasta_dataset, arquivo)
        caminho_txt = os.path.join(pasta_dataset, f'{nome}.txt')
        if os.path.exists(caminho_txt):
            arquivos.append((caminho_img, caminho_txt))

# Embaralha aleatoriamente
random.shuffle(arquivos)

# Seleciona 70%
total_70 = int(len(arquivos) * proporcao_70)
subset = arquivos[:total_70]

# Divide entre treino e validação
total_train = int(len(subset) * proporcao_train)
train_set = subset[:total_train]
val_set = subset[total_train:]

# Função para copiar arquivos e salvar .txt de lista
def processar(lista, tipo):
    txt_path = os.path.join(saida_base, f'{tipo}.txt')
    with open(txt_path, 'w') as f:
        for img, label in lista:
            nome_arquivo = os.path.basename(img)
            novo_img = os.path.join(pastas[tipo], nome_arquivo)
            novo_txt = os.path.join(pastas[tipo], os.path.basename(label))
            
            shutil.copy(img, novo_img)
            shutil.copy(label, novo_txt)

            f.write(novo_img + '\n')

# Executa
processar(train_set, 'train')
processar(val_set, 'val')

print(f'Total de arquivos encontrados: {len(arquivos)}')
print(f'Treinamento: {len(train_set)} imagens')
print(f'Validação: {len(val_set)} imagens')
