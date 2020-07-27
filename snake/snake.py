import pygame
import random
import math
pygame.mixer.init()
pygame.init()

#GAME VARIABLES
WIDTH = 800
HEIGHT = 600
FPS = 25

#FONTS
FONT = pygame.font.SysFont('Cambria', 30, True)
GAMEFONT = pygame.font.SysFont('Algerian', 35, True, True)

#COLORS   #R    #G    #B
RED    =  (255,   0,   0)
BLACK  =  (0  ,   0,   0)
WHITE  =  (255, 255, 255)
RANDOM =  (128, 128, 255)
ORANGE  = (200, 128,   0)

#WINDOW
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SNAKE")
icon = pygame.image.load('SNAKE.png')
pygame.display.set_icon(icon)

#CLOCK
clock = pygame.time.Clock()

#BACKGROUND IMAGE
bg = pygame.image.load('background.jpg')
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT)).convert_alpha()

#MUSIC
music = pygame.mixer.music.load('background.mp3')
pygame.mixer.music.play(-1)
hitSound = pygame.mixer.Sound('beep.wav')
gameOverSound = pygame.mixer.Sound('gameover.wav')

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 8
        self.dirX = 0
        self.dirY = 0
        self.hitbox = (self.x, self.y, self.width + 1, self.height + 1)
        self.head = []
        self.lst = []
        self.len = 1
        self.score = 0
        fh = open('highscore.txt', 'r')
        self.h_score = fh.read()

    def draw(self, win):
        pygame.draw.rect(win, RED, (self.x, self.y, self.width, self.height))
        self.hitbox = (self.x, self.y, self.width + 1, self.height + 1)
        pygame.draw.rect(win, WHITE, self.hitbox, 1)


class food(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True

    def draw(self, win):
        if self.visible:
            food1 = pygame.image.load('apple.png')
            win.blit(food1, (self.x, self.y))
        else:
            food1 = pygame.image.load('apple.png')
            win.blit(food1, (self.x, self.y))

def ifHit(SNAKE, APPLE):
    distance = math.sqrt(((SNAKE.x - APPLE.x) ** 2) + ((SNAKE.y - APPLE.y) ** 2))
    if distance <= 15:
        return True
    return False

def drawSNAKE(SNAKE):
    for x, y in SNAKE.lst:
        pygame.draw.rect(win, RED, (x, y, SNAKE.width, SNAKE.height))
        SNAKE.hitbox = (x, y, SNAKE.width + 1, SNAKE.height + 1)
        pygame.draw.rect(win, BLACK, SNAKE.hitbox, 1)

def checkLoss(SNAKE):
    if SNAKE.x >= WIDTH or SNAKE.x <= 0 or SNAKE.y >= HEIGHT or SNAKE.y <= 0:
        return True
    elif SNAKE.head in SNAKE.lst[:-1]:
        return True

def textScore(text, color, x, y):
    screen_text = FONT.render(text, 1, color)
    win.blit(screen_text, (x, y))

def textScreen(text, color, x, y):
    screen_text = GAMEFONT.render(text, 1, color)
    win.blit(screen_text, (x, y))

def gameOverDisplay(SNAKE):
    win.fill(ORANGE)
    pygame.time.wait(1000)
    textScore('Score:' + str(SNAKE.score), WHITE, 10, 10)
    textScore('High Score:' + str(SNAKE.h_score),WHITE, WIDTH - 250, 10)
    textScreen('GAME OVER', WHITE, WIDTH/2 - 100, HEIGHT/2)
    textScreen('PRESS ENTER TO RESTART', WHITE, WIDTH/2 - 200, HEIGHT/2 + 50)
    fh = open('highscore.txt', 'w')
    fh.write(str(SNAKE.h_score))

def gameStartDisplay(SNAKE):
    win.blit(bg, (0, 0))
    SNAKE.draw(win)
    APPLE.draw(win)
    drawSNAKE(SNAKE)
    textScore('Score:' + str(SNAKE.score), WHITE, 10, 10)
    textScore('High Score:' + str(SNAKE.h_score), WHITE, WIDTH - 250, 10)

def redrawGameWindow():
    gameStartDisplay(SNAKE)
    game_over = checkLoss(SNAKE)
    if game_over:
        gameOverSound.play()
        gameOverDisplay(SNAKE)
    pygame.display.update()

#OBJECTS
SNAKE = player(WIDTH/2, HEIGHT/2, 30, 30)
APPLE = food(random.randint(WIDTH * 0.25, WIDTH * 0.75), random.randint(HEIGHT * 0.25, HEIGHT * 0.75), 24, 24)

def startGame():
    exit_game = False
    while not exit_game:
        win.fill(RANDOM)
        textScreen("WELCOME TO SNAKES", BLACK, WIDTH/2 -150, HEIGHT/2)
        textScreen("PRESS SPACE TO PLAY", BLACK, WIDTH/2 - 160, HEIGHT/2 + 40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()

        pygame.display.update()
        clock.tick(FPS)

def main():
    run = True
    exit_game = False
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            SNAKE.dirY = 0
            SNAKE.dirX = -SNAKE.vel
        if keys[pygame.K_RIGHT]:
            SNAKE.dirY = 0
            SNAKE.dirX = SNAKE.vel
        if keys[pygame.K_UP]:
            SNAKE.dirX = 0
            SNAKE.dirY = -SNAKE.vel
        if keys[pygame.K_DOWN]:
            SNAKE.dirX = 0
            SNAKE.dirY = SNAKE.vel
        if keys[pygame.K_RETURN]:
            SNAKE.x = WIDTH/2
            SNAKE.y = HEIGHT/2
            SNAKE.score = 0
            SNAKE.len = 1
            SNAKE.lst = []
            SNAKE.head = []
            redrawGameWindow()

        SNAKE.x += SNAKE.dirX
        SNAKE.y += SNAKE.dirY

        collision = ifHit(SNAKE, APPLE)
        if collision:
            APPLE.x = random.randint(0, WIDTH - 24)
            APPLE.y = random.randint(50, HEIGHT - 24)
            APPLE.visible = False
            SNAKE.score += 10
            SNAKE.len += 3
            if SNAKE.score > int(SNAKE.h_score):
                SNAKE.h_score = SNAKE.score
            hitSound.play()

        SNAKE.head = []
        SNAKE.head.append(SNAKE.x)
        SNAKE.head.append(SNAKE.y)
        SNAKE.lst.append(SNAKE.head)

        if len(SNAKE.lst) >= SNAKE.len:
            del SNAKE.lst[0]

        redrawGameWindow()

    pygame.quit()

startGame()
