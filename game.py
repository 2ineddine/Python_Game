import pygame
import random
import sys
import os
import inspect 
from cells import *
from unit import  * 
from Func_extra import * 
#################################################################################################################

ICON_PATHS = {  # Dictionnaire associant le nom d'une unité au chemin de son icône.
    "Noah": "/home/ityt/Documents/Hicham/Cours FAC/Python/Projet_jeu_zineddine/images/Noah.PNG",
    "Sena": "/home/ityt/Documents/Hicham/Cours FAC/Python/Projet_jeu_zineddine/images/Sena.PNG",
    "Alexandria": "/home/ityt/Documents/Hicham/Cours FAC/Python/Projet_jeu_zineddine/images/Alexandria.PNG",
    "Cammuravi": "/home/ityt/Documents/Hicham/Cours FAC/Python/Projet_jeu_zineddine/images/Cammuravi.PNG",
    "Lanz": "/home/ityt/Documents/Hicham/Cours FAC/Python/Projet_jeu_zineddine/images/Lanz.PNG",
    "Mio": "/home/ityt/Documents/Hicham/Cours FAC/Python/Projet_jeu_zineddine/images/Mio.PNG",
    "Ashera": "/home/ityt/Documents/Hicham/Cours FAC/Python/Projet_jeu_zineddine/images/Ashera.PNG", 
    "Zeon": "/home/ityt/Documents/Hicham/Cours FAC/Python/Projet_jeu_zineddine/images/Zeon.PNG",
    "Eunie": "/home/ityt/Documents/Hicham/Cours FAC/Python/Projet_jeu_zineddine/images/Eunie.PNG",
    "Taion": "/home/ityt/Documents/Hicham/Cours FAC/Python/Projet_jeu_zineddine/images/Taion.PNG",
    "Valdi": "/home/ityt/Documents/Hicham/Cours FAC/Python/Projet_jeu_zineddine/images/Valdi.PNG",
    "Maitre": "/home/ityt/Documents/Hicham/Cours FAC/Python/Projet_jeu_zineddine/images/Maitre.PNG"
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
                
        

    
                
    def handle_player_turn(self, skill_selector,unit,all_unit):
        """
        Gère les tours des deux joueurs avec gestion des phases marche et attaque,
        en affichant correctement la portée d'attaque.
        """
        current_player = 0  # Le joueur actuel (0 pour le joueur 1, 1 pour le joueur 2)
    
        # Phase de déplacement : Calcul de la portée de mouvement
        movement_range = unit.generate_circle(unit.x, unit.y, [(wall.x, wall.y) for wall in self.walls])
        positions_units = {(u.x, u.y) for u in all_unit}
        movement_range = [p for p in movement_range if p not in positions_units]

        attack_range = []  # Initialiser la portée d'attaque
        effect_zone = []  # Zone d'effet initiale
        destination = (unit.x, unit.y)
        unit.is_selected = True
        has_acted = False
        has_attacked = False
        has_moved = False
        in_movement_phase = False  # Phase de marche
        in_attack_phase = False  # Phase d'attaque
        target_attack = False  # Phase du choix de la zone d'effet

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
                selected_units=self.player1_units if unit.team=="player 1" else self.player2_units,
                current_player=current_player,
                movement_range=movement_range if in_movement_phase else None,
                attack_range=attack_range if not has_attacked else None,  # Toujours afficher la zone rouge
                destination=destination if in_movement_phase else None,
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
                    if not in_movement_phase and not in_attack_phase:
                        if event.key == pygame.K_m and not has_moved:
                            in_movement_phase = True
                            print("Phase de mouvement activée")
                        elif event.key == pygame.K_p and not has_attacked:
                            in_attack_phase = True
                            print("Phase d'attaque activée")
                    
                    # Phase de marche
                    if in_movement_phase and has_moved==False:
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
                                has_moved = True
                                in_attack_phase = True  # Passer à la phase d'attaque

                        # Passer la marche avec Tab
                        if event.key == pygame.K_TAB:
                            in_movement_phase = False  # Fin de la phase marche
                            has_moved = True
                            in_attack_phase = True  # Passer à la phase d'attaque
                            
                    # Phase d'attaque
                    elif in_attack_phase and has_attacked==False:
                        """
                        # Naviguer dans les compétences
                        if event.key == pygame.K_UP:
                            skill_selector.update_selection(-1, len(classes_methods(Unit, type(unit))))
                        elif event.key == pygame.K_DOWN:
                            skill_selector.update_selection(1, len(classes_methods(Unit, type(unit))))
                        """
                         # Sélectionner la compétence avec les touches numériques 1, 2, 3, 4
                        if event.key == pygame.K_1:
                            skill_selector.selected_skill_index = 0  # La première compétence (index 0)
                        elif event.key == pygame.K_2:
                            skill_selector.selected_skill_index = 1  # La deuxième compétence (index 1)
                        elif event.key == pygame.K_3:
                            skill_selector.selected_skill_index = 2  # La troisième compétence (index 2)
                        elif event.key == pygame.K_4:
                            skill_selector.selected_skill_index = 3  # La quatrième compétence (index 3)
                        # Valider l'attaque avec A
                        if event.key == pygame.K_a:
                            selected_skill = skill_selector.get_selected_skill(unit)
                            print(f"Attaque validée avec la compétence : {selected_skill}")
                            in_attack_phase = False
                            target_attack = True

                        # Passer l'attaque avec Tab
                        if event.key == pygame.K_TAB:
                            print("Hors zone de portée.")
                            in_attack_phase=False
                            has_attacked = True  # Fin du tour de l'unité
                            in_movement_phase= True

                    # Phase d'attaque sur la cible
                    elif target_attack:
                        # Initialisation de la zone d’effet et du type de zone
                        if not effect_zone:
                            effect_center = [unit.x,unit.y]  # Par défaut, le centre est la destination de l’unité
                            effect_size =unit.effect_zone[skill_selector.selected_skill_index]   # Taille par défaut de la zone d’effet
                            selected_effect_type = unit.effect_shape[skill_selector.selected_skill_index]  # Par défaut, la forme est un carré
                            effect_zone = generate_square_coordinates(effect_center[0], effect_center[1], size=1)
                        if event.key == pygame.K_TAB:
                            print("Hors zone de portée.")
                            in_attack_phase=False
                            has_attacked = True  # Fin du tour de l'unité
                            in_movement_phase= True
                            target_attack=False
                    
                        # Déplacement de la zone d’effet à l’intérieur de la zone rouge
                        elif event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                            dx, dy = 0, 0
                            if event.key == pygame.K_LEFT:
                                dx = -1
                            elif event.key == pygame.K_RIGHT:
                                dx = 1
                            elif event.key == pygame.K_UP:
                                dy = -1
                            elif event.key == pygame.K_DOWN:
                                dy = 1
                    
                            # Calcul de la nouvelle position du centre
                            new_center = (effect_center[0] + dx, effect_center[1] + dy)
                    
                            # Vérification : la nouvelle position doit être dans la zone rouge
                            if new_center in attack_range:
                                effect_center = new_center
                    
                            # Recalcule la zone d’effet en fonction du type sélectionné
                            if selected_effect_type == "square":
                                effect_zone = generate_square_coordinates(effect_center[0], effect_center[1], size=effect_size)
                            elif selected_effect_type == "line":
                                if effect_center[0] <destination[0]  and effect_center[1] ==destination[1] :
                                    effect_zone = generate_horizontal_bar_gauche(effect_center[0], effect_center[1], length=effect_size)
                                elif effect_center[0] >destination[0]  and effect_center[1] ==destination[1]:
                                    effect_zone = generate_horizontal_bar(effect_center[0], effect_center[1], length=effect_size)
                                elif effect_center[0] ==destination[0]  and effect_center[1] <destination[1] :
                                    effect_zone = generate_vertical_bar_haut(effect_center[0], effect_center[1], length=effect_size)
                                elif effect_center[0] ==destination[0]  and effect_center[1] >destination[1]:
                                    effect_zone = generate_vertical_bar(effect_center[0], effect_center[1], length=effect_size)
                                elif effect_center[0] ==destination[0]  and effect_center[1] ==destination[1]:
                                    effect_zone = generate_square_coordinates(effect_center[0], effect_center[1], size=1)
                            elif selected_effect_type == "rhombus":
                                effect_zone = generate_rhombus(effect_center[0], effect_center[1], size=effect_size)
                    
                        # Met à jour l’affichage avec la zone d’effet et la portée d’attaque
                        self.flip_display(
                            selected_units=self.player1_units if unit.team=="player 1" else self.player2_units,
                            current_player=current_player,
                            movement_range=None,
                            attack_range=attack_range,  # La zone rouge reste affichée
                            destination=destination,
                            effect_zone=effect_zone,  # Affiche la zone d’effet jaune
                            skill_selector=skill_selector,
                            unit=unit
                        )
                    
                        # Validation de l’attaque avec 'A'
                        if event.key == pygame.K_a:
                            print("Attaque validée.")
                            for effect_cell in effect_zone:
                                # Vérifiez si une unité ennemie est dans la zone d’effet
                                for target in all_unit:
                                    if (target.x, target.y) == effect_cell:
                                        attack_target(unit, target, skill_selector.selected_skill_index)
                                        if target.health<=0:
                                            print(f"target = {target}")
                                            if target in self.player1_units:
                                                self.player1_units.remove(target)
                                            elif target in self.player2_units:
                                                self.player2_units.remove(target)
                                            all_unit.remove(target)
                            in_attack_phase=False
                            has_attacked = True
                            in_movement_phase= True
                            target_attack=False
                    if has_attacked and has_moved:
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
    global current_unit_index
    current_unit_index = 0
    all_unit = game.player1_units + game.player2_units
    random.shuffle(all_unit)
    print(all_unit)
    clock = pygame.time.Clock()  # Pour gérer les FPS
    fin=0
    while fin==0:
          # Passe le sélecteur de compétences au jeu
        current_unit = all_unit[current_unit_index]
        if ("chute" in current_unit.effects and current_unit.effects["chute"]["applied"]) or ("ejection" in current_unit.effects and current_unit.effects["ejection"]["applied"]) or ("commotion" in current_unit.effects and current_unit.effects["commotion"]["applied"]): #VERIFIE SI L'UNITE EST EN ETAT DE CHUTE EJECTION OU COMMOTION
            current_unit.apply_effects() #applique les effets, supprime ceux qui ont fait leur nombre de tours
            current_unit_index = (current_unit_index + 1) % len(all_unit) #augmente l'indice, donc saute le tour de l'unité
            current_unit = all_unit[current_unit_index] #Ca devient le tour de l'unité suivante
        current_unit.apply_effects() #applique les effets de l'unité qui va jouer
        print(f"{current_unit} joue son tour.")
        game.handle_player_turn(skill_selector,current_unit,all_unit) #je sais pas si c'est possible mais si possible il faudrait qu'on puisse mettre en parametre "current_unit", comme ça, ça prend bien en compte l'unité qui a sauté de tour je sais pas si tu vois ce que je veux dire
        print(f"Fin du tour de {current_unit}.")
        current_unit_index = (current_unit_index + 1) % len(all_unit)
        clock.tick(FPS)  # Limite la boucle à un certain nombre de FPS
        if len(game.player1_units)==0 or len(game.player2_units)==0 :
            fin = 1
    print("fin de la partie")
    if len(game.player1_units)==0 :
        print("Bravo à l'équipe 2 d'avoir gagné !!")
    else :
        print("Bravo à l'équipe 1 d'avoir gagné !!")
        

if __name__ == "__main__":
    main()