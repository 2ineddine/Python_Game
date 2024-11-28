import pygame
import os

GRID_SIZE = 25
CELL_SIZE = 25
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE






class GridCell:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
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
    
    def on_interact(self, unit):
        """
        Interaction par défaut : ne fait rien. Les sous-classes peuvent la surcharger.
        """
        pass
    
class NormalCell(GridCell):
    def __init__(self, x, y, image_path):
        super().__init__(x, y, image_path)  # Appeler le constructeur de la classe parente
        self.type = "normal"  # Définir le type de la cellule comme "normal"
        self.load_image(image_path)  # Appeler la méthode pour charger l'image

    def load_image(self, image_path):
        try:
            
            self.image = pygame.image.load(image_path).convert_alpha()  # Charger l'image avec transparence
            self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))  # Redimensionner l'image pour correspondre à la taille de la cellule
            
        except Exception as e:
            print(f"Error loading image: {e}")  # Afficher l'erreur si l'image ne peut pas être chargée
            self.image = None  # Si l'image ne peut pas être chargée, assigner None

    
    
    
    
    
    
    


class PoisonCell(GridCell):
    def __init__(self, x, y, image_path):
        super().__init__(x, y, (152,200,2))
        self.type = "poison"
        self.load_image(image_path)
        
    def load_image(self, image_path):
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))  # Redimensionner l'image
        except Exception as e:
            print(f"Error loading image: {e}")
            self.image = None  # Aucune image en cas d'erreur
    def on_interact(self, unit):
        pass
        

class SpeedUpCell(GridCell):
    def __init__(self, x, y, image_path):
        # Charge une image spécifique pour la cellule de vitesse +
        super().__init__(x, y, image_path)
        self.type = "speed_up"

class SpeedDownCell(GridCell):
    def __init__(self, x, y, image_path):
        # Charge une image spécifique pour la cellule de vitesse -
        super().__init__(x, y, image_path)
        self.type = "speed_down"

class WallsCell(GridCell):
    def __init__(self, x, y, image_path):
        super().__init__(x, y, image_path)
        self.type = "wall"
        self.load_image(image_path)
        
    def load_image(self, image_path):
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))  # Redimensionner l'image
        except Exception as e:
            print(f"Error loading image: {e}")
            self.image = None  # Aucune image en cas d'erreur


class WaterCell(GridCell):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.type = "water"
    
    def on_interact(self, unit):
        pass
        """
        Logique spécifique pour les cellules d'eau.
        Par exemple : réduire la vitesse de l'unité ou appliquer des dégâts.
        """
    
class WindCell(GridCell):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.type = "Wind"
    
    def on_interact(self, unit):
        pass
        """
        Logique spécifique pour les cellules d'eau.
        Par exemple : réduire la vitesse de l'unité ou appliquer des dégâts.
        """





  