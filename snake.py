
import pygame
from pygame.locals import *
import time
import random

SIZE = 40
class Screen:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        # Although this is not necessary, I decided to express this way to show
        # Inheritance
class Mouse(Screen):
    def __init__(self, parent_screen):
        super().__init__(parent_screen)
        self.image = pygame.image.load("resources/mouse.png").convert() #image
        self.x = 120    # Starting Position X
        self.y = 120    # Staring Position Y

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip() # updates the content of the entire display to show new
                                # mouse position

    def move(self):
        self.x = random.randint(1,24)*SIZE      # moves the mouse randomly x axis
        self.y = random.randint(1,19)*SIZE      # moves the mouse randomly y axis

class Snake(Screen):
    def __init__(self, parent_screen):
        super().__init__(parent_screen)
        self.image2 = pygame.image.load("resources/ball.jpg").convert() #blocks
        self.image1 = pygame.image.load("resources/headright.png").convert()
        self.image3 = pygame.image.load("resources/headleft.png").convert() #heads
        self.image4 = pygame.image.load("resources/headup.png").convert()
        self.image5 = pygame.image.load("resources/headdown.png").convert()
        self.direction = 'right' # It will start moving towards the right
        self.length = 1 # starts with one block
        self.x = [400]  # Initial position x
        self.y = [400]  # Initial position y
        self.speed = 1
    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def slide(self):
        # updates body position
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update head position
        if self.direction == 'left':
            self.x[0] = (self.x[0] - SIZE)
        if self.direction == 'right':
            self.x[0] = (self.x[0] + SIZE)
        if self.direction == 'up':
            self.y[0] = (self.y[0] - SIZE)
        if self.direction == 'down':
            self.y[0] =(self.y[0] + SIZE)
        self.draw()

    def draw(self):
        #head
        if(self.direction == 'right'):
            self.parent_screen.blit(self.image1, (self.x[0], self.y[0]))
        elif(self.direction == 'left'):
            self.parent_screen.blit(self.image3, (self.x[0], self.y[0]))
        elif (self.direction == 'up'):
            self.parent_screen.blit(self.image4, (self.x[0], self.y[0]))
        elif (self.direction == 'down'):
            self.parent_screen.blit(self.image5, (self.x[0], self.y[0]))
        #body
        for i in range(1,self.length):
            self.parent_screen.blit(self.image2, (self.x[i], self.y[i]))

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game: # In charge of setting the rules and boundaries.
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")

        pygame.mixer.init()
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.mouse = Mouse(self.surface)
        self.mouse.draw()

    def reset(self):
        self.snake = Snake(self.surface)
        self.mouse = Mouse(self.surface)

    def collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def hitwall(self, x, y):
         if  x  > 1000 or x < 0:
           return True
         elif  y  < 0 or y > 800:
          return True
         else:
           return False

    def background(self):
        bg = (0, 150, 137)
        self.surface.fill(bg)

    def play(self):
        self.background()
        self.snake.slide()
        self.mouse.draw()
        self.score()
        pygame.display.flip()

        # snake eating mouse scenario
        if self.collision(self.snake.x[0], self.snake.y[0], self.mouse.x, self.mouse.y):
            self.snake.increase_length()
            self.mouse.move()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Collision Occurred"
        # snake hits wall
        if self.hitwall(self.snake.x[0], self.snake.y[0]):
                raise "Collision Occurred"

    def score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"SCORE: {self.snake.length}",True,(200,200,200))
        self.surface.blit(score,(850,10))

    def game_over(self):
        self.background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"You lost! ! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To go back to the menu  press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                        exec(open('menu.py').read())
                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                elif event.type == QUIT:
                    running = False
                    exec(open('menu.py').read())
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.game_over()
                pause = True
                self.reset()
            time.sleep(.25)
def main():
    game = Game()
    game.run()

main()