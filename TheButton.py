from tkinter import *
import tkinter as Tk
from PIL import Image, ImageTk
import pygame
import random

def check_for_invalid_click_amounts(): # Only checks the current click amounts, not the best/total amount(s).
    with open("clicks.txt", "r+") as clicks_reader:
        amount = int(clicks_reader.read().strip())
        if int(amount) < 0 or int(amount) > 100:
            print("Invalid number detected, fixing.")
            clicks_reader.seek(0)
            clicks_reader.write("0")
            clicks_reader.truncate()
            clicks_reader.close()

def new_pb_check(current_clicks):
    with open("best_amt_of_clicks.txt", "r+") as f:
        best_amount_of_clicks_count = int(f.read().strip())
        if current_clicks > best_amount_of_clicks_count:
            best_amount_of_clicks = current_clicks
            f.seek(0)
            f.write(str(best_amount_of_clicks))
            f.truncate()
            f.close()

def update_button(): # Called this because it was originally going to be a label on a button but that's difficult in Tkinter because of label backgrounds and stuff. Might implement it one day.
    with open("clicks.txt", "r") as clicks_reader:
        amount_of_clicks.set(f"Current clicks: {clicks_reader.read().strip()}")
    with open("total_clicks.txt", "r") as total_clicks_reader:
        total_amount_of_clicks.set(f"Total clicks: {total_clicks_reader.read().strip()}")
    with open("best_amt_of_clicks.txt", "r") as best_amt_of_clicks_reader:
        # Yes this does set it for every click but eh whatever.
        best_amount_of_clicks.set(f"Best: {best_amt_of_clicks_reader.read().strip()}")
    window.after(75, update_button)

pygame.mixer.init() # Initialising Pygame to play sound(s)

background_music = pygame.mixer.Sound("background_music.mp3")
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.Channel(3).play(background_music, loops=-1)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(1)

button_clickable = True

def set_button_clickable(value):
    global button_clickable
    button_clickable = value

def add_click():
    global button_clickable
    if button_clickable:
        #pygame.mixer.music.load("button_click.mp3")
        #pygame.mixer.music.play(loops=0)
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('button_click.mp3'))
        with open("clicks.txt", "r+") as f:
            amount_of_clicks = int(f.read().strip())
            amount_of_clicks += 1
            f.seek(0)
            f.write(str(amount_of_clicks))
            f.close()
        with open("total_clicks.txt", "r+") as f:
            total_amount_of_clicks = int(f.read().strip())
            total_amount_of_clicks += 1
            f.seek(0)
            f.write(str(total_amount_of_clicks))
            f.close()

        new_pb_check(current_clicks=amount_of_clicks)
        set_button_clickable(False)
        window.after(600, lambda: set_button_clickable(True))
        reset_counter()

def reset_counter():
    with open("clicks.txt", "r") as f:
        percentage_chance = int(f.read().strip())
        f.close()

    if reset_check(percentage_chance):
        print("Unlucky! Resetting counter!")
        with open("clicks.txt", "r+") as resetter:
            amount_of_clicks = int(resetter.read().strip())
            amount_of_clicks = 0
            resetter.seek(0)
            resetter.write(str(amount_of_clicks))
            resetter.truncate()
            resetter.close()
            pygame.mixer.music.load("KABOOM.mp3")
            pygame.mixer.Channel(2).play(pygame.mixer.Sound("KABOOM.mp3"))
    else:
        print("Lucky! Keeping counter as it should be.")

def reset_check(chance):
    # Ensuring the chance is between 0 and 100
    chance = max(0, min(100, chance))

    # Generating the random number to choose if the click counter should reset.
    random_number = random.randint(0, 100)

    # Check if it's less than or equal to the given percentage chance
    return random_number <= chance

