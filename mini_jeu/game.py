#from cgitb import reset
import os
#os.environ["SDL_VIDEODRIVER"] = "dummy"
from os import remove
from utils import colors, sp
import pygame
#from enum import Enum
#from collections import namedtuple
from player import Player
from projectiles import Projectiles, Projectile
import time
import numpy as np
import sys 


class world:
    def __init__(self, generationRate=0.1, nombreProjectilesMax=8, width=480, height=640):
        self.w = width
        self.h = height
        self.player = Player(height, width, 70, 40)
        self.projectiles = Projectiles(generationRate, nombreProjectilesMax, width, height)
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Train')
        self.clock = pygame.time.Clock()
        
    def _update_ui(self):
        self.display.fill(colors.GREY)
        self.player.draw(self.display)
        self.projectiles.draw_projectiles(self.display)
        pygame.display.flip()
    
    def play_step_and_draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        action = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            action = -10
        if keys[pygame.K_RIGHT]:
            action = 10

                
        self.player.updatePos(action)
        self.projectiles.update()
        gameOver = self.projectiles.gameOver(self.player)

        self._update_ui()
        self.clock.tick(sp.SPEED)
         
        return gameOver

    #def go_screen(self):
        #my_font = pygame.font.SysFont('Comic Sans MS', 30)
        #text = my_font.render('GAME OVER', True, (255, 255, 255))
        #self.display.blit(text, (50,50))
        #pass
    
if __name__ == '__main__':
    game = world()
    
    #game loop
    while True:
        game_over = game.play_step_and_draw()
    #    
        if game_over == True:
            break     
    pygame.quit()
    
    
    