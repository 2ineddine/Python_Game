import pygame
from unit import * 
from abc import ABC, abstractmethod

class GridCell(ABC):
    def __init__(self, x, y, color=None ):
        self.x = x
        self.y = y
        self.color = color or (169, 169, 169) 
        self.image = None  # Par défaut, aucune image
    
    def set_image(self, image_path):
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        except pygame.error as e:
            print(f"Erreur de chargement d'image : {e}")
            self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
            self.image.fill((255, 0, 0))  # Rouge pour signaler une erreur

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        else:
            rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, self.color, rect)      
    
    @abstractmethod
    def on_interact(self, unit):
        """
        Interaction par défaut : ne fait rien. Les sous-classes peuvent la surcharger.
        """
        pass


class WallCell(GridCell):
    """
    Représente une cellule de type mur sur la grille.
    """
    def __init__(self, x, y, color=(169, 169,169)):  # Par défaut, mur en vert
        super().__init__(x, y, color)  # Initialisation de GridCell
        self.block_movement = True  # Le mur bloque le déplacement
    
    def on_interact(self, unit):
        """
        Interaction avec une unité. Les murs bloquent simplement le mouvement.
        """
        print(f"L'unité {unit.name} a tenté d'entrer dans un mur à ({self.x}, {self.y}). Mouvement bloqué.")
        
        
class PoisonCell (GridCell):
    def __init__(self,x,y):
        super.__init__(x,y)

    def on_interact(self, unit):
        #Applique l'effet poison
        print("Effet poison appliqué sur l'unité !")
        
#Autre type de cases mais plus necessaire