# backend.py
# Henry Heyden
# Comp 123-04
# The purpose of this file is to define various helper functions for frontend.py. Functions present on this file either
# deal with accessing files on the user's drive or with mathematical functions that would've made frontend.py
# unnecessarily dense.

from pydub import AudioSegment

# AudioSegment.converter = '/opt/homebrew/bin/ffmpeg'
# the above line tells pydub where to look for ffmpeg; it is only necessary on m1 or m2 chip apple machines


def create_audio_object(filepath: str):
    """Function receives a file path as a string and returns a pydub AudioSegment object"""
    try:
        return AudioSegment.from_file(filepath)
    except Exception:  # Sorry we have to use except Exception here, pydub and ffmpeg don't raise normal errors. :(
        print('invalid file :/')
        return 1


def export_audio_object(clip: AudioSegment, filepath, filename: str):
    """Function receives an AudioSegment object (clip), a filepath, and a filename (probably given by the gui),
    then exports the AudioSegment to the designated location.
    Note that when called within AudioGUI we use tk.filedialog.askdirectory() as the filepath arg. :)"""
    filepath += '/' + filename + '.mp3'
    # print(filepath) This was here for testing.
    clip.export(filepath)


def coord_to_freq(coordinate: int):
    """Function receives an x coordinate on the low pass filter visualizer canvas and returns the corresponding
    frequency based on a function that maps the coordinates to the frequencies."""
    return ((coordinate / 22) ** 4) + 10


def freq_to_coord(frequency: float):
    """Inverse function to coord_to_freq."""
    return 22 * ((frequency - 10)**(1/4))


def slope_calc(x1: float):
    """A recursive function that receives a frequency and returns the y coordinate of the right side of the line that
     visualizes the low pass filter on the lpf canvas.
     The low pass filter from pydub cuts 6db of volume per octave, and a recursive function seemed like the easiest
     way to handle that."""
    db_per_coordinate = 2  # this is defined separately to facilitate visual experimentation; 2 looks pretty good
    if x1 >= 10378:  # coord_to_freq of the right side of the canvas
        return 6
    else:
        return (6 * db_per_coordinate) + slope_calc(2 * x1)


if __name__ == '__main__':
    # The functions create_audio_segment and export_audio_object are called within methods of the AudioGUI object
    # defined in frontend.py, and were tested through the GUI.

    # Test calls for the three functions that help with the low pass filter visualization canvas:
    assert int(coord_to_freq(20)) == 10
    assert int(freq_to_coord(10000)) == 219
    assert slope_calc(1000) == 54

    # Test calls for various methods for pydub's AudioSegment method:
    # IMPORTANT: when running the following tests, line 27 of this file was modified so that the export_audio_object
    # method didn't add '/' to the beginning of the filepath variable, so that we can save the file to the same
    # directory as the project itself. If running these tests, make sure that you perform that modification too. :)
    test_file = 'misty.wav'
    test_audio_segment = create_audio_object(test_file)
    if test_audio_segment != 1:  # this tests that create_audio_object functioned properly
        export_audio_object(test_audio_segment.speedup(playback_speed=1.5, chunk_size=100), '', 'speed_test')
        export_audio_object(test_audio_segment.low_pass_filter(4000), '', 'lowpass_test')
        export_audio_object(test_audio_segment.normalize(0.2), '', 'normalize_test')
        export_audio_object(test_audio_segment.reverse(), '', 'reverse_test')
    elif test_audio_segment == 1:
        print('create_audio_object failed test :( \nmake sure test_file (i.e. misty.wav) exists in the same directory'
              'as the project code')
