"""
Created on May 15, 2017

@author: pdesai
"""

import pygame
from radio import Radio
from tire import Tire

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (40, 227, 143)
RED =  (227, 96, 40)
BLUE = (14, 63, 142)
GREY = (90, 90, 90)

# port specification for Linux / Windows  
#RADIO_PORT = '/dev/ttyUSB0'
APPLICATION_HDR = "pdesai:TPM"
RADIO_PORT = 'COM6'

pygame.init ()

# Enhance readability with class Dimensions.
class Dimensions:
    def __init__(self, x, y):
        self.w = x
        self.h = y


# Set the width and height of the screen [width, height]
screen_pixels = Dimensions(320, 240)
car_pixels = Dimensions(65, 142)

screen = pygame.display.set_mode((screen_pixels.w, screen_pixels.h))


pygame.display.set_caption(APPLICATION_HDR)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

PIXEL_MULT = 100

# noinspection PyUnresolvedReferences
mazda = pygame.image.load('img//mazda.png')

pfont = pygame.font.SysFont('arial', 35,bold=True)
tfont = pygame.font.SysFont('arial', 25,bold=True)
status_font = pygame.font.SysFont('arial', 12)

Y_N_OFFSET = -35
Y_P_OFFSET = 10
X_OFFSET = 10
N_OFFSET = -20
FL = Tire("0d224bff",  # ID
          "FL ",
           (0, 0, screen_pixels.w / 2, screen_pixels.h / 2),  # Background Area
           (screen_pixels.w * 1 / 8 - X_OFFSET, (Y_N_OFFSET + screen_pixels.h / 4)),  # Pressure position
           (screen_pixels.w * 1 / 8 - X_OFFSET, (Y_P_OFFSET + screen_pixels.h / 4)),  # Temperature position
           (0+Y_P_OFFSET, (screen_pixels.h/2)+N_OFFSET),  # status position           
           )

FR = Tire("0d224bf4",
          "FR ",
           (screen_pixels.w / 2, 0, screen_pixels.w / 2, screen_pixels.h / 2),
           (screen_pixels.w * 3 / 4 - X_OFFSET, (Y_N_OFFSET + screen_pixels.h / 4)),
           (screen_pixels.w * 3 / 4 - X_OFFSET, (Y_P_OFFSET + screen_pixels.h / 4)),
           (screen_pixels.w/2+Y_P_OFFSET*4, (screen_pixels.h / 2)+N_OFFSET)  # status position
           )
RR = Tire("0d22622a",
          "RR ",
           (screen_pixels.w / 2, screen_pixels.h / 2, screen_pixels.w / 2, screen_pixels.h / 2),
           (screen_pixels.w * 3 / 4 - X_OFFSET, (Y_N_OFFSET + screen_pixels.h * 3 / 4)),
           (screen_pixels.w * 3 / 4 - X_OFFSET, (Y_P_OFFSET + screen_pixels.h * 3 / 4)),
           (screen_pixels.w/2+Y_P_OFFSET*4, (screen_pixels.h)+N_OFFSET)  # status position
           )

RL = Tire("0d2262b9",
          "RL ",
           (0, screen_pixels.h / 2, screen_pixels.w / 2, screen_pixels.h / 2),
           (screen_pixels.w * 1 / 8 - X_OFFSET, (Y_N_OFFSET + screen_pixels.h * 3 / 4)),
           (screen_pixels.w * 1 / 8 - X_OFFSET, (Y_P_OFFSET + screen_pixels.h * 3 / 4)),
           (0+Y_P_OFFSET, (screen_pixels.h)+N_OFFSET)  # status position
           )


All_Tires = [FL, FR, RR, RL]
 

radio_dev = Radio(RADIO_PORT)

print "Downloading Receiver Configuration..."
radio_dev.configure_device()
print "Done! "

def test_params(presvalues, tempvalues):
    index = 0
    for tire in All_Tires:
        tire.update_params(presvalues[index], tempvalues[index])
        index = index + 1


count = 0
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    # --- Game logic should go here
    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill((168, 168, 168))
    # screen.blit(bg3, (screen_pixels.w/2-car_pixels.w/2,0))
    '''
    ########################################################
    #######          Test cases for UI testing       #######   
    ########################################################
    
    if (count <500):
        test_params([27,35,35,35], # pressure values
                    [62,60,63,65])  # temperature values        
    elif(count >=500 and count<1000):
        test_params([35,27,35,35],                    
                    [70,75,75,68])    
    elif(count >=1000 and count<1500):
        test_params([35,35,27,35],                    
                    [80,81,82,83])
    elif(count >=1500 and count<2000):
        test_params([35,27,35,27],                    
                    [55,56,57,54])
    elif(count >=2000 and count<2500):
        test_params([27,27,35,35],                    
                    [75,76,74,73])
    elif(count >=2500 and count<3000):
        test_params([27,27,27,27],                    
                    [65,66,67,64])
    else:
        count =0
    count=count+1

    ########################################################
    #######        End of Test cases for UI          #######   
    ########################################################
    
    '''
    
    ''' 
    This is where the sensor data and UI ( user interface)
    are linked to each other.
    '''
    radio_dev.read_tpm_sensors()
    all_sensor_data = radio_dev.get_sensor_data()
    print all_sensor_data
    for key, val in all_sensor_data.iteritems():
        if key == FL.identifier:
            FL.update_params(val[0], val[1])
        elif key == FR.identifier:
            FR.update_params(val[0], val[1])
        elif key == RR.identifier:
            RR.update_params(val[0], val[1])
        elif key == RL.identifier:
            RL.update_params(val[0], val[1])
 
    for each in All_Tires:
        pygame.draw.rect(screen, each.get_color(), each.background_area)
        screen.blit(pfont.render(each.pressure(), 1, BLACK), each.pressure_pos)
        screen.blit(tfont.render(each.temperature(), 1, GREY), each.temperature_pos)
        screen.blit(status_font.render(each.tire_status(), 1, BLUE), each.status_pos)

    screen.blit(mazda, (screen_pixels.w/2 - car_pixels.w/2, 40))

    # print count
    # --- Drawing code should go here

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 10 frames per second
    clock.tick(30)

# Close the window and quit.
radio_dev.close()
pygame.quit()
