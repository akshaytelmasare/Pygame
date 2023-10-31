import pygame
from globals import *

def draw_box(board,box,xpos,ypos,color):
    for y in range(len(box)):
        for x in range(len(box[0])):
            if(box[y][x]==1):
                pygame.draw.rect(board, color, pygame.Rect((x+xpos)*size, (y+ypos)*size, size, size))
    

def draw_gamestack(board,gmst):
    for y in range(height):
            for x in range(width):
                if(gmst[y][x]==1):
                    pygame.draw.rect(board, blue, pygame.Rect(x*size, y*size, size, size))
    

def draw_numbers(num):
    caption = 'Score = ' + str(num.score) + '; Level = ' + str(num.level)
    pygame.display.set_caption(caption)
