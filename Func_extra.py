import sys
import pygame
import sys
from game import * 
from cells import *
from unit import *  

from All_Variables import *  


# pour avoir les méthodes appelable de chaque unité
def classes_methods(parent_class, child_class):
    all_methods = set(dir(child_class))  # Récupère toutes les méthodes de l'enfant
    parent_methods = set(dir(parent_class))  # Récupère les méthodes de la classe parente
    child_methods_ordered = all_methods - parent_methods  # Méthodes spécifiques de l'enfant
    
    # Filtrage pour ne conserver que les méthodes qui commencent par 'def'
    filtered_methods = [method for method in child_methods_ordered if callable(getattr(child_class, method)) and not method.startswith("__")]
    
    return sorted(filtered_methods, key=lambda mot: (mot[0], mot[1] if len(mot) > 1 else "")) #oganiser en ordre alphabétique les dénomination des méthodes
     

# Application d'une méthode spécifique sur une instance
def application_of_specific_method_of_instance(target_unit, instance, child_methods_ordered, method_number):
    """
    Applique une méthode spécifique sur une cible.

    Arguments :
    - target_unit : L'objet cible sur lequel appliquer la méthode.
    - instance : L'instance contenant la méthode.
    - child_methods_ordered : Liste triée des méthodes spécifiques (résultat de `classes_methods`).
    - method_number : L'indice de la méthode à appeler dans la liste triée.

    Retourne :
    - Aucun. Appelle la méthode directement sur `target_unit`.
    """
    # Vérifier si method_number est valide
    if method_number < 0 or method_number >= len(child_methods_ordered):
        raise IndexError(f"method_number {method_number} est hors des limites.")
    
    # Récupérer la méthode depuis l'instance
    instance_method_name = child_methods_ordered[method_number]
    instance_method = getattr(instance, instance_method_name)
    
    # Appeler la méthode avec target_unit
    try:
        instance_method(target_unit)
    except TypeError as e:
        raise TypeError(f"Erreur lors de l'appel de la méthode '{instance_method_name}': {e}")
        
        
        
        
        
    
# la fonction qui combinerai les 2 précédentes     
def attack_target (child_instance, target_instance, method_number):
    """
    Récupère les méthodes spécifiques, trie, puis applique la méthode spécifique sur la cible.

    Arguments :
    - parent_class : La classe parente.
    - child_instance : L'instance de la classe enfant contenant les méthodes spécifiques.
    - target_instance : L'instance cible sur laquelle appliquer la méthode.
    - method_number : L'indice de la méthode spécifique à appliquer dans la liste triée.

    Retourne :
    - La liste triée des méthodes spécifiques pour référence.
    """
    # Étape 1 : Récupérer les méthodes spécifiques triées
    child_methods_ordered = classes_methods(Unit, child_instance)
    
    # Affichage des méthodes spécifiques pour débogage
    #print("Méthodes spécifiques triées :", child_methods_ordered)
    
    # Étape 2 : Appliquer la méthode spécifique sur l'instance cible
    application_of_specific_method_of_instance(target_instance, child_instance, child_methods_ordered, method_number)
    
    # Retourner la liste triée des méthodes pour référence
    return child_methods_ordered

     



# Génération d'un carré avec contraintes sur x et y
def generate_square_coordinates(x, y, size=1):
    """
    Génère toutes les coordonnées à l'intérieur d'un carré de taille `size` à partir du coin supérieur gauche (x, y).
    Cette version ne vérifie pas si les coordonnées dépassent une grille donnée.
    
    :param x: Coordonnée x du coin supérieur gauche du carré.
    :param y: Coordonnée y du coin supérieur gauche du carré.
    :param size: La taille du carré (par défaut 1).
    :return: Liste de toutes les coordonnées dans le carré.
    """
    # Liste pour stocker toutes les coordonnées à l'intérieur du carré
    square_coordinates = []

    # Parcours de toutes les coordonnées à l'intérieur du carré de taille `size`
    for i in range(x, x + size):
        for j in range(y, y + size):
            square_coordinates.append((i, j))
    
    return square_coordinates

