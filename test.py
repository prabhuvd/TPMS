'''
Created on May 24, 2017

@author: pdesai
'''
def list_hex_int(list_input):
    res=list()
    for each in list_input:
        res.append(int(each,16))
    return res    
    
test_input=['20','0C','50','00','57','02']
 
print int(test_input[4],16)  
print int(test_input[1],16) 