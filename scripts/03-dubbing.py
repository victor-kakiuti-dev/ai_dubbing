from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

transc_path = "../output/traducao.json"

# 1. Ler arquivo com timestamps
with open(transc_path, "r", encoding="utf-8") as f:
    dados = json.load(f)

# 2. Extrair segmentos
segmentos = dados.get("segments", [])

print(f"🎤 Gerando dublagem para {len(segmentos)} segmentos...")

# 3. Para cada segmento, gerar áudio da tradução
for i, seg in enumerate(segmentos):
    texto = seg.get("texto_traduzido", seg.get("text", ""))
    
    if not texto.strip():
        print(f"⚠️ Segmento {i} sem texto, pulando...")
        continue
    
    print(f"  {i+1}. [{seg['start']:.1f}s-{seg['end']:.1f}s] {texto[:40]}...")
    
    try:
        resposta = client.audio.speech.create(
            model="tts-1",
            voice="nova",  # Escolha: alloy, echo, fable, onyx, nova, shimmer
            input=texto,
            speed=1.0
        )
        
        # Salvar segmento
        nome_arquivo = f"dublagem_seg_{i}.mp3"
        resposta.stream_to_file(nome_arquivo)
        
        print(f"    ✅ Salvo: {nome_arquivo}")
        
    except Exception as e:
        print(f"    ❌ Erro: {str(e)[:50]}")

print("\n✅ Dublagem gerada! Arquivos:")
print("   dublagem_seg_000.mp3, dublagem_seg_001.mp3, ...")