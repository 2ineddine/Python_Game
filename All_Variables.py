#################################################################################################################
ICON_PATHS = {  # Dictionnaire associant le nom d'une unité au chemin de son icône.
    
    "Noah": "Noah.png",
    "Sena": "Sena.png",
    "Alexandria": "Alexandria.png",
    "Cammuravi": "Cammuravi.png",
    "Lanz": "Lanz.png",
    "Mio": "Mio.png",
    "Ashera": "Ashera.png", 
    "Zeon": "Zeon.png",
    "Eunie": "Eunie.png",
    "Taion": "Taion.png",
    "Valdi": "Valdi.png",
    "Maitre": "Maitre.png"
}
# Constantes
#################################################################################################################

# Constantes
#GRID_SIZE = 25
#CELL_SIZE = 25
#WIDTH = GRID_SIZE * CELL_SIZE
#HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
gray_mouse = (169, 169, 167)
light_gray = (211, 211, 211)

# Définir les couleurs dans des variables
player1_color = (182, 0, 0)
player2_color = (0, 0, 160)
WHITE = (255, 255, 255)  # Blanc pour l'unité sélectionnée
GRAY = (169, 169, 169)   # Gris clair pour l'unité non sélectionnée (effet nébuleux)
SEMI_TRANSPARENT = (255, 255, 255, 128)  # Blanc semi-transparent pour l'effet flou (alpha 128)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BROWN = (165, 42, 42)

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
courier_font_path = "CourierPrime-Bold.ttf"
consolas_font_path = "ConsolaMono-Bold.ttf"
din_font_path  = "DIN1451-36breit.ttf"
roboto_regular_font_path = "Roboto-Regular.ttf"
roboto_thin_font_path = "Roboto-Thin.ttf"
Trajan_Regular_font_path = "Trajan-Regular.ttf"
Orbitron_Regular_font_path = "Orbitron-Regular.ttf"
OrbitronV_font_path  = "Orbitron-V.ttf"

#################################################################################################################

FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRID_SIZE = 18
CELL_SIZE = 35
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
gris_transparent = (125, 125, 125,170 )
red_transparent = (255, 0, 0, 130)
jaune_transparent = (255, 255, 0, 128)

extended_width = WIDTH + 300

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