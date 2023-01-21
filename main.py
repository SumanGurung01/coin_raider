"""
    Date : Sat Jan 21 2023 22:27:05 GMT+0530 (India Standard Time)
    Author : Suman Gurung
    Description : Coin Raiders is a game created using pygame
"""

import pygame
from pygame import mixer
import random

pygame.init()

# CONSTANTS
WIN_HEIGHT,WIN_WIDTH = 600,600

WIN = pygame.display.set_mode((WIN_WIDTH , WIN_HEIGHT))
pygame.display.set_caption("One Stone Two Bird")

SCORE_FONT = pygame.font.SysFont("comicsans",25)
MSG_FONT = pygame.font.SysFont("comicsans" , 30)

# CLASSES
class Player:
    def __init__(self , x , y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 70
        self.out = 0

        PLAYERS = [[pygame.image.load("assets/player1L.png"),pygame.image.load("assets/player1R.png")] , [pygame.image.load("assets/player2L.png"),pygame.image.load("assets/player2R.png")] , [pygame.image.load("assets/player3l.png"),pygame.image.load("assets/player3R.png")]]

        self.player = random.choice(PLAYERS) 
        self.image =self. player[1]

    def move(self,direction):
        if direction == "left":
            self.x -= 3
            self.image = self.player[0]
        if direction == "right":
            self.x += 3
            self.image = self.player[1]
        if direction == "up":
            self.y -= 3 
        if direction == "down":
            self.y += 3

class Coin:
    def __init__(self , x , y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.image = pygame.image.load("assets/coin.png") 

class Fireball:
    def __init__(self):
        movement_info = [[[100,500],[-60,-50]] , [[650,660],[100,500]] , [[100,500],[650 , 660]] , [[-60,-50],[100,500]]]
        index = random.choice([0,1,2,3])   
        
        self.x = random.randrange(movement_info[index][0][0],movement_info[index][0][1])
        self.y = random.randrange(movement_info[index][1][0],movement_info[index][1][1])

        if index == 0 :
            self.dirX = random.choice([-1,1])
            self.dirY = 1
        elif index == 1:
            self.dirX = -1
            self.dirY = random.choice([-1,1])
        elif index == 2:
            self.dirX = random.choice([-1,1])
            self.dirY = -1
        elif index == 3:
            self.dirX = 1
            self.dirY = random.choice([-1,1])
        self.width = 50
        self.height = 50
        self.velX = random.randrange(2,5)
        self.velY = random.randrange(2,5)
        self.appear = 0
        self.degree = 0
        self.image = pygame.image.load("assets/fireball.png") 

    def move(self):
        self.x += self.dirX * self.velX
        self.y += self.dirY * self.velY

# SCREENS
def draw_screen(win,screentype):
    if screentype=="welcome":
        background = pygame.transform.scale( pygame.image.load("assets/bg.png"), (600,600))
        
        win.blit(background , (0 , 0))

        title = pygame.transform.scale( pygame.image.load("assets/title.png"), (350,50))
        win.blit(title , (WIN_WIDTH//2-180, WIN_HEIGHT//2-90))

        text = MSG_FONT.render(f"Press Enter to Start", 1 , (0,0,0))
        win.blit(text,(WIN_WIDTH//2 - 90, WIN_HEIGHT//2))
    
    if screentype=="retry":
        background = pygame.transform.scale( pygame.image.load("assets/bg.png"), (600,600))
        
        win.blit(background , (0 , 0))

        title = pygame.transform.scale( pygame.image.load("assets/gameover.png"), (350,50))
        win.blit(title , (WIN_WIDTH//2-180, WIN_HEIGHT//2-90))

        text = MSG_FONT.render(f"Press Enter to Continue", 1 , (0,0,0))
        win.blit(text,(WIN_WIDTH//2 - 120, WIN_HEIGHT//2))
    
    if screentype=="won":
        background = pygame.transform.scale( pygame.image.load("assets/bg.png"), (600,600))
        
        win.blit(background , (0 , 0))

        title = pygame.transform.scale( pygame.image.load("assets/youwin.png"), (350,50))
        win.blit(title , (WIN_WIDTH//2-180, WIN_HEIGHT//2-90))

        text = MSG_FONT.render(f"Created by Suman Gurung", 1 , (0,0,0))
        win.blit(text,(WIN_WIDTH//2 - 125, WIN_HEIGHT//2))
        
    pygame.display.update()

# DRAW SPRITES
def draw(win , player , coins , dangers , level):
    background = pygame.transform.scale( pygame.image.load("assets/bg.png"), (600,600))
    win.blit(background , (0 , 0))

    board = pygame.transform.scale( pygame.image.load("assets/board.png"), (100,40))
    win.blit(board , (500 , 0))

    board_text = SCORE_FONT.render(f"Level x {level}", 1 , (0,0,0))
    win.blit(board_text,(515, 12))


    player_sprite = pygame.transform.scale( player.image, (player.width,player.height))
    win.blit(player_sprite, (player.x , player.y))

    for coin in coins:
        coin_sprite = pygame.transform.scale( coin.image, (coin.width,coin.height))
        win.blit(coin_sprite, (coin.x , coin.y))

    for danger in dangers:
        danger_sprite = pygame.transform.scale( danger.image, (danger.width,danger.height))
        win.blit(danger_sprite, (danger.x , danger.y))
        danger.move()

    pygame.display.update()

# CONTROLS
def handle_player_movement(keys , player):
    if keys[pygame.K_a] and player.x - 3 >= 0:
        player.move("left")
    if keys[pygame.K_d] and player.x + 50 + 3 <= WIN_WIDTH:
        player.move("right")
    if keys[pygame.K_w] and player.y - 3 >= 0:
        player.move("up")
    if keys[pygame.K_s] and player.y + 70 + 3 <= WIN_HEIGHT:
        player.move("down")

def handle_collision(player , coins , dangers):
    for i , coin in enumerate(coins , start=0):
        if player.x+50>=coin.x and player.x<=coin.x+30 and player.y<=coin.y+30 and player.y+70>=coin.y:
            coins.pop(i)  
    for danger in dangers:
        if danger.x+25<WIN_WIDTH and danger.x+25>0 and danger.y+25<WIN_HEIGHT and danger.y+25>0:  
            danger.appear = 1
    for i,danger in enumerate(dangers , start=0):
        if danger.x+25>WIN_WIDTH or danger.x+25<0 or danger.y+25>WIN_HEIGHT or danger.y+25<0:  
            if danger.appear == 1:
                dangers.pop(i)
    for danger in dangers:
        if player.x <= danger.x+50 and player.x+50 >= danger.x and player.y <= danger.y+50 and player.y+70 >= danger.y:
            player.out = 1

# MAIN FUNCTION
def main():
    run = True 
    gameover = 0
    level = 1
    won = 0
    clock = pygame.time.Clock()

    while run:   # welcome screen loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        draw_screen(WIN , screentype = "welcome")
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_RETURN]:
            run = False    
    
    run = True

    player = Player(WIN_WIDTH//2 , WIN_HEIGHT//2)

    while run:  # level loop
        player.out = 0
        gameover = 0

        if level == 1:
            coins = []
            dangers = []
            for i in range(1):
                coins.append(Coin(random.randrange(50,550) , random.randrange(50,550)))
            for i in range(2):
                dangers.append(Fireball())

        if level == 2:
            coins = []
            dangers = []
            for i in range(2):
                coins.append(Coin(random.randrange(50,550) , random.randrange(50,550)))
            for i in range(4):
                dangers.append(Fireball())
        
        if level == 3:
            coins = []
            dangers = []
            for i in range(3):
                coins.append(Coin(random.randrange(50,550) , random.randrange(50,550)))
            for i in range(5):
                dangers.append(Fireball())
        
        if level == 4:
            coins = []
            dangers = []
            for i in range(4):
                coins.append(Coin(random.randrange(50,550) , random.randrange(50,550)))
            for i in range(6):
                dangers.append(Fireball())
        
        if level == 5:
            coins = []
            dangers = []
            for i in range(5):
                coins.append(Coin(random.randrange(50,550) , random.randrange(50,550)))
            for i in range(7):
                dangers.append(Fireball())

        if level == 6:
            coins = []
            dangers = []
            for i in range(6):
                coins.append(Coin(random.randrange(50,550) , random.randrange(50,550)))
            for i in range(7):
                dangers.append(Fireball())

        if level == 7:
            coins = []
            dangers = []
            for i in range(7):
                coins.append(Coin(random.randrange(50,550) , random.randrange(50,550)))
            for i in range(9):
                dangers.append(Fireball())

        isrunning = True

        danger_count = len(dangers)

        while isrunning:   # game screen loop
            clock.tick(60) 
            while len(dangers) != danger_count :
                dangers.append(Fireball())
            draw(WIN , player , coins , dangers , level)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            keys = pygame.key.get_pressed() 
            handle_player_movement(keys , player)
            handle_collision(player,coins,dangers) 

            if len(coins)==0 :
                level += 1 
                isrunning = False

            if player.out == 1:
                gameover = 1
                isrunning = False 
            
            if level > 7 : 
                won = True
                isrunning = False

        if gameover==1:
            while True:   # retry screen loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                draw_screen(WIN,screentype = "retry")
                keys = pygame.key.get_pressed() 
                if keys[pygame.K_RETURN]:
                    break
        
        if won :
            while True:   # won screen loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                draw_screen(WIN,screentype="won")
            run = False    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
if __name__ == "__main__":
    main()