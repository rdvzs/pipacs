# Pipacs Youtube Downloader

> [!WARNING]
> This project was created for educational purposes only. I do not assume any responsibility for its use.

## Függőségek
- Python3
- TKinter modul (Windows-on alapból tartalmazza a Python, de az a Ubuntu 22.04 hiányolta)
``` bash
sudo apt install python3-tk
```
- PIP csomagkezelő
``` bash
sudo apt install python3-pip
```
- PyTube modul
``` bash
# virtuális környezet pythonhoz, nem kötelező, de ajánlott
# python3 -m venv project_yt
# source ./project_yt/bin/activate

pip3 install pytube==15.0.0
```

- FFmpeg (nem kötelező, csak a FullHD videókhoz kell)

    - https://www.ffmpeg.org
``` bash
sudo apt install ffmpeg
```
(jelenleg a `/usr/lib/ffmpeg` elérési út bele van égetve a kódba, nyilván Windows vagy más disztribúciók esetén változtatás szükséges lehet)

## Indítás
``` bash
python3 pipacs.py
```

## Tulajdonságok
- képes youtube url alapján mp3-at, HD vagy FullHD videót letölteni 
- ugyanezeket tudja playlistek esetén is, de ekkor át kell állítani a felső radiógombot
- ha nem található (vagy valamiért nem tudja letölteni) a FullHD-t vagy HD-t, akkor a következő legnagyobbal próbálkozik
- a különleges karakterekkel néha problémája akadt, így a címek nem mindig felelnek meg a youtube-on található címekkel, előfordult, hogy egyszerűsítésre kerülnek, illetve FullHD esetén egy `_FHD` toldást kapnak
