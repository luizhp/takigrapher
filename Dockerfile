FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
LABEL maintainer="luizhp <luizhp@yahoo.com>"
LABEL description="Dockerfile for OpenAi Whisper ASR with CUDA support"
LABEL version="0.0.13"
LABEL repository="https://github.com/luizhp/takigrapher"
LABEL homepage="https://github.com/luizhp/takigrapher"
LABEL license="GPLv3"
LABEL org.opencontainers.image.source="https://github.com/luizhp/takigrapher"

# Installs system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg libpng-dev libjpeg-dev libopenblas-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Install Whisper and torch (with CUDA support)
RUN pip3 install --upgrade pip --root-user-action=ignore && \
    pip3 install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu121 --root-user-action=ignore && \
    pip3 cache purge

    # Creates work directory
WORKDIR /app

# Copy the script to the container
COPY src/ ./src/
COPY requirements.txt README.md ./

# Copy the takigrapher script to the container
RUN touch /usr/local/bin/takigrapher && \
    echo '#!/bin/bash\npython3 /app/src/main.py "$@"' > /usr/local/bin/takigrapher && \
    chmod +x /usr/local/bin/takigrapher

# Creates directory for media files (can be overridden by volume)
RUN mkdir -p /app/media
COPY media/sample.mp3 media/sample3trk.mp4 ./media/

# Installs Python dependencies
RUN if [ -f requirements.txt ]; then pip3 install -r requirements.txt --root-user-action=ignore; fi && \
    pip3 cache purge

# Keeps container running
CMD ["tail", "-f", "/dev/null"]
