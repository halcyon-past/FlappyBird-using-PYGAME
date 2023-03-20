import pygame, os, random,sys

def draw_floor():
    WIN.blit(floor_surface,(floor_x_pos,620))
    WIN.blit(floor_surface,(floor_x_pos+576,620))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos-150))
    
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 720:
            WIN.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            WIN.blit(flip_pipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
            
    if bird_rect.top <= -100 or bird_rect.bottom >= 620:
        die_sound.play()
        return False
        
    else:
        return True
            
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement*3,1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect
    
def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,30))
        WIN.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render("Score: "+str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,30))
        WIN.blit(score_surface,score_rect)

        gameover = game_font2.render("GAME OVER",True,(255,255,255))
        gameover_rect = gameover.get_rect(center = (288,310))
        WIN.blit(gameover,gameover_rect)

        gameovertext = game_font3.render("PRESS 'ENTER' TO CONTINUE",True,(255,255,255))
        gameovertext_rect = gameovertext.get_rect(center = (288,380))
        WIN.blit(gameovertext,gameovertext_rect)

        high_score_surface = game_font.render("High Score: "+str(int(high_score)),True,(255,255,255))
        high_score_rect = score_surface.get_rect(center = (280/2+100,590))
        WIN.blit(high_score_surface,high_score_rect)

def update_score(score):
    f = open("marks.txt","r")
    high_score = f.read()
    f.close()
    if int(score) > int(high_score):
        high_score = score
        f = open("marks.txt","w")
        f.write(str(int(high_score)))
        f.close()
    return high_score
        
pygame.init()

WIN = pygame.display.set_mode((576,720))
pygame.display.set_caption("Aritro's Flappy Bird!!!")
pygame.display.set_icon(pygame.image.load("favicon.ico"))
clock = pygame.time.Clock()
game_font = pygame.font.SysFont('comicsans',60)
game_font2 = pygame.font.SysFont('comicsans',120)
game_font3 = pygame.font.SysFont('comicsans',40)

#game variables
FPS = 60
gravity = 0.1
bird_movement = 0
game_active = True
score  = 0
high_score = 0

bg_surface = pygame.image.load(os.path.join("sprites","background-day.png")).convert()
bg_surface = pygame.transform.scale(bg_surface,(576,720))

floor_surface = pygame.image.load(os.path.join("sprites","base.png")).convert()
floor_surface = pygame.transform.scale(floor_surface,(576,100))
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load(os.path.join("sprites","bluebird-downflap.png")).convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load(os.path.join("sprites","bluebird-midflap.png")).convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load(os.path.join("sprites","bluebird-upflap.png")).convert_alpha())
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,360))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

#bird_surface = pygame.image.load(os.path.join("sprites","bluebird-midflap.png")).convert_alpha()
#bird_surface = pygame.transform.scale2x(bird_surface)
#bird_rect = bird_surface.get_rect(center = (100,360))

pipe_surface = pygame.image.load(os.path.join("sprites","pipe-green.png")).convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,2000)
pipe_height = [200,300,400]

flap_sound = pygame.mixer.Sound(os.path.join('audio','wing.wav'))
die_sound = pygame.mixer.Sound(os.path.join('audio','die.wav'))
hit_sound = pygame.mixer.Sound(os.path.join('audio','hit.wav'))
score_sound = pygame.mixer.Sound(os.path.join('audio','point.wav'))
score_sound_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == True:
                bird_movement = 0
                bird_movement -= 5
                flap_sound.play()
            if event.key == pygame.K_RETURN and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,360)
                bird_movement = 0
                score = 0
                
                
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface,bird_rect = bird_animation()

    WIN.blit(bg_surface,(0,0))

    if game_active:
    #bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        WIN.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)

    #pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        high_score = update_score(score)
        score_display('game_over')
        

#floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    credits = game_font3.render("Game Developed by Aritro Saha",True,(255,255,255))
    credits_rect = credits.get_rect(center = (288,700))
    WIN.blit(credits,credits_rect)

    pygame.display.update()
    clock.tick(120)
            
            
    
