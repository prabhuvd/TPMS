'''
Created on May 15, 2017

@author: pdesai
'''
'''
Created on May 11, 2016

@author: pdesai
'''
 
import pygame
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

 
pygame.init()
 
# Set the width and height of the screen [width, height]
screen_size = ( 320, 240)
car_pixels = [86,189]
screen = pygame.display.set_mode(screen_size)
 
pygame.display.set_caption("Tire pressure monitor (Mazda 5 Sport:pdesai)")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

PIXEL_MULT = 100
  
mazda = pygame.image.load('img//mazda.png')
##bg1   = pygame.image.load('img//bg1.jpg')
##bg2   = pygame.image.load('img//bg2.jpg')
##bg3   = pygame.image.load('img//bg3.jpg')

pressure_font   = pygame.font.SysFont('arial', 60)
temperature_font = pygame.font.SysFont('arial', 20)

 
FL_rectangle   = (0,0,screen_size[0]/2,screen_size[1]/2)
FR_rectangle   = (screen_size[0]/2,0,screen_size[0]/2,screen_size[1]/2)
RL_rectangle   = (0,screen_size[1]/2,screen_size[0]/2,screen_size[1]/2)
RR_rectangle   = (screen_size[0]/2,screen_size[1]/2,screen_size[0]/2,screen_size[1]/2)

FL_pressure_pos = (screen_size[0]*1/8, screen_size[1]/4)
FR_pressure_pos = (screen_size[0]*3/4, screen_size[1]/4)
RL_pressure_pos = (screen_size[0]*1/8, screen_size[1]*3/4)
RR_pressure_pos = (screen_size[0]*3/4, screen_size[1]*3/4)


''' Global variables for pressure and color ''' 
fl=0
fr=0
rr=0
rl=0

fl_color=GREEN
fr_color=GREEN
rl_color=GREEN
rr_color=GREEN

def get_color(pressure):
    if (pressure > 40 or pressure <28):
        return RED
    else :
        return GREEN

    
def update_pressure(fl_pres,fr_pres,rl_pres,rr_pres):
    global fl, fr , rl,rr
    global fl_color, fr_color , rl_color,rr_color

    fl=str(fl_pres)
    fr=str(fr_pres)
    rl=str(rl_pres)
    rr=str(rr_pres)

    fl_color=get_color(fl_pres)
    fr_color=get_color(fr_pres)
    rl_color=get_color(rl_pres)
    rr_color=get_color(rr_pres)
 
 
FL_Temperature = pressure_font.render('yy', 1, WHITE)


count=0
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
    screen.fill((168,168,168))
    #screen.blit(bg3, (screen_size[0]/2-car_pixels[0]/2,0))

    if (count <500):
        update_pressure(27,35,35,35)
    elif(count >=500 and count<1000):
        update_pressure(35,27,35,35)
    elif(count >=1000 and count<1500):
        update_pressure(35,35,27,35)
    elif(count >=1500 and count<2000):
        update_pressure(35,27,35,27)
    elif(count >=2000 and count<2500):
        update_pressure(27,27,35,35)
    elif(count >=2500 and count<3000):
        update_pressure(27,27,27,27)
    else:
        count =0
    count=count+1

    
    pygame.draw.rect(screen, fl_color, FL_rectangle)
    pygame.draw.rect(screen, fr_color, FR_rectangle)
    pygame.draw.rect(screen, rl_color, RL_rectangle)
    pygame.draw.rect(screen, rr_color, RR_rectangle)
 
    screen.blit(mazda, (screen_size[0]/2-car_pixels[0]/2,25))
    
    screen.blit(pressure_font.render(fl, 1, WHITE),FL_pressure_pos)
    screen.blit(pressure_font.render(fr, 1, WHITE),FR_pressure_pos)
    screen.blit(pressure_font.render(rl, 1, WHITE),RL_pressure_pos)
    screen.blit(pressure_font.render(rr, 1, WHITE),RR_pressure_pos)

    
    print count
    # --- Drawing code should go here
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(100)
 
# Close the window and quit.
pygame.quit()
