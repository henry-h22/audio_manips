# main.py
# Henry Heyden
# Comp 123-04
# The purpose of this file is to be a hyper-legible script that can be run to start the program.
from frontend import *

"""
~~ DEPENDENCIES ~~

    - install pydub with pip
    - install ffmpeg using the instructions here https://github.com/jiaaro/pydub#getting-ffmpeg-set-up

    - If you're using an apple silicone macbook (M1 or M2 chip), uncomment the tenth line of backend.py

"""

"""
    - Known issue: weird CATransaction synchronize garbage being printed. Occurs whenever the file dialog is present.
      Not 100% sure what causes it, but it should be okay to ignore it.
"""


if __name__ == '__main__':
    window = AudioGUI()
    window.run()
