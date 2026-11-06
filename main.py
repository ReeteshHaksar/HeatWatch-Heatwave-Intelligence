import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
from datetime import datetime

import analysis
import charts
import database
import sensors
from alerts import ALERT_LEVELS, get_alert
from models import InvalidReadingError, WeatherStation, create_stations
from theme import PAGE, PAGE_MID, PAGE_LOW, SIDEBAR, PANEL, FIELD, LINE, INK, SOFT, TEAL, CORAL, PURPLE, ACCENTS, LEVEL_COLORS
from theme import choose_font, font, mix, gradient

PAGE_NAMES = ["Overview", "Add Reading", "Live Monitor", "Records"]
LEVEL_ORDER = ["Normal", "Heatwave", "Severe Heatwave"]

class HeatWatchApp:
    def __init__(self, root):
        self.root = root
        root.title("HeatWatch – Heatwave Intelligence")
        root.geometry("1280x780")
        root.resizable(False, False)
        root.configure(bg=PAGE)
        choose_font(tkfont.families())
        self.stations = create_stations()
        self.station_names = list(map(lambda s: s.station_id + " – " + s.city, self.stations))
        database.setup(self.stations)
        self.setup_style()
        self.pages = {}
        self.frames = {}
        self.recent = []
        self.side = tk.Canvas(root, width=250, height=780, bg=SIDEBAR, highlightthickness=0, cursor="hand2")
        self.side.pack(side="left")
        self.side.bind("<Button-1>", self.nav_click)
        self.holder = tk.Frame(root, bg=PAGE)
        self.holder.pack(side="left")
        self.build_overview()
        self.build_add()
        self.build_live()
        self.build_records()
        self.show_page("Overview")
        self.update_live()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", background=FIELD, foreground=INK, borderwidth=0, relief="flat", padding=8, font=font(14))
        style.map("TButton", background=[("active", PURPLE)])
        style.configure("TCombobox", fieldbackground=FIELD, background=FIELD, foreground=INK, arrowcolor=INK, bordercolor=FIELD, lightcolor=FIELD, darkcolor=FIELD, padding=6)
        style.map("TCombobox", fieldbackground=[("readonly", FIELD)], foreground=[("readonly", INK)], selectbackground=[("readonly", FIELD)], selectforeground=[("readonly", INK)])
        style.configure("Treeview", background=PANEL, fieldbackground=PANEL, foreground=INK, rowheight=26, borderwidth=0, font=font(13))
        style.map("Treeview", background=[("selected", FIELD)])
        style.configure("Treeview.Heading", background=FIELD, foreground=INK, relief="flat", font=font(13))
        style.map("Treeview.Heading", background=[("active", FIELD)])
        self.root.option_add("*TCombobox*Listbox.background", FIELD)
        self.root.option_add("*TCombobox*Listbox.foreground", INK)
        self.root.option_add("*TCombobox*Listbox.font", font(14))

    def text(self, parent, words, size, color, weight="normal"):
        return tk.Label(parent, text=words, font=font(size, weight), fg=color, bg=parent["bg"], justify="left")

    def new_page(self, name, eyebrow, words):
        frame = tk.Frame(self.holder, bg=PAGE)
        frame.grid(row=0, column=0)
        page = tk.Canvas(frame, width=1030, height=780, bg=PAGE, highlightthickness=0)
        page.pack()
        gradient(page, 0, 0, 1030, 430, PAGE, PAGE_MID, False)
        gradient(page, 0, 430, 1030, 350, PAGE_MID, PAGE_LOW, False)
        if name != "Overview":
            page.create_text(40, 30, text=" ".join(eyebrow.upper()), fill=CORAL, anchor="nw", font=font(12))
            page.create_text(38, 50, text=name, fill=INK, anchor="nw", font=font(42))
            page.create_text(40, 108, text=words, fill=SOFT, anchor="nw", font=font(15))
        self.pages[name] = page
        self.frames[name] = frame
        return page

    def card(self, page, x, y, width, height, title, note):
        frame = tk.Frame(page, bg=PANEL, padx=22, pady=18)
        frame.pack_propagate(False)
        page.create_window(x, y, window=frame, width=width, height=height, anchor="nw")
        if title != "":
            self.text(frame, title, 20, INK).pack(anchor="w")
            tk.Frame(frame, bg=LINE, height=1, width=int(width * 0.55)).pack(anchor="w", pady=(4, 8))
        if note != "":
            self.text(frame, note, 13, SOFT).pack(anchor="w", pady=(0, 6))
        return frame

    def canvas(self, parent, width, height):
        area = tk.Canvas(parent, width=width, height=height, bg=PANEL, highlightthickness=0)
        area.pack(anchor="w")
        return area

    def note_block(self, parent, wrap):
        block = tk.Frame(parent, bg=CORAL)
        block.pack(anchor="w", pady=(10, 0))
        label = self.text(block, "", 14, SOFT)
        label.configure(bg=PANEL, padx=12, wraplength=wrap)
        label.pack(padx=(2, 0))
        return label

    def nice_button(self, parent, words, command):
        return ttk.Button(parent, text=words, command=command, cursor="hand2", takefocus=False)

    def entry(self, parent, words):
        box = tk.Entry(parent, bg=FIELD, fg=INK, insertbackground="white", relief="flat", highlightthickness=0, width=22, font=font(14))
        box.insert(0, words)
        return box

    def draw_sidebar(self, active):
        side = self.side
        side.delete("all")
        side.create_line(249, 0, 249, 780, fill=mix(SIDEBAR, INK, 0.06))
        side.create_text(22, 30, text="Heatwave\nIntelligence", fill=INK, anchor="nw", font=font(22, "bold"))
        side.create_text(22, 92, text="OOP-PY mini project · KJS-CES-01", fill=SOFT, anchor="nw", font=font(12))
        side.create_text(22, 132, text=" ".join("SECTIONS"), fill=SOFT, anchor="nw", font=font(11))
        side.create_line(22, 154, 228, 154, fill=mix(SIDEBAR, INK, 0.12))
        y = 164
        for name in PAGE_NAMES:
            if name == active:
                gradient(side, 22, y, 206, 38, PURPLE, mix(SIDEBAR, PURPLE, 0.08), True)
            side.create_text(34, y + 20, text=name, fill=INK, anchor="w", font=font(15))
            y = y + 40
        side.create_text(22, 352, text=" ".join("STATIONS"), fill=SOFT, anchor="nw", font=font(11))
        side.create_line(22, 374, 228, 374, fill=mix(SIDEBAR, INK, 0.12))
        averages = dict(database.average_per_city())
        y = 390
        for station in self.stations:
            average = averages.get(station.city, 0)
            color = get_alert(average, station.threshold, station.city).color
            side.create_oval(24, y, 34, y + 10, fill=color, outline="")
            side.create_text(46, y + 6, text=station.city, fill=INK, anchor="w", font=font(14))
            side.create_text(228, y + 6, text=str(average) + " °C", fill=SOFT, anchor="e", font=font(12))
            y = y + 28
        total = database.overview_numbers()[0]
        side.create_text(22, y + 12, text=str(total) + " readings stored\nDot colour = average alert level", fill=SOFT, anchor="nw", font=font(11))

    def nav_click(self, event):
        index = (event.y - 164) // 40
        if index >= 0 and index < len(PAGE_NAMES):
            self.show_page(PAGE_NAMES[index])

    def show_page(self, name):
        self.frames[name].tkraise()
        if name == "Overview":
            self.load_overview()
        if name == "Records":
            self.show_rows(database.all_readings())
        self.draw_sidebar(name)

    def build_overview(self):
        page = self.new_page("Overview", "", "")
        page.create_text(38, 38, text="HeatWatch", fill=INK, anchor="nw", font=font(50, "bold"))
        page.create_text(40, 106, text="Heatwave Early Warning", fill=INK, anchor="nw", font=font(22))
        gradient(page, 40, 158, 264, 44, INK, "#c9cbdc", False)
        page.create_text(172, 181, text=str(WeatherStation.station_count) + " stations · Maharashtra", fill=PAGE, font=font(17, "bold"))
        chart_card = self.card(page, 344, 28, 658, 372, "Recent Readings", "Max temperature of the latest 40 readings. Hover over the chart to read any one.")
        self.area = self.canvas(chart_card, 610, 228)
        self.area.bind("<Motion>", self.hover_area)
        key = self.canvas(chart_card, 610, 24)
        charts.legend(key, 40, 12, [(TEAL, "Below 40 °C"), (CORAL, "40 °C and above"), (PURPLE, "47 °C and above")])
        mix_card = self.card(page, 28, 416, 314, 336, "Alert Mix", "Share of all readings by alert level.")
        self.donut = self.canvas(mix_card, 270, 220)
        limit_card = self.card(page, 358, 416, 314, 336, "Over the Limit", "")
        self.big_word = self.text(limit_card, "", 38, TEAL)
        self.big_word.pack(anchor="w")
        self.text(limit_card, "Percent of all readings crossed\nthe IMD heatwave limit.", 15, INK).pack(anchor="w", pady=(0, 12))
        self.bars = self.canvas(limit_card, 270, 150)
        rank_card = self.card(page, 688, 416, 314, 336, "Hottest Cities", "Average max temperature per city.")
        self.rank_box = tk.Frame(rank_card, bg=PANEL)
        self.rank_box.pack(fill="x")

    def load_overview(self):
        page = self.pages["Overview"]
        numbers = database.overview_numbers()
        page.delete("stats")
        charts.stat(page, 40, 232, str(numbers[1]), "Heatwave readings", "of " + str(numbers[0]) + " stored", TEAL)
        charts.stat(page, 196, 232, str(numbers[2]), "Cities affected", "of " + str(len(self.stations)), CORAL)
        charts.stat(page, 40, 316, str(numbers[3]) + " °C", "Hottest reading", numbers[4], PURPLE)
        self.recent = list(reversed(database.all_readings()[:40]))
        charts.area_chart(self.area, list(map(lambda row: row[3], self.recent)), 600)
        counts = dict(database.count_per_level())
        slices = []
        for level in LEVEL_ORDER:
            slices.append((level, counts.get(level, 0), LEVEL_COLORS[level]))
        charts.donut(self.donut, slices)
        percent = 0
        if numbers[0] > 0:
            percent = round(numbers[1] * 100 / numbers[0])
        self.big_word.configure(text=analysis.in_words(percent))
        charts.gradient_bars(self.bars, database.heatwaves_per_city()[:4])
        for widget in self.rank_box.winfo_children():
            widget.destroy()
        position = 0
        for city, average in sorted(database.average_per_city(), key=lambda pair: pair[1], reverse=True):
            name = city
            size = 15
            color = INK
            weight = "normal"
            if position < 3:
                name = city.upper()
                size = 24
                color = ACCENTS[position]
                weight = "bold"
            row = tk.Frame(self.rank_box, bg=PANEL)
            row.pack(fill="x", pady=2)
            self.text(row, name, size, color, weight).pack(side="left")
            value = tk.Frame(row, bg=PANEL)
            value.pack(side="left", fill="x", expand=True, padx=(12, 0))
            self.text(value, str(average) + " °C", 14, color).pack(anchor="e")
            tk.Frame(value, bg=color, height=1).pack(fill="x")
            position = position + 1

    def hover_area(self, event):
        self.area.delete("hover")
        if len(self.recent) < 2:
            return
        step = 560 / (len(self.recent) - 1)
        index = round((event.x - 40) / step)
        if index < 0 or index >= len(self.recent):
            return
        row = self.recent[index]
        x = 40 + index * step
        self.area.create_line(x, 24, x, 204, fill=INK, tags="hover")
        self.area.create_text(600, 0, text=row[2] + " · " + str(row[3]) + " °C · " + row[6], fill=INK, anchor="ne", font=font(13), tags="hover")

    def build_add(self):
        page = self.new_page("Add Reading", "Manual entry", "Type a station's maximum temperatures. Each one is checked against the IMD limit and saved.")
        form = self.card(page, 28, 150, 400, 388, "New Reading", "Temperatures are comma-separated, in °C.")
        grid = tk.Frame(form, bg=PANEL)
        grid.pack(anchor="w")
        self.add_station = ttk.Combobox(grid, values=self.station_names, state="readonly", width=20, font=font(14))
        self.add_station.current(0)
        self.add_station.bind("<<ComboboxSelected>>", self.show_station)
        self.temps_entry = self.entry(grid, "36, 39, 41, 43")
        self.humidity_entry = self.entry(grid, "45")
        self.wind_entry = self.entry(grid, "12")
        self.condition_entry = self.entry(grid, "Sunny")
        fields = [
            ("Station", self.add_station),
            ("Temperatures °C", self.temps_entry),
            ("Humidity %", self.humidity_entry),
            ("Wind km/h", self.wind_entry),
            ("Condition", self.condition_entry),
        ]
        row = 0
        for caption, widget in fields:
            self.text(grid, caption, 13, SOFT).grid(row=row, column=0, sticky="w", padx=(0, 14), pady=7)
            widget.grid(row=row, column=1, sticky="w", ipady=5)
            row = row + 1
        self.nice_button(form, "Analyse & Save", self.analyse).pack(anchor="w", pady=12)
        info = self.card(page, 28, 554, 400, 198, "Station", "")
        self.station_info = self.text(info, "", 14, SOFT)
        self.station_info.pack(anchor="w")
        self.show_station(None)
        result = self.card(page, 444, 150, 558, 602, "Analysis Result", "Worked out with map, filter and reduce.")
        self.result_level = self.text(result, "No reading yet", 38, TEAL)
        self.result_level.pack(anchor="w")
        self.result_stats = self.canvas(result, 510, 84)
        self.result_bars = self.canvas(result, 510, 150)
        self.result_text = self.note_block(result, 480)
        self.result_text.configure(text="Enter readings and press Analyse & Save.")

    def show_station(self, event):
        station = self.stations[self.add_station.current()]
        words = station.info[0] + " · " + station.info[1] + " · " + station.kind + " station\n"
        words = words + "Latitude " + str(station.info[2]) + " · Longitude " + str(station.info[3]) + "\n"
        words = words + "IMD heatwave limit: " + str(station.threshold) + " °C · severe at 47 °C\n"
        words = words + "Readings held in memory: " + str(len(station.readings))
        self.station_info.configure(text=words)

    def analyse(self):
        station = self.stations[self.add_station.current()]
        temps = []
        try:
            for part in self.temps_entry.get().split(","):
                temp = float(part.strip())
                station.set_temperature(temp)
                temps.append(temp)
            humidity = float(self.humidity_entry.get())
            wind = float(self.wind_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter numbers only, for example: 36, 39, 41, 43")
            return
        except InvalidReadingError as error:
            messagebox.showerror("Invalid reading", str(error))
            return
        condition = self.condition_entry.get().strip().capitalize()
        pairs = []
        for temp in temps:
            station.add_reading(temp)
            alert = get_alert(temp, station.threshold, station.city)
            pairs.append((temp, alert.color))
            database.insert_reading(station.station_id, station.city, temp, humidity, wind, condition, alert.level)
        result = analysis.summary(temps, station.threshold)
        alert = get_alert(result["max"], station.threshold, station.city)
        self.result_level.configure(text=alert.level, fg=alert.color)
        self.result_stats.delete("stats")
        charts.stat(self.result_stats, 0, 6, str(result["average"]) + " °C", "Average", "of " + str(len(temps)) + " readings", TEAL)
        charts.stat(self.result_stats, 135, 6, str(result["max"]) + " °C", "Highest", "found with reduce", CORAL)
        charts.stat(self.result_stats, 270, 6, str(len(result["over_limit"])), "Over the limit", "found with filter", PURPLE)
        charts.stat(self.result_stats, 405, 6, str(result["total"]), "Total", "added with reduce", TEAL)
        charts.reading_bars(self.result_bars, pairs, station.threshold)
        words = "In °F (map): " + ", ".join(map(str, result["fahrenheit"])) + "\n"
        words = words + "At or over " + str(station.threshold) + " °C (filter): " + ", ".join(map(str, result["over_limit"])) + "\n\n"
        self.result_text.configure(text=words + alert.message())
        self.show_station(None)

    def build_live(self):
        page = self.new_page("Live Monitor", "Sensor threads", "Three background threads act as sensors. The screen reads their latest values every second.")
        control = self.card(page, 28, 150, 300, 160, "Station", "")
        self.live_station = ttk.Combobox(control, values=self.station_names, state="readonly", width=20, font=font(14))
        self.live_station.current(0)
        self.live_station.pack(anchor="w")
        buttons = tk.Frame(control, bg=PANEL)
        buttons.pack(anchor="w", pady=10)
        self.live_button = self.nice_button(buttons, "Start", self.toggle_live)
        self.live_button.pack(side="left", padx=(0, 8))
        self.nice_button(buttons, "Save to database", self.save_live).pack(side="left")
        tiles = self.card(page, 344, 150, 658, 160, "Sensors", "")
        self.live_stats = self.canvas(tiles, 610, 80)
        banner = self.card(page, 28, 324, 974, 116, "", "")
        self.banner_bar = tk.Frame(banner, bg=TEAL, width=4)
        self.banner_bar.pack(side="left", fill="y", padx=(0, 16))
        self.banner_level = self.text(banner, "Waiting for sensors", 22, TEAL)
        self.banner_level.pack(anchor="w")
        self.banner_text = self.text(banner, "Press Start. The advisory for citizens, farmers and hospitals appears here.", 14, SOFT)
        self.banner_text.pack(anchor="w")
        gauge_card = self.card(page, 28, 452, 190, 300, "Thermometer", "")
        self.gauge = self.canvas(gauge_card, 146, 226)
        charts.gauge(self.gauge, 0, TEAL)
        trend_card = self.card(page, 234, 452, 452, 300, "Live Trend", "")
        self.trend = self.canvas(trend_card, 408, 226)
        charts.area_chart(self.trend, [], 400)
        log_card = self.card(page, 702, 452, 300, 300, "Last 8 Readings", "")
        self.log = tk.Listbox(log_card, bg=PANEL, fg=INK, relief="flat", highlightthickness=0, borderwidth=0, selectbackground=FIELD, font=font(13))
        self.log.pack(fill="both", expand=True)

    def toggle_live(self):
        if sensors.running["on"]:
            sensors.stop()
            self.live_button.configure(text="Start")
            return
        station = self.stations[self.live_station.current()]
        sensors.start(station.threshold - 6, station.threshold + 9)
        self.live_button.configure(text="Stop")

    def update_live(self):
        self.root.after(1000, self.update_live)
        value = sensors.live["temperature"]
        if not sensors.running["on"] or value is None:
            return
        station = self.stations[self.live_station.current()]
        stamp = datetime.now().strftime("%H:%M:%S") + "  "
        try:
            station.set_temperature(value)
            station.add_reading(value)
            alert = get_alert(value, station.threshold, station.city)
            self.banner_bar.configure(bg=alert.color)
            self.banner_level.configure(text=alert.level, fg=alert.color)
            self.banner_text.configure(text=alert.message())
            charts.gauge(self.gauge, value, alert.color)
            charts.area_chart(self.trend, station.readings, 400)
            self.log.insert(0, stamp + str(value) + " °C  " + alert.level)
        except InvalidReadingError:
            self.log.insert(0, stamp + "Sensor fault – value rejected")
        self.log.delete(8, "end")
        temp = station.get_temperature()
        self.live_stats.delete("stats")
        charts.stat(self.live_stats, 0, 6, str(temp) + " °C", "Temperature", str(WeatherStation.c_to_f(temp)) + " °F", TEAL)
        charts.stat(self.live_stats, 210, 6, str(sensors.live["humidity"]) + " %", "Humidity", "relative", CORAL)
        charts.stat(self.live_stats, 420, 6, str(sensors.live["wind"]) + " km/h", "Wind", "speed", PURPLE)

    def save_live(self):
        station = self.stations[self.live_station.current()]
        if len(station.readings) == 0:
            messagebox.showerror("No reading yet", "Start the monitor for this station first.")
            return
        temp = station.get_temperature()
        alert = get_alert(temp, station.threshold, station.city)
        database.insert_reading(station.station_id, station.city, temp, sensors.live["humidity"], sensors.live["wind"], "Live sensor", alert.level)
        self.log.insert(0, "Saved " + str(temp) + " °C to the database")

    def build_records(self):
        page = self.new_page("Records", "SQLite database", "Every saved reading. Search by city, filter, mark a row as reviewed or delete it.")
        box = self.card(page, 28, 150, 974, 602, "", "")
        bar = tk.Frame(box, bg=PANEL)
        bar.pack(fill="x", pady=(0, 12))
        self.search_entry = self.entry(bar, "")
        self.search_entry.configure(width=16)
        self.search_entry.pack(side="left", ipady=7, padx=(0, 6))
        actions = [
            ("Search", lambda: self.show_rows(database.search_city(self.search_entry.get().strip()))),
            ("All", lambda: self.show_rows(database.all_readings())),
            ("Heatwave only", lambda: self.show_rows(database.heatwave_readings())),
            ("Hottest 10", lambda: self.show_rows(database.hottest_readings())),
            ("Mark reviewed", self.mark_reviewed),
            ("Delete", self.delete_selected),
        ]
        for words, command in actions:
            self.nice_button(bar, words, command).pack(side="left", padx=3)
        columns = ("ID", "Station", "City", "Temp", "Humidity", "Wind", "Alert", "Reviewed", "Time")
        self.tree = ttk.Treeview(box, columns=columns, show="headings", height=15)
        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=100, anchor="center")
        for level in ALERT_LEVELS:
            self.tree.tag_configure(level, foreground=LEVEL_COLORS[level])
        self.tree.pack(fill="x")
        self.summary_label = self.note_block(box, 900)

    def show_rows(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in rows:
            self.tree.insert("", "end", values=row, tags=(row[6],))
        averages = list(map(lambda pair: pair[0] + " " + str(pair[1]) + " °C", database.average_per_city()))
        counts = dict(database.count_per_level())
        levels = []
        for level in LEVEL_ORDER:
            levels.append(level + " " + str(counts.get(level, 0)))
        words = str(len(rows)) + " rows shown\nAverage per city:  " + "  ·  ".join(averages) + "\nReadings per alert level:  " + "  ·  ".join(levels)
        self.summary_label.configure(text=words)

    def mark_reviewed(self):
        for item in self.tree.selection():
            database.mark_reviewed(self.tree.item(item)["values"][0])
        self.show_rows(database.all_readings())

    def delete_selected(self):
        selection = self.tree.selection()
        if len(selection) > 0 and messagebox.askyesno("Delete reading", "Delete the selected reading permanently?"):
            for item in selection:
                database.delete_reading(self.tree.item(item)["values"][0])
            self.show_rows(database.all_readings())

if __name__ == "__main__":
    window = tk.Tk()
    HeatWatchApp(window)
    window.mainloop()
