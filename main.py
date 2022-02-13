import pygame
import sys
import random

# object used for bird handling

class GameObject:

    def __init__(self, image, height, speed):
        self.speed = speed
        self.image = image
        self.pos = image.get_rect().move(0, height)

    def move(self):
        self.pos = self.pos.move(0, self.speed)
        if self.pos.bottom < 0:
            pygame.quit()

    def moveUp(self):
        self.pos = self.pos.move(0, -15)
        if self.pos.right > 288:
            self.pos.left = 0

# handling bottom pipes

class pipeObject:

    def __init__(self, image, height, speed):
        self.speed = speed
        self.image = image
        self.pos = image.get_rect().move(600, height - random.randrange(160) - 80)

    def move(self):
        self.pos = self.pos.move(self.speed, 0)
        if self.pos.right < 0:
            self.pos.left = WIDTH
            self.pos.top = HEIGHT/2 + 100
            return 1
        return 0

# handling top pipes

class pipeObjectUp:
    def __init__(self, image, speed, lowerPipe):
        self.speed = speed
        self.image = image
        self.pos = image.get_rect().move(lowerPipe.pos.x, lowerPipe.pos.top - 850)

    def move(self, lowerPipe):
        self.pos = self.pos.move(self.speed, 0)
        if self.pos.right < 0:
            self.pos.left = lowerPipe.pos.left
            self.pos.top = lowerPipe.pos.top - 850

pygame.init()

WIDTH = 288*2
HEIGHT = 512*2
points = 0
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# loading images

background = pygame.image.load('./flappy-bird-assets/sprites/background-day.png').convert()
background = pygame.transform.scale2x(background)
bird = pygame.image.load("./flappy-bird-assets/sprites/redbird-midflap.png").convert()
bird = pygame.transform.scale2x(bird)
pipeDown = pygame.image.load("./flappy-bird-assets/sprites/pipe-green.png").convert()
pipeDown = pygame.transform.scale2x(pipeDown)
pipeUp = pygame.transform.rotate(pipeDown, 180)  # rotating bottom pipe as it can be top

# displaying text

font = pygame.font.Font('./font.woff', 100)
text = font.render(str(points), False, (255,255,255))
textRect = text.get_rect()
textRect.center = (144, 50)
# creating objects

birdObject = GameObject(bird, HEIGHT/2, 3)

pipesDown = []   # pipes down table
pipesDown.append(pipeObject(pipeDown, 600, -10))
pipesDown.append(pipeObject(pipeDown, 600, -10))
pipesDown[1].pos.x -= 380

pipesUp = []
pipesUp.append(pipeObjectUp(pipeUp, -10, pipesDown[0]))
pipesUp.append(pipeObjectUp(pipeUp, -10, pipesDown[1]))

canMove = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if canMove and event.type == pygame.KEYDOWN:
            birdObject.moveUp()

    for pipe in pipesDown:
        if pipe.pos.colliderect(birdObject.pos):
            canMove = False
            birdObject.speed = 15

    for pipe in pipesUp:
        if pipe.pos.colliderect(birdObject.pos):
            canMove = False
            birdObject.speed = 30

    screen.blit(background, (0, 0))
    birdObject.move()
    for i in range(0, len(pipesDown)):
        if pipesDown[i].move() and canMove:
            points += 1
            text = font.render(str(points), True, (255, 255, 255))
        screen.blit(pipesDown[i].image, pipesDown[i].pos)
        pipesUp[i].move(pipesDown[i])
        screen.blit(pipesUp[i].image, pipesUp[i].pos)


    screen.blit(birdObject.image, birdObject.pos)
    screen.blit(text, textRect)

    pygame.display.update()
    pygame.time.delay(80)
