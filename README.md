Tire Pressure monitoring System.

System Components :
RF receiver , Raspberry Pi3 (master) and 3.2 LCD display
RF receiver : is a  NXP ( NCK2912) connected to Raspberry on USB port.  The master communicates to the RF device over serial comm to configure the device and also read the received data.

Raspberry Pi3 ( Master) : Periodically communicates to the RF receiver and updates the GUI on the LCD display. The GUI is developed using pygame library

3.2 LCD display : Standard Display compatible with pi3

Next release : Analytics to log tire pressure data and help peform offline analysis.
