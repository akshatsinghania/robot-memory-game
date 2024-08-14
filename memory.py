from tkinter import messagebox, Tk, Canvas, Label, StringVar
from roboid import HamsterS, wait
import random
import os

hamster = HamsterS()

COLORS = [hamster.COLOR_NAME_RED, hamster.COLOR_NAME_GREEN, hamster.COLOR_NAME_BLUE, hamster.COLOR_NAME_YELLOW]
COLOR_NAMES = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00"] 

sequence = []
player_sequence = []
level = 1
high_score = 0
high_score_file = "high_score.txt"

def load_high_score():
    global high_score
    if os.path.exists(high_score_file):
        with open(high_score_file, "r") as file:
            high_score = int(file.read())
    else:
        high_score = 0

def save_high_score():
    global high_score
    with open(high_score_file, "w") as file:
        file.write(str(high_score))

def display_sequence(seq):
    for color in seq:
        hamster.left_led(color)
        hamster.sound(hamster.SOUND_BEEP)
        wait(500)
        hamster.left_led(hamster.COLOR_NAME_OFF)
        wait(250)

def start_game():
    global level, sequence, player_sequence
    level = 1
    sequence = []
    player_sequence = []
    status_var.set(f"Level {level} | High Score: {high_score}")
    next_level()

def next_level():

    global sequence, player_sequence
    sequence.append(random.choice(COLORS))
    player_sequence = []
    status_var.set(f"Level {level}: Watch the sequence")
    display_sequence(sequence)
    wait(1000)
    status_var.set("Repeat the sequence")

def canvas_click(event):
    color_index = event.widget.color_index
    button_click(COLORS[color_index])

def button_click(color):

    global player_sequence
    player_sequence.append(color)
    if len(player_sequence) == len(sequence):
        check_sequence()

def check_sequence():
    global level, high_score
    if player_sequence == sequence:
        hamster.sound(hamster.SOUND_HAPPY)
        status_var.set("Correct! Level up.")
        level += 1
        if level > high_score:
            high_score = level
            save_high_score()
        wait(1000)
        next_level()
    else:
        hamster.sound(hamster.SOUND_SAD)
        wait(100)
        status_var.set("Incorrect. Game Over!")
        messagebox.showinfo("Game Over", f"You lose! Your score: {level}. High Score: {high_score}")
        reset_game()

def reset_game():
    global level, sequence
    level = 1
    sequence = []
    player_sequence = []
    status_var.set(f"Press White Button to begin | High Score: {high_score}")

root = Tk()
root.title("Memory Game")

status_var = StringVar()

load_high_score()
status_var.set(f"Press White Button to begin | High Score: {high_score}")


status_label = Label(root, textvariable=status_var)
status_label.pack(pady=10)

canvas_list = []
for i, hex_code in enumerate(COLOR_NAMES):
    canvas = Canvas(root, width=100, height=100, bg=hex_code, highlightthickness=0)
    canvas.color_index = i
    canvas.bind("<Button-1>", canvas_click)
    canvas.pack(side='left', padx=5, pady=5)
    canvas_list.append(canvas)

start_button = Label(root, text="Start", bg="white", relief="raised", width=10, height=2, cursor="hand2")
start_button.bind("<Button-1>", lambda event: start_game())
start_button.pack(pady=20)


root.mainloop()
