import pygame
import random
import time
from pygame.locals import *

SIZE = 40
COLOR = (20,55,112)

class Snake:
    def __init__(self, background, snake_lenght):
        self.lenght = snake_lenght
        self.main_screen = background
        self.snake_part = pygame.image.load("data/block.jpg").convert()
        self.x = [SIZE] * snake_lenght
        self.y = [SIZE] * snake_lenght
        self.direct = "down"
    
    def len_increase(self):
        self.lenght +=1
        self.x.append(-1)
        self.y.append(-1)
        
    def move_left(self):
        self.direct = "left"
        
    def move_up(self):
        self.direct = "up"
        
    def move_down(self):
        self.direct = "down"
        
    def move_right(self):
        self.direct = "right"
        
    def move(self):
        for i in range(self.lenght - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
            
        if self.direct == "up":
            self.y[0] -= SIZE
            
        if self.direct == "left":
            self.x[0] -= SIZE
            
        if self.direct == "down":
            self.y[0] += SIZE
            
        if self.direct == "right":
            self.x[0] += SIZE
            
        self.draw()
        
        
    def draw(self):
        self.main_screen.fill(COLOR)
        for i in range(self.lenght): 
            self.main_screen.blit(self.snake_part, (self.x[i], self.y[i]))
        pygame.display.flip()
        
class Watermellon:
    def __init__(self, main_screen):
        self.watermellon = pygame.image.load("data/watermellon.jpg").convert()
        self.screen = main_screen
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 19) * SIZE
        
    def draw(self):
        self.screen.blit(self.watermellon, (self.x, self.y))
        pygame.display.flip()
    
    def transport(self):
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 19) * SIZE
        

class Run:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Snake")
        self.music()
        self.background = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.background, 1)
        self.snake.draw()
        self.watermellon = Watermellon(self.background)
        self.watermellon.draw()
    
    def play(self):
        self.snake.move()
        self.watermellon.draw()
        self.score()
        pygame.display.flip()
        
        #collision with food
        if self.coll(self.snake.x[0], self.snake.y[0], self.watermellon.x, self.watermellon.y):
            eat = pygame.mixer.Sound("data/ding.mp3")
            pygame.mixer.Sound.play(eat)
            self.watermellon.transport()
            self.snake.len_increase()
            
            
        #collision with snake
        for i in range(2, self.snake.lenght): 
            if self.coll(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                crash = pygame.mixer.Sound("data/crash.mp3")
                pygame.mixer.Sound.play(crash)
                raise "Collision"
            
        #collision with border
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 1000):
            crash = pygame.mixer.Sound("data/crash.mp3")
            pygame.mixer.Sound.play(crash)
            raise "Hit the boundry error"      
          
    def music(self):
        pygame.mixer.music.load("data/music.mp3")
        pygame.mixer.music.play()
        
    def score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.lenght - 1}",True,(200,200,200))
        self.background.blit(score,(850,10))
      
    def coll(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:  
            if y1 >= y2 and y1 < y2 + SIZE: 
                return True
        return False
    
    def reset_game(self):
        self.snake = Snake(self.background, 1)
        self.watermellon = Watermellon(self.background)
        
    def game_over_msg(self): # shows msg after collision 
        self.background.fill(COLOR)
        font = pygame.font.SysFont('arial',30)
        line1 = font.render(f"Your score is: {self.snake.lenght - 1}",True,(200,200,200))
        self.background.blit(line1, (200,300))
        line2 = font.render(f"To play again press R. To exit press Escape.",True,(200,200,200))
        self.background.blit(line2, (200, 350))
        pygame.display.flip()
        pygame.mixer.music.pause()
        
    
    def run(self):
        started = True
        stop = False
        while started:
            for i in pygame.event.get():
                if i.type == KEYDOWN:
                    if i.key == K_ESCAPE: #closes the program on pressing ESCAPE button
                        started = False
                    
                    if i.key == K_r: #restarts the game
                        stop = False
                        pygame.mixer.music.unpause()
                        
                    if not stop:  
                        if i.key == K_UP:
                            self.snake.move_up()
                            
                        if i.key == K_DOWN:
                            self.snake.move_down()
                            
                        if i.key == K_LEFT:
                            self.snake.move_left()
                            
                        if i.key == K_RIGHT:
                            self.snake.move_right()
                        
                elif i.type == QUIT: # closes the program on pressing EXIT button
                    started = False
            
            try:
                if not stop:
                    self.play()
                    
            except Exception as e:
                self.game_over_msg()
                stop = True
                self.reset_game()
            
            time.sleep(0.2)
    
if __name__ == "__main__": 
    game = Run()
    game.run()