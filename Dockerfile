FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

# Installs system dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

# Install Whisper and torch (with CUDA support)
RUN pip3 install --upgrade pip && \
    pip3 install torch --index-url https://download.pytorch.org/whl/cu121 && \
    pip3 install openai-whisper

# Creates work directory
WORKDIR /app

# Copy the script to the container
COPY *.py .

# Creates directory for media files (can be overridden by volume)
RUN mkdir /app/media

# Default command: runs the script
ENTRYPOINT ["python3", "takigrapher.py"]
