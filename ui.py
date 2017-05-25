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
screen_size = (600, 600)
car_pixels = [160,360]
screen = pygame.display.set_mode(screen_size)
 
pygame.display.set_caption("TPMS")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

PIXEL_MULT = 100
  
mazda = pygame.image.load('img\\mazda.png')
bg1   = pygame.image.load('img\\bg1.jpg')
bg2   = pygame.image.load('img\\bg2.jpg')
bg3   = pygame.image.load('img\\bg3.jpg')

pressure_font   = pygame.font.SysFont('arial', 60)
temperature_font = pygame.font.SysFont('arial', 20)

FL_rectangle   = (0,0,screen_size[0]/2,screen_size[1]/2)
FR_rectangle   = (screen_size[0]/2,0,screen_size[0]/2,screen_size[1]/2)
RL_rectangle   = (0,screen_size[1]/2,screen_size[0]/2,screen_size[1]/2)
RR_rectangle   = (screen_size[0]/2,screen_size[1]/2,screen_size[0]/2,screen_size[1]/2)

FL_Pressure    = pressure_font.render('FL', 1, WHITE)
FR_Pressure    = pressure_font.render('FR', 1, WHITE)
RL_Pressure    = pressure_font.render('RL', 1, WHITE)
RR_Pressure    = pressure_font.render('RR', 1, WHITE)

FL_Temperature = pressure_font.render('yy', 1, WHITE)



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
    pygame.draw.rect(screen, GREEN, FL_rectangle)
    pygame.draw.rect(screen, GREEN, FR_rectangle)
    pygame.draw.rect(screen, RED, RL_rectangle)
    pygame.draw.rect(screen, GREEN, RR_rectangle)
 
    screen.blit(mazda, (screen_size[0]/2-car_pixels[0]/2,100))
    
    screen.blit(FL_Pressure, (screen_size[0]*1/8, screen_size[1]/4))
    screen.blit(FR_Pressure, (screen_size[0]*3/4, screen_size[1]/4))
    screen.blit(RL_Pressure, (screen_size[0]*1/8, screen_size[1]*3/4))
    screen.blit(RR_Pressure, (screen_size[0]*3/4, screen_size[1]*3/4))
  
  
    # --- Drawing code should go here
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()