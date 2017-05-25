'''
Created on April 6, 2015

@author: pdesai
'''
# ----------

#import FTDI_Usage
import irec
import time
import random

IREC_PORT = 'COM6'
 
CMD_DELAY= 0.00 # 100msec
CMD_INDEX=0
DELAY_INDEX=1
 

DEBUG_PIN_TRUE  = "B1"
DEBUG_PIN_FALSE = "00"

TPM_TIME_SEQ= [110,190,160,120,100,110,130,110]
TPM_ON_OFF = [["06 20 20 00 00 F4 01",CMD_DELAY],              
              #["02 20 21",CMD_DELAY] 
              ]     

''' 
RC_CMD_RADIO_TX_DEFAULTS
RC_CMD_RADIO_TX_STATIC_NCK2983
RC_CMD_RADIO_TX_DBG_CTRL
RC_CMD_RADIO_TX_WUP
RC_CMD_RADIO_TX_PREAMBLE
RC_CMD_RADIO_TX_DATA
RC_CMD_RADIO_LO_FREQUENCY
RC_CMD_RADIO_TX_ON
RC_CMD_RADIO_TX_OFF         
'''
TPM_WUP_433p92=[
["03 20 22 01 ",CMD_DELAY],                                     
["14 20 24 65 1B 00 00 50 00 00 00 00 00 FF 00 FF 06 08 00 00 00",CMD_DELAY],                                      
["03 20 29 "+ DEBUG_PIN_TRUE,CMD_DELAY],                                                       
["08 20 25 08 28 00 28 00 FF",CMD_DELAY],                                                  
["08 20 26 09 28 00 28 00 66",CMD_DELAY],                                                  
["3A 20 28 A0 A9 00 28 FF 44 44 CC CC FF FF 44 44 CC CC FF FF 44 44 CC CC FF FF 44 44 CC CC FF FF 44 44 CC CC FF FF 44 44 CC CC FF FF 44 44 CC CC FF FF 44 44 CC CC FF FF 44 44 CC",CMD_DELAY],
["0B 20 13 10 3E 8C 03 00 EE 03 1F 02",CMD_DELAY],                                               
["06 20 20 00 00 F4 01",CMD_DELAY],                                                    
["02 20 21",CMD_DELAY] ]                                                       

''' 
RC_CMD_RADIO_TX_DEFAULTS
RC_CMD_RADIO_TX_STATIC_NCK2983
RC_CMD_RADIO_TX_DBG_CTRL
RC_CMD_RADIO_TX_WUP
RC_CMD_RADIO_TX_PREAMBLE
RC_CMD_RADIO_TX_DATA
RC_CMD_RADIO_LO_FREQUENCY
RC_CMD_RADIO_TX_ON
RC_CMD_RADIO_TX_OFF         
'''
TPM_FRAME_433p92=[
#["03 20 22 01",CMD_DELAY],                 
["14 20 24 65 13 00 00 8C 00 00 00 00 00 FF 00 FF 03 08 00 01 00",CMD_DELAY],
#["03 20 29 "+ DEBUG_PIN_TRUE,CMD_DELAY],                
["08 20 25 08 38 01 29 00 FF",CMD_DELAY],            
["08 20 26 09 28 00 29 00 66",CMD_DELAY],            
["12 20 28 58 A8 00 29 33 44 11 22 66 77 44 55 22 33 00 11",CMD_DELAY],  
#["0B 20 13 10 3E 8C 03 00 EE 03 1F 02",CMD_DELAY],         
#["06 20 20 00 00 F4 01",CMD_DELAY],              
#["02 20 21",CMD_DELAY]            
]

startVal=0
def initTimeGap():    
    global startVal
    startVal = random.randint(0, 7)
    print "Start Val # ",startVal
    
def getTimeGap():
    global startVal
    
    if(startVal>7):
        startVal=0
 
    ret_val = TPM_TIME_SEQ [startVal]           
    startVal =startVal+1  
    return ret_val  
        
                                                                                                                                                                                                                                                                                                                                                                        
def executeCMDList(cmdlist):    
    for commands in range(len(cmdlist)):
        #print (cmdlist[commands][0])
        irecinst.write_command(cmdlist[commands][CMD_INDEX]) 
        #time.sleep(cmdlist[commands][DELAY_INDEX]);    

irecinst=0
irecinst = irec.Radio() 

contExecution=False    
if(irecinst.open(IREC_PORT,115200)==0):      
    exit
else:
    contExecution=True    
    exec_time = []
    
    framecount=0 
    initTimeGap() 
    
    #Preload TPM params
    executeCMDList(TPM_WUP_433p92)
     
    #executeCMDList(TPM_FRAME_433p92)
    
    while (framecount < 100) :    
        #Configure Radio     
        start_time = time.clock()     
        executeCMDList(TPM_ON_OFF)
        sleep_time = (getTimeGap()-32-7.5)/1000.0
        #print sleep_time
        time.sleep(sleep_time)
        exec_time.append(time.clock() - start_time)    
        framecount=framecount+1
        print "Frame #",framecount
            
    irecinst.close()
            
    tot=0
    for t in exec_time:
        tot = t+tot
                
    print "execution time : ",exec_time
    print "Total time : ",tot
