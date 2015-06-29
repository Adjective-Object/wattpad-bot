# ＢＯＴＴＰＡＤ

**oRIGINAL PROJECT DO NOT STEAL IF U STEAL I WILL COME TO UR ACCOUNT & CT YU**

A wattpad-trained rnn for making dumb videos to put on youtube.

Very hacky, do not use.

trains with [char-rnn](https://github.com/karpathy/char-rnn)  
renders with [Spectrum.py](https://github.com/Adjective-Object/Spectrum.py)  
uploads with [youtube-upload](https://github.com/tokland/youtube-upload)

For it to even have a chance of running, you need to..

- `(sudo) pip install -r requirements.txt` for each of 
	- wattfetcher/requirements.txt
	- vidmaker/requirements.txt
- install youtube-upload
- clone char-rnn inside the project root
- generate a build_epoch.t7 file from from char-rnn
- symlink Spectrum.py from its real directory to `vidmaker`
- put images in `vidmaker/pics`
- put fonts in `vidmaker/fonts`
- run bottpad.sh from the project root

Something will probably break.
Spectrum.py is just bad in a lot of ways, so it _needs_ to be redone with
[cSpectrum](https://github.com/Adjective-Object/cSpectrum) once that's
minimally viable
