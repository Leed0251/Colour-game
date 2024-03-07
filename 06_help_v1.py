from tkinter import *
from functools import partial # To prevent unwanted windows
import csv
import random

# users choose 3, 5 or 10 rounds
class ChooseRounds:

    def __init__(self):
        # invoke play class with three rounds for testing purposes.
        self.to_play(3)

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

        # Variables used to work out statistics, when game ends etc
        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        # Initially set rounds played and rounds won to 0
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_won = IntVar()
        self.rounds_won.set(0)

        self.quest_frame = Frame(self.play_box,
            padx=10, pady=10
        )
        self.quest_frame.grid()

        self.control_frame = Frame(self.quest_frame)
        self.control_frame.grid(row=6)

        control_buttons = [
            ["#CC6600", "Help", "get help"],
            ["#004C99", "Statistics", "get stats"],
            ["#808080", "Start Over", "start over"]
        ]

        # list to hold references for control buttons
        # so that the text of the 'start over' button
        # can easily be configured when the game is over
        self.control_button_ref = []

        for item in range(0, 3):
            self.make_control_button = Button(self.control_frame,
                fg="#FFFFFF",
                bg=control_buttons[item][0],
                text=control_buttons[item][1],
                width=11, font=("Arial", "12", "bold"),
                command=lambda i=item: self.to_do(control_buttons[i][2])
            )
            self.make_control_button.grid(row=0, column=item, padx=5, pady=5)

            # Add buttons to control list
            self.control_button_ref.append(self.make_control_button)

        self.to_help_btn = self.control_button_ref[0]

    # retrieve colours from csv file
    def get_all_colours(self):
        file = open("00_colour_list_hex_v3.csv", "r")
        var_all_colors = list(csv.reader(file, delimiter=","))
        file.close()

        # removes first entry in list (ie: the heade row).
        var_all_colors.pop(0)
        return var_all_colors

    # randomly choose six colours for buttons
    def get_round_colors(self):
        round_color_list = []
        color_scores = []

        # Get six unique colours
        while len(round_color_list) < 6:
            # choose item
            chosen_colour = random.choice(self.all_colours)
            index_chosen = self.all_colours.index(chosen_colour)

            # check score is not already in list
            if chosen_colour[1] not in color_scores:
                # add item to rounds list
                round_color_list.append(chosen_colour)
                color_scores.append(chosen_colour[1])

                # remove item from master list
                self.all_colours.pop(index_chosen)

        return round_color_list

    def to_compare(self, user_choice):
        how_many = self.rounds_wanted.get()

        # Add one to number of rounds played
        current_round = self.rounds_played.get()
        current_round += 1
        self.rounds_played.set(current_round)

        # deactivate colour buttons!
        for item in self.choice_button_ref:
            item.config(state=DISABLED)

        # set up background colours...
        win_colour = "#D5E8D4"
        lose_colour = "#F8CECC"

        # retrieve user score, make it into an integer
        # and add to list for stats
        user_score_current = int(user_choice[1])
        self.user_scores.append(user_score_current)

        # remove user choice from button colours list
        to_remove = self.button_colours_list.index(user_choice)
        self.button_colours_list.pop(to_remove)

        # get computer choice and add to list for stats
        # when getting score, change it to an integer before appending
        comp_choice = random.choice(self.button_colours_list)
        comp_score_current = int(comp_choice[1])

        self.computer_scores.append(comp_score_current)

        comp_announce = f"The computer chose {comp_choice[0]}"

        self.comp_choice_label.config(
            text=comp_announce,
            bg=comp_choice[0],
            fg=comp_choice[2]
        )

        # Change button colours
        for item in self.choice_button_ref:
            if user_choice[0] != item['text'] and comp_choice[0] != item['text']:
                item.config(bg="#C0C0C0")

        # Get colours and Show results!
        if user_score_current > comp_score_current:
            round_results_bg = win_colour
        else:
            round_results_bg = lose_colour

        rounds_outcome_txt = f"Round {current_round}: User {user_score_current} \tComputer: {comp_score_current}"

        self.round_results_label.config(
            bg=round_results_bg,
            text=rounds_outcome_txt
        )

        # get total scores for user and computer ..
        user_total = sum(self.user_scores)
        comp_total = sum(self.computer_scores)

        if user_total > comp_total:
            self.game_results_label.config(bg=win_colour)
            status = "You Win!"
        else:
            self.game_results_label.config(bg=lose_colour)
            status = "You Lose!"

        game_outcome_txt = f"Total Score: User {user_total} \tComputer: {comp_total}"
        self.game_results_label.config(text=game_outcome_txt)

        # if the game is over, disable all buttons
        # and change text of 'next' button to either
        # 'You Win' or 'You Lose' and disable all buttons

        if current_round == how_many:
            # Change 'next' button to show overall
            # win / loss result and disable it
            self.next_button.config(state=DISABLED, text=status)

            # update 'start over button'
            start_over_button = self.control_button_ref[2]
            start_over_button['text'] = "Play Again"
            start_over_button['bg'] = "#009900"

            # change all colour button background to light grey
            for item in self.choice_button_ref:
                item['bg'] = "#C0C0C0"

        else:
            # enable next round button and update heading
            self.next_button.config(state=NORMAL)

    def new_round(self):
        # disable next button (renable it at the end of the round)
        self.next_button.config(state=DISABLED)

        # empty button list so we can get new colours
        self.button_colours_list.clear()

        # get new colours for buttons
        self.button_colours_list = self.get_round_colors()

        # set button bg, fg and text
        count = 0
        for item in self.choice_button_ref:
            item['fg'] = self.button_colours_list[count][2]
            item['bg'] = self.button_colours_list[count][0]
            item['text'] = f"{self.button_colours_list[count][0]}"
            item['state'] = NORMAL

            count += 1

        # retrieve number of rounds wanted / played and update heading.
        how_many = self.rounds_wanted.get()
        current_round = self.rounds_played.get()
        new_heading = f"Choose - Round {current_round + 1} of {how_many}"
        self.choose_heading.config(text=new_heading)

    # Detects which 'control' button was pressed and
    # invokes necessary function. Can possibly replace functions
    # with calls to classes in this section!
    def to_do(self, action):
        if action == "get help":
            DisplayHelp(self)
        elif action == "get stats":
            pass
        else:
            self.close_play()

    def get_stats(self):
        print("You chose to get the statistics")

    # DON'T USE THIS FUNCTION IN BASE AS IT KILLS THE ROOT
    def close_play(self):
        root.destroy()


