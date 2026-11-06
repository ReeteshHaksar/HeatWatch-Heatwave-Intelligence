class InvalidReadingError(Exception):
    pass

class WeatherStation:
    station_count = 0

    def __init__(self, station_id, city, latitude, longitude):
        self.station_id = station_id.strip().upper()
        self.city = city.strip().title()
        self.info = (self.station_id, self.city, latitude, longitude)
        self.readings = []
        self._temperature = 0.0
        self.threshold = 40
        self.kind = "plains"
        WeatherStation.station_count += 1

    def get_temperature(self):
        return self._temperature

    def set_temperature(self, value):
        if value < 0 or value > 60:
            raise InvalidReadingError("Temperature " + str(value) + " °C is outside 0-60 °C")
        self._temperature = value

    def add_reading(self, temp):
        self.readings.append(temp)
        self.readings = self.readings[-20:]

    @classmethod
    def from_text(cls, text):
        parts = text.split(",")
        return cls(parts[0], parts[1], float(parts[2]), float(parts[3]))

    @staticmethod
    def c_to_f(c):
        return round(c * 9 / 5 + 32, 1)

class PlainsStation(WeatherStation):
    def __init__(self, station_id, city, latitude, longitude):
        super().__init__(station_id, city, latitude, longitude)
        self.threshold = 40
        self.kind = "plains"

class CoastalStation(WeatherStation):
    def __init__(self, station_id, city, latitude, longitude):
        super().__init__(station_id, city, latitude, longitude)
        self.threshold = 37
        self.kind = "coastal"

def create_stations():
    stations = []
    stations.append(PlainsStation.from_text("WS101, Pune, 18.52, 73.86"))
    stations.append(CoastalStation.from_text("WS102, Mumbai, 19.08, 72.88"))
    stations.append(PlainsStation.from_text("WS103, Nagpur, 21.15, 79.09"))
    stations.append(PlainsStation.from_text("WS104, Chandrapur, 19.96, 79.30"))
    stations.append(CoastalStation.from_text("WS105, Ratnagiri, 16.99, 73.31"))
    stations.append(PlainsStation.from_text("WS106, Jalgaon, 21.00, 75.56"))
    return stations
