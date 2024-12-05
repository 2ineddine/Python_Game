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
    
    return filtered_methods



# Application d'une méthode spécifique sur une instance
def application_of_specific_method_of_instance(target, instance, child_methods_ordered, method_number):
    # Récupérer la méthode à partir de la liste
    instance_method = getattr(instance, child_methods_ordered[method_number])
    # Appeler la méthode avec le bon argument
    instance_method(target)  # Passer 'target' en argument à la méthode
     
    
    



# Génération d'un carré avec contraintes sur x et y
def generate_square_coordinates(x, y, size=1):
    if x < 0 or y < 0 or x >= GRID_SIZE or y >= GRID_SIZE:
        return []  # Retourner une liste vide si les coordonnées sont invalides
    # Les 4 coins du carré
    square_coordinates = [
        (x, y),              # Coin en haut à gauche
        (x + size, y),       # Coin en haut à droite
        (x, y + size),       # Coin en bas à gauche
        (x + size, y + size) # Coin en bas à droite
    ]
    
    # Vérifier que les coordonnées restent dans les limites de la grille
    valid_coordinates = [(x_, y_) for x_, y_ in square_coordinates if 0 <= x_ < GRID_SIZE and 0 <= y_ < GRID_SIZE]
    
    return valid_coordinates




# Génération d'une barre horizontale avec contraintes
def generate_horizontal_bar(x, y, length):
    if x < 0 or y < 0 or x >= GRID_SIZE or y >= GRID_SIZE:
        return []  # Retourner une liste vide si les coordonnées sont invalides
    
    # Liste pour stocker les coordonnées de la barre
    bar_coordinates = []
    
    # Générer les coordonnées le long de l'axe horizontal (augmentation de x)
    for i in range(length):
        new_x = x + i
        if new_x >= GRID_SIZE:  # Si la nouvelle coordonnée dépasse la taille de la grille
            break
        bar_coordinates.append((new_x, y))
    
    return bar_coordinates


# Génération d'une barre verticale avec contraintes
def generate_vertical_bar(x, y, length):
    if x < 0 or y < 0 or x >= GRID_SIZE or y >= GRID_SIZE:
        return []  # Retourner une liste vide si les coordonnées sont invalides
    
    # Liste pour stocker les coordonnées de la barre
    bar_coordinates = []
    
    # Générer les coordonnées le long de l'axe vertical (augmentation de y)
    for i in range(length):
        new_y = y + i
        if new_y >= GRID_SIZE:  # Si la nouvelle coordonnée dépasse la taille de la grille
            break
        bar_coordinates.append((x, new_y))
    
    return bar_coordinates


# Générer un losange avec contraintes
def generate_rhombus(x, y, size):
    if x < 0 or y < 0 or x >= GRID_SIZE or y >= GRID_SIZE:
        return []  # Retourner une liste vide si les coordonnées sont invalides
    
    # Liste pour stocker les coordonnées du losange
    rhombus_coordinates = []
    
    # Les 4 sommets du losange (en fonction de la taille)
    coordinates = [
        (x, y - size),  # Haut
        (x + size, y),  # Droite
        (x, y + size),  # Bas
        (x - size, y)   # Gauche
    ]
    
    # Vérifier que les coordonnées restent dans les limites de la grille
    valid_coordinates = [(x_, y_) for x_, y_ in coordinates if 0 <= x_ < GRID_SIZE and 0 <= y_ < GRID_SIZE]
    
    return valid_coordinates

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
