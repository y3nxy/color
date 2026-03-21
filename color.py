import time
import shutil
import sys
import os
import signal
import re
import random

bold = "\033[1m"
reset = "\033[0m"

ascii_font = {
    "A":["  ██  "," █  █ ","██████","█    █","█    █","      "],
    "B":["████ ","█   █","████ ","█   █","████ ","     "],
    "C":[" ████","█    ","█    ","█    "," ████","     "],
    "D":["████ ","█   █","█   █","█   █","████ ","     "],
    "E":["█████","█    ","████ ","█    ","█████","     "],
    "F":["█████","█    ","████ ","█    ","█    ","     "],
    "G":[" ████","█    ","█  ██","█   █"," ████","     "],
    "H":["█   █","█   █","█████","█   █","█   █","     "],
    "I":["█████","  █  ","  █  ","  █  ","█████","     "],
    "J":["  ███","   █ ","   █ ","█  █ "," ██  ","     "],
    "K":["█  █","█ █ ","██  ","█ █ ","█  █","     "],
    "L":["█    ","█    ","█    ","█    ","█████","     "],
    "M":["█   █","██ ██","█ █ █","█   █","█   █","     "],
    "N":["█   █","██  █","█ █ █","█  ██","█   █","     "],
    "O":[" ███ ","█   █","█   █","█   █"," ███ ","     "],
    "P":["████ ","█   █","████ ","█    ","█    ","     "],
    "Q":[" ███ ","█   █","█   █","█  █ "," ██ █","     "],
    "R":["████ ","█   █","████ ","█ █  ","█  ██","     "],
    "S":[" ████","█    "," ███ ","    █","████ ","     "],
    "T":["█████","  █  ","  █  ","  █  ","  █  ","     "],
    "U":["█   █","█   █","█   █","█   █"," ███ ","     "],
    "V":["█   █","█   █","█   █"," █ █ ","  █  ","     "],
    "W":["█   █","█   █","█ █ █","██ ██","█   █","     "],
    "X":["█   █"," █ █ ","  █  "," █ █ ","█   █","     "],
    "Y":["█   █"," █ █ ","  █  ","  █  ","  █  ","     "],
    "Z":["█████","   █ ","  █  "," █   ","█████","     "],
    " ":["      ","      ","      ","      ","      ","      "],
    "!":["  █  ","  █  ","  █  ","     ","  █  ","     "],
    "?":[" ███ ","█   █","  ██ ","     ","  █  ","     "],
}

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def exit_cleanly(signum=None, frame=None):
    clear_screen()
    sys.exit(0)

signal.signal(signal.SIGINT, exit_cleanly)

def word_to_ascii(word):
    word = word.upper()
    lines = [""] * 6
    for char in word:
        for i in range(6):
            lines[i] += ascii_font.get(char, ["      "]*6)[i] + "  "
    return lines

def scale_text(lines, term_width, term_height):
    orig_height = len(lines)
    orig_width = max(len(line) for line in lines)
    v_scale = max(1, term_height // orig_height)
    h_scale = max(1, term_width // orig_width)
    scale = min(v_scale, h_scale)

    scaled_lines = []
    for line in lines:
        new_line = "".join(char * scale for char in line)
        for _ in range(scale):
            scaled_lines.append(new_line[:term_width])
    return scaled_lines[:term_height]

def hex_to_ansi(hex_color):
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    return f"\033[38;2;{r};{g};{b}m"

def random_hex():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def animate(scaled, mode):
    try:
        if mode == "rainbow":
            colors = [
                "\033[38;2;255;0;0m",
                "\033[38;2;255;165;0m",
                "\033[38;2;255;255;0m",
                "\033[38;2;0;255;0m",
                "\033[38;2;0;127;255m",
                "\033[38;2;139;0;255m"
            ]
            while True:
                for color in colors:
                    sys.stdout.write("\033[H")
                    for line in scaled:
                        print(color + bold + line + reset)
                    time.sleep(0.2)

        elif mode == "random":
            color = hex_to_ansi(random_hex())
            while True:
                sys.stdout.write("\033[H")
                for line in scaled:
                    print(color + bold + line + reset)
                time.sleep(0.2)

        else:
            color = hex_to_ansi(mode)
            while True:
                sys.stdout.write("\033[H")
                for line in scaled:
                    print(color + bold + line + reset)
                time.sleep(0.2)

    except KeyboardInterrupt:
        exit_cleanly()

# === Main ===
clear_screen()

# take input (prompts will be wiped after)
word = input("Enter text: ")
while True:
    color_input = input("Color (hex / rainbow / random): ").strip().lower()
    if color_input in ["rainbow", "random"] or re.match(r"^#([0-9a-fA-F]{6})$", color_input):
        break

# 🔥 clear everything before showing output
clear_screen()

term_size = shutil.get_terminal_size()
term_width, term_height = term_size.columns, term_size.lines

ascii_lines = word_to_ascii(word)
scaled = scale_text(ascii_lines, term_width, term_height)

animate(scaled, color_input)
