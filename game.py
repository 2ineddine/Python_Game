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
#################################################################################################################
extended_width = WIDTH + 300
# Constantes
#GRID_SIZE = 25
#CELL_SIZE = 25
#WIDTH = GRID_SIZE * CELL_SIZE
#HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
gray_mouse = (169, 169, 167)
light_gray = (211, 211, 211)

# Définir les couleurs dans des variables
WHITE = (255, 255, 255)  # Blanc pour l'unité sélectionnée
GRAY = (169, 169, 169)   # Gris clair pour l'unité non sélectionnée (effet nébuleux)
SEMI_TRANSPARENT = (255, 255, 255, 128)  # Blanc semi-transparent pour l'effet flou (alpha 128)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BROWN = (165, 42, 42)
BLUE = (0, 0, 255)
SEMI_TRANSPARENT_BLUE = (0, 0, 255, 128)  # For glowing effects
LIGHT_BLUE = (0, 0, 255, 64)             # Softer glow
DODGER_BLUE = (30, 144, 255)  # Original color
LIGHTER_BLUE = (100, 180, 255)  # Brighter version of blue for the border
SEMI_TRANSPARENT_LIGHTER_BLUE = (100, 180, 255, 128)  # Transparent blue for glowing effect
DODGER_BLUE = (30, 144, 255)  # Original blue color
LIGHT_BLUE = (100, 180, 255)  # Lighter blue for the glowing effect
SEMI_TRANSPARENT_BLUE = (100, 180, 255, 128)  # Transparent blue for the glowing effect
DODGER_BLUE = (30, 144, 255)  # Original blue color
LIGHT_BLUE = (100, 180, 255)  # Lighter blue for the glowing effect
SEMI_TRANSPARENT_BLUE = (100, 180, 255, 128)  # Transparent blue for the glowing effect
BLACK = (0, 0, 0)  # Color for the background
BLUE_BORDER = (30, 144, 255)  # The desired blue color for the thin border
Gold= (255, 239, 140)

noir_charbon = (43, 43, 43)
blanc_casse = (244, 244, 244)
gris_acier = (161, 161, 161)
bleu_marine = (0, 51, 102)

# Palette énergique et vive
orange_vif = (255, 131, 0)
jaune_citron = (255, 235, 0)
rose_corail = (255, 73, 113)
bleu_roi = (0, 71, 171)

# Palette douce et naturelle
vert_menthe = (152, 255, 152)
lavande_pastel = (214, 168, 255)
beige_sable = (245, 222, 179)
bleu_poudre = (176, 224, 230)
#################################################################################################################
#Fonts_paths 
courier_font_path = "E:\PythonV0.02\CourierPrime-Bold.ttf"
consolas_font_path = "E:\PythonV0.02\ConsolaMono-Bold.ttf"
din_font_path  = "E:\PythonV0.02\DIN1451-36breit.ttf"
roboto_regular_font_path = "E:\PythonV0.02\Roboto-Regular.ttf"
roboto_thin_font_path = "E:\PythonV0.02\Roboto-Thin.ttf"
Trajan_Regular_font_path = "E:\PythonV0.02\Trajan-Regular.ttf"
Orbitron_Regular_font_path = "E:\PythonV0.02\Orbitron-Regular.ttf"
OrbitronV_font_path  = "E:\PythonV0.02\Orbitron-V.ttf" 

#################################################################################################################

