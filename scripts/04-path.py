import json
import os

# Caminho do arquivo JSON original
input_json = "../output/traducao.json"

# Caminho onde os áudios estão salvos (ajuste para o seu caminho)
audio_dir = "../output/"

# Caminho de saída do novo JSON
output_json = "transcricao_final.json"

# Carregar JSON
with open(input_json, "r", encoding="utf-8") as f:
    data = json.load(f)

# Garantir que a pasta existe
os.makedirs(audio_dir, exist_ok=True)

# Para cada segmento, adicionar o file_path
for seg in data.get("segments", []):
    seg_id = seg["id"]
    filename = f"dublagem_seg_{seg_id}.mp3"    # padrão recomendado
    seg["file_path"] = os.path.join(audio_dir, filename)

# Salvar resultado
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("JSON atualizado com file_path criado com sucesso!")