# Show users help / game tips
class DisplayHelp:
    def __init__(self, partner):
        # setup dialogue box and background colour
        background = "#ffe6cc"
        self.help_box = Toplevel()

        # disable help button
        partner.to_help_btn.config(state=DISABLED)
        
        # If users press cross at top, closes help and
        # 'releases' help button
        self.help_box.protocol(
            "WM_DELETE_WINDOW",
            partial(self.close_help, partner)
        )

        self.help_frame = Frame(self.help_box, width=300,
            height=200,
            bg=background
        )
        self.help_frame.grid()

        self.help_heading_label = Label(
            self.help_frame,
            bg=background,
            text="Help / Hints",
            font=("Arial", "14", "bold")
        )
        self.help_heading_label.grid(row=0)

        help_text = "Your goal in this game is to beat the computer and you have an advantage - you get to choose your colour first. The points associated with the colours are based on the colour's hex code.\nThe higher the value of the colour the greater your score. To see your statistics, click on the 'Statistics' button.\n\nWin the game by scoring more than the computer overall. Don't be discouraged if you don't win a round, it's your overall score that counts.\n\nGood luck! Choose carefully."
        self.help_text_label = Label(
            self.help_frame,
            bg=background,
            text=help_text,
            wraplength=350,
            justify="left"
        )
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(
            self.help_frame,
            font=("Arial", "12", "bold"),
            text="Dismiss",
            bg="#CC6600",
            fg="#ffffff",
            command=partial(self.close_help, partner)
        )
        self.dismiss_button.grid(row=2, padx=10, pady=10)

    # closes help dialogue (used by button and x at top of dialogue)
    def close_help(self, partner):
        # Put help button back to normal...

        partner.to_help_btn.config(state=NORMAL)
        self.help_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Game")
    ChooseRounds()
    root.mainloop()