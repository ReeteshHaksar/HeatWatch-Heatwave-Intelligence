from abc import ABC, abstractmethod

from theme import TEAL, CORAL, PURPLE

class Alert(ABC):
    def __init__(self, temperature, city):
        self.temperature = temperature
        self.city = city

    @abstractmethod
    def message(self):
        pass

class NormalAlert(Alert):
    level = "Normal"
    color = TEAL

    def message(self):
        line1 = self.city + " is at " + str(self.temperature) + " °C. Citizens and farmers can work as usual."
        line2 = "Hospitals: routine readiness, keep ORS stock checked."
        return line1 + "\n" + line2

class HeatwaveAlert(Alert):
    level = "Heatwave"
    color = CORAL

    def message(self):
        line1 = self.city + " is at " + str(self.temperature) + " °C. Citizens: stay indoors 12-4 pm and drink water often."
        line2 = "Farmers: irrigate in the evening. Hospitals: prepare heat-stroke beds."
        return line1 + "\n" + line2

class SevereAlert(Alert):
    level = "Severe Heatwave"
    color = PURPLE

    def message(self):
        line1 = self.city + " is at " + str(self.temperature) + " °C. Citizens: do not go outdoors, check on the elderly."
        line2 = "Farmers: stop field work and shade livestock. Hospitals: emergency wards on full alert."
        return line1 + "\n" + line2

ALERT_LEVELS = {"Normal", "Heatwave", "Severe Heatwave"}

def get_alert(temp, threshold, city):
    if temp >= 47:
        return SevereAlert(temp, city)
    if temp >= threshold:
        return HeatwaveAlert(temp, city)
    return NormalAlert(temp, city)
