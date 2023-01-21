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



class Player:
    def __init__(self , x , y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 70

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

class Axe:
    def __init__(self , x , y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.dirX = random.choice([-1,1])
        self.dirY = random.choice([-1,1])
        self.velX = randpm.randrange(2,7)
        self.velY = randpm.randrange(2,7)
        self.image = pygame.image.load("assets/axe.png") 

    def move():
        self.x = self.dirX * velX
        self.y = self.dirY * velY

    

def draw_screen(win,screentype):
    if screentype=="welcome":
        background = pygame.transform.scale( pygame.image.load("assets/bg.png"), (600,600))
        
        win.blit(background , (0 , 0))

        title = pygame.transform.scale( pygame.image.load("assets/title.png"), (350,50))
        win.blit(title , (WIN_WIDTH//2-180, WIN_HEIGHT//2-90))

        text = MSG_FONT.render(f"Press Enter to Start", 1 , (0,0,0))
        win.blit(text,(WIN_WIDTH//2 - 90, WIN_HEIGHT//2))
        
        pygame.display.update()


def draw(win , player , coins):
    background = pygame.transform.scale( pygame.image.load("assets/bg.png"), (600,600))
    win.blit(background , (0 , 0))

    player_sprite = pygame.transform.scale( player.image, (player.width,player.height))
    win.blit(player_sprite, (player.x , player.y))

    for coin in coins:
        coin_sprite = pygame.transform.scale( coin.image, (coin.width,coin.height))
        win.blit(coin_sprite, (coin.x , coin.y))

    pygame.display.update()


def handle_player_movement(keys , player):
    if keys[pygame.K_a] and player.x - 3 >= 0:
        player.move("left")
    if keys[pygame.K_d] and player.x + 3 <= WIN_WIDTH:
        player.move("right")
    if keys[pygame.K_w] and player.y - 3 >= 0:
        player.move("up")
    if keys[pygame.K_s] and player.y + 3 <= WIN_HEIGHT:
        player.move("down")


def handle_collision(player , coins):
    
    for i , coin in enumerate(coins , start=0):
        if player.x+50>=coin.x and player.x<=coin.x+30 and player.y<=coin.y+30 and player.y+70>=coin.y:
            coins.pop(i)
    
        


# MAIN FUNCTION
def main():
    run = True 
    gameover = 0
    level = 1
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

    while run:  # level loop
        if level == 1:
            player = Player(WIN_WIDTH//2 , WIN_HEIGHT//2)
            coins = []
            for i in range(2):
                coins.append(Coin(random.randrange(50,550) , random.randrange(50,550)))
        
        isrunning = True

        while isrunning:   # game screen loop
            clock.tick(60) 
            draw(WIN , player , coins)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            keys = pygame.key.get_pressed() 
            handle_player_movement(keys , player)
            handle_collision(player,coins) 

            # if len(birds)>0 and slingblade.shot == 0:
            #     gameover = 1
            #     isrunning = False
            
            # if level > 7 : 
            #     won = True
            #     isrunning = False

        # if gameover==1:
        #     while True:   # retry screen loop
        #         for event in pygame.event.get():
        #             if event.type == pygame.QUIT:
        #                 pygame.quit()
        #         retry_screen(WIN)
        #         keys = pygame.key.get_pressed() 
        #         if keys[pygame.K_RETURN]:
        #             break
        # if won :
        #     while True:   # won screen loop
        #         for event in pygame.event.get():
        #             if event.type == pygame.QUIT:
        #                 pygame.quit()
        #         win_screen(WIN)
        #     run = False    
        print("ee")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        

if __name__ == "__main__":
    main()