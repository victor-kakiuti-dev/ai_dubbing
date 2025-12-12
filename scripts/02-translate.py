from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
transc_path = "../output/timestamps.json"

# 1. Carregar JSON
with open(transc_path, "r", encoding="utf-8") as f:
    transcript_data = json.load(f)

# 2. Extrair TODOS os textos de forma organizada
textos_info = {
    "texto_completo": transcript_data.get("text", ""),  # Texto inteiro
    "segmentos": []
}

# Para cada segmento, guardar texto E metadata
for segment in transcript_data.get("segments", []):
    textos_info["segmentos"].append({
        "id": segment["id"],
        "start": segment["start"],
        "end": segment["end"],
        "texto_original": segment["text"]
    })

# 3. Preparar para tradução - DUAS OPÇÕES:

# OPÇÃO A: Traduzir segmento por segmento (RECOMENDADO para dublagem)
textos_para_traduzir = []
for seg in textos_info["segmentos"]:
    textos_para_traduzir.append(seg["texto_original"])

texto_para_api = "\n".join(textos_para_traduzir)

# OPÇÃO B: Traduzir texto completo primeiro (para contexto)
# texto_para_api = textos_info["texto_completo"]

# 4. Pedir tradução preservando estrutura
prompt = f"""
Você é um tradutor musical profissional.

TEXTO ORIGINAL (cada item é um segmento com timestamp específico):
{texto_para_api}

INSTRUÇÕES CRÍTICAS:
1. Traduza CADA LINHA individualmente
2. Mantenha EXATAMENTE o mesmo número de linhas
3. Cada linha traduzida deve corresponder ao segmento original
4. Preserve a estrutura rítmica para sincronização labial
5. Não adicione números, apenas as traduções

TRADUÇÃO EM PORTUGUÊS (uma linha por segmento):
"""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Especialista em tradução musical para dublagem."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.1
)

# 5. Processar traduções
traducoes_brutas = response.choices[0].message.content.strip().split("\n")
traducoes_limpas = [t.strip().strip('"').strip("'") for t in traducoes_brutas if t.strip()]

# 6. Adicionar traduções ao JSON original
transcript_data["texto_traduzido_completo"] = " ".join(traducoes_limpas)  # Texto completo traduzido

# Adicionar a cada segmento
for i, segment in enumerate(transcript_data["segments"]):
    if i < len(traducoes_limpas):
        segment["texto_traduzido"] = traducoes_limpas[i]
    else:
        segment["texto_traduzido"] = f"[ERRO: Sem tradução] {segment['text']}"

# 7. Salvar versão enriquecida
with open("traducao.json", "w", encoding="utf-8") as f:
    json.dump(transcript_data, f, indent=2, ensure_ascii=False)

