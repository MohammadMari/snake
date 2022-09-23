from cmath import sqrt
from heapq import heappush
from itertools import count
from operator import truediv
from turtle import width
import pygame
import numpy
import random

MAP_SIZE = 20 

playGround = numpy.zeros((MAP_SIZE, MAP_SIZE))

pygame.init()
size = width, height = MAP_SIZE * 50, MAP_SIZE * 50
screen = pygame.display.set_mode(size)
pygame.time.set_timer(24, 100)

#randomly generate apple and snake head position.
apple = (random.randint(0,MAP_SIZE - 1), random.randint(0,MAP_SIZE - 1))
playGround[apple[0]][apple[1]] = 1

# this snake list is going to be a list of all the snake body
snake = [(random.randint(0,MAP_SIZE - 1), random.randint(0,MAP_SIZE - 1))]

snakeAte = False # did the snake eat an apple this move?
lost = False # have we lost the game?
movePos=[0,1] # position snake will be moving in
lastMove = movePos # we check this for to make sure we can move in a certain direction


class listNode:
    def __init__(self, h, g, pos):
        self.pos = (pos[0],pos[1])
        self.f = h + g
        self.h = h
        self.g = g
    snake = (0,0)
    f = 0
    h = 0
    g = 0

# used to sort openNodes array from least to greatest F.
def sorts(node):
    return(node.f)

# g cost
def distanceFromSnake(node):
    return abs(node[0] - snake[0][0]) + abs(node[1] - snake[0][1])

# h cost
def heuristic(node):
    return abs(node[0] - apple[0]) + abs(node[1] - apple[1])


openNodes = []
closedNodes = []

def exploreSurounding(node):

    # for loop to hit surrounding nodes
    for x in range(-1,2):
        for y in range(-1, 2):

            # if both X and Y are not equal to 0, that means we are going diagonal
            # continue pls
            if x and y:
                continue

            # make sure we are actually in the map
            if (x + node.pos[0]) < 0 or (x+node.pos[0]) >= MAP_SIZE:
                continue
            if (y+ node.pos[0]) < 0 or (y + node.pos[1]) >= MAP_SIZE:
                continue

            # can't hit a border
            if ((x + node.pos[0], y + node.pos[1]) in snake):
                continue

            # make sure its not in closed nodes as well
            for n in closedNodes:
                if ((x + node.pos[0], y + node.pos[1]) == n.pos):
                    continue

            # so right here, im pretty sure i'm supposed to see if its already in openlist
            # now the problem is, evertime I try to do it, it just freezes.
            # thats a later problem for now
            tempNode = listNode(heuristic((x + node.pos[0], y + node.pos[1])), node.g + 1, (node.pos[0] + x, node.pos[1] + y))

            # this completely breaks everything
            # its 8 AM and I can't be bothered to fix it rn
            # for x in range(len(openNodes)):
            #     if (tempNode.pos[0] == openNodes[x].pos[0] and tempNode.pos[1] == openNodes[x].pos[1]):
            #         if openNodes[x].g < tempNode.g:
            #             print("WOOOW")

            openNodes.append(tempNode)



def aStar(node):
    # probably shouldn't clear it and just use the path we have already created.
    # but right now with the way things are setup it breaks things.
    # temporary fix for now
    openNodes.clear()
    closedNodes.clear()
    path = []

    # we need a node to begin
    if (len(openNodes) == 0): 
        openNodes.append(listNode(heuristic(node), distanceFromSnake(node), (node[0], node[1])))
        openNodes[0].f = 0


    while len(openNodes) > 0:
        # sort by lowest F. Put it at the back
        openNodes.sort(key=sorts, reverse=True)

        # take current node, add it to closedNodes
        curNode = openNodes.pop()
        closedNodes.append(curNode)

        # if this is the position for apple, cool, we are done
        if curNode.pos == apple:
            break

        # here we take the end of closedNodes 
        exploreSurounding(curNode)

        # temporary fix for a dumb crash
        if (len(closedNodes) > 200):
            break


    
        


def moveSnake(movePos, ate):
    # add the move pos to the head, and add that to the list
    snake.insert(0, ((snake[0][0] + movePos[0]) % MAP_SIZE, (snake[0][1] + movePos[1]) % MAP_SIZE))

    # if the snake eats, don't remove tail
    if not ate:
        snake.pop()
    return snake

def drawBoard():
    #draw board and apple            
    for x in range(MAP_SIZE):
        for y in range(MAP_SIZE):
            col = (255,255,255)
            if playGround[x][y] == 1:
                col = (255,100,100)

            pygame.draw.rect(screen, col, pygame.Rect((x * 50) + 2.5, (y * 50) + 2.5 ,45,45))
            # label = my_font.render(str(exploreNode((x,y), apple, snake)), 1, col2)
            # screen.blit(label, ((x * 50) + 5, (y * 50) + 5))
    
    
    # draw snake
    for pos in snake:
        col = (100,255,100)
        pygame.draw.rect(screen, col, pygame.Rect((pos[0] * 50) + 2.5, (pos[1] * 50) + 2.5 ,45,45))


    # debugging stuff down here 
    col3 = (1,100,200)
    col4 = (200,100,200)

    for n in openNodes:
        pygame.draw.rect(screen, col3, pygame.Rect((n.pos[0] * 50) + 2.5, (n.pos[1] * 50) + 2.5 ,45,45))
    for n in closedNodes:
        pygame.draw.rect(screen, col4, pygame.Rect((n.pos[0] * 50) + 2.5, (n.pos[1] * 50) + 2.5 ,45,45))


while not lost:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
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
            snake = moveSnake(movePos, snakeAte)
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

    # run aStar
    aStar(snake[0])
    # set movePos to the first closedNode.
    movePos = (closedNodes[1].pos[0] - snake[0][0], closedNodes[1].pos[1] - snake[0][1])

    drawBoard()
    pygame.display.flip()