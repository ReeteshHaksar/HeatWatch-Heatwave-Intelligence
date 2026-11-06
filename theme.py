PAGE = "#232744"
PAGE_MID = "#282c49"
PAGE_LOW = "#4b4c63"
SIDEBAR = "#1c2039"
PANEL = "#20243f"
FIELD = "#323759"
GRID = "#353a5e"
LINE = "#5e6175"
INK = "#ffffff"
SOFT = "#b9bcd6"
TEAL = "#5eb6d1"
CORAL = "#ee6f87"
PURPLE = "#a47df2"
ORCHID = "#d98ad6"
PEACH = "#eaa57c"
ACCENTS = [TEAL, CORAL, PURPLE, ORCHID, PEACH]
LEVEL_COLORS = {"Normal": TEAL, "Heatwave": CORAL, "Severe Heatwave": PURPLE}
FONT_CHOICES = ["Josefin Sans", "Century Gothic", "Futura", "Segoe UI"]
settings = {"font": "Segoe UI"}

def choose_font(installed):
    for name in FONT_CHOICES:
        if name in installed:
            settings["font"] = name
            return

def font(size, weight="normal"):
    return (settings["font"], -size, weight)

def mix(start, end, amount):
    result = "#"
    for position in (1, 3, 5):
        first = int(start[position:position + 2], 16)
        second = int(end[position:position + 2], 16)
        result = result + format(int(first + (second - first) * amount), "02x")
    return result

def gradient(canvas, x, y, width, height, start, end, sideways):
    steps = 40
    for step in range(steps):
        color = mix(start, end, step / steps)
        if sideways:
            left = x + width * step / steps
            canvas.create_rectangle(left, y, left + width / steps + 1, y + height, fill=color, outline="")
        else:
            top = y + height * step / steps
            canvas.create_rectangle(x, top, x + width, top + height / steps + 1, fill=color, outline="")