# Génération d'une barre horizontale avec contraintes
def generate_horizontal_bar(x, y, length):
    """
    Génère les coordonnées d'une barre horizontale de longueur `length` à partir du point (x, y).
    Cette version ne vérifie pas si les coordonnées dépassent une grille donnée.
    
    :param x: Coordonnée x du point de départ de la barre.
    :param y: Coordonnée y du point de départ de la barre.
    :param length: La longueur de la barre horizontale.
    :return: Liste de toutes les coordonnées le long de la barre.
    """
    # Liste pour stocker les coordonnées de la barre
    bar_coordinates = []
    
    # Générer les coordonnées le long de l'axe horizontal (augmentation de x)
    for i in range(length):
        new_x = x + i
        bar_coordinates.append((new_x, y))
    
    return bar_coordinates
def generate_horizontal_bar(x, y, length):
    """
    Génère les coordonnées d'une barre horizontale de longueur `length` à partir du point (x, y).
    Cette version ne vérifie pas si les coordonnées dépassent une grille donnée.
    
    :param x: Coordonnée x du point de départ de la barre.
    :param y: Coordonnée y du point de départ de la barre.
    :param length: La longueur de la barre horizontale.
    :return: Liste de toutes les coordonnées le long de la barre.
    """
    # Liste pour stocker les coordonnées de la barre
    bar_coordinates = []
    
    # Générer les coordonnées le long de l'axe horizontal (augmentation de x)
    for i in range(length):
        new_x = x + i
        bar_coordinates.append((new_x, y))
    
    return bar_coordinates

def generate_horizontal_bar_gauche(x, y, length):
    """
    Génère les coordonnées d'une barre horizontale de longueur `length` à partir du point (x, y).
    Cette version ne vérifie pas si les coordonnées dépassent une grille donnée.
    
    :param x: Coordonnée x du point de départ de la barre.
    :param y: Coordonnée y du point de départ de la barre.
    :param length: La longueur de la barre horizontale.
    :return: Liste de toutes les coordonnées le long de la barre.
    """
    # Liste pour stocker les coordonnées de la barre
    bar_coordinates = []
    
    # Générer les coordonnées le long de l'axe horizontal (augmentation de x)
    for i in range(length):
        new_x = x - i
        bar_coordinates.append((new_x, y))
    
    return bar_coordinates



# Génération d'une barre verticale avec contraintes
def generate_vertical_bar(x, y, length):
    """
    Génère les coordonnées d'une barre verticale de longueur `length` à partir du point (x, y).
    Cette version ne vérifie pas si les coordonnées dépassent une grille donnée.
    
    :param x: Coordonnée x du point de départ de la barre.
    :param y: Coordonnée y du point de départ de la barre.
    :param length: La longueur de la barre verticale.
    :return: Liste de toutes les coordonnées le long de la barre.
    """
    # Liste pour stocker les coordonnées de la barre
    bar_coordinates = []
    
    # Générer les coordonnées le long de l'axe vertical (augmentation de y)
    for i in range(length):
        new_y = y + i
        bar_coordinates.append((x, new_y))
    
    return bar_coordinates

def generate_vertical_bar_haut(x, y, length):
    """
    Génère les coordonnées d'une barre verticale de longueur `length` à partir du point (x, y).
    Cette version ne vérifie pas si les coordonnées dépassent une grille donnée.
    
    :param x: Coordonnée x du point de départ de la barre.
    :param y: Coordonnée y du point de départ de la barre.
    :param length: La longueur de la barre verticale.
    :return: Liste de toutes les coordonnées le long de la barre.
    """
    # Liste pour stocker les coordonnées de la barre
    bar_coordinates = []
    
    # Générer les coordonnées le long de l'axe vertical (augmentation de y)
    for i in range(length):
        new_y = y - i
        bar_coordinates.append((x, new_y))
    
    return bar_coordinates

# Génération d'une barre verticale avec contraintes
def generate_vertical_bar(x, y, length):
    """
    Génère les coordonnées d'une barre verticale de longueur `length` à partir du point (x, y).
    Cette version ne vérifie pas si les coordonnées dépassent une grille donnée.
    
    :param x: Coordonnée x du point de départ de la barre.
    :param y: Coordonnée y du point de départ de la barre.
    :param length: La longueur de la barre verticale.
    :return: Liste de toutes les coordonnées le long de la barre.
    """
    # Liste pour stocker les coordonnées de la barre
    bar_coordinates = []
    
    # Générer les coordonnées le long de l'axe vertical (augmentation de y)
    for i in range(length):
        new_y = y + i
        bar_coordinates.append((x, new_y))
    
    return bar_coordinates

