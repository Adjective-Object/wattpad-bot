#!/usr/bin/python
import os
import sys
import subprocess
from random import choice, seed, randint

FONTS_DIR = "./fonts"
PICS_DIR = "./pics/vaporware"

OUT_PATH = "output.mkv"

def mk_rand_arg(picture, font, title, subtitle):
    r,g,b = randint(0,255), randint(0,255), randint(0,255)
    resolution = randint(5,100)
    options = [
        ["-e", ("bkgimg %s, " % picture) +
              "bareq ONE_THIRD 0 0, "
              "hbar ONE_THIRD -8 5",
         "--colormain=%s,%s,%s,200" % (r,g,b),
         "--colorsub=%s,%s,%s,250" % (r,g,b),
         '-q %s' % (resolution),
         "--font=%s" % (font)],

        ["-e", ("bkgimg %s, " % picture) +
              "polyeq BOTTOM 0 1, "
              "polyeq BOTTOM -20 1 1, "
              "polyeq BOTTOM -40 1 1, "
              "hbar BOTTOM -70 -10",
         "--colormain=%s,%s,%s,200" % (r,g,b),
         "--colorsub=%s,%s,%s,250" % (r,g,b),
         '-q %s' % (resolution),
         "--font=%s" % (font)],

        ["-e", ("bkgimg %s, " % picture) +
              "polyeq TOP 0 0",
         "--colormain=%s,%s,%s,200" % (r,g,b),
         "--colorsub=%s,%s,%s,250" % (r,g,b),
         '-q %s' % (resolution),
         "--font=%s" % (font)]
        ]

    return choice(options)

def render_video(text, audio_path):
    print "beginning video render.."

    picture = os.path.realpath(os.path.join(
        PICS_DIR,  choice(os.listdir(PICS_DIR))))
    font = "%s,20" % os.path.realpath(os.path.join(
        FONTS_DIR, choice(os.listdir(FONTS_DIR))))

    splitpoint = randint(0, len(text))

    title = "_" + text[:min(15,splitpoint)]
    subtitle = "_" + text[splitpoint:min(splitpoint+25, len(text))]

    sp_args = (
        ["./Spectrum.py"] +
        mk_rand_arg(picture, font, title, subtitle) +
        ["-r", "1920x1080",
         "-f", OUT_PATH,
         audio_path])

    print sp_args

    subprocess.call(sp_args)

def print_helptext():
    print "usage: %s text_path audio_path output_path" % sys.argv[0]


if __name__ == "__main__":
    seed()
    if len(sys.argv) != 4:
        print_helptext()
        exit(1)

    text_path = sys.argv[1]
    audio_path = sys.argv[2]
    OUT_PATH = sys.argv[3]

    with open(text_path) as t:
        text = t.read().replace(" ", "_").replace("\n", "__")

    render_video(text, audio_path)
