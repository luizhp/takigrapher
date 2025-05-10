# media2lrc
Automatic folder recursive transcription of audio files to LRC subtitle format using OpenAI Whisper.

## Usage

### GPU
```sh
docker run -d --gpus all \
--name media2lrc \
-v "./data/whisper/cache:/root/.cache/whisper" \
-v "/mnt/nas/music/:/app/media/" \
media2lrc:latest
```
### CPU
```sh
docker run -name media2lrc \
-v "/mnt/nas/music/:/app/media/" \
media2lrc:latest
```
