"""
Created on May 25, 2017
The class handle all the tire related data including some GUI related 
data for poisitioning of the values.
@author: pdesai
"""


class Tire:
    identifier = 0
    background_area = 0
    __GREEN = (40, 227, 143)
    __RED = (227, 96, 40)
    __LIGHT_RED = (155, 0, 0)
    # Create a gradient of RED to give a nice effect. This is display only when a low pressure or a 
    # High temperature is detected.
    _red_blinking = [(199, 107, 68), (208, 103, 59), (218, 99, 49), (227, 95, 40), (236, 91, 31), (246, 87, 21)]

    def __init__(self, fourbyteid, backarea, ppos, tpos, pressure=0, temp=0):
        self.identifier = fourbyteid
        self._temperature = temp
        self._pressure = pressure
        self.pressure_pos = ppos
        self.temperature_pos = tpos
        self.background_area = backarea
        self._color = self.__GREEN
        self._blink = False
        self._alternate_color = 0

    def get_color(self):
        if self._blink:
            self._alternate_color = self._alternate_color + 1
            if self._alternate_color >= len(self._red_blinking):
                self._alternate_color = 0

            return self._red_blinking[self._alternate_color]

        else:
            self._alternate_color = 0
            return self._color

    def pressure(self):
        return str(self._pressure) + "c"

    def temperature(self):
        return str(self._temperature) + "F"

    def update_params(self, pres, temperature):
        self._pressure = pres
        self._temperature = temperature
        if (self._pressure > 40 or self._pressure < 28) or \
                (self._temperature > 80 or self._pressure < 10):
            self._color = self.__RED
            self._blink = True
        else:
            self._color = self.__GREEN
            self._blink = False
