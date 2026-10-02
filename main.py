import subprocess
import os
import sys

def empacotar_h264_para_mp4_forca_bruta(arquivo_entrada: str, arquivo_saida: str, fps: int = 30) -> None:
    """
    Abordagem de Força Bruta: Ignora DTS quebrado, força uma escala de tempo 
    aceitável para MP4 e salva o log em um arquivo para não travar o terminal.
    
    Args:
        arquivo_entrada: O caminho para o H.264 corrompido.
        arquivo_saida: O destino final em MP4.
        fps: A taxa de quadros (frames por segundo).
    """
    arquivo_log = "log_cirurgia_ffmpeg.txt"

    # Validação de existencia
    if not os.path.exists(arquivo_entrada):
        print(f"Erro fatal: O arquivo '{arquivo_entrada}' não existe.")
        sys.exit(1)

    print(f"Iniciando o trator temporal no arquivo: {arquivo_entrada}")
    print(f"Se houverem reclamações do FFmpeg, elas estarão no arquivo: {arquivo_log}")
    print("Por favor, aguarde. O terminal não vai mostrar o progresso para não travar...\n")

    # O comando para limpar o H.264 cru e corrompido
    comando = [
        'ffmpeg',
        '-y',                           # Sobrescreve o destino se existir
        '-fflags', '+genpts+igndts',    # GERA os PTS e IGNORA os DTS bugados (O Trator)
        '-r', str(fps),                 # Força a taxa de quadros ANTES de processar
        '-i', arquivo_entrada,          # Arquivo de origem
        '-video_track_timescale', '90k',# Escala de tempo padrão da indústria para H.264
        '-c', 'copy',                   # Continua sem recodificar
        arquivo_saida                   # Arquivo final
    ]

    # Abre um arquivo de texto para vomitar os logs
    with open(arquivo_log, "w") as log_file:
        try:
            # Redireciona os erros (stderr) para o arquivo de log. 
            subprocess.run(comando, check=True, stderr=log_file, stdout=log_file)
            print(f"✅ 🎬 O teu vídeo pronto está em: {arquivo_saida}")
            
        except subprocess.CalledProcessError:
            print(f"❌ Ocorreu um erro. Abre o arquivo '{arquivo_log}' para ver o que o FFmpeg disse.")
    

# ==========================================
# Ponto de Entrada
# ==========================================
if __name__ == "__main__":
    video_cru = "05_20260728_090000.h264"
    video_pronto = "28_07_2026.mp4"

    empacotar_h264_para_mp4_forca_bruta(video_cru, video_pronto, fps=30)