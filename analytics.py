'''
Created on May 26, 2017

@author: pdesai
'''
import time
import csv

class TPMLogger:
    def __init__(self,logfile):
        self.__filename = logfile
        self.__filename= self.__filename+".csv"        
        self.__pval_temp=[0,0,0,0]
        self.__pval_pressure=[0,0,0,0]
     
    def write_to_file(self,key,press,temp):
        # Update the csv file 
        with open(self.__filename, 'a') as f:
            w = csv.writer(f)
            row = [time.ctime(), time.time(), key,press,temp]
            w.writerow(row)
            
    def log_data(self,dict_press_temp):
        index=0        
        # Check if the values match the previous set of temperature of pressure values.
        for key, values in dict_press_temp.iteritems():
            if(self.__pval_pressure[index]!=values[0]) or (self.__pval_temp[index]!=values[1]):
                self.__pval_pressure[index] = values[0]
                self.__pval_temp[index]     = values[1]
                self.write_to_file(key, self.__pval_pressure[index], self.__pval_temp[index])
            index=index+1
        
 
        