# HeatWatch – Heatwave Intelligence

OOP-with-Python mini project for AI use case KJS-CES-01: "Climate Intelligence for Heatwave Monitoring, Prediction, and Early Warning" (IMD Mumbai–Pune).

## How to run

```
python main.py
```

Needs only Python 3 (no pip installs). The first run creates `heatwatch.db` next to the scripts with 6 stations and 50 sample readings. Delete that file to start again with fresh sample data.

## Look

The screens copy the FDS mini project dashboard (github.com/Tanmay1123/FDS-MINI-PROJECT): the same navy gradient page, teal / coral / purple accents, underlined card titles, donut, gradient bars and big-name ranking. The app uses the first of these fonts it finds: Josefin Sans, Century Gothic, Futura, Segoe UI. Install Josefin Sans from Google Fonts for the exact typeface of the web dashboard.

## Features

Simulated Maharashtra weather stations, IMD heatwave checks (40 °C plains, 37 °C coastal, 47 °C severe), an overview dashboard (area chart with hover, donut, gradient bars, city ranking), manual reading entry with analysis, a live threaded sensor monitor with thermometer, trend chart and advisories, and a searchable SQLite records table.

## Where each experiment is shown

| Expt | Concept | Where to point in the viva |
|------|---------|----------------------------|
| 1 | Class, object, constructor, instance / class / static methods, getter and setter | `models.py` → `WeatherStation`: `__init__`, `station_count`, `add_reading()`, `from_text()` (`@classmethod`), `c_to_f()` (`@staticmethod`), `get_temperature()` / `set_temperature()` |
| 2 | Constructors and lists of objects | `models.py` → `create_stations()` returns a list of 6 station objects; looped over in `main.py` → `draw_sidebar()` |
| 3 | String handling and inheritance with `super()` | `models.py` → `strip().upper()`, `strip().title()`, `split(",")`; `PlainsStation` and `CoastalStation` call `super().__init__`. Also `" ".join("SECTIONS")` in `draw_sidebar()`, `in_words()` in `analysis.py` and `mix()` in `theme.py` |
| 4 | Abstract class and polymorphism | `alerts.py` → `Alert(ABC)` with `@abstractmethod message()`, overridden in `NormalAlert`, `HeatwaveAlert`, `SevereAlert`; `get_alert()` picks the object and `main.py` calls `alert.message()` without knowing which class it is |
| 5 | Exception handling, own modules, multithreading | `models.py` → `InvalidReadingError`; `main.py` → `try/except` in `analyse()` and `update_live()`; the seven imported modules; `sensors.py` → `start()` launches three daemon threads running `sensor_loop()` |
| 6 | List, tuple, set, dict, lambda, map, filter, reduce | `analysis.py` → `summary()` (lambda, map, filter, reduce, returns a dict); `self.info` tuple and `self.readings` list in `models.py`; `ALERT_LEVELS` set in `alerts.py`; `live` dict in `sensors.py`; `LEVEL_COLORS` dict in `theme.py` |
| 7 | Tkinter GUI and Canvas drawing (pack and grid) | `main.py` → `HeatWatchApp`: Canvas sidebar in `draw_sidebar()`, `grid` form in `build_add()`, `pack` inside every card, Treeview in `build_records()`; `charts.py` → `area_chart()`, `donut()`, `gradient_bars()`, `reading_bars()`, `gauge()` |
| 8 | SQLite with two tables and 7+ queries | `database.py` → `setup()` creates `stations` and `readings`; `insert_reading()`, `all_readings()`, `heatwave_readings()`, `hottest_readings()`, `search_city()`, `average_per_city()`, `count_per_level()`, `heatwaves_per_city()`, `overview_numbers()`, `mark_reviewed()`, `delete_reading()` |

## Files

| File | Lines | What it holds |
|------|-------|---------------|
| `main.py` | 440 | The Tkinter app (`HeatWatchApp`) |
| `charts.py` | 91 | Canvas drawing functions for every chart |
| `theme.py` | 47 | Colours, font choice and the gradient helper |
| `models.py` | 58 | Station classes and the custom exception |
| `alerts.py` | 48 | Abstract `Alert` and its three subclasses |
| `analysis.py` | 22 | map / filter / reduce summary, number to words |
| `sensors.py` | 24 | Sensor threads |
| `database.py` | 72 | All SQLite queries |
