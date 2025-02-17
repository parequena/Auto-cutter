# Auto-cutter
This is a script I use to automate the use of `auto-editor`, as I was a bit tired of using it with videos, there is still work to be done, feel free to make a PR to contribute to the repository.

## Usage
``` bash
$ python auto-cutter.py -h
usage: auto-cutter.py [-h] [-f [FOLDER]] [-q QUIET] [video]

Auto cutter python script, used to call auto-editor in a folder.

positional arguments:
  video                 Input video or playlist to edit/download

options:
  -h, --help            show this help message and exit
  -f, --folder [FOLDER]
                        Folder to work with
  -q, --quiet QUIET     Enables quiet mode for yt_dlp and auto-editor
```

### Options
- **video** : Allows to auto-edit a video, if a URL is provided, it will download it with `yt-dlp`
- **f/folder** : If a URL was provided, it will download all files into that file, and treat it as an input folder in `auto-editor`

# Dependencies
Currently, we are working with some dependencies, those are:
- `python3` to execute the script (in theory it should be compatible with Windows 11 Terminal, but not tested)
- [ffmpeg](https://www.ffmpeg.org/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [auto-editor](https://github.com/WyattBlue/auto-editor)

> All python dependencies has been installed via pip

# Tested on
- [x] Arch Linux WSL (x86_64) `Linux xxxxx 5.15.167.4-microsoft-standard-WSL2`
- [x] Ubuntu 24.04.1 LTS  (x86_64) `Linux xxxxx 5.15.167.4-microsoft-standard-WSL2`
- [x] Windows 10/11 Terminal (x86_64)

# TODO
- [x] Automatize yt-dlp download to the folder and use it as input.
- [x] Allow a single video input.
- [ ] Add a script parameter to parametrice `auto-editor` (currently parameters are hardcoded).
- [ ] ~~Add a script parameter to parametrice `yt-dlp` (currently parameters are hardcoded).~~
- [ ] Move `auto-editor` from `subprocess.run()` to python calls.
- [x] Move `yt-dlp` from `subprocess.run()` to python calls.
- [ ] Add a verbose option
- [ ] Add a quiet version that mutes all messages from this script
- [ ] Enable colors
- [ ] Add an option to download audio.
- [ ] Add an option to transcribe audio.

# Troubleshooting
### OSError: [Errno 28] No space left on device in WSL
I got this error while executing a very long video with `auto-editor` I could not open an [Discussion](https://github.com/WyattBlue/auto-editor/discussions) but as far as I investigated, it could be solved with: `TMPDIR=<enought_space> && python auto-cutter.py` (or in defect, calling `auto-editor`)

# Get in Touch
If you want to get in touch with me, here are my social networks
- [Twitter](https://x.com/conPdePABLO)
- [BlueSky](https://bsky.app/profile/theapoca.bsky.social)
- [Youtube](https://www.youtube.com/@conpdepab)
- [Instagram](https://www.instagram.com/conpdepab/)
- [LinkedIn](https://www.linkedin.com/in/parequena/)
