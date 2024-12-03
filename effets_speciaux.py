import numpy 
import pygame
import random
from unit_Youdas import *
import time



#class effets_specieaux(Unit):
class draw_effets(Unit):
    def draw_hp(self, screen,color):
        return super().draw_hp(screen)
        """Affiche l'unité sur l'écran."""

        hp_x=random.randint(0,WIDTH )
        hp_y=random.randint(0,HEIGHT )
        if self.hp_regen== True :
            color = GREEN
     
        pygame.draw.circle(screen, color, (hp_x,hp_y), CELL_SIZE // 3)
    
        pass
    class eau (Unit):
        def __init__(self,screen, x, y,color):
            pygame.draw.rect(screen, color, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
          


def restor_hp(self):
        self.health = self.max_health   # Restaure les HP
        if self.health > self.max_health:
            self.health = self.max_health
        
def _regenerate_hp(self):
        while self.regeneration_active:
            Hp=self.health
            regen_amount = self.max_health * 0.05       # Régénère 5% des HP
            self.health = min(self.health + regen_amount, self.max_health)
            print(f"HP régénérés: {self.health-Hp}")
            time.sleep(5)  # Attente de 5 secondes

def stop_regeneration(self):
        """Arrête la régénération"""
        self.regeneration_active = False


def brulure(self):
        hp= self.health
        self.health -= self.max_health * 0.05 # Brûle 5% des HP
        print(f"HP brûlés: {hp-self.max_health}")
        time.sleep(5)





        


      