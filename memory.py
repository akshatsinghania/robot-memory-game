from tkinter import *
from roboid import HamsterS, wait
import random


hamster = HamsterS()


COLORS = [hamster.COLOR_NAME_RED, hamster.COLOR_NAME_GREEN, hamster.COLOR_NAME_BLUE, hamster.COLOR_NAME_YELLOW]
COLOR_NAMES = ["Red", "Green", "Blue", "Yellow"]


sequence = []
player_sequence = []
level = 1

def display_sequence(seq):
    for color in seq:
        hamster.left_led(color)
        wait(500)
        hamster.left_led(hamster.COLOR_NAME_OFF)
        wait(250)

def start_game():

    global level, sequence, player_sequence
    level = 1
    sequence = []
    player_sequence = []
    next_level()

def next_level():

    global sequence, player_sequence
    sequence.append(random.choice(COLORS))
    player_sequence = []
    status_var.set(f"Level {level}: Watch the sequence")
    display_sequence(sequence)
    wait(1000)  
    status_var.set("Repeat the sequence")

def button_click(color):

    global player_sequence
    player_sequence.append(color)
    if len(player_sequence) == len(sequence):
        check_sequence()

def check_sequence():

    if player_sequence == sequence:
        status_var.set("Correct! Level up.")
        global level
        level += 1
        wait(1000)
        next_level()
    else:
        status_var.set("Incorrect. Game Over!")
        messagebox.showinfo("Game Over", "You lose! Try again.")
        reset_game()

def reset_game():

    global level, sequence
    level = 1
    sequence = []
    player_sequence = []
    status_var.set("Press 'Start' to begin")


root = Tk()
root.title("Memory Game")


status_var = StringVar()
status_var.set("Press 'Start' to begin")
status_label = Label(root, textvariable=status_var)
status_label.pack(pady=10)


for color, name in zip(COLORS, COLOR_NAMES):
    button = Button(root, text=name, bg=color.lower(), command=lambda c=color: button_click(c))
    button.pack(side='left', padx=5, pady=5)


start_button = Button(root, text="Start", command=start_game)
start_button.pack(pady=20)


root.mainloop()
