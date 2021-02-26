# import library

import pygame
import sys
import time
import random

# pygame models
pygame.init()

# variable
display_whdth = 288
display_height = 512
floor_x = 0
gravity = 0.25
bird_movement = 0
pipe_list = []
game_status = True
bird_list_index = 0
game_font = pygame.font.Font('assets/font/Flappy.TTF' , 20)
score = 0
high_score = 0
active_score = True
#-------------------------------------#
create_pipe = pygame.USEREVENT
create_flap = pygame.USEREVENT +1
pygame.time.set_timer( create_flap, 75)
pygame.time.set_timer( create_pipe, 1200)
#--------------------------------------------#
win_sound = pygame.mixer.Sound('assets/sound/smb_stomp.wav')
game_over_sound = pygame.mixer.Sound('assets/sound/smb_mariodie.wav')
#--------------------------------------------#

background_image = (pygame.image.load('assets/img/bg1.png'))
floor_image = (pygame.image.load('assets/img/floor.png'))
bird_image_down = (pygame.image.load('assets/img/red_bird_down_flap.png'))
bird_image_mid = (pygame.image.load('assets/img/red_bird_mid_flap.png'))
bird_image_up = (pygame.image.load('assets/img/red_bird_up_flap.png'))
bird_list =[bird_image_down, bird_image_mid, bird_image_up]
bird_image = bird_list[bird_list_index]
pipe_image = (pygame.image.load('assets/img/pipe_green.png'))
game_over_image = (pygame.image.load('assets/img/message.png'))
game_over_image_rect = game_over_image.get_rect(center= (144 , 256))
#--------------------------------------------#


def generate_pipe_rect():
    random_pipe = random.randrange(200 , 400)
    pipe_rect_top = pipe_image.get_rect(midbottom = (350,random_pipe - 150 ))
    pipe_rect_bottom = pipe_image.get_rect(midtop = (350,random_pipe))
    return pipe_rect_top , pipe_rect_bottom


def move_pipe_rect( pipes):
    for pipe in pipes:
        pipe.centerx -= 2.5 
    inside_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return inside_pipes 


def display_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            main_screen.blit(pipe_image , pipe)
        else:
            reversed_pipe = pygame.transform.flip(pipe_image ,False , True)
            main_screen.blit(reversed_pipe , pipe)


def check_collision(pipes):
    global active_score
    for pipe in pipes:
        if bird_image_rect.colliderect(pipe):
            game_over_sound.play()
            time.sleep(3)
            active_score = True
            return False
        if bird_image_rect.top <= -25 or bird_image_rect.bottom >=450 :
            game_over_sound.play()
            time.sleep(3)
            active_score = True
            return False
    return True

def bird_animition():
    new_bird = bird_list[bird_list_index] 
    new_bird_rect = new_bird.get_rect(center= (50 ,bird_image_rect.centery))
    return new_bird , new_bird_rect


def display_score(status):
    if status == 'active':
        text1 = game_font.render(str(score), False, (255, 255, 255))
        text1_rect = text1.get_rect(center=(144, 50))
        main_screen.blit(text1, text1_rect)
    if status == 'game_over':
        # SCORE
        text1 = game_font.render(f'Score : {score}', False, (255, 255, 255))
        text1_rect = text1.get_rect(center=(144, 50))
        main_screen.blit(text1, text1_rect)
        # HIGH SCORE
        text2 = game_font.render(f'HighScore : {high_score}', False, (255, 255, 255))
        text2_rect = text2.get_rect(center=(144, 425))
        main_screen.blit(text2, text2_rect)



def update_score():
    global score, high_score, active_score
    if pipe_list:
        for pipe in pipe_list:
            if 47 < pipe.centerx < 52  and active_score:
                win_sound.play()
                score += 1
                active_score = False
            if pipe.centerx < 0 :
                active_score = True

    if score > high_score:
        high_score = score
    return high_score

#---------------make-rect-------------------#
bird_image_rect = bird_image.get_rect(center=( 50 , 260))

# game display
main_screen = pygame.display.set_mode(( display_whdth, display_height))



# game time 
clock = pygame.time.Clock()

# game logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # end pygame
            pygame.quit()
            #termineat program
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 5
            if event.key == pygame.K_r and game_status == False:
                game_status = True 
                pipe_list.clear()
                bird_image_rect.center =(50 , 256 )
                bird_movement = 0
                score =0 
        if event.type == create_pipe:
            pipe_list.extend(generate_pipe_rect())
        if event.type == create_flap:
            if bird_list_index < 2 :
                bird_list_index += 1
            else:
                bird_list_index = 0

            bird_image , bird_image_rect = bird_animition()
            
            

    # display main screen
    main_screen.blit(background_image, (0, 0))


    if game_status:
        #check collision
        check_collision(pipe_list)
        # display bird image
        main_screen.blit(bird_image, bird_image_rect)
        #check coliision
        game_status = check_collision(pipe_list)
        # move pipes
        pipe_list = move_pipe_rect(pipe_list)
        display_pipes(pipe_list)
        #bird geravity and movement
        bird_movement += gravity
        bird_image_rect.centery += bird_movement
        #show score 
        update_score()  
        display_score('active')
    else:
        main_screen.blit(game_over_image , game_over_image_rect)
        display_score('game_over')

    
    # floot imge
    floor_x -= 1
    main_screen.blit(floor_image, (floor_x, 450))
    main_screen.blit(floor_image, (floor_x + 288, 450))
    if floor_x <= -288:
        floor_x = 0
    
    # display updarer
    pygame.display.update()
    # game speed
    clock.tick(90)