# Générer un losange avec contraintes
def generate_rhombus(x, y, size):
    """
    Génère toutes les coordonnées à l'intérieur d'un losange centré en (x, y) et de taille `size`.
    Cette version ne vérifie pas si les coordonnées dépassent une grille donnée.
    
    :param x: Coordonnée x du centre du losange.
    :param y: Coordonnée y du centre du losange.
    :param size: La taille du losange, c'est-à-dire la distance du centre aux sommets.
    :return: Liste de toutes les coordonnées à l'intérieur du losange.
    """
    # Liste pour stocker les coordonnées du losange
    rhombus_coordinates = []
    
    # Pour chaque ligne y dans la plage de -size à +size (de haut en bas du losange)
    for i in range(-size, size + 1):
        # La distance horizontale à chaque ligne dépend de la ligne verticale
        horizontal_distance = size - abs(i)
        
        # Ajouter les coordonnées horizontales pour cette ligne
        for j in range(-horizontal_distance, horizontal_distance + 1):
            rhombus_coordinates.append((x + j, y + i))
    
    return rhombus_coordinates

def Display_introduction(screen):
    image = pygame.image.load("E:\PythonV0.00\introduction_picture.png")
    image = pygame.transform.scale(image, (extended_width, HEIGHT))
    screen.blit(image, (0, 0))

def render_text_with_border(text, font, text_color, border_color, border_width=2, x_pos=230, y_pos=10):
    # Ensure text is a string (if it’s a dynamic variable, ensure it's passed as a string)
    text = str(text)  # Convert to string just in case
    # Render the text in the border color
    for dx in range(-border_width, border_width + 1):
        for dy in range(-border_width, border_width + 1):
            if dx != 0 or dy != 0:  # Skip the center position to avoid overlapping
                # Render the border text
                border_text = font.render(text, True, border_color)
                screen.blit(border_text, (x_pos + dx, y_pos + dy))

    # Render the actual text on top of the border
    instruction_text = font.render(text, True, text_color)
    screen.blit(instruction_text, (x_pos, y_pos))

