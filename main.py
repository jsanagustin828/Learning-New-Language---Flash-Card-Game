from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
words_to_learn = {}

# ------------------------- Functionality ------------------- #

try:
    data = pd.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("./data/french_words.csv")
    words_to_learn = original_data.to_dict(orient="records")
else:
    words_to_learn = data.to_dict(orient="records")


def is_known():
    words_to_learn.remove(current_card)
    data = pd.DataFrame(words_to_learn)
    data.to_csv("./data/words_to_learn.csv", index=False)
    next_card()


def next_card():
    global current_card, timer
    window.after_cancel(timer)
    current_card = random.choice(words_to_learn)
    random_french_word = current_card['French']
    canvas.itemconfig(card_image, image=card_front)
    canvas.itemconfig(card_word, text=random_french_word, fill="black")
    canvas.itemconfig(card_title, text="French", fill="black")
    timer = window.after(3000, flip_card)


def flip_card():
    global current_card
    english_word = current_card['English']
    canvas.itemconfig(card_image, image=card_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=english_word, fill="white")


# ---------------------------- UI ------------------------- #

# Window
window = Tk()
window.title("Flash Card Game")
window.configure(padx=50, pady=50, bg=BACKGROUND_COLOR)

timer = window.after(3000, func=flip_card)

# Canvas
canvas = Canvas(width=800, height=526)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 156, text="", fill="black", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 280, text="", fill="black", font=("Arial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

# Red Button
red_btn_img = PhotoImage(file="./images/wrong.png")
red_btn = Button(image=red_btn_img, highlightthickness=0, command=next_card)
red_btn.grid(column=0, row=1)

# Green Button
green_btn_img = PhotoImage(file="./images/right.png")
green_btn = Button(image=green_btn_img, highlightthickness=0, command=is_known)
green_btn.grid(column=1, row=1)

next_card()
window.mainloop()
