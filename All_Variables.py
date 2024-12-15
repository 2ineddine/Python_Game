import os
current_dir = os.path.dirname(__file__)
icon_dir = os.path.join(current_dir, "units_images")
images_dir = os.path.join(current_dir, "display_images")
font_dir = os.path.join(current_dir, "fonts")
#################################################################################################################
ICON_PATHS = {  # Dictionnaire associant le nom d'une unité au chemin de son icône.
    
    "Noah": os.path.join(icon_dir, "Noah.png"),
    "Sena": os.path.join(icon_dir, "Sena.png"),
    "Alexandria": os.path.join(icon_dir, "Alexandria.png"),
    "Cammuravi": os.path.join(icon_dir, "Cammuravi.png"),
    "Lanz": os.path.join(icon_dir, "Lanz.png"),
    "Mio": os.path.join(icon_dir, "Mio.png"),
    "Ashera": os.path.join(icon_dir, "Ashera.png"), 
    "Zeon": os.path.join(icon_dir, "Zeon.png"),
    "Eunie": os.path.join(icon_dir, "Eunie.png"),
    "Taion": os.path.join(icon_dir, "Taion.png"),
    "Valdi": os.path.join(icon_dir, "Valdi.png"),
    "Maitre": os.path.join(icon_dir, "Maitre.png")
}

win_player1_path = os.path.join(images_dir, "win_player1.png")
win_player2_path = os.path.join(images_dir, "win_player2.png")
introduction_img_path = os.path.join(images_dir, "image_debut.jpg")
map_img_path = os.path.join(images_dir, "map.png")
bar_img_path = os.path.join(images_dir, "menu_barre.png")

# Constantes
#################################################################################################################

# Définir les couleurs dans des variables
player1_color = (182, 0, 0)
player2_color = (0, 0, 160)

#################################################################################################################
#Fonts_paths 
courier_font_path = os.path.join(font_dir, "CourierPrime-Bold.ttf")
consolas_font_path = os.path.join(font_dir, "ConsolaMono-Bold.ttf")
din_font_path  = os.path.join(font_dir, "DIN1451-36breit.ttf")
roboto_regular_font_path = os.path.join(font_dir, "Roboto-Regular.ttf")
roboto_thin_font_path = os.path.join(font_dir, "oboto-Thin.ttf")
Trajan_Regular_font_path = os.path.join(font_dir, "Trajan-Regular.ttf")
Orbitron_Regular_font_path = os.path.join(font_dir, "Orbitron-Regular.ttf")
OrbitronV_font_path  = os.path.join(font_dir, "Orbitron-V.ttf")

#################################################################################################################

FPS = 30

# couleurs 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)
LIGHT_GRAY = (211, 211, 211)  # Light gray color (RGB)
gris_transparent = (125, 125, 125,170 )
red_transparent = (255, 0, 0, 130)
jaune_transparent = (255, 255, 0, 128)
gris_acier = (161, 161, 161)
gray_mouse = (169, 169, 167)
Gold= (255, 239, 140)


# Taille de la fenêtre
GRID_SIZE = 18
CELL_SIZE = 35
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE

extended_width = WIDTH + 300


# Coordonnées des murs
wall_coor=[     (0, 2), (3, 8), (6, 5), (8, 2),
    (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0), (16, 0), (17, 0),
    (12, 1), (13, 1), (14, 1), (15, 1), (16, 1), (17, 1),
    (13, 2), (14, 2), (15, 2), (16, 2), (17, 1),
    (12, 3), (13, 3), (14, 3), (15, 3), (16, 3), (17, 3),
    (12, 4), (13, 4), (14, 4), (15, 4), (16, 4), (17, 4),
    (12, 5), (13, 5), (16, 5), (17, 5),
    (12, 6), (13, 6), (17, 6),
    (13, 7), (17, 7),
    (15, 8), (8, 8), (9, 8),
    (6, 9), (7, 9), (8, 9), (9, 9),
    (6, 10), (7, 10), (8, 10), (9, 10),
    (4, 11), (5, 11), (6, 11), (7, 11),
     (5, 12), (6, 12), (7, 12),
    (5, 13),
    (8, 14), (11, 14), (17, 14),(8,7),(9,7),(17,2)
    ]


# Coordonnées des cellules empoison
poison_cell=[
    (0,9),(0,10),(0,11),(0,12),(0,13),(0,14),(0,15),(0,16),(0,17),
    (1,11),(1,12),(1,13),(1,14),(1,15),(1,16),(1,17),
    (2,12),(2,13),(2,14),(2,15),(2,16),(2,17),
    (3,12),(3,13),(3,14),(3,15),(3,16),(3,17),
    (4,12),(4,13),(4,14),(4,15),(4,16),(4,17),
    (5,14),(5,15),(5,16),(5,17),
    (6,16),(6,17),
    (7,17),
    (8,17)

]


createurs=["Youdas BEDHOUCHE","Hicham TIERCE","Zineddine BOUHADJIRA"]

player1_color = (138, 0, 0)
player2_color = (0, 0, 101)