class Game:
    def __init__(self, screen, skill_select):
       # pour créer une relation de composition ou d'agrégation entre la classe game et la classe unit, vu que l'instanciation de la classe unit se fait principalement par 
       #la classe game et même l'interaction avec la classe unit se fait principalement par la classe game 
       self.skill_select= skill_select
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
        
        self.flip_display(
        selected_units=selected_units,
        player_choice=player_choice,
        current_player=player_number
        )   
    
        while len(selected_units) < 3:  # Chaque joueur choisit 4 unités
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
        """
        Gère les tours des deux joueurs avec gestion des phases marche et attaque,
        en affichant correctement la portée d'attaque.
        """
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
                                    has_acted = True  # Fin du tour de l'unité
    
                            # Phase d'attaque sur la cible
                            elif target_attack:
                                # Initialisation de la zone d’effet et du type de zone
                                if not effect_zone:
                                    effect_center = destination  # Par défaut, le centre est la destination de l’unité
                                    effect_size =2   # Taille par défaut de la zone d’effet
                                    selected_effect_type = "square"  # Par défaut, la forme est un carré
                                    effect_zone = generate_square_coordinates(effect_center[0], effect_center[1], size=unit.effect_zone[skill_selector.selected_skill_index])
                                if event.key == pygame.K_TAB:
                                    print("Hors zone de portée.")
                                    has_acted = True  # Fin du tour de l'unité
                                    
                                # Gestion des événements pour la zone d’effet
                                if event.key == pygame.K_z:  # Choix d'une zone carrée
                                    selected_effect_type = "square"
                                    effect_zone = generate_square_coordinates(effect_center[0], effect_center[1], size=unit.effect_zone[skill_selector.selected_skill_index])
                                    print("Zone carrée sélectionnée.")
                            
                                elif event.key == pygame.K_e:  # Choix d'une barre horizontale
                                    selected_effect_type = "horizontal"
                                    effect_zone = generate_horizontal_bar(effect_center[0], effect_center[1], length=unit.effect_zone[skill_selector.selected_skill_index])
                                    print("Barre horizontale sélectionnée.")
                            
                                elif event.key == pygame.K_r:  # Choix d'une barre verticale
                                    selected_effect_type = "vertical"
                                    effect_zone = generate_vertical_bar(effect_center[0], effect_center[1], length=unit.effect_zone[skill_selector.selected_skill_index])
                                    print("Barre verticale sélectionnée.")
                            
                                elif event.key == pygame.K_f:  # Choix d'une zone losange
                                    selected_effect_type = "rhombus"
                                    effect_zone = generate_rhombus(effect_center[0], effect_center[1], size=unit.effect_zone[skill_selector.selected_skill_index])                                    
                                    print("Losange sélectionné.")
                            
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
                                        elif selected_effect_type == "horizontal":
                                            effect_zone = generate_horizontal_bar(effect_center[0], effect_center[1], length=effect_size)
                                        elif selected_effect_type == "vertical":
                                            effect_zone = generate_vertical_bar(effect_center[0], effect_center[1], length=effect_size)
                                        elif selected_effect_type == "rhombus":
                                            effect_zone = generate_rhombus(effect_center[0], effect_center[1], size=effect_size)
                            
                                # Met à jour l’affichage avec la zone d’effet et la portée d’attaque
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
                            
                                # Validation de l’attaque avec 'A'
                                if event.key == pygame.K_a:
                                    print("Attaque validée.")
                                    for effect_cell in effect_zone:
                                        # Vérifiez si une unité ennemie est dans la zone d’effet
                                        for enemy in self.player2_units if unit.team == "player1" else self.player1_units:
                                            if (enemy.x, enemy.y) == effect_cell:
                                                attack_target(unit, enemy, skill_selector.selected_skill_index)
                                                print(f"l'unité  {unit.__class__.__name__} a attaqué l'unité {enemy.__class__.__name__} et son hp est égale à {enemy.health} ")
                                                
                                    target_attack = False  # Fin de la phase d’attaque
                                    has_acted = True
                            


            if has_acted and current_player ==0:
                current_player+=1
            else :
                current_player-=1



                
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
        #self.screen.fill(BLACK)  # Efface l'écran
        
        """Affiche la grille, les murs, la portée, et les unités selon l'état du jeu."""
        
        background_image = pygame.image.load("E:/PythonV0.00/introduction_picture.png").convert()  # Remplacez avec votre chemin d'image
        background_image = pygame.transform.scale(background_image, (extended_width , HEIGHT))  # Adapter à la taille de l'écran
       
        self.screen.blit(background_image, (0, 0))
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Couleur noire avec alpha (150/255)
        self.screen.blit(overlay, (0, 0))
        
        if selected_units is not None and player_choice is not None:
            
            
            # Affichage des instructions et des choix
            font = pygame.font.Font(Orbitron_Regular_font_path , 35)
            
            instruction_text = font.render(f"Le choix du joueur {current_player}", True, (182, 0, 0) if current_player ==1 else (0, 0, 160))

            self.screen.blit(instruction_text, (230, 10))

            # Afficher la liste des unités disponibles
            font = pygame.font.Font(courier_font_path , 23)
            for i, unit in enumerate(self.available_units):
                
                # Si l'unité est sélectionnée, elle est en blanc, sinon en gris transparent
                if i == player_choice:
                    
                    color = WHITE  # Couleur pour l'unité sélectionnée (en clair)
                    
                    # Afficher l'unité sélectionnée en couleur normale (blanche)
                    text = font.render(f"{unit.__class__.__name__}", True, color)
                    self.screen.blit(text, (50, 90 + i * 31))  # Positionner normalement
                else:
                    color = gris_acier  # Couleur gris clair pour l'unité non sélectionnée (pour l'effet nébuleux)
            
                    # Créer un texte avec transparence (effet nébuleux)
                    text_surface = font.render(f"{unit.__class__.__name__}", True, color)
            
                    # Créer une surface transparente et appliquer le texte avec transparence
                    blurred_surface = pygame.Surface((text_surface.get_width(), text_surface.get_height()), pygame.SRCALPHA)
                    blurred_surface.blit(text_surface, (0, 0))
            
                    # Appliquer un léger flou sur la surface (blurry effect)
                    blurred_surface.set_alpha(128)  # Appliquer un alpha de 128 pour le flou (semi-transparent)
            
                    # Afficher le texte nébuleux (flou) pour les unités non sélectionnées
                    self.screen.blit(blurred_surface, (50, 90 + i * 31))
    
            # Afficher les unités déjà sélectionnées
            for j, unit in enumerate(selected_units):
                selected_text = font.render(f"Choisie: {unit.__class__.__name__}", True, (0, 255, 255))
                self.screen.blit(selected_text, (400, 50 + j * 30))
    
            # Afficher les détails de l'unité actuellement survolée
            hovered_unit = self.available_units[player_choice]
            if hovered_unit.icon_path:
                # Charger et redimensionner l'icône
                icon = pygame.image.load(hovered_unit.icon_path).convert_alpha()
                icon = pygame.transform.scale(icon, (150, 160))  # Adjust the icon size
                
                # Définir la couleur gris clair
                LIGHT_GRAY = (211, 211, 211)  # Light gray color (RGB)
                
                # Dessiner l'arrière-plan gris clair avec des coins arrondis
                pygame.draw.rect(
                    self.screen,
                    LIGHT_GRAY,  # Light gray color for the background
                    (600, 200+40, 150, 180)  # Position and size of the upper part
                )
                
                pygame.draw.rect(
                    self.screen,
                    LIGHT_GRAY,  # Light gray color for the background
                    (600, 300+40, 150, 120),  # Position and size of the lower part
                    border_radius=20  # Rounded corners only at the bottom
                )
                
                # Create a transparent surface for the icon
                rounded_icon_surface = pygame.Surface((150, 160+40), pygame.SRCALPHA)  # Transparent surface for the icon
                
                # Create a mask with rounded corners only at the top
                pygame.draw.rect(
                    rounded_icon_surface,  # Surface to draw on
                    (255, 255, 255, 255),  # Fill color for the rounded top corners (opaque white)
                    (0, 0, 150, 160),  # Size of the icon rectangle
                    border_top_left_radius=20,  # Rounded top-left corner
                    border_top_right_radius=20  # Rounded top-right corner
                )
                
                # Blit the icon onto the rounded surface
                rounded_icon_surface.blit(icon, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
                
                # Blit the rounded surface to the screen
                self.screen.blit(rounded_icon_surface, (600, 50+40))  # Place the icon at the desired position
                
                # Optional: Draw a border around the icon (with rounded corners)
                gray_mouse = (169, 169, 169)  # Mouse-over border color
                pygame.draw.rect(
                    self.screen,
                    gray_mouse,  # Border color around the icon
                    (600, 50+40, 150, 372),  # Position and size of the icon
                    border_radius=20,  # Rounded corners for the icon
                    width=3  # Border thickness
                )

            # Afficher les caractéristiques de l'unité
            stats = [
                f"Health: {hovered_unit.health}",
                f"Attack Power: {hovered_unit.attack_power}",
                f"Magic Power: {hovered_unit.magic_power}",
                f"Defence: {hovered_unit.defence}",
                f"Speed: {hovered_unit.speed}",
                f"Agility: {hovered_unit.agility}",
            ]
            font = pygame.font.Font(courier_font_path , 14)
            for k, stat in enumerate(stats):
                stat_text = font.render(stat, True, BLACK)
                self.screen.blit(stat_text, (605, 270 + k * 30))
            
        else:
            self.screen.fill(BLACK)
             
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

    # Créer une instance de SkillSelector
    skill_selector = SkillSelector(screen, width=200)
    game = Game(screen, skill_selector)

    # Charger l'image de fond
    background_image = pygame.image.load("E:/PythonV0.00/introduction_picture.png").convert()  # Remplacez avec votre chemin d'image
    background_image = pygame.transform.scale(background_image, (extended_width, HEIGHT))  # Adapter à la taille de l'écran
    
    # Boucle principale du menu
    while True:
        choice_index = show_menu(screen, background_image)
        
        if choice_index == -1:  # L'utilisateur a fermé la fenêtre
            print("Fermeture du programme...")
            break
        elif choice_index == 0:  # START
            print("Option START choisie")
            break  # Sortir de la boucle pour démarrer le jeu
        elif choice_index == 1:  # QUITTER
            print("Option QUITTER choisie")
            break  # Fermer la fenêtre

    # Si l'utilisateur a choisi "START", on lance le jeu
    print("Joueur 1 : choisissez vos unités")
    game.select_units(player_number=1)

    print("Joueur 2 : choisissez vos unités")
    game.select_units(player_number=2)

    # Place les unités sur la grille
    game.assign_unit_positions()

    print("Le jeu commence !")
    
    clock = pygame.time.Clock()  # Pour gérer les FPS
    while True:
        game.handle_player_turn(skill_selector)  # Passe le sélecteur de compétences au jeu
        clock.tick(FPS)  # Limite la boucle à un certain nombre de FPS

if __name__ == "__main__":
    main()