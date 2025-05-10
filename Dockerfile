FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install -y python3 python3-pip ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

# Instala o Whisper e torch (com suporte a CUDA)
RUN pip3 install --upgrade pip && \
    pip3 install torch --index-url https://download.pytorch.org/whl/cu121 && \
    pip3 install git+https://github.com/openai/whisper.git

# Cria diretório de trabalho
WORKDIR /app

# Copia o script para o container
COPY media2lrc.py .

# Cria diretório para os arquivos de media (pode ser sobrescrito por volume)
RUN mkdir /app/mp3

# Comando padrão: executa o script
ENTRYPOINT ["python3", "media2lrc.py"]
