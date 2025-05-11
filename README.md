# takigrapher
Automatic folder recursive transcription of audio files using OpenAI Whisper.

Audio files supported:
.mp3, .wav, .m4a, .flac, .aac, .ogg, .wma, .mp4, .mkv, .webm, .opus, .mov, .avi

Files will be saved in the same directory as the media file, with the same base name.

Supported output files types:
.lrc, .vtt, .srt, .txt, .json

## Usage

### Docker

#### GPU
```sh
docker run -d --gpus all \
--name takigrapher \
-v "./data/whisper/cache:/root/.cache/whisper" \
-v "/mnt/nas/music/:/app/media/" \
takigrapher:latest
```
#### CPU
```sh
docker run -name takigrapher \
-v "/mnt/nas/music/:/app/media/" \
takigrapher:latest
```
