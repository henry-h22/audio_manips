Welcome to Henry's Audio Manips!

This project was created as a part of the introductory computer science course at Macalester College, which uses a different file management system than Github.
As such, the purpose of this repository is just to show off the end result of this project.

This project is a simple graphical user interface which allows a user to apply simple effects to most types of audio files (such as .mp3 and .wav files).
The manipulations it can perform are changing the speed, applying a low pass filter (which decreases the t volume of the higher frequencies), normalizing the file (increasing the volume of the quieter parts), and reversing the file.

Before running the program on your computer, there are some requirements you may need to install: <br />
➢ Firstly, you should have Python installed on your machine. <br />
➢ Next, go to your terminal and run this command:
```shell
pip install pydub
```
<br />
  ↳ If that doesn't work, try replacing pip with pip3<br />
➢ The last thing you need to install is ffmpeg, which can be done by following the instructions outlined at <a href=github.com/jiaaro/pydub#getting-ffmpeg-set-up> this link! </a> <br />
➢ Finally, if you have an Apple silicone machine (a Macbook with an M1 or M2 chip), uncomment (delete the # in front of) line 10 of backend.py. <br />
After those steps, you should be ready to use the program! This can be done by simply running main.py. <br />
