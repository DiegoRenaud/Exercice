import numpy as np
import random
import pygame
from utils import colors, sp



class Projectile:
    def __init__(self, width, height, speed, types):
        x = random.randint(0,width )
        if types == 1 : 
            icone = pygame.image.load('assets/externe.png')
            self.hauteur = 40
            self.largeur = 40
        elif types ==2 :
            icone = pygame.image.load('assets/infra.png')
            self.hauteur = 40
            self.largeur = 70
        elif types ==3 :
            icone = pygame.image.load('assets/mat_roulant.png')
            self.hauteur = 20
            self.largeur = 20
        elif types ==4 :
            icone = pygame.image.load('assets/voyageur.png')
            self.hauteur = 35
            self.largeur = 35
        elif types ==5 :
            icone = pygame.image.load('assets/trafic.png')
            self.hauteur = 20
            self.largeur = 20
        else :
            icone = pygame.image.load('assets/gestion_gare.png')
            self.hauteur = 20
            self.largeur = 20
        self.image = pygame.transform.scale(icone, (self.largeur, self.hauteur))

        self.pos = np.array([x, 0])
        self.speed = speed
        self.w = width
        self.h = height

        
    
    def update(self):
        self.pos[1] += self.speed
        
    def isCollision(self, player):
        # Si on est a la meme hauteur
        hautPlayer = player.pos[1] - player.hauteur/2
        basPlayer = player.pos[1] + player.hauteur/2
        hautProjectile = self.pos[1] - self.hauteur/2
        basProjectile = self.pos[1] + self.hauteur/2
        print("proj haut", hautProjectile)
        print("proj bas", basProjectile)
        print("player haut", hautPlayer)
        print("player bas", basPlayer)
        if basProjectile >= hautPlayer:
            # mais qu on est pas en dessous
            if hautProjectile <= basPlayer:
                print("collision1")
                # Si jamais il y a chevauchement
                posProjectileDroite = self.pos[0] + self.largeur/2
                posProjectileGauche = self.pos[0] - self.largeur/2
                posPlayerDroite = player.pos[0] + player.largeur/2
                posPlayerGauche = player.pos[0] - player.largeur/2
                #print("proj droite", posProjectileDroite)
                #print("proj gauche", posProjectileGauche)
                #print("player droite", posPlayerDroite)
                #print("player gauche", posPlayerGauche)
                if posPlayerDroite <= posProjectileDroite and posPlayerDroite >= posProjectileGauche:
                    #print("collision2")
                    return True
                if posPlayerGauche <= posProjectileDroite and posPlayerGauche >= posProjectileGauche:
                    #print("collision2")
                    return True
                if posPlayerGauche <= posProjectileGauche and posPlayerDroite >= posProjectileDroite:
                    #print("collision2")
                    return True

        return False
    
    def isOutOfScreen(self):
        if self.pos[1] > self.h:
            return True
        return False
    
    def draw_projectile(self, surface):
        surface.blit(self.image, (self.pos[0] - self.largeur/2, self.pos[1] - self.hauteur/2))
        #pygame.draw.circle(surface, colors.WHITE, (self.pos[0], self.pos[1]), 10)   
    
class Projectiles:
    def __init__(self, generationRate, nombreProjectilesMax, width, height):
        self.projectiles = []
        self.generationRate = generationRate
        self.nombreProjectilesMax = nombreProjectilesMax
        self.w = width
        self.h = height
    
    def update(self):
        i = 0
        for projectile in self.projectiles:
            projectile.update()
            if projectile.isOutOfScreen():
                self.projectiles.pop(i)
                i -= 1
            i+=1
        generation = random.randint(0, 99)/100
        if generation < self.generationRate and self.nombreProjectilesMax >= len(self.projectiles):
            speed = random.randint(5,10)
            #probas differentes en fonction de l'impact des causes sur le retard
            types = np.random.choice(list(range(1,7)), size=None, replace=True, p=[0.24,0.21,0.17,0.10,0.21, 0.07])
            self.projectiles.append(Projectile(self.w, self.h, speed, types))
        
    def gameOver(self, player):
        for projectile in self.projectiles:
            if projectile.isCollision(player):
                return True
        return False
    

    def draw_projectiles(self, surface):
        for projectile in self.projectiles:
            projectile.draw_projectile(surface)