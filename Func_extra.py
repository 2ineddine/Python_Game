from game import * 
import sys
from cells import *
from unit import *  
import pygame
import sys






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
    if size % 2 == 0:
        print("size", size)
        for i in range(x-int(size/2), x + int(size/2)):
            for j in range(y-int(size/2), y + int(size/2)):
                square_coordinates.append((i, j))
    else:
        for i in range(x-(size//2), x + (size//2) + 1):
            for j in range(y-(size//2), y + (size//2) + 1):
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






class SkillSelector:
    def __init__(self, screen, width=200):
        """
        Initialise l'interface de sélection des compétences.
        :param screen: Surface Pygame où dessiner l'interface.
        :param width: Largeur de la zone de sélection (par défaut : 200 pixels).
        """
        self.screen = screen
        self.width = width
        self.selected_skill_index = 0  # Index de la compétence actuellement sélectionnée

    def display(self, unit, x_offset):
        """
        Affiche les compétences disponibles pour une unité.
        :param unit: L'unité dont les compétences doivent être affichées.
        :param x_offset: Décalage en x pour positionner la zone à droite de la grille.
        """
        # Obtenir les compétences spécifiques de l'unité
        skills = classes_methods(Unit, type(unit))

        # Dessiner la zone de fond
        pygame.draw.rect(self.screen, (50, 50, 50), (x_offset, 0, self.width+100, HEIGHT))  # Fond sombre
        pygame.draw.rect(self.screen, (200, 200, 200), (x_offset, 0, self.width+100, HEIGHT), width=2)  # Contour

        # Afficher le titre
        font = pygame.font.Font(None, 28)
        title = font.render("Compétences", True, (255, 255, 255))
        self.screen.blit(title, (x_offset + 40, 20))

        # Afficher les compétences
        for i, skill in enumerate(skills):
            color = (255, 255, 0) if i == self.selected_skill_index else (255, 255, 255)
            text = font.render(f"{i + 1}. {skill}", True, color)
            self.screen.blit(text, (x_offset + 20, 60 + i * 40))

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









