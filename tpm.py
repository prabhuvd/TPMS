'''
Created on May 15, 2017

@author: pdesai
'''
 
from radio import Radio




radio_dev = Radio('COM6')
print "Downloading Receiver Configuration..."
radio_dev.configure_device()
print "Done"
 
Done = False
while not Done:
    rx_status = radio_dev.read_tpm_sensors()    
    print radio_dev.print_sensor_data()
     
  
radio_dev.close()  