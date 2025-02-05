import os
import random

# File system paths for reading images
FS_LETTER_SETS_DIR = "../client/public/images/letters"

# Public URLs for the HTML output
PUBLIC_LETTER_SETS_DIR = "/images/letters"
PUBLIC_BACKGROUND_IMAGE = "/images/background.png"

OUTPUT_FILE = "output.html"
INPUT_FILE = "input.txt"

LETTER_COLORS = ("blue", "black")
CHAR_HEIGHT = 25
CHAR_WIDTH = 15
CHAR_MARGIN_TOP = 5
CHAR_MARGIN_BOTTOM = 10

HTML_HEADER = [
    "<html>",
    "<head>",
    "<style>",
    ".lines { width: 100%; height: auto; float: left; }",
    f"#paper {{ background: white; background-image: url('{PUBLIC_BACKGROUND_IMAGE}'); height: auto; float: left; padding: 50px 50px; width: 90%; }}",
    f"img, span {{ height: {CHAR_HEIGHT}px; width: {CHAR_WIDTH}px; float: left; margin-top: {CHAR_MARGIN_TOP}px; margin-bottom: {CHAR_MARGIN_BOTTOM}px; }}",
    ".clblack { filter: brightness(30%); }",
    ".clblue { filter: brightness(100%); }",
    "</style>",
    "</head>",
    "<body>",
    "<div id='paper'>",
]

def process_line(line, letter_set_count):
    html_content = ['<div class="lines">']
    current_color = "blue"
    toggle_color = False
    for char in line.strip():
        char_code = ord(char)
        if char_code == 35:  # '#'
            current_color = LETTER_COLORS[toggle_color]
            toggle_color = not toggle_color
        elif char_code in (32, 36):  # ' ' or '$'
            html_content.append("<span></span>")
        else:
            letter_set = f"set{random.randint(1, letter_set_count)}"
            html_content.append(f"<img src='{PUBLIC_LETTER_SETS_DIR}/{letter_set}/{current_color}/{char_code}.png'/>")
    html_content.append("</div>")
    return html_content

def generate_output():
    try:
        letter_set_count = len(os.listdir(FS_LETTER_SETS_DIR))
        with open(INPUT_FILE, "r") as file:
            lines = file.readlines()

        with open(OUTPUT_FILE, "w") as file:
            file.write("\n".join(HTML_HEADER))
            for line in lines:
                file.write("\n".join(process_line(line, letter_set_count)))
            file.write("\n</div></body></html>")
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found.")

generate_output()
