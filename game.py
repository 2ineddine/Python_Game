import pygame
import random
import sys
import os
import inspect 
from cells import *
from unit import  * 
from Func_extra import * 
import time

#################################################################################################################

"""pour jouer d'abord choisir les personnages en appuyant sur espace pour valider le choix 
apres ca avec les fleches directionnelles pour se deplacer et espace pour valider le deplacement
ensuite choisir la competence avec les boutons 1,2,3,4 et attaquer valider avec a 
a la fin on appuie sur e pour valider l attaque et tab pur anuller et passer au prochain personnage 
"""

ICON_PATHS = {  # Dictionnaire associant le nom d'une unité au chemin de son icône.
    "Noah": "E:\Projet jeu python\jeux\Ashera.png",
    "Sena": "E:\Projet jeu python\jeux\Sena.png",
    "Alexandria": "E:\Projet jeu python\jeux\Alexandria.png",
    "Cammuravi": "E:\Projet jeu python\jeux\Cammuravi.png",
    "Lanz": "E:\Projet jeu python\jeux\Lanz.png",
    "Mio": "E:\Projet jeu python\jeux\Mio.png",
    "Ashera": "E:\Projet jeu python\jeux\Ashera.png", 
    "Zeon": "E:\Projet jeu python\jeux\Zeon.png",
    "Eunie": "E:\Projet jeu python\jeux\Eunie.png",
    "Taion": "E:\Projet jeu python\jeux\Taion.png",
    "Valdi": "E:\Projet jeu python\jeux\Valdi.png",
    "Maitre": "E:\Projet jeu python\jeux\Maitre.png"
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
BROWN = (139,69,19)



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
                
        

        
    def handle_player_turn(self, skill_selector):
        
        #Gère les tours des deux joueurs avec gestion des phases marche et attaque,
        #en affichant correctement la portée d'attaque.
        
        players = [self.player1_units, self.player2_units]
        current_player = 0  # Le joueur actuel (0 pour le joueur 1, 1 pour le joueur 2)
    
        while True:  # Boucle pour gérer les tours des joueurs
            player_units = players[current_player]
            for unit in player_units:
                # Phase de déplacement : Calcul de la portée de mouvement
                movement_range = unit.generate_circle(unit.x, unit.y, [(wall.x, wall.y) for wall in self.walls])
                positions_units = {(u.x, u.y) for u in self.player1_units + self.player2_units}
                movement_range = [p for p in movement_range if p not in positions_units]
    
                attack_range = []  # Initialiser la portée d'attaque
                effect_zone = []  # Zone d'effet initiale
                destination = (unit.x, unit.y)
                unit.is_selected = True
                has_acted = False
                in_movement_phase = True  # Phase de marche
                in_attack_phase = False  # Phase d'attaque
                target_attack = False  # Phase du choix de la zone d'effet
                indice=None
                attaque=False
                deplacement_x=0
                deplacement_y=0
    
                while not has_acted:  # Boucle pour gérer les actions de l'unité
                    # Gestion de la portée d'attaque si en phase d'attaque
                    if in_attack_phase and not target_attack:
                        skill_index = skill_selector.selected_skill_index
                        if hasattr(unit, 'attack_range') and len(unit.attack_range) > skill_index:
                            skill_range = unit.attack_range[skill_index]
                            attack_range = unit.generate_circle(
                                unit.x, unit.y, [(wall.x, wall.y) for wall in self.walls], skill_range
                            )
                        else:
                            print("Erreur : attack_range manquant ou index de compétence invalide.")
                            attack_range = []
    
                    # Met à jour l'affichage
                    self.flip_display(
                        player_choice=None,
                        selected_units=player_units,
                        current_player=current_player,
                        movement_range=movement_range if in_movement_phase else None,
                        attack_range=attack_range,  # Toujours afficher la zone rouge
                        destination=destination,
                        skill_selector=skill_selector,
                        effect_zone=effect_zone if target_attack else None,  # Affiche la zone jaune uniquement si active
                        unit=unit
                    )
    
                    # Afficher l'interface des compétences
                    skill_selector.display(unit, WIDTH)
        
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
    
                        if event.type == pygame.KEYDOWN:
                            dx, dy = 0, 0
    
                            # Phase de marche
                            if in_movement_phase:
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
                                if new_destination in movement_range:
                                    destination = new_destination

                                # Validation de la marche avec Espace
                                if event.key == pygame.K_SPACE:
                                    if destination in movement_range and destination not in positions_units:
                                        unit.x, unit.y = destination  # Déplacer l'unité
                                        in_movement_phase = False  # Fin de la phase marche
                                        in_attack_phase = True  # Passer à la phase d'attaque
    
                                # Passer la marche avec Tab
                                if event.key == pygame.K_TAB:
                                    in_movement_phase = False  # Fin de la phase marche
                                    in_attack_phase = True  # Passer à la phase d'attaque
    
                            # Phase d'attaque
                            elif in_attack_phase:

                                    # Naviguer dans les compétences
                                if event.key == pygame.K_UP:
                                    skill_selector.update_selection(-1, len(classes_methods(Unit, type(unit))))
                                elif event.key == pygame.K_DOWN:
                                    skill_selector.update_selection(1, len(classes_methods(Unit, type(unit))))
                                
                                # Sélectionner la compétence avec les touches numériques 1, 2, 3, 4
                                if event.key == pygame.K_1:
                                    skill_selector.selected_skill_index = 0  # La première compétence (index 0)
                                    indice=0
                                    print(f"indice={indice}")
                                elif event.key == pygame.K_2:
                                    skill_selector.selected_skill_index = 1  # La deuxième compétence (index 1)
                                    indice=1
                                    print(f"indice={indice}")
                                elif event.key == pygame.K_3:
                                    skill_selector.selected_skill_index = 2  # La troisième compétence (index 2)
                                    indice=2
                                    print(f"indice={indice}")
                                elif event.key == pygame.K_4:
                                    skill_selector.selected_skill_index = 3  # La quatrième compétence (index 3)
                                    indice=3
                                    print(f"indice={indice}")
                                # Valider l'attaque avec A
                                
                                
                                if indice is not None:
                                    print(f"indice={indice}")
                                    if event.key == pygame.K_a:
                                        selected_skill = skill_selector.get_selected_skill(unit)
                                        print(f"Attaque validée avec la compétence : {selected_skill}")
                                        in_attack_phase = False
                                        target_attack = True
                                        print(f"target_attack={target_attack}")
        
                                    # Passer l'attaque avec Tab
                                    if event.key == pygame.K_TAB:
                                        print("Hors zone de portée.")
                                        has_acted = True  # Fin du tour de l'unité
        
                                # Phase d'attaque sur la cible
                                    
                                    attaque=True
                                    while target_attack:
                                        print(f"target_attack={target_attack}")
                                        effect_center = destination  # Par défaut, le centre est la destination de l’unité
                                        # Initialisation de la zone d’effet et du type de zone
                                        
                                        if not effect_zone:
                                            effect_center = destination # Par défaut, le centre est la destination de l’unité
                                            effect_size =2   # Taille par défaut de la zone d’effet
                                            selected_effect_type = "square"  # Par défaut, la forme est un carré
                                            effect_zone = generate_square_coordinates(effect_center[0], effect_center[1], size=unit.rayon[indice])
                                            

                                        if event.key == pygame.K_TAB:
                                            print("Hors zone de portée.")
                                            has_acted = True  # Fin du tour de l'unité
                                            target_attack = False
                                            print("Attaque annulée.")
                                            
                                        # Gestion des événements pour la zone d’effet
                                

                                        
                                        elif unit.effect_zone[indice]=="carré":  # Choix d'une zone carré
                                            print("losange selectionne.")
                                            running = True
                                            x_pos, y_pos = effect_center
                                            print(f"position x={x_pos} et y={y_pos}")
                                            print("center")
                                            while running:
                                                for event in pygame.event.get():
                                                    if event.type == pygame.QUIT:
                                                        pygame.quit()
                                                        exit()
                                                    if event.type == pygame.KEYDOWN:  
                                                                                                   
                                                        if event.key==pygame.K_e:
                                                            print("Fin du choix de la position de l'attaque.")
                                                            running = False
                                                       
                                                          
                                                        if event.key == pygame.K_LEFT:
                                                            if (x_pos-1, y_pos) in attack_range :
                                                                x_pos-=1
                                                        elif event.key == pygame.K_RIGHT:
                                                            if (x_pos+1, y_pos) in attack_range :
                                                                x_pos+=1
                                                        elif event.key == pygame.K_UP:
                                                            if (x_pos, y_pos-1) in attack_range :
                                                                y_pos-=1
                                                        elif event.key == pygame.K_DOWN:
                                                            if (x_pos, y_pos+1) in attack_range :
                                                                y_pos+=1
                                                        effect_center = (x_pos, y_pos)
                                                        effect_center=effect_center
                                                        effect_zone = generate_square_coordinates(effect_center[0], effect_center[1], size=unit.rayon[indice])  
                                                                                                        
                                                        target_attack = False  # Fin de la phase d’attaque
                                                effect_zone = [effet for effet in effect_zone if effet in attack_range] # On garde que les effets dans la zone d'attaque
                                                self.flip_display(
                                                    selected_units=player_units,
                                                    current_player=current_player,
                                                    movement_range=None,
                                                    attack_range=attack_range,  # La zone rouge reste affichée
                                                    destination=destination,
                                                    effect_zone=effect_zone,  # Affiche la zone d’effet jaune
                                                    skill_selector=skill_selector,
                                                    unit=unit
                                                )



                                        elif unit.effect_zone[indice]=="rhombus":  # Choix d'une zone losange
                                            print("losange selectionne.")
                                            running = True
                                            x_pos, y_pos = effect_center
                                            print(f"position x={x_pos} et y={y_pos}")
                                            print("center")
                                            while running:
                                                for event in pygame.event.get():
                                                    if event.type == pygame.QUIT:
                                                        pygame.quit()
                                                        exit()
                                                    if event.type == pygame.KEYDOWN:  
                                                                                                   
                                                        if event.key==pygame.K_e:
                                                            print("Fin du choix de la position de l'attaque.")
                                                            running = False
                                                       
                                                          
                                                        if event.key == pygame.K_LEFT:
                                                            if (x_pos-1, y_pos) in attack_range :
                                                                x_pos-=1
                                                        elif event.key == pygame.K_RIGHT:
                                                            if (x_pos+1, y_pos) in attack_range :
                                                                x_pos+=1
                                                        elif event.key == pygame.K_UP:
                                                            if (x_pos, y_pos-1) in attack_range :
                                                                y_pos-=1
                                                        elif event.key == pygame.K_DOWN:
                                                            if (x_pos, y_pos+1) in attack_range :
                                                                y_pos+=1
                                                        effect_center = (x_pos, y_pos)
                                                        effect_center=effect_center
                                                        effect_zone = generate_rhombus(effect_center[0], effect_center[1], size=unit.rayon[indice])  
                                                                                                        
                                                        target_attack = False  # Fin de la phase d’attaque
                                                effect_zone = [effet for effet in effect_zone if effet in attack_range] # On garde que les effets dans la zone d'attaque
                                                self.flip_display(
                                                    selected_units=player_units,
                                                    current_player=current_player,
                                                    movement_range=None,
                                                    attack_range=attack_range,  # La zone rouge reste affichée
                                                    destination=destination,
                                                    effect_zone=effect_zone,  # Affiche la zone d’effet jaune
                                                    skill_selector=skill_selector,
                                                    unit=unit
                                                )

                                        elif unit.effect_zone[indice]=="ligne":  # Choix d'une ligne
                                            print("ligne sélectionnée.")
                                            running = True
                                            x_pos, y_pos = effect_center
                                            print(f"position x={x_pos} et y={y_pos}")
                                            print("center")
                                            while running:
                                                for event in pygame.event.get():
                                                    if event.type == pygame.QUIT:
                                                        pygame.quit()
                                                        exit()
                                                    if event.type == pygame.KEYDOWN:  
                                                                                                   
                                                        if event.key==pygame.K_e:
                                                            print("Fin du choix de la position de l'attaque.")
                                                            running = False
                                                        elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :  # Choix d'une barre horizontale
                                                            selected_effect_type = "horizontal"
                                                            if event.key == pygame.K_LEFT:
                                                                if (x_pos-1, y_pos) in attack_range :
                                                                    x_pos-=1
                                                            elif event.key == pygame.K_RIGHT:
                                                                if (x_pos+1, y_pos) in attack_range :
                                                                    x_pos+=1
                                                            effect_center = (x_pos, y_pos)
                                                            effect_center=effect_center
                                                            effect_zone = generate_horizontal_bar(effect_center[0], effect_center[1], length=unit.rayon[indice])
                                                            print("Barre horizontale sélectionnée.")
                                                            print(f"position x={x_pos} et y={y_pos}")                                                        
                                                            target_attack = False  # Fin de la phase d’attaque

                                                        elif event.key == pygame.K_UP or event.key== pygame.K_DOWN:  # Choix d'une barre verticale
                                                            selected_effect_type = "vertical"
                                                            if event.key == pygame.K_UP:
                                                                if (x_pos, y_pos-1) in attack_range :
                                                                    y_pos-=1
                                                            elif event.key == pygame.K_DOWN:
                                                                if (x_pos, y_pos+1) in attack_range :
                                                                    y_pos+=1
                                                            effect_center = (x_pos, y_pos)
                                                            effect_center=effect_center
                                                            effect_zone = generate_vertical_bar(effect_center[0], effect_center[1], length=unit.rayon[indice])
                                                            print("Barre verticale sélectionnée.")
                                                            print(f"position x={x_pos} et y={y_pos}")
                                                            target_attack = False  # Fin de la phase d’attaque
                                                        else:
                                                            print("la zone d'effet doit être dans la zone de portée")
                                                        

                                                            print(f"effect_zone={effect_zone}")
                                                            print("Barre verticale sélectionnée.")
                                                            print(f"position x={x_pos} et y={y_pos}")
                                                            target_attack = False  # Fin de la phase d’attaque
                                                        self.flip_display(
                                                            selected_units=player_units,
                                                            current_player=current_player,
                                                            movement_range=None,
                                                            attack_range=attack_range,  # La zone rouge reste affichée
                                                            destination=destination,
                                                            effect_zone=effect_zone,  # Affiche la zone d’effet jaune
                                                            skill_selector=skill_selector,
                                                            unit=unit
                                                    )
                                                                                        
                                       
                                        print("Attaque validée.")
                                        for effect_cell in effect_zone:
                                            # Vérifiez si une unité ennemie est dans la zone d’effet
                                            for enemy in self.player2_units if unit.team == "player1" else self.player1_units:
                                                if (enemy.x, enemy.y) == effect_cell:
                                                    attack_target(unit, enemy, skill_selector.selected_skill_index)
                                                    print(f"l'unité  {unit.__class__.__name__} a attaqué l'unité {enemy.__class__.__name__} et son hp est égale à {enemy.health} ")
                                                    
                                        target_attack = False  # Fin de la phase d’attaque
                                        has_acted = True






                
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
            
    def flip_display(
    self,
    selected_units=None,
    player_choice=None,
    current_player=None,
    movement_range=None,
    destination=None,
    attack_range=None,
    skill_selector=None,
    effect_zone = None,
    unit=None
):
        """Affiche la grille, les murs, la portée, et les unités selon l'état du jeu."""
        self.screen.fill(BLACK)  # Efface l'écran
    
        # Phase de sélection
        if selected_units is not None and player_choice is not None:
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
            # Grille et murs
            for x in range(0, WIDTH, CELL_SIZE):
                for y in range(0, HEIGHT, CELL_SIZE):
                    rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, WHITE, rect, 1)
    
            for wall in self.walls:
                pygame.draw.rect(
                    self.screen, BROWN,
                    (wall.x * CELL_SIZE, wall.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )
    
            # Portée de déplacement
            if movement_range:
                for (px, py) in movement_range:
                    pygame.draw.rect(
                        self.screen, (169, 169, 169),  # Gris clair
                        (px * CELL_SIZE + 1, py * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2)
                    )
    
            # Portée d'attaque
            
            if attack_range:
                for (px, py) in attack_range:
                    pygame.draw.rect(
                        self.screen, RED,  # Rouge pour portée d'attaque
                        (px * CELL_SIZE + 1, py * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2)
                    )
    
            # Destination (carré violet)
            if destination:
                dx, dy = destination
                pygame.draw.rect(
                    self.screen, (138, 43, 226),  # Violet pour la destination
                    (dx * CELL_SIZE, dy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )
            if effect_zone:
                for (px, py) in effect_zone:
                    pygame.draw.rect(self.screen, (255, 255, 0), (px * CELL_SIZE + 1, py * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2))

    
            # Dessin des unités
            for unit1 in self.player1_units:
                unit1.draw(self.screen)
            for unit2 in self.player2_units:
                unit2.draw(self.screen)
    
        # Appeler l'interface des compétences si disponible
        if skill_selector and unit:
            skill_selector.display(unit, WIDTH)
    
        pygame.display.flip()





    
    



def main():
    pygame.init()
    
    # Définir une fenêtre élargie pour inclure l'interface des compétences
    extended_width = WIDTH + 300  # Largeur étendue pour inclure les compétences
    screen = pygame.display.set_mode((extended_width, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    game = Game(screen)

    # Créer une instance de SkillSelector
    skill_selector = SkillSelector(screen, width=200)

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
    
    clock = pygame.time.Clock()  # Pour gérer les FPS
    while True:
        game.handle_player_turn(skill_selector)  # Passe le sélecteur de compétences au jeu
        clock.tick(FPS)  # Limite la boucle à un certain nombre de FPS

        

if __name__ == "__main__":
    main()