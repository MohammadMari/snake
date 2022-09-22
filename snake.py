from cmath import sqrt
from turtle import width
import pygame
import numpy
import random
import time

MAP_SIZE = 20 

class listNode:
    def __init__(self, snakeHead, f):
        self.snake = snakeHead
        self.f = f
    snake = (0,0)
    f = 0
    
def sorting(input):
    return input.f


def heuristic(snake, apple):
    pass

def aStar(snake, apple):
    pass
    


def moveSnake(snake, movePos, ate):
    # add the move pos to the head, and add that to the list
    snake.insert(0, ((snake[0][0] + movePos[0]) % MAP_SIZE, (snake[0][1] + movePos[1]) % MAP_SIZE))

    # if the snake eats, don't remove tail
    if not ate:
        snake.pop()
    return snake

def drawBoard(playGround, snake):
    #draw board and apple
    for x in range(MAP_SIZE):
        for y in range(MAP_SIZE):
            col = (255,255,255)
            if playGround[x][y] == 1:
                col = (255,100,100)

            pygame.draw.rect(screen, col, pygame.Rect((x * 50) + 2.5, (y * 50) + 2.5 ,45,45))

    # draw snake
    for pos in snake:
        col = (100,255,100)
        pygame.draw.rect(screen, col, pygame.Rect((pos[0] * 50) + 2.5, (pos[1] * 50) + 2.5 ,45,45))



playGround = numpy.zeros((MAP_SIZE, MAP_SIZE))

pygame.init()
size = width, height = MAP_SIZE * 50, MAP_SIZE * 50
screen = pygame.display.set_mode(size)
pygame.time.set_timer(24, 1000)

#randomly generate apple and snake head position.
apple = (random.randint(0,MAP_SIZE - 1), random.randint(0,MAP_SIZE - 1))
playGround[apple[0]][apple[1]] = 1

# this snake list is going to be a list of all the snake body
snake = [(random.randint(0,MAP_SIZE - 1), random.randint(0,MAP_SIZE - 1))]

snakeAte = False # did the snake eat an apple this move?
lost = False # have we lost the game?
movePos=[0,1] # position snake will be moving in
lastMove = movePos # we check this for to make sure we can move in a certain direction

while not lost:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN: # change movePos based off last key pressed. 
            if event.key == pygame.K_DOWN and lastMove != [0,-1]:
                movePos = [0, 1]
            elif event.key == pygame.K_UP and lastMove != [0,1]:
                movePos = [0, -1]
            elif event.key == pygame.K_RIGHT and lastMove != [-1,0]:
                movePos = [1, 0]
            elif event.key == pygame.K_LEFT and lastMove != [1,0]:
                movePos = [-1, 0]
        if event.type == 24:
            snake = moveSnake(snake, movePos, snakeAte)
            # Set lastMove because if a player clicks two different keys in the same move,
            # checking movePos will instead return the key the player last pressed instead 
            # of the direction the snake was moving
            lastMove = movePos 
            snakeAte = False     
            pygame.time.set_timer(24, 100)
        
    # check to see if the snake head is at the apple position 
    if (playGround[snake[0]] == 1):
        snakeAte = True
        playGround[snake[0]] = 0
        apple = (random.randint(0,MAP_SIZE - 1), random.randint(0,MAP_SIZE - 1))

        # make sure apple isn't spawning inside of the snake
        while apple in snake:
            apple = (random.randint(0,MAP_SIZE - 1), random.randint(0,MAP_SIZE - 1))
        playGround[apple[0]][apple[1]] = 1

    # check to see if the snake head has collided with its body.
    for x in range(1, len(snake)):
        if snake[x] == snake[0]:
            lost = True
            break


    drawBoard(playGround, snake)
    pygame.display.flip()