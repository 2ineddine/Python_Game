import pygame
import random
import sys
import os
from cells import *
from unit import  * 
#################################################################################################################

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
# Constantes



# Constantes


FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)




#################################################################################################################

# Constantes
#GRID_SIZE = 25
#CELL_SIZE = 25
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BROWN = (165, 42, 42)



class Game:
    def __init__(self, screen):
       
        self.screen = screen
        self.available_units = [
           Eunie(x=1, y=1, health=90, attack_power=30, magic_power=80, defence=50, speed=3, agility=7, team="player",icon_path=ICON_PATHS["Eunie"]),
           Noah(x=2, y=2, health=100, attack_power=60, magic_power=70, defence=40, speed=4, agility=6, team="player",icon_path=ICON_PATHS["Noah"]),
           Alexandria(x=3, y=3, health=120, attack_power=50, magic_power=60, defence=30, speed=5, agility=5, team="player",icon_path=ICON_PATHS["Alexandria"]),
           Lanz(x=4, y=4, health=80, attack_power=40, magic_power=60, defence=25, speed=7, agility=8, team="player",icon_path=ICON_PATHS["Lanz"]),
           Mio(x=5, y=5, health=70, attack_power=50, magic_power=40, defence=30, speed=6, agility=6, team="player",icon_path=ICON_PATHS["Mio"]),
           Ashera(x=6, y=6, health=110, attack_power=60, magic_power=70, defence=40, speed=5, agility=7, team="player",icon_path=ICON_PATHS["Ashera"]),
           Zeon(x=7, y=7, health=130, attack_power=80, magic_power=50, defence=60, speed=4, agility=5, team="player",icon_path=ICON_PATHS["Zeon"]),
           Sena(x=8, y=8, health=85, attack_power=45, magic_power=25, defence=90, speed=6, agility=7, team="player", icon_path=ICON_PATHS["Sena"]),
           Maitre(x=9, y=9, health=60, attack_power=50, magic_power=31, defence=87, speed=3, agility=41, team="player", icon_path=ICON_PATHS["Maitre"]),
           Valdi(x=10, y=10, health=32, attack_power=60, magic_power=41, defence=70, speed=4, agility=20, team="player", icon_path=ICON_PATHS["Valdi"]),
           Taion(x=11, y=11, health=32, attack_power=60, magic_power=41, defence=70, speed=4, agility=20, team="player", icon_path=ICON_PATHS["Taion"]),
           Cammuravi(x=12, y=12, health=32, attack_power=60, magic_power=41, defence=70, speed=4, agility=20, team="player",icon_path=ICON_PATHS["Cammuravi"])
       ]
    
        self.walls = [WallCell(4, 4), WallCell(5, 5), WallCell(6, 6), WallCell(7, 7)] 
        
        self.player1_units = []
        self.player2_units = []
        



        
    def get_active_units(self):
        """
        Retourne la liste des unités du joueur actif.
        """
        return self.player1_units if self.current_player == 1 else self.player2_units
    
    
    def select_units(self, player_number):
        """Permet à un joueur de choisir ses unités."""
        player_units = self.player1_units if player_number == 1 else self.player2_units
        selected_units = []
        player_choice = 0  # Initialisation de l'unité à choisir
    
        while len(selected_units) < 4:  # Chaque joueur choisit 4 unités
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
    
                if event.type == pygame.KEYDOWN:
                    # Déplacer la sélection
                    if event.key == pygame.K_DOWN:
                        player_choice = (player_choice + 1) % len(self.available_units)
                    elif event.key == pygame.K_UP:
                        player_choice = (player_choice - 1) % len(self.available_units)
    
                    # Sélectionner une unité avec ESPACE
                    if event.key == pygame.K_SPACE:
                        selected_unit = self.available_units[player_choice].clone()
                    
                        # Vérification basée sur les noms de classe pour éviter les doublons
                        if selected_unit.__class__.__name__ not in [unit.__class__.__name__ for unit in selected_units]:
                            selected_units.append(selected_unit)
                       

    
                    self.flip_display(selected_units, player_choice,current_player=player_number)
    
        # Ajout des unités sélectionnées
        if player_number == 1:
            self.player1_units = selected_units
            print("les unités choisies par le joueur 1 sont : ")
            for units_player in self.player1_units:
                units_player.team = "player 1"
                print(f"{units_player.__class__.__name__} -- {units_player.team} \n")
        else:
            self.player2_units = selected_units
            print("les unités choisies par le joueur 2 sont : ")
            for units_player in self.player2_units:
                units_player.team = "player 2"
                print(f"{units_player.__class__.__name__} -- {units_player.team} \n")
                
        

    
                
    def handle_player_turn(self):
        """Gère les tours des deux joueurs avec gestion des murs et des limites de la grille."""
        players = [self.player1_units, self.player2_units]
        current_player = 0  # Le joueur actuel (0 pour le joueur 1, 1 pour le joueur 2)
    
        while True:  # Boucle pour gérer les tours
            player_units = players[current_player]
            for unit in player_units:
                # Générer la portée de déplacement
                movement_range = unit.generate_circle(unit.x, unit.y, [(walls.x,walls.y) for walls in self.walls])
    
                # Exclure les murs et les cases occupées par d'autres unités
                positions_units = {(u.x, u.y) for u in self.player1_units + self.player2_units}
                movement_range = [p for p in movement_range if p not in positions_units]
    
                # Initialisation de la position du carré violet
                destination = (unit.x, unit.y)
                unit.is_selected = True
                has_acted = False
    
                while not has_acted:  # Boucle pour sélectionner une action
                    self.flip_display(
                        player_choice=None,
                        selected_units=player_units,
                        current_player=current_player,
                        movement_range=movement_range,
                        destination=destination
                    )
    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
    
                        if event.type == pygame.KEYDOWN:
                            dx, dy = 0, 0
    
                            # Déplacement du carré violet
                            if event.key == pygame.K_LEFT:
                                dx = -1
                            elif event.key == pygame.K_RIGHT:
                                dx = 1
                            elif event.key == pygame.K_UP:
                                dy = -1
                            elif event.key == pygame.K_DOWN:
                                dy = 1
    
                            # Calcul de la nouvelle destination
                            new_destination = (destination[0] + dx, destination[1] + dy)
                            if (
                                new_destination in movement_range and
                                new_destination not in [(wall.x, wall.y) for wall in self.walls]
                            ):
                                destination = new_destination
                            
                            if event.key == pygame.K_a:
                                attack_range = unit.generate_circle(unit.x, unit.y, [(walls.x,walls.y) for walls in self.walls],self)
                                
    
                            # Confirmation du déplacement
                            if event.key == pygame.K_SPACE:
                                if destination in movement_range and destination not in positions_units:
                                    unit.x, unit.y = destination  # Déplacer l'unité
                                    has_acted = True
                            #if 
                            # Passer à l'unité suivante
                            if event.key == pygame.K_TAB:
                                unit.is_selected = False
                                has_acted = True
    
                unit.is_selected = False
    
            # Passer au joueur suivant après que toutes les unités aient agi
            current_player = (current_player + 1) % len(players)
            if current_player == 0:
                break  # Fin du tour complet



                
    def assign_unit_positions(self):
        """Attribue des positions initiales aux unités des joueurs."""
        #self.player1_units.clear()
        #self.player2_units.clear()        
        
        for i, unit1 in enumerate(self.player1_units):
            
            #unit1.x, unit1.y = i, 0  # Ligne supérieure pour le joueur 1
            unit1.changes(i,0,team='player1')
            print(f"l'unité {unit1.__class__.__name__} -- joueur 1 de coordonnées {unit1.x}-{unit1.y} a été ajoutée ")
            #self.player1_units.append(unit1)
        
        for j, unit2 in enumerate(self.player2_units):
            #unit2.x, unit2.y = j, GRID_SIZE - 1  # Ligne inférieure pour le joueur 2
            unit2.changes(j,GRID_SIZE-1,team='player2')
            print(f"l'unité {unit2.__class__.__name__} -- joueur 1 de coordonnées {unit2.x}-{unit2.y} a été ajouté ")
            #self.player1_units.append(unit2)
            
    def flip_display(self, selected_units=None, player_choice=None, current_player=None, movement_range=None, destination=None,attack_range = None):
        """Affiche la grille, les murs, la portée, et les unités selon l'état du jeu."""
        self.screen.fill(BLACK)  # Efface l'écran
    
        if selected_units is not None and player_choice is not None:
            # Phase de sélection
            font = pygame.font.Font(None, 28)
            instruction_text = font.render(f"Le choix du joueur {current_player} :", True, (255, 255, 0))
            self.screen.blit(instruction_text, (50, 10))
    
            for i, unit in enumerate(self.available_units):
                color = (0, 255, 0) if i == player_choice else (255, 255, 255)
                text = font.render(f"{i + 1}. {unit.__class__.__name__}", True, color)
                self.screen.blit(text, (50, 50 + i * 30))
    
            for j, unit in enumerate(selected_units):
                selected_text = font.render(f"Choisie: {unit.__class__.__name__}", True, (0, 255, 255))
                self.screen.blit(selected_text, (400, 50 + j * 30))
    
        else:
            # Phase de déplacement
            for x in range(0, WIDTH, CELL_SIZE):
                for y in range(0, HEIGHT, CELL_SIZE):
                    rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, WHITE, rect, 1)
    
            for wall in self.walls:
                pygame.draw.rect(
                    self.screen, BROWN,
                    (wall.x * CELL_SIZE, wall.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )
    
            if movement_range:
                for (px, py) in movement_range:
                    pygame.draw.rect(
                    self.screen, (169, 169, 169),  # Couleur de fond (gris clair)
                    (px * CELL_SIZE + 1, py * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2)
                    )
                    
            if destination:
                dx, dy = destination
                pygame.draw.rect(
                    self.screen, (138, 43, 226),
                    (dx * CELL_SIZE, dy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )
            if attack_range:
                for (px, py) in attack_range:
                    pygame.draw.rect(
                    self.screen, (169, 169, 169),  # Couleur de fond (gris clair)
                    (px * CELL_SIZE + 1, py * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2)
                    )
                
                
            for unit1 in self.player1_units:
                unit1.draw(self.screen)
            for unit2 in self.player2_units:
                unit2.draw(self.screen)
    
        pygame.display.flip()


    
    



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Taille adaptée
    pygame.display.set_caption("Mon jeu de stratégie")

    game = Game(screen)

    # Le joueur 1 choisit ses unités
    print("Joueur 1 : choisissez vos unités")
    game.select_units(player_number=1)

    # Le joueur 2 choisit ses unités
    print("Joueur 2 : choisissez vos unités")
    game.select_units(player_number=2)

    # Place les unités sur la grille
    game.assign_unit_positions()

    # Lance le jeu
    print("Le jeu commence !")
    while True:
        game.handle_player_turn()
        

if __name__ == "__main__":
    main()