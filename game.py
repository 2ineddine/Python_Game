import pygame
import random
import os
from cell import *  # Importe les types de cellules définis dans un autre fichier.
from unit import *  # Importe les classes des unités (joueurs et ennemis).

# Classe principale du jeu
class Game:
    def __init__(self, screen):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.screen = screen

        # Coordonnées des murs (positions des cellules de type mur).
        self.walls_coordinates = [
            (4, 11), (4, 12), (4, 13), (4, 14), (4, 15), (4, 16), (4, 17),
            (5, 11), (5, 12), (5, 13), (5, 14), (5, 15), (5, 16), (5, 17),
            (6, 11), (6, 12), (6, 13), (6, 14), (6, 15), (6, 16), (6, 17),
            (7, 11), (7, 12), (7, 13), (7, 14), (7, 15), (7, 16), (7, 17),
            (8, 13), (8, 14), (8, 15), (9, 13), (9, 14), (9, 15),
            (16, 9), (16, 10), (16, 11), (16, 12), (16, 13), (16, 14), (16, 15), (16, 16), (16, 17),
            (17, 9), (17, 10), (17, 11), (17, 12), (17, 13), (17, 14), (17, 15), (17, 16), (17, 17),
            (18, 9), (18, 10), (18, 11), (18, 12), (18, 13), (18, 14), (18, 15), (18, 16), (18, 17),
            (14, 16), (14, 17), (15, 16), (15, 17),
            (21, 16), (21, 17), (22, 16), (22, 17),
            (20, 1), (20, 2), (20, 3), (20, 4),
            (21, 1), (21, 2), (21, 3), (21, 4),
            (22, 1), (22, 2), (22, 3), (22, 4),
            (16, 2), (17, 2), (18, 2), (19, 2),
            (7, 3), (8, 3), (9, 3), (10, 3), (11, 3)
        ]

        # Coordonnées des cellules d'eau
        self.water_coordinates = [
            (8, 11), (9, 11), (10, 11), (11, 11),
            (10, 13), (11, 13), (10, 14),
            (8, 12), (9, 12), (10, 12), (11, 12),
            (8, 10), (9, 10), (10, 10), (11, 10), (12, 10),
            (10, 9), (11, 9), (12, 9), (13, 9), (14, 9),
            (13, 8), (12, 8),
        ]

        # Coordonnées des cellules de poison
        self.poison_coordinates = [
            (8, 16), (15, 15), (24, 1), (19, 3), (14, 15), (18, 3),
            (8, 17), (23, 1), (11, 20), (5, 6)
        ]

        # Coordonnées des cellules de vent
        self.wind_coordinates = [
            (23, 16), (22, 0), (24, 16), (20, 17), (19, 17),
            (24, 24), (3, 14), (3, 3), (21, 7)
        ]

        # Chemin de l'image pour les murs
        self.walls_image_path = "E:/Python/Project/walls.png"

        # Création de la grille
        self.grid = self.create_grid()

        # Création des unités (joueurs et ennemis)
        self.player_units = [Noah(), Sena(), Alexandria(), Lanz(), Cammuravi(), Mio()]
        self.enemy_units = [Maitre(), Zeon(), Eunie(), Taion(), Valdi(), Ashera()]

    def place_walls(self, grid):
        """
        Place les cellules de type mur aux positions spécifiées.
        """
        for x, y in self.walls_coordinates:
            grid[x][y] = WallsCell(x, y, self.walls_image_path)

    def resize_units(self):
        """
        Redimensionne les icônes des unités pour correspondre à la taille des cellules.
        """
        for unit in self.player_units + self.enemy_units:
            unit.update_icon_size()

    def create_grid(self):
        """
        Crée la grille de jeu avec différents types de cellules.
        """
        grid = []
        for x in range(GRID_SIZE):
            row = []
            for y in range(GRID_SIZE):
                # Définition des chemins d'image spécifiques pour chaque cellule.
                image_path = f"E:/Python/Project/gridimage/cell_{y}_{x}.png"
                image_path_poison = f"E:/Python/Project/gridimage/PoisonImage/cell_{y}_{x}.png"
                image_path_wind = f"E:/Python/Project/gridimage/WindImage/cell_{y}_{x}.png"

                # Attribution des types de cellules selon leurs coordonnées
                if (x, y) in self.water_coordinates:
                    cell = WaterCell(x, y, (0, 0, 255))
                    cell.set_image(image_path)
                elif (x, y) in self.walls_coordinates:
                    cell = WallsCell(x, y, self.walls_image_path)
                elif (x, y) in self.poison_coordinates:
                    cell = PoisonCell(x, y, image_path_poison)
                elif (x, y) in self.wind_coordinates:
                    cell = WindCell(x, y, (0, 0, 255))
                    cell.set_image(image_path_wind)
                else:
                    cell = NormalCell(x, y, image_path)

                row.append(cell)
            grid.append(row)
        return grid

    def flip_display(self):
        """
        Affiche la grille et les unités sur la fenêtre.
        """
        self.screen.fill(BLACK)  # Nettoyer l'écran
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                cell = self.grid[x][y]
                if cell.image:
                    self.screen.blit(cell.image, (x * CELL_SIZE, y * CELL_SIZE))
                else:
                    pygame.draw.rect(
                        self.screen, cell.color,
                        pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    )

        # Dessiner les unités (joueurs et ennemis)
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        pygame.display.flip()

    def handle_player_turn(self):
        """
        Gère le tour des joueurs, incluant les déplacements et les attaques.
        """
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
                        current_cell = self.grid[selected_unit.x][selected_unit.y]
                        if current_cell.type != "normal":
                            current_cell.on_land(selected_unit)

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
        """
        Gère le tour des ennemis, incluant les déplacements et les attaques.
        """
        for enemy in self.enemy_units:
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy)

            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.health <= 0:
                    self.player_units.remove(target)


# Fonction principale
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")
    game = Game(screen)
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()


if __name__ == "__main__":
    main()
