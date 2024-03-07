from tkinter import *
from functools import partial

class ChooseRounds:

    def __init__(self):
        button_fg = "#FFF"
        button_font = ("Arial", "13", "bold")

        # Set up GUI Frame
        self.intro_frame = Frame(padx=10, pady=10)
        self.intro_frame.grid()

        # heading and brief instructions
        self.intro_heading_label = Label(self.intro_frame,
            text="Colour Quest",
            font=("Arial", "16", "bold")
        )
        self.intro_heading_label.grid(row=0)

        choose_instructions_txt = "In each round you will be given six different colours to choose from. Pick a colour and see if you can beat the computers score!\n\nTo begin, choose how many rounds you'd like to play..."
        self.choose_instructions_label = Label(self.intro_frame,
            text=choose_instructions_txt,
            wraplength=300,
            justify="left"
        )
        self.choose_instructions_label.grid(row=1)

        # Rounds buttons...
        self.how_many_frame = Frame(self.intro_frame)
        self.how_many_frame.grid(row=2)

        self.three_button = Button(self.how_many_frame,
            fg=button_fg,
            bg="#C00",
            text="3 Rounds",
            font=button_font,
            width=10
        )
        self.three_button.grid(row=0, column=0, padx=5, pady=5)

        self.five_button = Button(self.how_many_frame,
            fg=button_fg,
            bg="#090",
            text="5 Rounds",
            font=button_font,
            width=10
        )
        self.five_button.grid(row=0, column=1, padx=5, pady=5)

        self.ten_button = Button(self.how_many_frame,
            fg=button_fg,
            bg="#009",
            text="10 Rounds",
            font=button_font, width=10
        )
        self.ten_button.grid(row=0, column=2, padx=5, pady=5)
        