class SkillSelector:
    def __init__(self, screen,width=200):
        """
        Initialise l'interface de sélection des compétences.
        :param screen: Surface Pygame où dessiner l'interface.
        :param width: Largeur de la zone de sélection (par défaut : 200 pixels).
        """
        self.screen = screen
        self.width = width
        self.selected_skill_index = 0  # Index de la compétence actuellement sélectionnée
        self.player1_units = []
        self.player2_units = []
        self.current_unit = None
        self.all_units = None
        
        
        
    def display(self, unit, x_offset,units_in_game):
        """
        Affiche les compétences disponibles pour une unité, ses statistiques, son image,
        ainsi que les icônes des unités ennemies sous la section "Compétences".
        :param unit: L'unité dont les compétences doivent être affichées.
        :param x_offset: Décalage en x pour positionner la zone à droite de la grille.
        """
        # Obtenir les compétences spécifiques de l'unité
        skills = classes_methods(Unit, self.current_unit)
        skills = [skill.replace('_', ' ') for skill in skills]
        #self.current_unit = unit
        #self.all_units = unit_in_game
        # Dessiner la zone de fond
        pygame.draw.rect(self.screen, player1_color if unit.team == "player1" else player2_color, (x_offset, 0, self.width + 100, HEIGHT))  # Fond sombre
        pygame.draw.rect(self.screen, (200, 200, 200), (x_offset, 0, self.width + 100, HEIGHT), width=2)  # Contour
    
        # Afficher l'image de l'unité
        unit_image_rect = pygame.Rect(x_offset + 25, 20, 80, 80)  # Zone pour l'image
        unit_image = None
    
        # Charger l'image de l'unité si elle existe dans ICON_PATHS
        unit_name = type(unit).__name__
        if unit_name in ICON_PATHS:
            try:
                unit_image = pygame.image.load(ICON_PATHS[unit_name])
                unit_image = pygame.transform.scale(unit_image, (unit_image_rect.width, unit_image_rect.height))
                
            except pygame.error:
                print(f"Erreur : Impossible de charger l'image pour {unit_name}. Chemin : {ICON_PATHS[unit_name]}")
    
        if unit_image:
            self.screen.blit(unit_image, unit_image_rect)
        else:
            # Placeholder si l'unité n'a pas d'image
            pygame.draw.rect(self.screen, (150, 150, 150), unit_image_rect)
            placeholder_font = pygame.font.SysFont(courier_font_path, 15)
            placeholder_text = placeholder_font.render("No Image", True, (0, 0, 0))
            placeholder_rect = placeholder_text.get_rect(center=unit_image_rect.center)
            self.screen.blit(placeholder_text, placeholder_rect)
    
        # Afficher les statistiques (santé, limite de dégâts)
        stats = [
            ("Health", unit.health, unit.max_stats["health_max"], (0, 230, 0)),  # Santé en vert
            ("Limit", unit.cumul_damage, int(1.5 * unit.max_stats["health_max"]), (128, 0, 128)),  # Limite en rouge
        ]
    
        bar_x = x_offset + 120  # Position X des barres
        bar_y = 40  # Position initiale Y
        bar_width = 150
        bar_height = 10
        bar_spacing = 25
        font = pygame.font.Font(courier_font_path, 16)
    
        for stat_name, value, max_value, color in stats:
            # Dessiner le fond de la barre
            pygame.draw.rect(self.screen, (150, 150, 150), (bar_x, bar_y, bar_width, bar_height))
            # Dessiner la barre remplie selon la valeur
            filled_width = int((value / max_value) * bar_width)
            pygame.draw.rect(self.screen, color, (bar_x, bar_y, filled_width, bar_height))
            # Dessiner la bordure de la barre
            pygame.draw.rect(self.screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 2)
            # Afficher le texte de la statistique
            stat_text = font.render(f"{stat_name}  {value}/{max_value}"if stat_name == "Health" else f"{stat_name}     {value}/{max_value}", True, WHITE)
            self.screen.blit(stat_text, (bar_x, bar_y - 15))  # Texte au-dessus de la barre
            bar_y += bar_height + bar_spacing  # Passer à la barre suivante
    
        # Afficher le titre "Compétences"
        font = pygame.font.Font(courier_font_path, 28)
        title = font.render("UNITÉS ENNEMIES", True, WHITE)
        self.screen.blit(title, (x_offset + 15, 180))
    
        # Afficher les compétences
        for i, skill in enumerate(skills):
            font = pygame.font.Font(courier_font_path, 13)
            color = (
                WHITE if i == self.selected_skill_index 
                else (0, 0, 75) if unit.team == "player2" 
                else (106, 0, 0)
            )
            text = font.render(f"{skill}", True, color)
            self.screen.blit(text, (x_offset + 20, 100 + i * 16))
    
        # --- Afficher les icônes des unités ennemies sous la section "Compétences" ---
        # Déterminer l'équipe ennemie
        # --- Afficher les icônes des unités ennemies sous la section "Compétences" ---
        # Déterminer l'équipe ennemie
        
        """
        Affiche les informations de l'unité sélectionnée et les icônes des unités ennemies avec leur barre de santé.
        """
        # Déterminer l'équipe ennemie
        enemy_team = "player2" if unit.team == "player1" else "player1"
        enemy_units = [unitee for unitee in units_in_game if unitee.team == enemy_team]
     
        icon_size = 40  # Taille des icônes
        spacing = 28  # Espacement entre les icônes
        start_x = x_offset + 20  # Position de départ en X
        start_y = 230  # Position de départ de la ligne des images
        health_bar_height = 5  # Hauteur de la barre de santé
     
        font = pygame.font.SysFont(courier_font_path, 10)
     
        for i, enemy_unit in enumerate(enemy_units):
            enemy_unit_name = enemy_unit.__class__.__name__
     
            # Chargement de l'image de l'unité ennemie
            if enemy_unit_name in ICON_PATHS:
                icon_path = ICON_PATHS[enemy_unit_name]
                try:
                    enemy_image = pygame.image.load(icon_path)
                    enemy_image = pygame.transform.scale(enemy_image, (icon_size, icon_size))
                except pygame.error as e:
                    print(f"Erreur de chargement de l'image pour {enemy_unit_name}: {e}")
                    enemy_image = None
            else:
                print(f"Aucune icône définie pour l'unité {enemy_unit_name}")
                enemy_image = None
     
            # Calculer la position de l'icône
            icon_rect = pygame.Rect(start_x + i * (icon_size + spacing), start_y, icon_size, icon_size)
     
            # Afficher la barre de santé au-dessus de l'image
            health_percentage = enemy_unit.health / enemy_unit.max_stats["health_max"]
            health_bar_width = int(health_percentage * icon_size)
            health_bar_color = (0, 230, 0) if health_percentage > 0.5 else (230, 230, 0) if health_percentage > 0.2 else (230, 0, 0)
     
            health_bar_rect = pygame.Rect(icon_rect.left, icon_rect.top - health_bar_height - 2, health_bar_width, health_bar_height)
            pygame.draw.rect(self.screen, health_bar_color, health_bar_rect)  # Barre de santé
            pygame.draw.rect(self.screen, (0, 0, 0), (icon_rect.left, icon_rect.top - health_bar_height - 2, icon_size, health_bar_height), 1)  # Contour noir
     
            # Afficher l'image de l'unité ennemie
            if enemy_image:
                self.screen.blit(enemy_image, icon_rect)
            else:
                # Afficher un carré vide si l'image est manquante
                pygame.draw.rect(self.screen, (150, 150, 150), icon_rect)
                pygame.draw.rect(self.screen, (0, 0, 0), icon_rect, 2)
                placeholder_text = font.render("No Icon", True, (0, 0, 0))
                placeholder_rect = placeholder_text.get_rect(center=icon_rect.center)
                self.screen.blit(placeholder_text, placeholder_rect)







    def update_selection(self, direction, num_skills):
        """
        Met à jour la sélection en fonction de l'entrée utilisateur.
        :param direction: 1 pour descendre, -1 pour monter.
        :param num_skills: Nombre total de compétences disponibles.
        """
        self.selected_skill_index = (self.selected_skill_index + direction) % num_skills

    def get_selected_skill(self, unit):
        """
        Retourne la compétence actuellement sélectionnée.
        :param unit: L'unité pour laquelle la compétence est sélectionnée.
        :return: Le nom de la compétence sélectionnée.
        """
        skills = classes_methods(Unit, type(unit))
        return skills[self.selected_skill_index]

    def show_intro(self, screen):
        """
        Affiche une image d'introduction jusqu'à ce que le joueur appuie sur Entrée.
        :param screen: Surface Pygame où afficher l'image.
        :param image_path: Chemin de l'image à afficher.
        """
        image_path = "E:\PythonV0.00\introduction_picture.png"
        intro_image = pygame.image.load(image_path)  # Charger l'image
        intro_image = pygame.transform.scale(intro_image, screen.get_size())  # Adapter à la taille de l'écran
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False  # Quitter l'introduction quand Entrée est pressée
    
            screen.blit(intro_image, (0, 0))  # Dessiner l'image
            pygame.display.flip()  # Mettre à jour l'écran




