# Imports
import pygame
import os
import sys

pygame.font.init()
pygame.mixer.init()

# Constants

# Sounds

BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('cowboysNThangs', "Assets", 'Gun+Silencer.mp3') )
END_SOUND = pygame.mixer.Sound(os.path.join('cowboysNThangs', "Assets", 'endingSound.mp3'))

# Creating window and its properties

WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cowboys N' Thangs!")

# Objects properties
# Size
COWBOY_WIDTH, COWBOY_HEIGHT = 55, 45

# Fonts

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# FPS
FPS = 60

# Velocities
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 6

# Colours

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('cowboysNThangs', 'Assets', 'background.jpg')), (WIDTH, HEIGHT))

# Creating our border

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# Creating our cowboy objects

LHS_HIT = pygame.USEREVENT + 1
RHS_HIT = pygame.USEREVENT + 2

COWBOY_LHS_IMAGE = pygame.image.load(os.path.join('cowboysNThangs','Assets' ,'cowboyLHS.png'))
COWBOY_LHS = pygame.transform.rotate(pygame.transform.scale(COWBOY_LHS_IMAGE, (COWBOY_WIDTH, COWBOY_HEIGHT)), 0)

COWBOY_RHS_IMAGE = pygame.image.load(os.path.join('cowboysNThangs','Assets' ,'cowboyRHS.png'))
COWBOY_RHS = pygame.transform.rotate(pygame.transform.scale(COWBOY_RHS_IMAGE, (COWBOY_WIDTH, COWBOY_HEIGHT)), 0)

# Functions

# Creates our main function
def main():

    # Creates our rectangles (of which represents our cowboys)
    LHS = pygame.Rect(100, 300, COWBOY_WIDTH, COWBOY_HEIGHT)
    RHS = pygame.Rect(700, 300, COWBOY_WIDTH, COWBOY_HEIGHT)

    # Health

    lhs_health = 10
    rhs_health = 10

    # Creates our bullets

    LHS_bullets = []
    RHS_bullets = []

    # Creates clock
    Clock = pygame.time.Clock()

    # Runs our game
    run = True
    while(run):
        


        # Sets our frames per seconds
        Clock.tick(FPS)

        # Runs our game
        for event in pygame.event.get():
          
          if event.type == pygame.QUIT:
                run = False
                sys.exit()

                

          if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_g and len(LHS_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(LHS.x + LHS.width, LHS.y + LHS.height//2 - 2, 10, 5)
                    BULLET_FIRE_SOUND.play()
                    LHS_bullets.append(bullet)
               if event.key == pygame.K_m and len(RHS_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(RHS.x , RHS.y + RHS.height//2 - 2, 10, 5)
                    BULLET_FIRE_SOUND.play()
                    RHS_bullets.append(bullet)
          
          if event.type == LHS_HIT:
                 lhs_health -= 1
            
          if event.type == RHS_HIT:
               rhs_health -= 1
     
      
        winner_text = ""
        if lhs_health <= 0:
             winner_text = "Right side wins!"
             END_SOUND.play()
          
    
        if rhs_health <= 0:
             winner_text = "Left side wins!"
             END_SOUND.play()
     
        if winner_text != "":
          draw_winner(winner_text)
          break

        # Calls all our sub functions
        keys_pressed = pygame.key.get_pressed()

        bullet_mechanics(LHS_bullets, RHS_bullets, LHS, RHS)

        LHS_handle_movement(keys_pressed, LHS)
        RHS_handle_movement(keys_pressed, RHS)

        draw_window(LHS, RHS, LHS_bullets, RHS_bullets, lhs_health, rhs_health)

    main()
     



# Draw our windows

def draw_window(LHS, RHS, LHS_bullets, RHS_bullets, lhs_health, rhs_health):
    WINDOW.blit(BACKGROUND, (0, 0))

    pygame.draw.rect(WINDOW, BLACK, BORDER)
    
    
    lhs_health_text = HEALTH_FONT.render("Health: " + str(lhs_health), 1, WHITE)
    rhs_health_text = HEALTH_FONT.render("Health: " + str(rhs_health), 1, WHITE)
    
    WINDOW.blit(rhs_health_text, (WIDTH - rhs_health_text.get_width() - 10, 10))
    WINDOW.blit(lhs_health_text, (10, 10))



    WINDOW.blit(COWBOY_LHS, (LHS.x, LHS.y))
    WINDOW.blit(COWBOY_RHS, (RHS.x, RHS.y))

    for bullet in LHS_bullets:
         pygame.draw.rect(WINDOW, YELLOW, bullet)
    
    for bullet in RHS_bullets:
         pygame.draw.rect(WINDOW, YELLOW, bullet)


    pygame.display.update() # Updates our display

def draw_winner(text):
     draw_text = WINNER_FONT.render(text, 1, WHITE)
     WINDOW.blit(draw_text, (WIDTH // 2 - draw_text.get_width() / 2, HEIGHT/2 - draw_text.get_height() / 2))

     pygame.display.update()
     pygame.time.delay(5000)

# Movement 

def LHS_handle_movement(keys_pressed, LHS):
        
        if keys_pressed[pygame.K_w] and LHS.y - VEL > 0:
             LHS.y -= VEL

        if keys_pressed[pygame.K_a] and LHS.x - VEL > 0: 
             LHS.x -= VEL

        if keys_pressed[pygame.K_s] and LHS.y + VEL + LHS.height < HEIGHT - 15: 
             LHS.y += VEL

        if keys_pressed[pygame.K_d] and LHS.x + LHS.width < BORDER.x: 
             LHS.x += VEL

def RHS_handle_movement(keys_pressed, RHS):
        
        if keys_pressed[pygame.K_UP] and RHS.y - VEL > 0:
             RHS.y -= VEL

        if keys_pressed[pygame.K_LEFT] and RHS.x - VEL > BORDER.x: 
             RHS.x -= VEL

        if keys_pressed[pygame.K_DOWN] and RHS.y + VEL + RHS.height < HEIGHT - 15: 
             RHS.y += VEL

        if keys_pressed[pygame.K_RIGHT] and RHS.x + RHS.width < WIDTH: 
             RHS.x += VEL

def bullet_mechanics(LHS_bullets, RHS_bullets, LHS, RHS):
    for bullet in LHS_bullets:
        bullet.x += BULLET_VEL
        if RHS.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RHS_HIT))
            LHS_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            LHS_bullets.remove(bullet)
        
    for bullet in RHS_bullets:
        bullet.x -= BULLET_VEL
        if LHS.colliderect(bullet):
            pygame.event.post(pygame.event.Event(LHS_HIT))
            RHS_bullets.remove(bullet)
        elif bullet.x < 0:
            RHS_bullets.remove(bullet)
     


# Run code

if __name__ == "__main__":
    main()