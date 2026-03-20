import time
import shutil
import sys
import os
import signal
import re

bold = "\033[1m"
reset = "\033[0m"

# 3D-style font
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
    # Clears terminal; Termux works as normal Linux
    os.system("cls" if os.name == "nt" else "clear")

def exit_cleanly(signum=None, frame=None):
    clear_screen()
    sys.exit(0)

# Catch Ctrl+C on any platform
signal.signal(signal.SIGINT, exit_cleanly)

def word_to_ascii(word):
    word = word.upper()
    lines = [""] * 6
    for char in word:
        if char in ascii_font:
            for i in range(6):
                lines[i] += ascii_font[char][i] + "  "
        else:
            for i in range(6):
                lines[i] += "      "
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

def parse_color_input(color_input):
    color_input = color_input.strip().lower()
    if color_input == "rainbow":
        return "rainbow"
    predefined = {"red":"\033[91m","yellow":"\033[93m","green":"\033[92m","blue":"\033[94m"}
    if color_input in predefined:
        return predefined[color_input]
    if re.match(r"^#([0-9A-Fa-f]{6})$", color_input):
        r = int(color_input[1:3], 16)
        g = int(color_input[3:5], 16)
        b = int(color_input[5:7], 16)
        return f"\033[38;2;{r};{g};{b}m"
    if color_input.isdigit():
        n = int(color_input)
        if 0 <= n <= 255:
            return f"\033[38;5;{n}m"
    return "\033[97m"  # fallback white

def animate(scaled, color_input):
    try:
        if color_input == "rainbow":
            colors = ["\033[91m","\033[93m","\033[92m","\033[96m","\033[94m","\033[95m"]
            while True:
                for color in colors:
                    sys.stdout.write("\033[H")
                    for line in scaled:
                        print(color + bold + line + reset)
                    time.sleep(0.2)
        else:
            color_code = color_input
            while True:
                sys.stdout.write("\033[H")
                for line in scaled:
                    print(color_code + bold + line + reset)
                time.sleep(0.2)
    except KeyboardInterrupt:
        exit_cleanly()

# === Main ===
clear_screen()  # Clear first
word = input("Enter any text to print: ")

color_input = ""
while True:
    color_input = input(
        "Choose color (red/yellow/green/blue/hex like #FF00FF/rainbow): "
    ).strip()
    if color_input.lower() in ["red","yellow","green","blue","rainbow"] or re.match(r"^#([0-9A-Fa-f]{6})$", color_input) or color_input.isdigit():
        break
color_choice = parse_color_input(color_input)

term_size = shutil.get_terminal_size()
term_width, term_height = term_size.columns, term_size.lines

ascii_lines = word_to_ascii(word)
scaled = scale_text(ascii_lines, term_width, term_height)

animate(scaled, color_choice)
