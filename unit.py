import pygame
import random

# Constantes
GRID_SIZE = 25  # Nombre de cases dans la grille (longueur/largeur).
CELL_SIZE = 25  # Taille en pixels de chaque cellule de la grille.
WIDTH = GRID_SIZE * CELL_SIZE  # Largeur de la fenêtre.
HEIGHT = GRID_SIZE * CELL_SIZE  # Hauteur de la fenêtre.
BLACK = (0, 0, 0)  # Définition de la couleur noire (RGB).
GREEN = (0, 255, 0)  # Définition de la couleur verte (RGB).

# Chargement des icônes des unités
ICON_PATHS = {  # Dictionnaire associant le nom d'une unité au chemin de son icône.
    "Noah": "E:/Python/Project/Noah.png",
    "Sena": "E:/Python/Project/Sena.png",
    "Alexandria": "E:/Python/Project/Alexandria.png",
    "Cammuravi": "E:/Python/Project/Cammuravi.png",
    "Lanz": "E:/Python/Project/Lanz.png",
    "Mio": "E:/Python/Project/Mio.png",
    "Ashera": "E:/Python/Project/Ashera.png", 
    "Zeon": "E:/Python/Project/Zeon.png",
    "Eunie": "E:/Python/Project/Eunie.png",
    "Taion": "E:/Python/Project/Taion.png",
    "Valdi": "E:/Python/Project/Valdi.png",
    "Maitre": "E:/Python/Project/Maitre.png"
}

walls_image_path = "E:/Python/Project/wall.jpg"  # Chemin de l'image des murs.


# Classe de base pour les unités
class Unit:
    def __init__(self, name, health, attack_power, defense, speed, evasion, magic, team, icon_path, x, y):
        self.name = name  # Nom de l'unité.
        self.health = health  # Points de vie de l'unité.
        self.attack_power = attack_power  # Puissance d'attaque.
        self.defense = defense  # Valeur de défense.
        self.speed = speed  # Vitesse de déplacement.
        self.evasion = evasion  # Probabilité d'esquiver une attaque.
        self.magic = magic  # Puissance magique.
        self.team = team  # Équipe à laquelle appartient l'unité ('player' ou 'enemy').
        self.icon_path = icon_path  # Chemin de l'icône associée à l'unité.
        self.icon = pygame.image.load(self.icon_path)  # Chargement de l'icône.
        self.x = x  # Position horizontale initiale sur la grille.
        self.y = y  # Position verticale initiale sur la grille.
        self.is_selected = False  # Indique si l'unité est sélectionnée.

        # Redimensionne l'icône pour correspondre à la taille des cellules.
        self.update_icon_size()

    def update_icon_size(self):
        """Redimensionne l'icône selon la taille actuelle de CELL_SIZE."""
        self.icon = pygame.image.load(self.icon_path)  # Recharge l'icône d'origine.
        self.icon = pygame.transform.scale(self.icon, (CELL_SIZE, CELL_SIZE))  # Redimensionnement.

    def move(self, dx, dy):
        """Déplace l'unité de (dx, dy) si elle reste dans les limites de la grille."""
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy

    def attack(self, target):
        """Effectue une attaque sur une cible si elle est adjacente."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power  # Réduit les points de vie de la cible.

    def draw(self, screen):
        """Dessine l'unité sur l'écran, avec une bordure verte si elle est sélectionnée."""
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        screen.blit(self.icon, (self.x * CELL_SIZE, self.y * CELL_SIZE))  # Affiche l'icône.

# Création des classes spécifiques pour chaque unité avec des paramètres prédéfinis.
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