alternating_text = [
    "THE BUTTON clone, by Slender the Blender, inspired\nby Elendow's THE BUTTON game.",
    "This is some text.",
    "Press the button once more. You know you want to.",
    "You should probably play the real version of this.\nMuch better than this version.",
    "Life is button. Button is life.",
    "There is no escape from the button.\nThe button knows where you are...",
    "Don't be scared of the button, it can't hurt you.",
    "Mum, can I get THE BUTTON?\nNo, we have THE BUTTON at home.\nTHE BUTTON at home:",
    "Use an autoclicker, nobody will know!\nSeriously, I would never know how to make the game check.",
    "Just ignore the ugly visual mishaps.\nPretend they don't exist.",
    "FUN FACT: Cows have best friends!\nMaybe me and you could be besties!",
    "Yes, the button above is indeed an image taken off Google.",
    "Maybe I could code THE BUTTON into a Discord bot!\nNow that's an idea I definitely want to put action to one day.",
    "FUN FACT: Bananas are berries but strawberries are not. Wow!",
    "Is water wet?",
    "Is a tomato a fruit?",
    "If a tomato is a fruit, does that mean ketchup is a smoothie?",
    "Coded by Slend, using a bit of Google...\n...and a small bit of ChatGPT.",
    "This button... why was it ever made?",
    "I'm surprised all this fit into only (insert number here) lines!", # might leave it like that for the memes (and because im lazy)
    "Why was Cinderalla so bad at football?\nShe kept running away from the ball.",
    "What did the horse say after it tripped?\nHelp, I've fallen and I can't giddyup!",
    "What do you call an angry carrot?\nA steamed veggie!",
    "How do you make an eggroll?\nYou push it!"
]

def update_changing_label_text():
    new_text = random.choice(alternating_text)
    changing_text_label.config(text=new_text)
    window.after(7500, update_changing_label_text)

bgcolour = "#f2e5d9"

window = Tk.Tk()
window.geometry("640x650")
window.title("THE BUTTON Clone")
window.config(bg=bgcolour)
window.resizable(False, False)
window.unbind_class("Button", "<Key-space>")
icon = Image.open("button_main_image.png")
icon_photo = ImageTk.PhotoImage(icon)
window.wm_iconphoto(False, icon_photo)

header = Tk.Label(window, text="THE BUTTON Clone", font=("Century Gothic", "32", "underline"), bg=bgcolour)
header.pack(pady=2)

amount_of_clicks = Tk.StringVar()
total_amount_of_clicks = Tk.StringVar()
best_amount_of_clicks = Tk.StringVar()

with open("clicks.txt", "r") as clicks_reader:                  # These might be redundant
    amount_of_clicks.set(int(clicks_reader.read()))             # but I'm keeping them
with open("total_clicks.txt", "r") as total_clicks_reader:      # just in case they're
    total_amount_of_clicks.set(int(total_clicks_reader.read())) # needed lol, we'll see

image_filepath = "button_main_image.png"
image = Image.open(image_filepath)
main_button_photo = ImageTk.PhotoImage(image)

# mainbutton = Tk.Button(window, textvariable=amount_of_clicks, image=PhotoImage("C:\\Users\\kyleo\\OneDrive\\Documents\\Desktop\\VS Code\\!Things I Coded or Am Coding\\Python\\Games\\THE BUTTON Clone\\button_main_image.png"), command=add_click) # change filepath to that which is stored on the usb when you can
mainbutton = Tk.Button(window, textvariable=amount_of_clicks, image=main_button_photo, command=add_click, bg=bgcolour, state="normal") # change filepath to that which is stored on the usb when you can
mainbutton.place(x="320", y="395", anchor="center")

amt_of_clicks_label = Tk.Label(window, textvariable=amount_of_clicks, font=("Century Gothic", "40", "bold", "italic"), bg=bgcolour)
amt_of_clicks_label.place(x="320", y="90", anchor="center")

total_amt_of_clicks_label = Tk.Label(window, textvariable=total_amount_of_clicks, font=("Century Gothic", "30"), bg=bgcolour)
total_amt_of_clicks_label.place(x="320", y="150", anchor="center")

best_amt_of_clicks_label = Tk.Label(window, textvariable=best_amount_of_clicks, font=("Century Gothic", "30"), bg=bgcolour)
best_amt_of_clicks_label.place(x="320", y="200", anchor="center")

changing_text_label = Tk.Label(window, text="THIS IS A TEST", font=("Century Gothic", "16"), bg=bgcolour) # why does this say "THIS IS A TEST"? idk, it works though so im not touching it.
changing_text_label.place(x="320", y="592.5", anchor="center") # decimal y value because 2.5 is cooler than 3

update_button()
check_for_invalid_click_amounts()
window.after(0, update_changing_label_text)

window.mainloop()