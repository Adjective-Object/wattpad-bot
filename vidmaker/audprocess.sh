#!/bin/sh

sox -v 3 tts.wav tts_gain.wav bass +50
sox -v 0.005 tts.wav tts_gain_warped.wav gain +30
sox -m tts.wav tts_gain.wav tts_gain_warped.wav \
	tts_merged.wav
sox tts_merged.wav tts_echo.wav \
	reverse reverb 30 reverse \
	speed 1 \

sox -v 0.5 tts_echo.wav tts_echo_high.wav pitch +500
sox -v 0.5 tts_echo.wav tts_echo_low.wav pitch -300

echo "==== merging warped streams"

sox -m  tts_echo_high.wav \
		tts_echo_low.wav \
		tts_echo.wav tts_final.wav # pad 0 1 

aplay tts_final.wav
