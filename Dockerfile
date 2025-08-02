FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

# Metadata
LABEL maintainer="luizhp <luizhp@yahoo.com>"
LABEL description="Dockerfile for OpenAi Whisper ASR with CUDA support"
LABEL version="0.0.13"
LABEL repository="https://github.com/luizhp/takigrapher"
LABEL homepage="https://github.com/luizhp/takigrapher"
LABEL license="GPLv3"
LABEL org.opencontainers.image.source="https://github.com/luizhp/takigrapher"
# Note: Requires NVIDIA GPU and NVIDIA Container Toolkit for CUDA support

# Install system dependencies
RUN apt-get update && \
    apt-get install -y apt-utils ffmpeg libpng-dev libjpeg-dev libopenblas-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Install PyTorch and related packages
RUN pip3 install --upgrade pip --root-user-action=ignore && \
    pip3 install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu121 --root-user-action=ignore && \
    pip3 cache purge

# Create work directory
WORKDIR /app

# Copy application files
COPY src/ ./src/
COPY requirements.txt README.md ./

# Create and configure takigrapher script
RUN touch /usr/local/bin/takigrapher && \
    echo '#!/bin/bash\npython3 /app/src/main.py "$@"' > /usr/local/bin/takigrapher && \
    chmod +x /usr/local/bin/takigrapher

# Create media directory and copy sample files
RUN mkdir -p /app/media
COPY media/sample.mp3 media/sample3trk.mp4 ./media/

# Install Python dependencies
RUN if [ -f requirements.txt ]; then pip3 install -r requirements.txt --root-user-action=ignore; fi && \
    pip3 cache purge

# Default command (keeps container running for debugging)
CMD ["tail", "-f", "/dev/null"]
