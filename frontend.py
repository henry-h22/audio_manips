# frontend.py
# Henry Heyden
# Comp 123-04
# The purpose of this file is to define the GUI and handle every action that the user can perform on the GUI.
# Methods are generally written in the order in which they will probably be called chronologically.
# Every method besides the constructor and .run() will be called by the user via button presses.

import tkinter as tk
from tkinter import filedialog
import backend
import math


class AudioGUI:

    def __init__(self):
        """Initializes the GUI, creating the header and the file select button."""
        self.mainWin = tk.Tk()
        self.mainWin.title("Henry's Audio Manips")
        self.mainWin.iconphoto(False, tk.PhotoImage(file='icon.png'))
        self.mainWin.config(bg='Black')
        tk.Label(
            text="Henry's Audio Manips",
            fg="medium turquoise",
            bg="gray1",
            width=25,
            height=1,
            font=('Impact', -69, 'bold')
        ).grid(row=0, column=0, columnspan=2)

        self.file_collector_button = tk.Button(
            text="Pick a File!",
            width=22,
            height=1,
            fg="black",
            font=('Times', -40, 'bold'),
            borderwidth=6,
            command=self.file_select)
        self.file_collector_button.grid(row=1, column=0, columnspan=2)

    def run(self):
        """Shows the GUI."""

        self.mainWin.mainloop()

    def file_select(self):
        """Allows the user to select a file to modify. Run from a button press within tkinter so returning something
        would be pointless, instead modifies object variable audioFile.
        Following a successful creation of the audio object audioFile, function creates the rest of the GUI (checkboxes,
        text boxes, etc)."""
        filename = filedialog.askopenfilename(title="Select an Audio File",
                                              filetypes=(("Audio Files", ["*.wav", "*.mp3", "*.ogg"]),
                                                         ("all files", "*.")))

        self.audioFile = backend.create_audio_object(filename)

        # backend's create_audio_object function returns 1 if something goes wrong. so this if statement makes sure
        # that if something goes wrong within that function, nothing happens visually.
        if self.audioFile != 1:
            self.file_collector_button.destroy()

            # creating speed effect portion of the gui
            speed_frame = tk.Frame(padx=10, pady=10, bd=2, bg='Black', relief=tk.GROOVE)
            speed_frame.grid(row=2, column=0, rowspan=2)

            self.speed_bool = tk.IntVar()  # This line initializes the variable for the speed checkbox.
            tk.Checkbutton(speed_frame, text='Speed Up', variable=self.speed_bool, bg='Black', fg='White',
                           font=('Times', -40, 'bold'), width=20, height=2).grid(row=0, column=0, columnspan=2)

            tk.Label(speed_frame, text='Scale:', font=('Times', -22, 'bold'), bg='Black', fg='White',
                     height=4).grid(row=1, column=0)

            self.speed_box = tk.Entry(speed_frame, fg='black', bg='light cyan', width=11, font=('Times', -40))
            self.speed_box.insert(0, '1.5')
            self.speed_box.grid(row=1, column=1)

            # creating low pass filter portion of the gui
            lpf_frame = tk.Frame(width=100000, padx=10, pady=10, bd=2, bg='Black', relief=tk.GROOVE)
            lpf_frame.grid(row=2, column=1, rowspan=3)
            self.lpf_bool = tk.IntVar()
            tk.Checkbutton(lpf_frame, text='Low Pass Filter', variable=self.lpf_bool, bg='Black', fg='White',
                           font=('Times', -40, 'bold'), width=15, height=2).grid(row=0, column=0, columnspan=3)
            tk.Label(lpf_frame, text='Cutoff Freq.:', font=('Times', -22, 'bold'), bg='Black', fg='White',
                     height=2).grid(row=1, column=0)
            self.lpf_box = tk.Entry(lpf_frame, fg='black', bg='light cyan', width=11, font=('Times', -40))
            self.lpf_box.insert(0, '4000')
            self.lpf_box.bind('<Return>', self.lpf_enter)
            self.lpf_box.grid(row=1, column=1)
            tk.Label(lpf_frame, text='Hz', font=('Times', -22, 'bold'), bg='Black', fg='White',
                     width=4, height=2).grid(row=1, column=2)

            self.lpf_canvas = tk.Canvas(lpf_frame, bg='medium turquoise', width=222, height=111)
            self.lpf_canvas.grid(row=2, column=0, columnspan=3)
            self.lpf_canvas.bind('<Button-1>', self.lpf_click)
            self.lpf_canvas.create_line(0, 36, backend.freq_to_coord(4000), 36, fill='blue')
            self.lpf_canvas.create_line(backend.freq_to_coord(4000), 36, 222, 36 + backend.slope_calc(4000),
                                        fill='blue')

            # creating normalization portion of the gui
            norm_frame = tk.Frame(padx=10, pady=10, bd=2, bg='Black', relief=tk.GROOVE)
            norm_frame.grid(row=4, column=0, rowspan=2)

            self.norm_bool = tk.IntVar()  # This line initializes the variable for the norm checkbox.
            tk.Checkbutton(norm_frame, text='Normalize', variable=self.norm_bool, bg='Black', fg='White',
                           font=('Times', -40, 'bold'), width=20, height=2).grid(row=0, column=0, columnspan=3)

            tk.Label(norm_frame, text='Headroom:', font=('Times', -22, 'bold'), bg='Black', fg='White',
                     height=4).grid(row=1, column=0)
            self.norm_box = tk.Entry(norm_frame, fg='black', bg='light cyan', width=11, font=('Times', -40))
            self.norm_box.insert(0, '0.2')
            self.norm_box.grid(row=1, column=1)
            tk.Label(norm_frame, text='dB:', font=('Times', -22, 'bold'), bg='Black', fg='White',
                     height=4).grid(row=1, column=2)

            # creating reverse effect portion of the gui
            rev_frame = tk.Frame(padx=10, pady=10, bd=2, bg='Black', relief=tk.GROOVE)
            rev_frame.grid(row=5, column=1, rowspan=1)
            self.rev_bool = tk.IntVar()
            tk.Checkbutton(rev_frame, text='Reverse', variable=self.rev_bool, bg='Black', fg='White',
                           font=('Times', -40, 'bold'), width=20, height=3).pack()

            tk.Button(
                text="Generate!",
                width=11,
                height=1,
                bg="medium turquoise",
                fg="black",
                font=('Times', -40, 'bold'),
                borderwidth=6,
                command=self.generate).grid(row=6, column=0, columnspan=2)

    def lpf_click(self, event):
        """Function called when the low pass filter visualizer canvas is clicked, handles changing the cutoff frequency
        to the value defined by where the user clicks the canvas, and updating the canvas."""
        cutoff = backend.coord_to_freq(event.x)
        cutoff = cutoff if cutoff <= 10378 else 10378
        self.lpf_box.delete(0, 22)
        self.lpf_box.insert(0, str(math.ceil(cutoff)))

        self.lpf_canvas.create_rectangle(0, 0, 1000, 1000, fill=self.lpf_canvas['bg'])  # clears the canvas lol
        self.lpf_canvas.create_line(0, 36, backend.freq_to_coord(cutoff), 36, fill='blue')
        self.lpf_canvas.create_line(backend.freq_to_coord(cutoff), 36, 222, 36 + backend.slope_calc(cutoff),
                                    fill='blue')

    def lpf_enter(self, event):
        """Function called when pressing enter after a new cutoff frequency is typed into the lpf textbox.
        Takes the new cutoff frequency and updates the visualization canvas. If the typed cutoff freq. isn't a valid
        integer, function puts the default value back in the box."""
        try:
            assert float(self.lpf_box.get()) >= 10
            cutoff = int(self.lpf_box.get())
        except AssertionError:  # for if the frequency is too low
            cutoff = 10
            self.lpf_box.delete(0, 22)
            self.lpf_box.insert(0, '10')
        except ValueError:
            cutoff = 4000
            self.lpf_box.delete(0, 22)
            self.lpf_box.insert(0, '4000')
        self.lpf_canvas.create_rectangle(0, 0, 1000, 1000, fill=self.lpf_canvas['bg'])  # clears the canvas
        self.lpf_canvas.create_line(0, 36, backend.freq_to_coord(cutoff), 36, fill='blue')
        self.lpf_canvas.create_line(backend.freq_to_coord(cutoff), 36, 222, 36 + backend.slope_calc(cutoff),
                                    fill='blue')

    def generate(self):
        """Function looks at all four checkboxes and does the corresponding manipulations to the audioFile variable
        before calling backend.export_audio_object to export the file as an .mp3. Function then closes the window."""
        if self.speed_bool.get() == 1:
            print('speed Text: ', self.speed_box.get())
            try:
                assert float(self.speed_box.get()) != 0
                speed_scale = abs(float(self.speed_box.get()))
            except AssertionError:
                print('0 was given as scale (that is not good); using default value 1.5 instead.')
                speed_scale = 1.5
            except ValueError:
                print('invalid speed scale value given:' + str(self.speed_box.get()) +
                      ' using default value 1.5 instead.')
                speed_scale = 1.5
            print('Speed Scale:', speed_scale)
            self.audioFile = self.audioFile.speedup(playback_speed=speed_scale, chunk_size=100)

        if self.lpf_bool.get() == 1:
            print('lpf Text:', self.lpf_box.get())
            try:
                assert float(self.lpf_box.get()) >= 10
                lpf_cutoff = float(self.lpf_box.get())
            except AssertionError:
                print('a number less than 10 was given for cutoff frequency :/ setting it to 4 kHz')
                lpf_cutoff = 4000
            except ValueError:
                print('invalid low pass cutoff value given: ', self.lpf_box.get(),
                      'using default value 4kHz instead.')
                lpf_cutoff = 4000
            print('Low Pass Filter Cutoff:', lpf_cutoff)
            self.audioFile = self.audioFile.low_pass_filter(lpf_cutoff)

        if self.norm_bool.get() == 1:
            print('norm Text:', self.norm_box.get())
            try:
                assert float(self.norm_box.get()) >= 0
                headroom = float(self.norm_box.get())
            except AssertionError:
                print('given headroom value is less than 0, using default value 0.2 db')
                headroom = 0.2
            except ValueError:
                print('invalid headroom value given: ', self.norm_box.get(), 'using default value 0.2 db')
                headroom = 0.2
            self.audioFile = self.audioFile.normalize(headroom)

        if self.rev_bool.get() == 1:
            print('file reversed!')
            self.audioFile = self.audioFile.reverse()

        while True:
            # we do a try/except loop here to make sure that the file is successfully exported before we destroy the gui
            # this way of doing this means that the user can't cancel generation if they mouse slip, which isn't great
            try:
                backend.export_audio_object(self.audioFile, filedialog.askdirectory(), 'new_file')
                self.mainWin.destroy()
                break
            except OSError:
                pass


if __name__ == '__main__':
    # Every method of our AudioGUI object was tested by running the program, because it's a GUI.
    window = AudioGUI()
    window.run()
