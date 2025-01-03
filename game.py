import pygame
import random
from cells import *
from unit import  * 
from Func_extra import * 
from All_Variables import * 
from abc import ABC, abstractmethod




class Game:
    def __init__(self, screen):
        """
         pour créer une relation de composition ou d'agrégation entre la classe game et la classe unit, vu que l'instanciation de la classe unit se fait principalement par 
        la classe game et même l'interaction avec la classe unit se fait principalement par la classe game 
        """

        self.skill_select = SkillSelector(screen, width=200)
        self.screen = screen        
        self.available_units = units_availables_game
        self.walls = wall_coor
        self.player1_units = []
        self.player2_units = []
        self.skill_select.player1_units = self.player1_units
        self.skill_select.player2_units = self.player2_units
        self.unit_in_game = None 
    
    def select_units(self, player_number):
        """Permet à un joueur de choisir ses unités."""
        selected_units = []
        player_choice = 0  # Initialisation de l'unité à choisir
        
        self.flip_display(
        selected_units=selected_units,
        player_choice=player_choice,
        current_player=player_number
        ) 
        
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
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        selected_unit = self.available_units[player_choice].clone()
                    
                        # Vérification basée sur les noms de classe pour éviter les doublons dans chaque equipe 
                        if selected_unit.__class__.__name__ not in [unit.__class__.__name__ for unit in selected_units]:
                            selected_units.append(selected_unit)
                       

    
                    self.flip_display(selected_units, player_choice,current_player=player_number)
    
        # Ajout des unités sélectionnées
        if player_number == 1:
            self.player1_units = selected_units
            print("les unités choisies par le joueur 1 sont : ")
            for units_player in self.player1_units:
                units_player.team = "player1"
                print(f"{units_player.__class__.__name__} -- {units_player.team} \n")
        else:
            self.player2_units = selected_units
            print("les unités choisies par le joueur 2 sont : ")
            for units_player in self.player2_units:
                units_player.team = "player2"
                print(f"{units_player.__class__.__name__} -- {units_player.team} \n")
                
        
  
    
                
    def handle_player_turn(self,unit,all_unit):
        """
        Gère les tours des deux joueurs avec gestion des phases marche et attaque,
        en affichant correctement la portée d'attaque.
        """
        #gestion de l'affichage de la barre à gauche 
        self.unit_in_game  = all_unit
        self.skill_select.current_unit = unit
        self.skill_select.all_units = all_unit
        self.skill_select.display(unit, WIDTH, all_unit) 

        current_player = 0  # Le joueur actuel (la valeur 0 pour le joueur 1, 1 pour le joueur 2)
    
        # Phase de déplacement : Calcul de la portée de mouvement
        movement_range = unit.generate_circle(unit.x, unit.y, [(wall[0], wall[1]) for wall in self.walls])
        positions_units = {(u.x, u.y) for u in all_unit}
        ally_positions = {(ally.x, ally.y) for ally in self.player1_units if unit.team == "player1"} or {(ally.x, ally.y) for ally in self.player2_units if unit.team == "player2"}
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
                skill_index = self.skill_select.selected_skill_index
                if hasattr(unit, 'attack_range') and len(unit.attack_range) > skill_index:
                    skill_range = unit.attack_range[skill_index]
                    attack_range = unit.generate_circle(
                        unit.x, unit.y, [(wall[0], wall[1]) for wall in self.walls], skill_range
                    )
                else:
                    print("Erreur : attack_range manquant ou index de compétence invalide.")
                    attack_range = []

            # Met à jour l'affichage
            self.flip_display(
                player_choice=None,
                selected_units=self.player1_units if unit.team=="player1" else self.player2_units,
                current_player=current_player,
                movement_range=movement_range if in_movement_phase else None,
                attack_range=attack_range if not has_attacked else None,  # Toujours afficher la zone rouge
                destination=destination if in_movement_phase else None,
                skill_selector=self.skill_select,
                effect_zone=effect_zone if target_attack else None,  # Affiche la zone jaune uniquement si active
                unit=unit
            )

            # Afficher l'interface des compétences
            self.skill_select.display(unit, WIDTH,self.unit_in_game)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
                if event.type == pygame.KEYDOWN:
                    dx, dy = 0, 0
                    if not in_movement_phase and not in_attack_phase:
                        if event.key == pygame.K_m and not has_moved:
                            in_movement_phase = True
                        elif event.key == pygame.K_p and not has_attacked:
                            in_attack_phase = True
                    
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
                        if new_destination in movement_range or new_destination in ally_positions:
                            destination = new_destination

                        # Validation de la marche avec Espace
                        if event.key == pygame.K_SPACE:
                            if destination in movement_range and destination not in positions_units:
                                unit.x, unit.y = destination  # Déplacer l'unité
                                in_movement_phase = False  # Fin de la phase marche
                                has_moved = True
                                in_attack_phase = True  # Passer à la phase d'attaque
                            if (unit.x , unit.y) in poison_cell: # si l'unité est sur une case poison elle subit les degats
                                unit.add_effect(unit,"poison", 0.07, 2)
                                print(f"{unit.__class__.__name__} est sur une case poison et devient donc empoisonné pendant 2 tours !")
                                if unit.health<=1  :
                                    print(f"{unit.__class__.__name__} ({unit.team}) n'a plus de PVs ! L'unité est donc éliminé !") 
                                    if unit in self.player1_units: # si l'unité appartient au joueur 1 on le supprime de la liste des unités du joueur 1
                                        self.player1_units.remove(unit)
                                    elif unit in self.player2_units:
                                        self.player2_units.remove(unit) # si l'unité appartient au joueur 2 on le supprime de la liste des unités du joueur 2
                                    all_unit.remove(unit) # on le supprime de la liste de toutes les unités

                            movement_range = unit.generate_circle(unit.x, unit.y, [(wall[0], wall[1]) for wall in self.walls])
                            positions_units = {(u.x, u.y) for u in all_unit}
                            ally_positions = {(ally.x, ally.y) for ally in self.player1_units if unit.team == "player1"} or {(ally.x, ally.y) for ally in self.player2_units if unit.team == "player2"}
                            movement_range = [p for p in movement_range if p not in positions_units]

                        # Passer la marche avec Tab
                        if event.key == pygame.K_TAB:
                            in_movement_phase = False  # Fin de la phase marche
                            has_moved = True
                            in_attack_phase = True  # Passer à la phase d'attaque
                            if (unit.x , unit.y) in poison_cell:
                                unit.add_effect(unit,"poison", 0.07, 2) # si l'unité est sur une case poison elle subit les degats
                                if unit.health<=1:
                                    print(f"{unit.__class__.__name__} ({unit.team}) n'a plus de PVs ! L'unité est donc éliminé !") 
                                    if unit in self.player1_units:
                                        self.player1_units.remove(unit) # si l'unité appartient au joueur 1 on le supprime de la liste des unités du joueur 1
                                    elif unit in self.player2_units:
                                        self.player2_units.remove(unit) # si l'unité appartient au joueur 2 on le supprime de la liste des unités du joueur 2
                                    all_unit.remove(unit)
                            movement_range = unit.generate_circle(unit.x, unit.y, [(wall[0], wall[1]) for wall in self.walls])
                            positions_units = {(u.x, u.y) for u in all_unit}
                            ally_positions = {(ally.x, ally.y) for ally in self.player1_units if unit.team == "player1"} or {(ally.x, ally.y) for ally in self.player2_units if unit.team == "player2"}
                            movement_range = [p for p in movement_range if p not in positions_units]
                        
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
                            self.skill_select.selected_skill_index = 0  # La première compétence pour chaque unité  (index 0)
                        elif event.key == pygame.K_2:
                            self.skill_select.selected_skill_index = 1  # La deuxième compétence (index 1)
                        elif event.key == pygame.K_3:
                            self.skill_select.selected_skill_index = 2  # La troisième compétence (index 2)
                        elif event.key == pygame.K_4:
                            self.skill_select.selected_skill_index = 3  # La quatrième compétence (index 3)
                        # Valider l'attaque avec A
                        if event.key == pygame.K_a:
                            selected_skill = self.skill_select.get_selected_skill(unit)
                            print(f"Attaque validée avec la compétence : {selected_skill}")
                            in_attack_phase = False
                            target_attack = True

                        # Passer l'attaque avec Tab
                        if event.key == pygame.K_TAB:
                            in_attack_phase=False
                            has_attacked = True  # Fin du tour de l'unité
                            in_movement_phase= True

                    # Phase d'attaque sur la cible
                    elif target_attack:
                        # Initialisation de la zone d’effet et du type de zone
                        if not effect_zone:
                            effect_center = [unit.x,unit.y]  # Par défaut, le centre est la destination de l’unité
                            effect_size =unit.effect_zone[self.skill_select.selected_skill_index]   # Taille par défaut de la zone d’effet
                            selected_effect_type = unit.effect_shape[self.skill_select.selected_skill_index]  # Par défaut, la forme est un carré
                            effect_zone = generate_square_coordinates(effect_center[0], effect_center[1], size=1) 
                        if event.key == pygame.K_TAB:
                            in_attack_phase=False
                            has_attacked = True  # Fin du tour de l'unité
                            in_movement_phase= True
                            target_attack=False
                    
                        # Déplacement de la zone d’effet à l’intérieur de la zone rouge
                        elif event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                            dx, dy = 0, 0
                            if event.key == pygame.K_LEFT: # Déplacement à gauche
                                dx = -1
                            elif event.key == pygame.K_RIGHT: # Déplacement à droite
                                dx = 1
                            elif event.key == pygame.K_UP: # Déplacement vers le haut
                                dy = -1
                            elif event.key == pygame.K_DOWN: # Déplacement vers le bas
                                dy = 1
                    
                            # Calcul de la nouvelle position du centre
                            new_center = (effect_center[0] + dx, effect_center[1] + dy)
                    
                            # Vérification : la nouvelle position doit être dans la zone rouge ( dans la zone d'attaque)
                            if new_center in attack_range:
                                effect_center = new_center
                    
                            # Recalcule la zone d’effet en fonction du type sélectionné
                            if selected_effect_type == "square":
                                effect_zone = generate_square_coordinates(effect_center[0], effect_center[1], size=effect_size) # pour les zonne d'effet de forme carré
                            elif selected_effect_type == "line":
                                if effect_center[0] <destination[0]  and effect_center[1] ==destination[1] :
                                    effect_zone = generate_horizontal_bar_gauche(effect_center[0], effect_center[1], length=effect_size) # pour les zonne d'effet de forme ligne ou case
                                elif effect_center[0] >destination[0]  and effect_center[1] ==destination[1]:
                                    effect_zone = generate_horizontal_bar(effect_center[0], effect_center[1], length=effect_size)
                                elif effect_center[0] ==destination[0]  and effect_center[1] <destination[1] :
                                    effect_zone = generate_vertical_bar_haut(effect_center[0], effect_center[1], length=effect_size)
                                elif effect_center[0] ==destination[0]  and effect_center[1] >destination[1]:
                                    effect_zone = generate_vertical_bar(effect_center[0], effect_center[1], length=effect_size)
                                elif effect_center[0] ==destination[0]  and effect_center[1] ==destination[1]:
                                    effect_zone = generate_square_coordinates(effect_center[0], effect_center[1], size=1)
                            elif selected_effect_type == "rhombus": 
                                effect_zone = generate_rhombus(effect_center[0], effect_center[1], size=effect_size) # pour les zonne d'effet de forme losange
                    
                        # Met à jour l’affichage avec la zone d’effet et la portée d’attaque
                        self.flip_display(
                            selected_units=self.player1_units if unit.team=="player1" else self.player2_units,
                            current_player=current_player,
                            movement_range=None,
                            attack_range=attack_range,  # La zone rouge reste affichée
                            destination=destination,
                            effect_zone=effect_zone,  # Affiche la zone d’effet jaune
                            skill_selector=self.skill_select,
                            unit=unit
                        )
                    
                        # Validation de l’attaque avec 'A'
                        if event.key == pygame.K_a:
                            print("Attaque validée.")
                            for effect_cell in effect_zone:
                                # Vérifiez si une unité ennemie est dans la zone d’effet
                                for target in all_unit:
                                    if (target.x, target.y) == effect_cell:
                                        attack_target(unit, target, self.skill_select.selected_skill_index)
                                        if target.health<=0:            # si l'unité n'a plus de PVs
                                            print(f"{target.__class__.__name__} ({target.team}) n'a plus de PVs ! L'unité est donc éliminé !")
                                            if target in self.player1_units:
                                                self.player1_units.remove(target) # si l'unité appartient au joueur 1 on le supprime de la liste des unités du joueur 1
                                            elif target in self.player2_units:
                                                self.player2_units.remove(target) # si l'unité appartient au joueur 2 on le supprime de la liste des unités du joueur 2
                                            all_unit.remove(target)
                            movement_range = unit.generate_circle(unit.x, unit.y, [(wall[0], wall[1]) for wall in self.walls])
                            positions_units = {(u.x, u.y) for u in all_unit}
                            ally_positions = {(ally.x, ally.y) for ally in self.player1_units if unit.team == "player1"} or {(ally.x, ally.y) for ally in self.player2_units if unit.team == "player2"}
                            movement_range = [p for p in movement_range if p not in positions_units]
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
            unit1.changes(2+i,5-i,team='player1')
            print(f"l'unité {unit1.__class__.__name__} -- joueur 1 de coordonnées {unit1.x}-{unit1.y} a été ajoutée ")
            #self.player1_units.append(unit1)
        
        for j, unit2 in enumerate(self.player2_units):
            #unit2.x, unit2.y = j, GRID_SIZE - 1  # Ligne inférieure pour le joueur 2
            unit2.changes(12+j,15-j,team='player2')
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
    progress_bar = None, 
    unit=None
):
        """Affiche la grille, les murs, la portée, et les unités selon l'état du jeu."""
        #self.screen.fill(BLACK)  # Efface l'écran
        
        """Affiche la grille, les murs, la portée, et les unités selon l'état du jeu."""
        
        background_image = pygame.image.load(introduction_img_path).convert()  # Remplacez avec votre chemin d'image
        background_image = pygame.transform.scale(background_image, (extended_width , HEIGHT))  # Adapter à la taille de l'écran
       
        self.screen.blit(background_image, (0, 0))
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Couleur noire avec alpha (150/255)
        self.screen.blit(overlay, (0, 0))
        
        if selected_units is not None and player_choice is not None:
            
        
            # Affichage des instructions et des choix
            font = pygame.font.Font(Orbitron_Regular_font_path , 35)
            
            instruction_text = font.render(f"Le choix du joueur {current_player}", True, player1_color if current_player ==1 else player2_color)

            self.screen.blit(instruction_text, (230, 10))

            # Afficher la liste des unités disponibles
            font = pygame.font.Font(courier_font_path , 23)
            for i, unit in enumerate(self.available_units):
                
                # Si l'unité est sélectionnée, elle est en blanc, sinon en gris transparent
                if i == player_choice:
                    
                    color = Gold  # Couleur pour l'unité sélectionnée (en clair)
                    
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
    
            # Afficher les om des unités sélectionnées
            pygame.draw.rect(
                    self.screen,
                    (230,230,230), 
                    (340, HEIGHT-315+(4*25),190,150),  
                    border_radius=20 
                )
            for j, unit in enumerate(selected_units):
                color = player1_color if current_player==1 else player2_color
                selected_text = font.render(f"{unit.__class__.__name__}", True,color)
                self.screen.blit(selected_text, (360, HEIGHT-200+(j*25)))
    
            # Afficher les détails de l'unité actuellement survolée
            hovered_unit = self.available_units[player_choice]
            if hovered_unit.icon_path:

                # Charger et redimensionner l'icône
                icon = pygame.image.load(hovered_unit.icon_path).convert_alpha()
                icon = pygame.transform.scale(icon, (150, 160))  # Adjust the icon size
                

        
                pygame.draw.rect(
                    self.screen,
                    LIGHT_GRAY, 
                    (700, 200+40, 150, 180)  
                )
                
                pygame.draw.rect(
                    self.screen,
                    LIGHT_GRAY,  
                    (700, 300+40, 150, 120),  
                    border_radius=20  
                )
                
                #Creation d une surface pour l'icône avec des coins arrondis
                rounded_icon_surface = pygame.Surface((150, 160+40), pygame.SRCALPHA)  # Transparent surface for the icon
                
                # creation d'un rectangle avec des coins arrondis
                pygame.draw.rect(
                    rounded_icon_surface,  
                    (255, 255, 255, 255), 
                    (0, 0, 150, 160),  
                    border_top_left_radius=20,  
                    border_top_right_radius=20 
                )
                
                # Appliquer l'icône à la surface avec des coins arrondis
                rounded_icon_surface.blit(icon, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
                
                # Afficher l'icône à la position souhaitée
                self.screen.blit(rounded_icon_surface, (700, 60+40))  # Place the icon at the desired position
                
                # Définir la couleur de la bordure:
                gray_mouse = (169, 169, 169)  
                pygame.draw.rect(self.screen,gray_mouse,  (700, 60+40, 150, 360),  border_radius=20,  width=3  )
            

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
                self.screen.blit(stat_text, (705, 270 + k * 30))

                
        elif progress_bar : 
            
            """
            Simule une barre de progression en bas de l'écran avec un contour blanc et un remplissage blanc.
            :param triggered_signal: Booléen indiquant si le processus doit démarrer.
            """
            # Définir les dimensions de la barre de progression
            bar_width = WIDTH   # Largeur de la barre (avec marges des bords)
            bar_height = 20  # Hauteur de la barre
            bar_x = 150  # Position X (centrée horizontalement)
            bar_y = HEIGHT - 35  # Position Y (près du bas de l'écran)
          
            # Vitesse de remplissage
            fill_speed = 5  # Nombre de pixels ajoutés à chaque mise à jour
          
            # Si le signal est activé, démarrez la simulation
            progress = 0  # Initialisez la progression à 0
            while progress < bar_width:
                # Effacer l'ancienne barre pour rafraîchir
                pygame.draw.rect(self.screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height))  # Fond noir pour effacer
      
                # Dessiner le contour de la barre en blanc
                pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
      
                # Dessiner la barre remplie en blanc
                pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, progress, bar_height))
      
                # Mettre à jour la progression
                progress += fill_speed
      
                # Actualiser l'affichage
                pygame.display.flip()
      
                # Ajouter un petit délai pour rendre la progression visible
                pygame.time.delay(10)
             
        else:
            self.screen.fill(BLACK)
            image =pygame.image.load(map_img_path)
            self.screen.blit(image,(0,0))

    
            # Portée de déplacement
            if movement_range:
                for (px, py) in movement_range:
                    surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)  # Transparence activée
                    surface.fill(gris_transparent)  # Remplir avec le gris transparent

                    # Dessiner la surface sur l'écran à la position correcte
                    self.screen.blit(surface, (px * CELL_SIZE + 1, py * CELL_SIZE + 1))  # Positionner
    
            # Portée d'attaque
            if attack_range: # Afficher la portée d'attaque
      
                for (px, py) in attack_range:
                    # Créer une surface pour le rectangle :
                    surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)  
                    surface.fill(red_transparent)  

                    # Dessiner la surface sur l'écran à la position correcte
                    self.screen.blit(surface, (px * CELL_SIZE + 1, py * CELL_SIZE + 1))  
    
            # Destination (carré violet)
            if destination:
                dx, dy = destination
                pygame.draw.rect(
                    self.screen, (138, 43, 226),  # Violet pour la destination
                    (dx * CELL_SIZE, dy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )
            if effect_zone: # affichage de la zone d'effet

                for (px, py) in effect_zone:
        
                    surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)  
                    surface.fill(jaune_transparent)  

                   
                    self.screen.blit(surface, (px * CELL_SIZE + 1, py * CELL_SIZE + 1))  

            # Dessin des unités
            for unit1 in self.player1_units:
                unit1.draw(self.screen)
                pygame.draw.rect(self.screen, RED, (unit1.x * CELL_SIZE, unit1.y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)
            for unit2 in self.player2_units:
                unit2.draw(self.screen)
                pygame.draw.rect(self.screen, BLUE, (unit2.x * CELL_SIZE, unit2.y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)
            if effect_zone:

                for (px, py) in effect_zone:
                    
                    surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)  
                    surface.fill(jaune_transparent)  
                    self.screen.blit(surface, (px * CELL_SIZE + 1, py * CELL_SIZE + 1))  # Positionner
        # Appeler l'interface des compétences si disponible
        if skill_selector and unit:
            skill_selector.display(unit, WIDTH,self.unit_in_game)
    
        pygame.display.flip()

def main():
    pygame.init()
    team1_win_image = pygame.image.load(win_player1_path)  # Image de victoire pour l'équipe 1
    team2_win_image = pygame.image.load(win_player2_path)  # Image de victoire pour l'équipe 2
    # Définir une fenêtre élargie pour inclure l'interface des compétences

    extended_width = WIDTH + 300  # Largeur étendue pour inclure les compétences
    screen = pygame.display.set_mode((extended_width, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Créer une instance de SkillSelector
    
    game = Game(screen)

    # Charger l'image de fond
    background_image = pygame.image.load(introduction_img_path).convert() 
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

    # Le joueur 1 choisit ses unités
    print("Joueur 1 : choisissez vos unités")
    game.select_units(player_number=1)

    # Le joueur 2 choisit ses unités
    print("Joueur 2 : choisissez vos unités")
    game.select_units(player_number=2)
    game.flip_display(progress_bar=True)

    # Place les unités sur la grille
    game.assign_unit_positions()

    # Lance le jeu
    print("Le jeu commence !")
    global current_unit_index
    current_unit_index = 0
    all_unit = game.player1_units + game.player2_units
    random.shuffle(all_unit)
    print("Dans cette partie, les unités joueront dans cet ordre : ")
    print('|| ',end='')
    for unit in all_unit :
        print(f"{unit.__class__.__name__} ({unit.team}) ||  ", end='')
    print('')
    clock = pygame.time.Clock()  # Pour gérer les FPS
    fin=0
    while fin==0:
          # Passe le sélecteur de compétences au jeu
        current_unit = all_unit[current_unit_index]
        if ("chute" in current_unit.effects and current_unit.effects["chute"]["applied"]) or ("ejection" in current_unit.effects and current_unit.effects["ejection"]["applied"]) or ("commotion" in current_unit.effects and current_unit.effects["commotion"]["applied"]): #VERIFIE SI L'UNITE EST EN ETAT DE CHUTE EJECTION OU COMMOTION
            print("---------------------------------------------------")
            print(f"{current_unit.__class__.__name__} n'est pas en état de se battre ! Son tour est sauté !")
            current_unit.apply_effects() #applique les effets, supprime ceux qui ont fait leur nombre de tours
            current_unit_index = (current_unit_index + 1) % len(all_unit) #augmente l'indice, donc saute le tour de l'unité
            current_unit = all_unit[current_unit_index] #Ca devient le tour de l'unité suivante
        print("---------------------------------------------------")
        current_unit.apply_effects() #applique les effets de l'unité qui va jouer
        print(f"{current_unit.__class__.__name__} ({current_unit.team}) joue son tour.")
        game.handle_player_turn(current_unit,all_unit) #je sais pas si c'est possible mais si possible il faudrait qu'on puisse mettre en parametre "current_unit", comme ça, ça prend bien en compte l'unité qui a sauté de tour je sais pas si tu vois ce que je veux dire
        #skill_selector.display()


        print(f"Fin du tour de {current_unit.__class__.__name__} ({current_unit.team}).")
        current_unit_index = (current_unit_index + 1) % len(all_unit)
        clock.tick(FPS)  # Limite la boucle à un certain nombre de FPS
       

        if len(game.player1_units) == 0:
            fin = 1
            winner_image = team2_win_image  # Équipe 2 a gagné
        elif len(game.player2_units) == 0:
            fin = 1
            winner_image = team1_win_image  # Équipe 1 a gagné

    # Affiche l'image de victoire
    display_winner(screen, winner_image)
    display_credits(screen, createurs, font_name="Arial", font_size=40, text_color=(255, 255, 255), bg_color=(0, 0, 0))
            
    print("fin de la partie")
    if len(game.player1_units)==0 :
        print("Bravo à l'équipe 2 d'avoir gagné !!")

          

    else :
        print("Bravo à l'équipe 1 d'avoir gagné !!")

      

if __name__ == "__main__":
    main()








