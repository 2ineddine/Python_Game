import pygame
import random
import sys
import os

from unit1 import  * 
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
           Maitre(x=9, y=9, health=60, attack_power=50, magic_power=31, defence=87, speed=39, agility=41, team="player", icon_path=ICON_PATHS["Maitre"]),
           Valdi(x=10, y=10, health=32, attack_power=60, magic_power=41, defence=70, speed=40, agility=20, team="player", icon_path=ICON_PATHS["Valdi"]),
           Taion(x=11, y=11, health=32, attack_power=60, magic_power=41, defence=70, speed=40, agility=20, team="player", icon_path=ICON_PATHS["Taion"]),
           Cammuravi(x=12, y=12, health=32, attack_power=60, magic_power=41, defence=70, speed=40, agility=20, team="player",icon_path=ICON_PATHS["Cammuravi"])
       ]
    
        
        self.player1_units = []
        self.player2_units = []
        
      
        
        
    
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
                        selected_unit = self.available_units[player_choice]
                        if selected_unit not in selected_units:  # Évite les doublons dans une sélection
                            selected_units.append(selected_unit)
    
                    self.flip_display(selected_units, player_choice)
    
        # Ajout des unités sélectionnées
        if player_number == 1:
            self.player1_units = selected_units
            print("les unités choisies par le joueur 1 sont : ")
            for units_player in self.player1_units:
                print(f"{units_player.__class__.__name__} \n")
        else:
            self.player2_units = selected_units
            print("les unités choisies par le joueur 2 sont : ")
            for units_player in self.player2_units:
                print(f"{units_player.__class__.__name__} \n")
        

    
                
    def handle_player_turn(self):
        """Gère les tours des deux joueurs."""
        players = [self.player1_units, self.player2_units]  # Liste des unités des joueurs
        print("le nombre d'unités du joueur 1 est ", len(self.player1_units), "le nombre d'unités du joueur 2 est ", len(self.player2_units))
        
        current_player = 0  # Le joueur actuel (0 pour le joueur 1, 1 pour le joueur 2)
        
        while True:  # Boucle pour gérer les tours des joueurs
            player_units = players[current_player]  # Unités du joueur actuel
            #self.display_turn_info(current_player + 1)  # Affiche des informations sur le tour actuel
    
            for unit in player_units:
                unit.is_selected = True  # Marquer l'unité comme sélectionnée
                self.flip_display(player_choice=None, selected_units=player_units)  # Affiche la grille et les unités
        
                has_acted = False
                
                while not has_acted:  # Boucle d'action pour chaque unité
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
    
                        if event.type == pygame.KEYDOWN:
                            dx, dy = 0, 0  # Déplacements de l'unité
    
                            # Déplacement de l'unité avec les touches fléchées
                            if event.key == pygame.K_LEFT:
                                dx = -1
                            elif event.key == pygame.K_RIGHT:
                                dx = 1
                            elif event.key == pygame.K_UP:
                                dy = -1
                            elif event.key == pygame.K_DOWN:
                                dy = 1
    
                            # Confirmer l'action de l'unité (fin du tour de l'unité)
                            if event.key == pygame.K_SPACE:
                                has_acted = True
                                unit.is_selected = False
    
                            # Passer à l'unité suivante
                            if event.key == pygame.K_TAB:
                                unit.is_selected = False
                                has_acted = True  # Force le passage à l'unité suivante
        
                            # Effectuer le déplacement
                            unit.move(dx, dy)
                            self.flip_display(player_choice=None, selected_units=player_units)  # Rafraîchir l'affichage
        
                # Rafraîchir l'affichage après que l'unité ait agi
                self.flip_display(player_choice=None, selected_units=player_units)  
        
            # Passer au joueur suivant après que toutes les unités aient agi
            current_player = (current_player + 1) % len(players)
            if current_player == 0:
                break  # Fin du tour complet (retour au joueur 1)
                
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
            print(f"l'unité {unit2} -- joueur 1 de coordonnées {unit2.x}-{unit2.y} a été ajouté ")
            #self.player1_units.append(unit2)
            
    def flip_display(self, selected_units=None, player_choice=None):
        """Affiche les unités ou la grille en fonction du contexte."""
        self.screen.fill((0, 0, 0))  # Efface l'écran avec une couleur noire
        

        # Dessiner les unités de chaque joueur
        
        if selected_units is not None and player_choice is not None:
            # Cas de sélection des unités
            font = pygame.font.Font(None, 36)
            for i, unit in enumerate(self.available_units):
                color = (0, 255, 0) if i == player_choice else (255, 255, 255)
                text = font.render(f"- {unit.__class__.__name__}", True, color)
                self.screen.blit(text, (20, 20 + i * 30))
            
            # Affiche les unités sélectionnées
            for i, unit in enumerate(selected_units):
                text = font.render(f"Choisi: {unit.__class__.__name__}", True, (0, 255, 0))
                self.screen.blit(text, (300, 20 + i * 30))
        else:
            # Cas du jeu (affiche la grille et les unités)
            for x in range(0, WIDTH, CELL_SIZE):
                for y in range(0, HEIGHT, CELL_SIZE):
                    rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, WHITE, rect, 1)
                    
            for unit1 in self.player1_units:
                unit1.draw(self.screen)  # Assurez-vous que la méthode `draw` existe dans les unités
            for unit2 in self.player2_units:
                unit2.draw(self.screen) 
        pygame.display.flip()
    
    



def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # Taille adaptée
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