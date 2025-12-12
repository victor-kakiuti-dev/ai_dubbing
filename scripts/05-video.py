from moviepy.editor import AudioFileClip, VideoFileClip, CompositeAudioClip
import json

video_path = "../input/video.mp4"

video = VideoFileClip(video_path)

audio_clips = []

transc_path = "../output/transcricao_final.json"

with open(transc_path, "r", encoding="utf-8") as f:
    dados = json.load(f)

# 2. Extrair segmentos
segmentos = dados.get("segments", [])

for item in segmentos:  # cada item contém: start, end, file_path
    audio = AudioFileClip(item["file_path"]).set_start(item["start"])
    audio_clips.append(audio)

audio_final = CompositeAudioClip(audio_clips)
video_final = video.set_audio(audio_final)

video_final.write_videofile("video_dublado.mp4", codec="libx264", audio_codec="aac")




from moviepy.editor import AudioFileClip, VideoFileClip, CompositeAudioClip


video_path = "../input/video.mp4"
# Carrega o vídeo original
video = VideoFileClip(video_path)

# Áudio original do vídeo (música)
audio_original = video.audio

audio_original = audio_original.volumex(0.4)

# Lista para guardar todos os áudios da dublagem
audio_clips = [audio_original]  # <- já colocamos o áudio original aqui

transc_path = "../output/transcricao_final.json"

# Carregue seu JSON
import json
with open(transc_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Para cada segmento, adiciona o áudio no tempo correto
for seg in data["segments"]:
    audio = AudioFileClip(seg["file_path"]).volumex(4.0).set_start(seg["start"])
    audio_clips.append(audio)

# Faz o mix final
audio_final = CompositeAudioClip(audio_clips)

# Coloca esse áudio final no vídeo
video_final = video.set_audio(audio_final)

# Exporta
video_final.write_videofile("video_dublado.mp4",
                            codec="libx264",
                            audio_codec="aac")
