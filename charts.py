from theme import PANEL, FIELD, GRID, INK, SOFT, TEAL, CORAL, PURPLE, ACCENTS, font, mix, gradient

def stat(canvas, x, y, value, label, note, color):
    number = canvas.create_text(x, y, text=value, fill=color, anchor="nw", font=font(22), tags="stats")
    box = canvas.bbox(number)
    canvas.create_line(box[0], box[3] + 2, box[2], box[3] + 2, fill=color, tags="stats")
    canvas.create_text(x, box[3] + 9, text=label, fill=INK, anchor="nw", font=font(13), tags="stats")
    canvas.create_text(x, box[3] + 27, text=note, fill=SOFT, anchor="nw", font=font(12), tags="stats")

def legend(canvas, x, y, items):
    for color, text in items:
        canvas.create_oval(x, y - 5, x + 10, y + 5, fill=color, outline="")
        label = canvas.create_text(x + 16, y, text=text, fill=INK, anchor="w", font=font(13))
        x = canvas.bbox(label)[2] + 16

def to_y(temp):
    return 204 - (temp - 25) * 7.2

def area_layer(canvas, temps, floor, color, step):
    points = [40, to_y(floor)]
    x = 40
    for temp in temps:
        points.append(x)
        points.append(to_y(max(temp, floor)))
        x = x + step
    points.append(x - step)
    points.append(to_y(floor))
    canvas.create_polygon(points, fill=mix(PANEL, color, 0.8), outline="")

def area_chart(canvas, temps, right):
    canvas.delete("all")
    for level in (25, 30, 35, 40, 45, 50):
        canvas.create_line(40, to_y(level), right, to_y(level), fill=GRID)
        canvas.create_text(32, to_y(level), text=str(level), fill=SOFT, anchor="e", font=font(12))
    canvas.create_text(40, 218, text="oldest", fill=SOFT, anchor="w", font=font(12))
    canvas.create_text(right, 218, text="latest", fill=SOFT, anchor="e", font=font(12))
    if len(temps) < 2:
        return
    step = (right - 40) / (len(temps) - 1)
    area_layer(canvas, temps, 25, TEAL, step)
    area_layer(canvas, temps, 40, CORAL, step)
    area_layer(canvas, temps, 47, PURPLE, step)

def donut(canvas, slices):
    canvas.delete("all")
    total = 0
    for label, count, color in slices:
        total = total + count
    if total == 0:
        return
    start = 90
    keys = []
    for label, count, color in slices:
        extent = max(-360 * count / total, -359.9)
        canvas.create_arc(50, 4, 220, 174, start=start, extent=extent, fill=color, outline=PANEL, width=4)
        start = start + extent
        keys.append((color, label.replace(" Heatwave", "") + " " + str(count)))
    canvas.create_oval(107, 61, 163, 117, fill=PANEL, outline="")
    canvas.create_oval(123, 77, 147, 101, fill=INK, outline="")
    legend(canvas, 4, 200, keys)

def gradient_bars(canvas, rows):
    canvas.delete("all")
    y = 0
    position = 0
    for label, value in rows:
        width = 225 * value / rows[0][1]
        gradient(canvas, 0, y, width, 28, mix(PANEL, INK, 0.04), ACCENTS[position % 5], True)
        canvas.create_text(12, y + 15, text=label, fill=INK, anchor="w", font=font(15))
        canvas.create_text(270, y + 15, text=str(value), fill=INK, anchor="e", font=font(15))
        y = y + 38
        position = position + 1

def reading_bars(canvas, pairs, limit):
    canvas.delete("all")
    x = 4
    for temp, color in pairs:
        top = 140 - temp * 2
        canvas.create_rectangle(x, top, x + 34, 140, fill=color, outline="")
        canvas.create_text(x + 17, top - 10, text=str(temp), fill=INK, font=font(12))
        x = x + 46
    canvas.create_line(0, 140 - limit * 2, 510, 140 - limit * 2, fill=SOFT, dash=(4, 4))
    canvas.create_text(510, 130 - limit * 2, text="limit " + str(limit) + " °C", fill=SOFT, anchor="e", font=font(12))

def gauge(canvas, value, color):
    canvas.delete("all")
    canvas.create_rectangle(52, 8, 72, 190, fill=FIELD, outline="")
    canvas.create_rectangle(52, 190 - value * 3, 72, 190, fill=color, outline="")
    canvas.create_oval(40, 178, 84, 222, fill=color, outline="")
    for mark in (0, 20, 40, 60):
        canvas.create_text(84, 190 - mark * 3, text=str(mark) + " °C", fill=SOFT, anchor="w", font=font(12))
