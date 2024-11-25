import pygame
import random

# Constantes
GRID_SIZE = 25
CELL_SIZE = 25
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Chargement des icônes des unités
ICON_PATHS = {
    "Noah": "E:/Python/Project/Noah1.png",
    "Sena": "E:/Python/Project/Sena1.png",
    "Alexandria": "E:/Python/Project/Alexandria1.png",
    "Cammuravi": "E:/Python/Project/Cammuravi1.png",
    "Lanz": "E:/Python/Project/Lanz1.png",
    "Mio": "E:/Python/Project/Mio1.png",
    "Ashera": "E:/Python/Project/Ashera1.png",
    "Zeon": "E:/Python/Project/Zeon1.png",
    "Eunie": "E:/Python/Project/Eunie1.png",
    "Taion": "E:/Python/Project/Taion1.png",
    "Valdi": "E:/Python/Project/Valdi1.png",
    "Maitre": "E:/Python/Project/Maitre1.png"
}

class Unit:
    """
    Classe pour représenter une unité avec des icônes.
    """
    def __init__(self, name, health, attack_power, defense, speed, evasion, magic, team, icon_path, x, y):
        """
        Construit une unité avec une position, des statistiques et une icône.

        Paramètres
        ----------
        name : str
            Le nom de l'unité.
        health : int
            La santé de l'unité.
        attack_power : int
            La puissance d'attaque de l'unité.
        defense : int
            La défense de l'unité.
        speed : int
            La vitesse de l'unité.
        evasion : int
            L'esquive de l'unité.
        magic : int
            La magie de l'unité.
        team : str
            L'équipe de l'unité ('player' ou 'enemy').
        icon_path : str
            Le chemin de l'icône de l'unité.
        x : int
            La position initiale en X.
        y : int
            La position initiale en Y.
        """
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.defense = defense
        self.speed = speed
        self.evasion = evasion
        self.magic = magic
        self.team = team  # 'player' ou 'enemy'
        self.icon = pygame.image.load(icon_path)
        self.icon = pygame.transform.scale(self.icon, (CELL_SIZE, CELL_SIZE))  # Redimensionner l'icône
        self.x = x  # Position initiale X
        self.y = y  # Position initiale Y
        self.is_selected = False

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    def draw(self, screen):
        """Affiche l'unité sur l'écran avec son icône."""
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        # Affiche l'icône de l'unité sur la grille
        screen.blit(self.icon, (self.x * CELL_SIZE, self.y * CELL_SIZE))


# Création des unités avec icônes
class Noah(Unit):
    def __init__(self):
        super().__init__("Noah", 90, 80, 50, 70, 60, 40, "player", ICON_PATHS["Noah"], 0, 24)

class Sena(Unit):
    def __init__(self):
        super().__init__("Sena", 100, 60, 55, 80, 70, 45, "player", ICON_PATHS["Sena"], 1, 24)

class Alexandria(Unit):
    def __init__(self):
        super().__init__("Alexandria", 110, 75, 60, 65, 80, 50, "player", ICON_PATHS["Alexandria"], 2, 24)

class Cammuravi(Unit):
    def __init__(self):
        super().__init__("Cammuravi", 95, 85, 40, 75, 60, 35, "player", ICON_PATHS["Cammuravi"], 3, 24)

class Lanz(Unit):
    def __init__(self):
        super().__init__("Lanz", 120, 50, 45, 95, 50, 30, "player", ICON_PATHS["Lanz"], 4, 24)

class Mio(Unit):
    def __init__(self):
        super().__init__("Mio", 100, 55, 50, 85, 65, 40, "player", ICON_PATHS["Mio"], 5, 24)

class Ashera(Unit):
    def __init__(self):
        super().__init__("Ashera", 110, 60, 60, 80, 70, 50, "enemy", ICON_PATHS["Ashera"], 0, 0)

class Zeon(Unit):
    def __init__(self):
        super().__init__("Zeon", 115, 65, 50, 90, 60, 45, "enemy", ICON_PATHS["Zeon"], 1, 0)

class Eunie(Unit):
    def __init__(self):
        super().__init__("Eunie", 80, 50, 70, 60, 85, 55, "enemy", ICON_PATHS["Eunie"], 2, 0)

class Taion(Unit):
    def __init__(self):
        super().__init__("Taion", 85, 55, 75, 70, 80, 50, "enemy", ICON_PATHS["Taion"], 3, 0)

class Valdi(Unit):
    def __init__(self):
        super().__init__("Valdi", 95, 50, 80, 65, 75, 45, "enemy", ICON_PATHS["Valdi"], 4, 0)

class Maitre(Unit):
    def __init__(self):
        super().__init__("Maitre", 100, 60, 65, 70, 80, 50, "enemy", ICON_PATHS["Maitre"], 5, 0)
        
        

#création des types de cellules 

class GridCell:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.type = "normal"  # Par défaut une cellule normale

    def draw(self, screen):
        """Dessine la cellule sur l'écran."""
        pygame.draw.rect(screen, self.color, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

class SandCell(GridCell):
    def __init__(self, x, y):
        super().__init__(x, y, (212, 176, 23))  # Couleur beige
        self.type = "sand"

    def on_land(self, unit):
        """Fonction pour gérer l'effet de cette cellule plus tard."""
        pass

class PoisonCell(GridCell):
    def __init__(self, x, y):
        super().__init__(x, y, (214, 22, 22))  # Couleur rouge
        self.type = "poison"

    def on_land(self, unit):
        """Fonction pour gérer l'effet de cette cellule plus tard."""
        pass

class SpeedUpCell(GridCell):
    def __init__(self, x, y):
        super().__init__(x, y, (39, 190, 14))  # Couleur verte
        self.type = "speed_up"

    def on_land(self, unit):
        """Fonction pour gérer l'effet de cette cellule plus tard."""
        pass

class SpeedDownCell(GridCell):
    def __init__(self, x, y):
        super().__init__(x, y, (7, 98, 206))  # Couleur bleue
        self.type = "speed_down"

    def on_land(self, unit):
        """Fonction pour gérer l'effet de cette cellule plus tard."""
        pass

class WaterCell(GridCell):
    def __init__(self, x, y):
        super().__init__(x, y, (98, 214, 252))  # Couleur bleue
        self.type = "water"

    def on_land(self, unit):
        """Fonction pour gérer l'effet de cette cellule plus tard."""
        pass


















# Exemple d'utilisation avec Pygame
