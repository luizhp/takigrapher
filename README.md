# takigrapher
Automatic folder recursive transcription of any file containing audio using OpenAI Whisper.

Audio files supported:
.mp3, .wav, .m4a, .flac, .aac, .ogg, .wma, .mp4, .mkv, .webm, .opus, .mov, .avi

Files will be saved in the same directory as the media file, with the same base name.

Supported output files types:
.lrc, .vtt, .srt, .txt, .json

## Usage

### Help

```sh
usage: python3 src/main.py [options]

Transcribe media files to LRC using Whisper

options:
  -h, --help            show this help message and exit
  -m [PATH], --media [PATH]
                        media folder path to recursively search for media files
  -n [MODEL], --modelname [MODEL]
                        available whisper models: (Default: tiny)
                        tiny: Smallest and fastest, with lower accuracy.
                        tiny.en: English-only version of tiny; slightly more accurate for English tasks.
                        base: Balance between size, speed, and accuracy.
                        base.en: English-only version of base; better accuracy on English data.
                        small: More accurate than base, but larger and slower.
                        small.en: English-only version of small; improved performance in English.
                        medium: High accuracy, consumes more resources.
                        medium.en: English-only version of medium; better results on English tasks.
                        large: Largest and most accurate in the original series, but heavy and slow.
                        large-v1: First major large variant; improved accuracy and stability.
                        large-v2: Enhanced version of v1 with better alignment and reasoning.
                        large-v3: Latest and most advanced version; best overall performance.
  -d [DEVICE], --device [DEVICE]
                        available devices: cpu or cuda
  -v, --verbose         activate verbose mode
  -st [TYPE], --sourcetype [TYPE]
                        available types: mp3, wav, m4a, flac, aac, ogg, wma, mp4, mkv, webm, opus, mov, avi. (Default: all)
  -sl [LANGUAGE], --sourcelanguage [LANGUAGE]
                        ISO 639-1 available languages:
                        af: afrikaans, am: amharic, ar: arabic, as: assamese, az: azerbaijani, ba: bashkir, be: belarusian, bg: bulgarian, bn: bengali, bo: tibetan, br: breton, bs: bosnian, ca: catalan, cs: czech, cy: welsh, da: danish, de: german, el: greek, en: english, es: spanish, et: estonian, eu: basque, fa: persian, fi: finnish, fo: faroese, fr: french, gl: galician, gu: gujarati, ha: hausa, haw: hawaiian, he: hebrew, hi: hindi, hr: croatian, ht: haitian creole, hu: hungarian, hy: armenian, id: indonesian, is: icelandic, it: italian, ja: japanese, jw: javanese, ka: georgian, kk: kazakh, km: khmer, kn: kannada, ko: korean, la: latin, lb: luxembourgish, ln: lingala, lo: lao, lt: lithuanian, lv: latvian, mg: malagasy, mi: maori, mk: macedonian, ml: malayalam, mn: mongolian, mr: marathi, ms: malay, mt: maltese, my: myanmar, ne: nepali, nl: dutch, nn: nynorsk, no: norwegian, oc: occitan, pa: punjabi, pl: polish, ps: pashto, pt: portuguese, ro: romanian, ru: russian, sa: sanskrit, sd: sindhi, si: sinhala, sk: slovak, sl: slovenian, sn: shona, so: somali, sq: albanian, sr: serbian, su: sundanese, sv: swedish, sw: swahili, ta: tamil, te: telugu, tg: tajik, th: thai, tk: turkmen, tl: tagalog, tr: turkish, tt: tatar, uk: ukrainian, ur: urdu, uz: uzbek, vi: vietnamese, yi: yiddish, yo: yoruba, yue: cantonese, zh: chinese.  (Default: auto)
  -tl [LANGUAGE], --targetlanguage [LANGUAGE]
                        ISO 639-1 available languages:
                        af: afrikaans, am: amharic, ar: arabic, as: assamese, az: azerbaijani, ba: bashkir, be: belarusian, bg: bulgarian, bn: bengali, bo: tibetan, br: breton, bs: bosnian, ca: catalan, cs: czech, cy: welsh, da: danish, de: german, el: greek, en: english, es: spanish, et: estonian, eu: basque, fa: persian, fi: finnish, fo: faroese, fr: french, gl: galician, gu: gujarati, ha: hausa, haw: hawaiian, he: hebrew, hi: hindi, hr: croatian, ht: haitian creole, hu: hungarian, hy: armenian, id: indonesian, is: icelandic, it: italian, ja: japanese, jw: javanese, ka: georgian, kk: kazakh, km: khmer, kn: kannada, ko: korean, la: latin, lb: luxembourgish, ln: lingala, lo: lao, lt: lithuanian, lv: latvian, mg: malagasy, mi: maori, mk: macedonian, ml: malayalam, mn: mongolian, mr: marathi, ms: malay, mt: maltese, my: myanmar, ne: nepali, nl: dutch, nn: nynorsk, no: norwegian, oc: occitan, pa: punjabi, pl: polish, ps: pashto, pt: portuguese, ro: romanian, ru: russian, sa: sanskrit, sd: sindhi, si: sinhala, sk: slovak, sl: slovenian, sn: shona, so: somali, sq: albanian, sr: serbian, su: sundanese, sv: swedish, sw: swahili, ta: tamil, te: telugu, tg: tajik, th: thai, tk: turkmen, tl: tagalog, tr: turkish, tt: tatar, uk: ukrainian, ur: urdu, uz: uzbek, vi: vietnamese, yi: yiddish, yo: yoruba, yue: cantonese, zh: chinese. (Default: auto)
  -tt [TYPE], --targettype [TYPE]
                        available types: lrc, txt, srt, json, vtt. (Default: lrc)
  -te [ACTION], --targetexists [ACTION]
                        available actions: overwrite, skip, rename. (Default: skip)
  -ts, --targetsuffix   add suffix to target file name. (Default: false)

Example usage:
python3 src/main.py --media ./media --modelname tiny --device cuda --verbose --sourcetype mp3 --sourcelanguage en --targetlanguage en
```

