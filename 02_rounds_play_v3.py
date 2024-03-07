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

        btn_color_value = [
            ["#CC0000", 3],
            ["#009900", 5],
            ["#CC0099", 10]
        ]

        for item in range(0, 3):
            self.rounds_button = Button(self.how_many_frame,
                fg=button_fg,
                bg=btn_color_value[item][0],
                text=f"{btn_color_value[item][1]} Rounds",
                font=button_font,
                width=10,
                command=lambda i=item: self.to_play(btn_color_value[i][1])
            )
            self.rounds_button.grid(row=0, column=item,
                padx=5, pady=5
            )


    def to_play(self, num_rounds):
        Play(num_rounds)

        # Hide root window (ie: hide rounds choice window).
        root.withdraw()

class Play:

    def __init__(self, how_many):
        self.play_box = Toplevel()

        # If users press cross at top, closes help and releases help button
        self.play_box.protocol('WM_DELETE_WINDOW',
            partial(self.close_play)
        )

        self.quest_frame = Frame(self.play_box,
            padx=10, pady=10
        )
        self.quest_frame.grid()

        rounds_heading = f"Choose - Round 1 of {how_many}"
        self.choose_heading = Label(self.quest_frame,
            text=rounds_heading,
            font=("Arial", "16", "bold")
        )
        self.choose_heading.grid(row=0)

        self.control_frame = Frame(self.quest_frame)
        self.control_frame.grid(row=6)

        self.start_over_button = Button(self.control_frame,
            text="Start Over",
            command=self.close_play
        )
        self.start_over_button.grid(row=0, column=2)

    def close_play(self):
        # reshow root (ie: choose rounds) and end current game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    ChooseRounds()
    root.mainloop