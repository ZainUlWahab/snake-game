import pygame,time
from sys import exit
from random import randint

def player_movement(movement_parameter):
    if movement_parameter == 0:
        player.x -=20
    elif movement_parameter == 1:
        player.x +=20
    elif movement_parameter == 2:
        player.y +=20
    elif movement_parameter == 3:
        player.y -=20


def boundary_check():
    if player.left <=-20:
        return 1
    if player.top <=-20:
        return 1
    if player.right >=820:
        return 1
    if player.bottom >=620:
        return 1
    else:
        return 0

def collision(score):
    if pygame.Rect.colliderect(player,food):
        pygame.mixer.Sound.play(soundeffect)
        food.x = randint(0,38) * 20
        food.y = randint(0,28) * 20
        player_list.append(pygame.rect.Rect(player.x,player.y,20,20))
        return score + 1
    return score

def self_collision():
    head = player_list[0]  # Get the head of the snake
    # Iterate through the segments of the snake starting from index 1
    for segment in player_list[1:]:
        if pygame.Rect.colliderect(head, segment):  # Check for collision
            return 1  # Return 1 if collision is detected
    return 0  # Return 0 if no collision is detected

pygame.init() 
width = 800
height = 600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock() # controls framerate
soundeffect = pygame.mixer.Sound('audio/eat_food.mp3')
#background
bg = pygame.image.load('bg/bg.png').convert_alpha()
bg = pygame.transform.scale(bg, (800,600))
bg_rect = bg.get_rect()
#Player shenanigans
player_sprite = pygame.image.load('graphics/snake_green_head.png').convert_alpha()
player_sprite = pygame.transform.scale(player_sprite, (20,20))
blop_sprite = pygame.image.load('graphics/snake_green_blob.png').convert_alpha()
blop_sprite = pygame.transform.scale(blop_sprite, (20,20))
player = pygame.rect.Rect(400,300,player_sprite.get_width(), player_sprite.get_height())
# movement_parameter --> 0 - left , 1 - right, 2 - down, 3 - up
movement_parameter = 0
horizontal_bool = 1
vertical_bool = 0
player_list = [player]
player_size = 1
game_over = 1
# Food/Nom
x_pos = randint(0,38) * 20
y_pos = randint(0,28) * 20
food_sprite = pygame.image.load('graphics/apple_red.png').convert_alpha()
food_sprite = pygame.transform.scale(food_sprite, (20,20))
food = pygame.rect.Rect(x_pos,y_pos,food_sprite.get_width(), food_sprite.get_height())
#Score
score = 0
font = pygame.font.Font('font/Pixeltype.ttf', 50)
text_color = 'Black'
score_text = font.render(f'Score : {score}',True, text_color)
score_text_Rect = score_text.get_rect()
score_text_Rect.x = 340
score_text_Rect.y = 20

#starting screen
starting_screen = pygame.image.load('bg/starting_screen.png').convert_alpha()
starting_screen_rect = starting_screen.get_rect()
start = 1
while True:
    if not game_over:
        start = 0
        font = pygame.font.Font('font/Pixeltype.ttf', 50)
        score_text_Rect.x = 340
        score_text_Rect.y = 20
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if not horizontal_bool:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        movement_parameter = 0
                        horizontal_bool,vertical_bool = 1,0
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        movement_parameter = 1
                        horizontal_bool,vertical_bool = 1,0
                        
                if not vertical_bool:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        movement_parameter = 2
                        vertical_bool,horizontal_bool = 1,0
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        movement_parameter = 3
                        vertical_bool,horizontal_bool = 1,0
        
        screen.blit(bg,bg_rect)
        score_text = font.render(f'Score : {score}', True, text_color)
        screen.blit(score_text, score_text_Rect)

        for i in range(len(player_list)):
            if i==0:
                screen.blit(player_sprite,player)
            else:
                screen.blit(blop_sprite,player_list[i])
            
        for i in range(len(player_list) - 1, 0, -1):
            player_list[i].x = player_list[i - 1].x
            player_list[i].y = player_list[i - 1].y
        screen.blit(food_sprite,food)
        player_movement(movement_parameter)
        game_over = boundary_check()
        if self_collision():
            game_over = 1
        score = collision(score)
        pygame.display.update()
        clock.tick(10) # set max framerate to 10
    else:
        if start:
            screen.blit(starting_screen,starting_screen_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_over = 0
            pygame.display.update()
            clock.tick(10) # set max framerate to 10
        else:
            movement_parameter = 0
            starting_screen = pygame.image.load('bg/ending_screen.png').convert_alpha()
            starting_screen_rect = starting_screen.get_rect()
            screen.blit(starting_screen,starting_screen_rect)
            #display score
            font = pygame.font.Font('font/Chewy-Regular.ttf', 100)
            score_text = font.render(f'Score : {score}', True, '#437456')
            score_text_Rect = score_text.get_rect()
            score_text_Rect.x = 250
            score_text_Rect.y = 20
            screen.blit(score_text, score_text_Rect)
            
            screen.blit(score_text, score_text_Rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    player.x = 400
                    player.y = 300
                    score = 0
                    food.x = randint(0,38) * 20
                    food.y = randint(0,28) * 20
                    player_list.clear()
                    player_list.append(player)
                    game_over = 0
            pygame.display.update()
            clock.tick(10) # set max framerate to 10