### CLI

#### Setup
```sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

#### Command line
```sh
python3 src/main.py -v -m ./media/holiday.mp4 -n base.en -tt lrc -te overwrite
```

### Docker

#### Device

##### CPU
```sh
docker run -name takigrapher \
-v "./data/whisper/cache:/root/.cache/whisper" \
-v "/mnt/nas/music/:/app/media/" \
luizhp/takigrapher:latest
```

##### GPU
```sh
docker run -d --gpus all \
--name takigrapher \
-v "./data/whisper/cache:/root/.cache/whisper" \
-v "/mnt/nas/music/:/app/media/" \
luizhp/takigrapher:latest
```
#### Volume Mounts

- mount media folder
`-v "/mnt/nas/music/:/app/media/"`

- keep models in /root/.cache/whisper
`-v "./data/whisper/cache:/root/.cache/whisper"`

#### Examples of how to execute the application

Below are some examples of how to execute the application for transcribing files or folders containing audio using different command-line options and Docker commands:
```sh
docker exec -it takigrapher python3 src/main.py -v -m ./media/music/bandname/ -n medium -tt lrc -te overwrite -ts
```

```sh
docker exec -it takigrapher python3 src/main.py -v -m ./media/music/bandname/song.mp3 -n medium -tt lrc -te overwrite -ts
```

```sh
docker exec -it takigrapher python3 src/main.py -m ./media/tv/mytvshow/ -n medium.en -sl en -tt srt -te rename
```


### Docker Compose

#### Devices

##### CPU
Check [here](docker-compose-cpu.yaml) for the docker-compose-cpu.yaml file

##### GPU
Check [here](docker-compose-gpu.yaml) for the docker-compose-gpu.yaml file

## License

This project is licensed under the GNU GPLv3 License - see the [LICENSE](./LICENSE) file for details.
