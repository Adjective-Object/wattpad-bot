#!/usr/bin/python

from random import randint
from gtts import gTTS
import sys

TTS_FILE = "tts2.mp3"


def create_video(text):
    sentences = text.split(".")[:-1]
    a, b = randint(0, len(sentences)), randint(0, len(sentences))
    body = text #".".join(sentences[min(a, b): max(a, b)]) + "."

    print body

    ind = text.find(" ", 3, 15)
    title = text[0: ind if ind != -1 else 15]
    
    print title

    with open(TEXT_TARGET+".body", "w") as f:
        f.write(body)

    with open(TEXT_TARGET+".title", "w") as f:
        f.write(title)

    tts = gTTS(text=body, lang="en")
    tts.save(TTS_FILE)

if __name__ == "__main__":
    TEXT_TARGET = sys.argv[1]
    TTS_FILE = sys.argv[2]

    with open(TEXT_TARGET) as text_target:
        create_video(text_target.read())