def display_introduction_picture( screen):
    """
    Affiche une image d'introduction jusqu'à ce que le joueur appuie sur Entrée.
    :param screen: Surface Pygame où afficher l'image.
    :param image_path: Chemin de l'image à afficher.
    """
    image_path = "E:\PythonV0.00\introduction_picture.png"
    intro_image = pygame.image.load(image_path)  # Charger l'image
    intro_image = pygame.transform.scale(intro_image, screen.get_size())  # Adapter à la taille de l'écran
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False  # Quitter l'introduction quand Entrée est pressée

        screen.blit(intro_image, (0, 0))  # Dessiner l'image
        pygame.display.flip()  # Mettre à jour l'écran


def display_picture1( screen):
    """
    Affiche une image d'introduction jusqu'à ce que le joueur appuie sur Entrée.
    :param screen: Surface Pygame où afficher l'image.
    :param image_path: Chemin de l'image à afficher.
    """
    image_path = "E:\PythonV0.00\introduction_picture.png"
    intro_image = pygame.image.load(image_path)  # Charger l'image
    intro_image = pygame.transform.scale(intro_image, screen.get_size())  # Adapter à la taille de l'écran
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.blit(intro_image, (0, 0))  # Dessiner l'image
        pygame.display.flip()  # Mettre à jour l'écran
    
