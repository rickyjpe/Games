import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((1000, 800))
background = pygame.image.load("menu/background.jpeg").convert()
screen.blit(background,[0,0])
pygame.display.set_caption('The 2000s Throwback')
font = pygame.font.SysFont('Arial', 30)

# colors
background = pygame.image.load("resources/background.jpeg")
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
clicked = False

class button():
    # colours for button and text
    button_col = (255, 0, 0)
    text_col = black
    width = 180
    height = 70
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
    def draw_button(self):
        global clicked
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()
        # create pygame Rect object for the button
        button_rect = Rect(self.x, self.y, self.width, self.height)
        # check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
        else:
            pygame.draw.rect(screen, self.button_col, button_rect)
        # add text to button
        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 25))
        return action

snake = button(150, 600, 'Snake')
alien = button(650, 600, 'Doodle Jump')
quit = button(400, 700, 'Quit')
run = True

while run:
    if snake.draw_button():
        pygame.display.set_caption('Snake')
        exec(open('snake.py').read())
    if alien.draw_button():
        pygame.display.set_caption('DoodleJump')
        exec(open('DoodleJump.py').read())
    if quit.draw_button():
        pygame.quit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()

