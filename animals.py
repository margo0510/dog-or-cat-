import pygame 
from pygame.locals import *
import os 

pygame.mixer.init()
pygame.font.init()

pygame.init()


WIDTH, HEIGHT = 900,500
screen = pygame.display.set_mode((WIDTH, HEIGHT))

ANIMAL_WIDTH, ANIMAL_HEIGHT =  165,120

pygame.display.set_caption("Dog or Cat")


#color used through the game
WHITE = (255,255,255)
PINK = (255,192,203)
GREEN = (1,50,32)
PURPLE = (160, 32, 240)

BORDER = pygame.Rect(WIDTH//2 -5, 0, 10, HEIGHT)

BULLET_VEL = 7 
MAX_BULLETS = 3

FPS = 60 
VEL = 5

HEALTH_FONT = pygame.font.SysFont("Arial", 40)
WINNER_FONT = pygame.font.SysFont("Arial", 100)

DOG_HIT = pygame.USEREVENT+1
CAT_HIT = pygame.USEREVENT+2


dog_image = pygame.image.load(os.path.join("animal", "dog.png"))
dogy = pygame.transform.rotate(pygame.transform.scale(dog_image, (ANIMAL_WIDTH, ANIMAL_HEIGHT)),0)

cat_image = pygame.image.load(os.path.join("animal", "cat.png"))
caty = pygame.transform.rotate(pygame.transform.scale(cat_image, (ANIMAL_WIDTH, ANIMAL_HEIGHT)),0)



bg_image = pygame.transform.scale(pygame.image.load(os.path.join("animal", "forest.jpg")), (WIDTH,HEIGHT))



def draw_window(dog, cat, dog_bullets, cat_bullets, dog_health, cat_health):
    screen.blit(bg_image, (0,0))
    pygame.draw.rect(screen, GREEN, BORDER)
    dog_health_text = HEALTH_FONT.render("Health: " + str(dog_health), 1, PURPLE)
    cat_health_text = HEALTH_FONT.render("Health: " + str(cat_health), 1, PURPLE)
    screen.blit(dog_health_text, (WIDTH - dog_health_text.get_width()-10, 10))
    screen.blit(cat_health_text, (10,10))

    screen.blit(dogy, (dog.x, dog.y))
    screen.blit(caty, (cat.x, cat.y))

    for bullet in dog_bullets:
        pygame.draw.rect(screen, PINK, bullet )

    for bullet in cat_bullets:
        pygame.draw.rect(screen, PINK, bullet)

    pygame.display.update()



def dog_handle_movement(keys_pressed, dog):
    #using up, down, left and right arrow keys to move the dogy using dog 
    if keys_pressed[pygame.K_LEFT] and dog.x - VEL >BORDER.x + BORDER.width:
        dog.x -= VEL 
    if keys_pressed[pygame.K_UP] and dog.y - VEL >0:
        dog.y -= VEL
    if keys_pressed[pygame.K_RIGHT] and dog.x + VEL + dog.width < WIDTH:
        dog.x += VEL
    if keys_pressed[pygame.K_DOWN] and dog.y + VEL + dog.height < HEIGHT - 15 :
        dog.y += VEL    


def cat_handle_movement(keys_pressed, cat):
    #using a,w,s,d keys to move the caty using cat 
    if keys_pressed[pygame.K_a] and cat.x - VEL >0: 
        cat.x -= VEL
    if keys_pressed[pygame.K_w] and cat.y - VEL >0: 
        cat.y -= VEL
    if keys_pressed[pygame.K_d] and cat.x + VEL + cat.width < BORDER.x:
        cat.x += VEL
    if keys_pressed[pygame.K_s] and cat.y + VEL + cat.height < HEIGHT - 15:
        cat.y += VEL


def handle_bullets(cat_bullets, dog_bullets, cat, dog):
    for bullet in cat_bullets:
        bullet.x += BULLET_VEL
        if dog.colliderect(bullet):
            pygame.event.post(pygame.event.Event(DOG_HIT))
            cat_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            cat_bullets.remove(bullet) 
    for bullet in dog_bullets:
        bullet.x -= BULLET_VEL
        if cat.colliderect(bullet):
            pygame.event.post(pygame.event.Event(CAT_HIT))
            dog_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            dog_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, PURPLE)
    screen.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(4000)



def main():
    dog = pygame.Rect(700,300, ANIMAL_WIDTH, ANIMAL_HEIGHT)
    cat = pygame.Rect(100, 300, ANIMAL_WIDTH, ANIMAL_HEIGHT)
    dog_bullets = []
    cat_bullets = []
    dog_health = 10 
    cat_health = 10
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(cat_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(cat.x + cat.width, cat.y + cat.height//2, 10, 5)
                    cat_bullets.append(bullet)
                if event.key == pygame.K_RSHIFT and len(dog_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(dog.x, dog.y + dog.height//2, 10, 5)
                    dog_bullets.append(bullet)

            if event.type == DOG_HIT:
                dog_health -= 1
            if event.type == CAT_HIT:
                cat_health -= 1

        
        winner_text = ""
        if dog_health <= 0:
            winner_text = "caty wins dogy sorry"
        if cat_health <= 0:
            winner_text = "dogy wins cats lose!"
        if  winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        cat_handle_movement(keys_pressed, cat)
        dog_handle_movement(keys_pressed, dog)
        handle_bullets(cat_bullets, dog_bullets, cat, dog)
        draw_window(dog, cat, dog_bullets, cat_bullets, dog_health, cat_health)
        
    

if __name__ == "__main__":
    main()