def display_picture(screen):
    """
    Affiche une image d'introduction et attend que la fenêtre soit fermée.
    :param screen: Surface Pygame où afficher l'image.
    """
    image_path = "E:/PythonV0.00/introduction_picture.png"
    intro_image = pygame.image.load(image_path)  # Charger l'image
    intro_image = pygame.transform.scale(intro_image, screen.get_size())  # Adapter à la taille de l'écran
    
    # Afficher l'image
    screen.blit(intro_image, (0, 0))  # Dessiner l'image
    pygame.display.flip()  # Mettre à jour l'écran
    
    # Attendre que l'utilisateur ferme la fenêtre
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Quitter la boucle lorsque l'utilisateur ferme la fenêtre
    pygame.quit()  # Quitter Pygame lorsque la fenêtre est fermée

################################ MENU PROGRAMME #########################################################################
# Remplacez ce chemin par le chemin correct de votre police
def show_menu(screen, background_image):
    """
    Affiche un menu interactif avec un effet de texte brouillé et une navigation au clavier.
    Retourne 0 si "START" est choisi ou quitte la fenêtre Pygame si "QUITTER" est choisi.
    
    Arguments:
    screen -- L'objet écran de Pygame (pygame.Surface)
    background_image -- Une surface (image) utilisée comme arrière-plan
    """
    # Options du menu
    menu_options = ["START", "QUITTER"]
    selected_index = 0  # Option actuellement sélectionnée

    # Charger l'image des rectangles derrière le texte
    menu_bar_image = pygame.image.load("menu_barre.png").convert_alpha()  # Utiliser convert_alpha() pour conserver la transparence
    menu_bar_image = pygame.transform.scale(menu_bar_image, (400, 240))  # Redimensionner l'image pour chaque option

    # Initialisation de la police
    font = pygame.font.Font(Orbitron_Regular_font_path , 29)

    # Fonction pour dessiner le menu
    def draw_menu(selected_index):
        screen.blit(background_image, (0, 0))

        # Ajouter un calque noir semi-transparent pour l'effet d'arrière-plan
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Couleur noire avec alpha (150/255)
        screen.blit(overlay, (0, 0))

        # Position des options de menu
        start_x = (screen.get_width()-300) // 2  # Position horizontale du rectangle
        start_y = screen.get_height() // 2  # Position verticale de la première option
        large_font =  pygame.font.Font( Trajan_Regular_font_path, 70)
        # Afficher "Jeux de stratégie" au centre du premier tiers
        title_text = "JEUX DE STRATEGIE"
        title_surface = large_font.render(title_text, True, (255, 255, 255))  # Texte blanc
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))
        screen.blit(title_surface, title_rect)


        for i, option in enumerate(menu_options):
            option_y = start_y + i * 70  # Espacement vertical entre les options

            # Dessiner le rectangle d'arrière-plan pour chaque option
            menu_rect = menu_bar_image.get_rect(center=(start_x + 143, option_y + 30))
            screen.blit(menu_bar_image, menu_rect)

            # Définir la couleur du texte en fonction de la sélection
            text_color = (5, 222, 255) if i == selected_index else (100, 100, 100)  # Bleu si sélectionné, gris sinon
            text_surface = font.render(option, True, text_color)

            # Calculer la position du texte pour le centrer dans le rectangle
            text_rect = text_surface.get_rect(center=(start_x + 150, option_y + 25))
            screen.blit(text_surface, text_rect)

    # Boucle principale d'affichage et gestion des événements
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return -1  # Code spécial pour quitter

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:  # Flèche bas
                    selected_index = (selected_index + 1) % len(menu_options)
                elif event.key == pygame.K_UP:  # Flèche haut
                    selected_index = (selected_index - 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:  # Touche Entrée
                    if selected_index == 0:  # START
                        return 0  # Retourne 0 pour démarrer
                    elif selected_index == 1:  # QUITTER
                        pygame.quit()
                        return -1  # Code spécial pour quitter

        # Dessiner le menu
        draw_menu(selected_index)
        pygame.display.flip()

def display_winner(screen, winner_image):
    # Redimensionne l'image à la taille de l'écran
    original_width = winner_image.get_width()
    scaled_image = pygame.transform.scale(winner_image, (original_width/2,200))

    # Affiche l'image redimensionnée
    screen.blit(scaled_image, (80, 200))
    pygame.display.flip()  # Met à jour l'affichage

    # Attente d'une action utilisateur
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

"""def display_credits(screen, creator_names, font_name="Arial", font_size=40, text_color=(255, 255, 255), bg_color=(0, 0, 0)):

    # Remplir l'écran avec la couleur de fond
    screen.fill(bg_color)
    
    # Initialiser la police
    font = pygame.font.SysFont(font_name, font_size)
    
    # Dessiner les noms au centre de l'écran
    screen_height = screen.get_height()
    screen_width = screen.get_width()
    total_text_height = len(creator_names) * font_size  # Estimation de la hauteur totale du texte
    start_y = (screen_height - total_text_height) // 2  # Calcul du point de départ vertical

    text_surface = font.render("Le jeu a été réaliser par :", True, text_color)
    text_rect = text_surface.get_rect(center=(screen_width // 2, start_y + -3* font_size))
    screen.blit(text_surface, text_rect)

    text_surface = font.render("Nintendo / MONOLITHSOFT", True, (255,0,0))
    text_rect = text_surface.get_rect(center=(200+screen_width // 2, start_y + 10))
    screen.blit(text_surface, text_rect)

    text_surface = font.render("appuyer sur espace pour fermer", True, (255,255,255))
    text_rect = text_surface.get_rect(center=(5+screen_width // 2, start_y + 5* font_size))
    screen.blit(text_surface, text_rect)
    

    for i, name in enumerate(creator_names):

        text_surface = font.render(name, True, text_color)
        text_rect = text_surface.get_rect(center=(screen_width // 2, start_y + i * font_size))
        screen.blit(text_surface, text_rect)
    
    pygame.display.flip()  # Met à jour l'écran
    
    # Attendre une action de l'utilisateur pour quitter
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False"""

def display_credits(screen, creator_names, font_name="Arial", font_size=40, text_color=(255, 255, 255), bg_color=(0, 0, 0)):

    # Remplir l'écran avec la couleur de fond
    screen.fill(bg_color)
    
    # Initialiser la police principale
    font = pygame.font.SysFont(font_name, font_size)
    
    # Dessiner les noms au centre de l'écran
    screen_height = screen.get_height()
    screen_width = screen.get_width()
    total_text_height = len(creator_names) * font_size  # Estimation de la hauteur totale du texte
    start_y = (screen_height - total_text_height) // 2  # Calcul du point de départ vertical

    # Afficher le texte principal
    text_surface = font.render("Le jeu a été réalisé par :", True, text_color)
    text_rect = text_surface.get_rect(center=(screen_width // 2, start_y + -3 * font_size))
    screen.blit(text_surface, text_rect)

    # Changer la taille de la police pour "Nintendo / MONOLITHSOFT"
    nintendo_font = pygame.font.SysFont(font_name, 10)  # Taille différente pour ce texte
    text_surface = nintendo_font.render("Nintendo / MONOLITHSOFT", True, (255, 0, 0))  # Texte en rouge
    text_rect = text_surface.get_rect(bottomright=(screen_width - 10, screen_height - 10))  # Position en bas à droite
    screen.blit(text_surface, text_rect)

    # Afficher l'instruction de fermer
    space= pygame.font.SysFont(font_name, 25)
    text_surface = space.render("-- Appuyer sur espace pour fermer  --", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(5 + screen_width // 2, start_y + 5 * font_size))
    screen.blit(text_surface, text_rect)

    # Afficher les noms des créateurs
    for i, name in enumerate(creator_names):
        text_surface = font.render(name, True, text_color)
        text_rect = text_surface.get_rect(center=(screen_width // 2, start_y + i * font_size))
        screen.blit(text_surface, text_rect)
    
    pygame.display.flip()  # Met à jour l'écran
    
    # Attendre une action de l'utilisateur pour quitter
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False


#########################################################################################################################
