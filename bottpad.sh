#!/bin/sh

# build sample

# #seed with random initial char
echo "==== generating text"

seeds=(A B C D E F G H I J K L M N O P Q R S T U V W X Y Z)
seed=${seeds[$RANDOM % ${#seeds[@]} ]}
 
temperature=$(python -c "import random; print random.random()")

echo "using temperature" $temperature

cd char-rnn
th sample.lua build_epoch.t7 \
	-gpuid -1 -primetext $seed -seed $RANDOM \
	-temperature $temperature -verbose 0 > ../sample.txt

echo "==== fetching google tts"
cd ../vidmaker
./audmaker.py ../sample.txt tts.mp3

echo "==== reencoding google tts for sox"
ffmpeg -y -loglevel panic -i tts.mp3 tts.wav

echo "==== warping audio"

bassgain=$(python -c "import random; print random.randint(0, 70)")
warpgain=$(python -c "import random; print random.randint(-300, 60)")
speedtweak=$(python -c "import random; print random.randrange(0.5, 1.2)")

echo $bassgain $warpgain $speedtweak

sox -v 10 tts.wav tts_gain.wav bass "+$bassgain"
sox -v 0.005 tts.wav tts_gain_warped.wav gain "+$warpgain"
sox -m tts.wav tts_gain.wav tts_gain_warped.wav \
	tts_merged.wav
sox tts_merged.wav tts_echo.wav \
	reverse reverb 30 reverse \
	speed $speedtweak \

echo "get +/-"

plus=$(python -c "import random; print random.randint(0,500)")
minus=$(python -c "import random; print random.randint(-300,0)")

sox tts_echo.wav tts_echo_high.wav pitch $plus
sox tts_echo.wav tts_echo_low.wav pitch $minus

echo "==== merging warped streams"

sox -m  tts_echo_high.wav \
		tts_echo_low.wav \
		tts_echo.wav tts_final.wav pad 0 2


ffmpeg -loglevel panic -y -i tts_final.wav -ar 16000 -ab 32k tts_final.mp3

echo "==== generating video"

./vidmaker.py ../sample.txt tts_final.mp3 ../render.mkv

echo "==== cleaning up"

cd ..
title=$(cat sample.txt.title)
body=$(cat sample.txt.body)

echo $title
echo $body

youtube-upload \
	--title="$title :: $temperature" \
	--description="$body" \
	--category="Education" "render.mkv"

while [[ $? -ne 0 ]]
do
youtube-upload \
	--title="$title :: $temperature" \
	--description="$bodyesc" \
	--category="Education" "render.mkv"
done 
