"""
Created on May 12, 2017
The class handle all the tire related data including 
some GUI related axis information .
@author: pdesai
"""


class Tire:
    identifier = 0
    background_area = 0
    __min_msg_length=2
    __GREEN = (40, 227, 143)
    __RED = (227, 0, 0)
    __MILD_RED = (247, 126, 106)
    __LIGHT_RED = (155, 0, 0)
    # Create a gradient of RED to give a nice effect. This is display only when a low pressure or a 
    # High temperature is detected.
    _red_blinking = [(199, 107, 68), (208, 103, 59), (218, 99, 49), (227, 95, 40), (236, 91, 31), (246, 87, 21)]

    def __init__(self, fourbyteid, name,backarea, ppos, tpos,spos, pressure=0, temp=0):
        self.identifier = fourbyteid
        self.tirename = name
        self._temperature = temp
        self._pressure = pressure
        self.pressure_pos = ppos
        self.temperature_pos = tpos
        self.status_pos = spos
        self.background_area = backarea
        self._color = self.__GREEN
        self._blink = False
        self._alternate_color = 0
        self._statusmsg=""

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
        return str(self._pressure) + ""
    
    def tire_status(self):
        return str(self._statusmsg)
    
    def temperature(self):
        return str(self._temperature) + "F"

    # When the pressure and temperature parameters are updated 
    # for each tire , the thresholds are checked and alert 
    # message for each tire is updated.
    def update_params(self, pres, temperature):
        self._pressure = pres
        self._temperature = temperature
        self._statusmsg=""
        if (self._pressure > 42 or self._pressure < 25):
            self._color = self.__RED
            self._statusmsg = "ALERT: Pressure "
            self._blink = False
        
        elif(self._pressure > 38 or self._pressure < 30):
            self._statusmsg= " SAVE FUEL "
            self._color = self.__MILD_RED     
        
        if (self._temperature > 158 or self._temperature < 50):
            self._color = self.__RED
            # If the pressure alert is already set then append only temperature
            if len(self._statusmsg) > self.__min_msg_length:
                self._statusmsg = self._statusmsg + "/temp"
            else:
                self._statusmsg = " ALERT:temperature"
                
            self._blink = False
                            
        if(len(self._statusmsg) < self.__min_msg_length):
            self._color = self.__GREEN
            self._statusmsg=""
            self._blink = False

__version = '0.1'