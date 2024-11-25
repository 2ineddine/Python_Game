import pygame
import random

from unit import *  
#from cell import *

# Constantes
GRID_SIZE = 25
CELL_SIZE = 25
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SAND_COLOR = (212, 176, 23)
POISON_COLOR = (214, 22, 22)
SPEEDUP_COLOR = (39, 190, 14)
SPEEDDOWN_COLOR = (7, 98, 206)
WATER_COLOR = (98, 214, 252)

class Game:
    """
    Classe pour représenter le jeu.

    Attributs
    ---------
    screen: pygame.Surface
        La surface de la fenêtre du jeu.
    player_units : list[Unit]
        La liste des unités du joueur.
    enemy_units : list[Unit]
        La liste des unités de l'adversaire.
    """

    def __init__(self, screen):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.screen = screen
        self.grid = self.create_grid()

        # Création des unités avec les sous-classes spécifiques
        self.player_units = [Noah(), Sena(), Alexandria(), Lanz(), Cammuravi(), Mio()]
        self.enemy_units = [Maitre(), Zeon(), Eunie(), Taion(), Valdi(), Ashera()]

    def create_grid(self):
        """Créer une grille avec des cellules normales et des cellules spéciales à des positions fixes."""
        grid = [[GridCell(x, y, WHITE) for y in range(GRID_SIZE)] for x in range(GRID_SIZE)]
        
        # Placer des cellules spéciales à des positions fixes
        self.place_fixed_cells(grid)

        return grid

    def place_fixed_cells(self, grid):
        """Place les cellules spéciales à des positions prédéfinies."""
        # Exemple : placer 3 cellules pour chaque type
        # Assigner les cellules de Sable
        grid[5][5] = SandCell(5, 5)
        grid[18][20] = SandCell(18, 20)
        
        # Assigner les cellules de Poison
        grid[22][10] = PoisonCell(22, 10)
        grid[14][1] = PoisonCell(14, 1)
        
        # Assigner les cellules de Vitesse +
        grid[3][18] = SpeedUpCell(3, 18)
        grid[9][16] = SpeedUpCell(9, 16)
        
        # Assigner les cellules de Vitesse -
        grid[24][24] = SpeedDownCell(24, 24)
        grid[0][12] = SpeedDownCell(0, 12)
        
        # Assigner les cellules d'Eau
        grid[10][12] = WaterCell(10, 12)
        grid[9][9] = WaterCell(9, 9)


    def flip_display(self):
        """Affiche le jeu avec les couleurs spécifiques des cellules et des bordures gris foncé."""
        self.screen.fill(BLACK)  # Remplir l'arrière-plan avec du noir 
    
        # Dessiner les cellules
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                cell = self.grid[x][y]
                
                # Déterminer la couleur de la cellule selon son type
                if isinstance(cell, SandCell):
                    pygame.draw.rect(self.screen, SAND_COLOR, rect)  # Couleur pour les cellules de sable
                elif isinstance(cell, PoisonCell):
                    pygame.draw.rect(self.screen, POISON_COLOR, rect)  # Couleur pour les cellules de poison
                elif isinstance(cell, SpeedUpCell):
                    pygame.draw.rect(self.screen, SPEEDUP_COLOR, rect)  # Couleur pour les cellules de vitesse +
                elif isinstance(cell, SpeedDownCell):
                    pygame.draw.rect(self.screen, SPEEDDOWN_COLOR, rect)  # Couleur pour les cellules de vitesse -
                elif isinstance(cell, WaterCell):
                    pygame.draw.rect(self.screen, WATER_COLOR, rect)  # Couleur pour les cellules d'eau
                else:
                    pygame.draw.rect(self.screen, BLACK, rect)  # Couleur pour les cellules normales (noir)
                
                # Dessiner les bordures des cellules en gris foncé
                pygame.draw.rect(self.screen, (169, 169, 169), rect, 1)  # Bordure gris foncé (code RGB: 169, 169, 169)
    
        # Dessiner les unités
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)
    
        pygame.display.flip()  # Actualiser l'affichage
    def handle_player_turn(self):
        """Tour du joueur"""
        for selected_unit in self.player_units:
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()
            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        # Gestion des déplacements
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1

                        selected_unit.move(dx, dy)

                        # Vérifie la cellule sur laquelle l'unité se déplace
                        current_cell = self.grid[selected_unit.x][selected_unit.y]
                        if current_cell.type != "normal":
                            current_cell.on_land(selected_unit)  # Applique l'effet de la cellule

                        self.flip_display()

                        # Gestion des attaques
                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attack(enemy)
                                    if enemy.health <= 0:
                                        self.enemy_units.remove(enemy)

                            has_acted = True
                            selected_unit.is_selected = False

    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:
            # Déplacement aléatoire
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy)

            # Attaque si possible
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.health <= 0:
                    self.player_units.remove(target)

# Fonction principale

def main():
    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Instanciation du jeu
    game = Game(screen)

    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()

if __name__ == "__main__":
    main()
