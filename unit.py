import pygame
import math

FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRID_SIZE = 25
CELL_SIZE = 25
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Unit:
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.magic_power = magic_power
        self.defence = defence
        self.speed = speed
        self.agility = agility
        self.icon_path = icon_path  # Chemin de l'icône associée à l'unité.
        self.icon = pygame.image.load(self.icon_path)  # Chargement de l'icône.
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy
        return[self.x,self.y]
    
    def changes (self, x=None, y=None, health=None, attack_power=None,magic_power=None, defence=None, speed=None, agility=None, team=None,icon_path = None):
        if (x and y) is not None:
            self.x= x
            self.y = y
            self.team = team
            
    def generate_circle(self, x, y,walls_instances):
        """Génère les coordonnées dans la portée de déplacement d'une unité."""
        circle_points = set()
    
        for dx in range(-self.speed, self.speed + 1):
            for dy in range(-self.speed, self.speed + 1):
                if math.sqrt(dx**2 + dy**2) <= self.speed:
                    new_x, new_y = x + dx, y + dy
                    # Vérifier les limites de la grille et les murs
                    if (
                        0 <= new_x < GRID_SIZE and
                        0 <= new_y < GRID_SIZE and
                        (new_x, new_y) not in [(wall.x, wall.y) for wall in walls_instances]
                    ):
                        circle_points.add((new_x, new_y))
    
        return list(circle_points)
        
        

    def attack(self, target,puissance_comp,precision_comp,crit_rate,att_range):
        """Attaque une unité cible."""
        print('fonction attaque') #debug
        if abs(self.x - target.x) <= att_range and abs(self.y - target.y) <= att_range:
            damage = int((self.attack_power/100)*puissance_comp*(50/target.defence))
            if calcul_precision_total(target.agility,precision_comp) ==1:
                if random.random() < crit_rate :
                    damage = int(damage*1.7)
                    print("Coup Critique !!!")
                target.health -= damage
                print(f"L'adversaire prend {damage} points de dégats")
                print(f"Il lui reste {target.health} PVs !")
            else :
                target.health -= 0
                print("L'adversaire a esquivé l'attaque !!")
        else : 
            print("l'unité est trop loin !")
        
    
    def heal(self, target,soin_comp,precision_comp,crit_rate,att_range):
        """Soigne une unité cible."""
        print("fonction heal") #debug
        if abs(self.x - target.x) <= att_range and abs(self.y - target.y) <= att_range:
            soin = int((self.magic_power/130)*soin_comp)
            if calcul_precision_total(target.agility,precision_comp) ==1:
                if random.random() < crit_rate :
                    soin = int(soin*1.7)
                    print("Coup Critique !!!")
                target.health += soin
                print(f"L'unité récupère {soin} PVs !")
                print(f"Il lui reste {target.health} PVs !")
            else :
                target.health -= 0
                print("Le soin a échoué !!")
        else : 
            print("l'unité est trop loin !")
    def update_icon_size(self):
        """Redimensionne l'icône selon la taille actuelle de CELL_SIZE."""
        self.icon = pygame.image.load(self.icon_path)  # Recharge l'icône d'origine.
        self.icon = pygame.transform.scale(self.icon, (CELL_SIZE, CELL_SIZE))  # Redimensionnement.

            

    def draw(self, screen):
        """Dessine l'unité sur l'écran, avec une bordure verte si elle est sélectionnée."""
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Redimensionner l'icône pour l'adapter à la taille de la cellule
        icon_scaled = pygame.transform.scale(self.icon, (CELL_SIZE, CELL_SIZE))
        
        # Afficher l'icône redimensionnée
        screen.blit(icon_scaled, (self.x * CELL_SIZE, self.y * CELL_SIZE))
       
    def clone (self):
        return self.__class__(self.x, self.y, self.health, self.attack_power,self.magic_power, self.defence, self.speed, self.agility, self.team,self.icon_path)
    


def calcul_precision_total(esquive_adv,precision_att):
    precision_totale = (100-esquive_adv)/100 * precision_att
    return 1 if random.random() < precision_totale else 0

class Noah(Unit): #noah=Noah(x,y,110,90,0,50,3,10,'team')
    #Classe pour l'unité Noah
 
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path)

    def coup_d_epee(self,target):
        puissance = 50
        precision = 0.95
        crit_rate = 0.02
        att_range=1
        self.attack(target,puissance,precision,crit_rate,att_range)
        
    def frappe_au_sol(self,target):
        puissance = 40
        precision = 0.95
        crit_rate = 0.02
        att_range=1
        self.attack(target,puissance,precision,crit_rate,att_range)
        #ajouter apres la zone d'effet et l'effet de commotion
        
    def entaille_aerienne(self,target):
        puissance=75
        precision=0.75
        att_range=1
        crit_rate=0.02
        self.attack(target,puissance,precision,crit_rate,att_range)
        
    def ravage_fulgurant(self,target):
        puissance = 100
        precision = 1
        crit_rate = 0.01
        att_range=3
        self.attack(target,puissance,precision,crit_rate,att_range)
        #ajouter zone d'effet

class Lanz(Unit): #lanz=Lanz(x,y,200,80,0,80,3,5,'team')
    #Classe pour l'unité Lanz 
 
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path)

    def entaille_uppercut(self,target):
        puissance = 55
        precision = 0.95
        crit_rate = 0.02
        att_range=1
        self.attack(target,puissance,precision,crit_rate,att_range)
        
    def charge_du_taureau(self,target):
        puissance=35
        precision=0.95
        att_range=1
        crit_rate=0.02
        self.attack(target,puissance,precision,crit_rate,att_range)
    
    def aplatissement(self,target):
        puissance = 40
        precision = 0.95
        crit_rate = 0.02
        att_range=1
        self.attack(target,puissance,precision,crit_rate,att_range)
        #ajouter l'effet de commotion
    
    def provocation_furieuse(self,target):
        #créer un effet de focus sur le personnage
        #buff de defense de 10 pts pdt 2 tours, pour l'effet de temps impartie chercher si y'a un truc genre lanz.iscalled et ca incremente une valeur pour compter chais pas
        pass
    
class Eunie(Unit): #eunie=Eunie(x,y,90,30,80,50,3,7,'team')
    #Classe pour l'unité Eunie
     
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path)

    def cercle_soigneur(self,target):
        soin = 50
        precision = 0.80
        crit_rate = 0.02
        att_range=2
        self.heal(target,soin,precision,crit_rate,att_range)
            
    def canon_a_ether(self,target):
        puissance = 50
        precision = 0.95
        crit_rate = 0.02
        att_range=2
        self.attack(target,puissance,precision,crit_rate,att_range)
        #ajouter apres la zone d'effet et l'effet de commotion
            
    def anneau_de_puissance(self,target):
        precision=1
        att_range=3
        #fonction pour le buff d'attaque de 10 pts pdt 3 tours
        
    def Anneau_de_guerison(self,target):
        precision = 1
        att_range=100
        #créer effet guerison -> soigne 10%hp total a chaque tour pdt 4 tours

class Taion(Unit):
    #Classe pour l'unité Taion
     
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path)

    def cieux_orageux(self,target):
        soin = 35
        precision = 0.90
        crit_rate = 0.02
        att_range=3
        self.heal(target,soin,precision,crit_rate,att_range)
        #ajouter effet de zone pour le heal
        
    def eaux_dechainees(self,target):
        puissance = 50
        precision = 0.95
        crit_rate = 0.02
        att_range=2
        self.attack(target,puissance,precision,crit_rate,att_range)
        #effet ejection
        
    def silhouette_brumeuse(self,target):
        precision=1
        att_range=3
        #effet de zone a ajouter
        #buff d'esquive pdt 2 tours de 5 pts
        
    def onde_deferlante(self,target):
        soin = 40
        puissance = 100
        precision = 1
        att_range=3
        crit_rate=0.01
        self.attack(target,puissance,precision,crit_rate,att_range)
        self.heal(target,soin,precision,crit_rate,att_range)
        #soigne tout les alliés dans un rayon de 3 cases de l'ennemi touché
        
class Valdi(Unit):
    #Classe pour l'unité Valdi
     
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path)

    def balle_de_soin(self,target):
        soin = 50
        precision = 0.90
        crit_rate = 0.02
        att_range=3
        self.heal(target,soin,precision,crit_rate,att_range)
        
    def frappe_sournoise(self,target):
        puissance = 60
        precision = 0.95
        crit_rate = 0.02
        att_range=3
        self.attack(target,puissance,precision,crit_rate,att_range)
        
    def hyper_recharge(self,target):
        precision=0.9
        att_range=3
        #effet de zone de rayon 2 cases a ajouter
        #buff de defense de 5pts pdt 3 tours
        
    def soin_technique(self,target):
        soin = 80
        precision = 1
        att_range=3
        crit_rate=0.01
        self.heal(target,soin,precision,crit_rate,att_range)
    
class Maitre(Unit):
    #Classe pour l'unité Maître
     
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path)

    def exterminateur(self,target):
        puissance = 90
        precision = 0.80
        crit_rate = 0.02
        att_range=1
        #effet commotion
        
    def briseur_de_rang(self,target):
        soin=50
        puissance = 50
        precision = 0.90
        crit_rate = 0.02
        att_range=1
        self.attack(target,puissance,precision,crit_rate,att_range)
        #effet de soin autour de l'ennemi
        
    def force_interieur(self,target):
        precision=0.9
        att_range=3
        #effet de zone de rayon 2 cases a ajouter
        #buff d'attaque de 5pts pdt 3 tours
        
    def estocade_du_trepas(self,target):
        puissance = 110
        precision = 1
        att_range=1
        crit_rate=0.01
        #effet de chute DIRECT
        
        
class Sena(Unit):
    #Classe pour l'unité Sena
 
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path)

    def coup_de_marteau (self,target):
        puissance = 50
        precision = 0.90
        crit_rate = 0.02
        att_range=1
        self.attack(target,puissance,precision,crit_rate,att_range)
        
    def impact_lourd(self,target):
        puissance = 60
        precision = 0.80
        crit_rate = 0.02
        att_range=1
        self.attack(target,puissance,precision,crit_rate,att_range)
        #ajouter l’effet qui pousse l’ennemi
        
    def toupie_geante(self,target):
        puissance=45
        precision=0.75
        att_range=1
        crit_rate=0.02
        self.attack(target,puissance,precision,crit_rate,att_range)
	  #ajouter l’effet de zone qui touche toutes les cases autours
        
    def chute_de_pression(self,target):
        puissance = 100
        precision = 1
        crit_rate = 0.01
        att_range=1
        self.attack(target,puissance,precision,crit_rate,att_range)
        #ajouter effet ejection
        
class Cammuravi (Unit):
    #Classe pour l'unité Cammuravi
 
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path)

    def tempete_frenetique (self,target):
        puissance = 50
        precision = 0.95
        crit_rate = 0.02
        att_range=1
        self.attack(target,puissance,precision,crit_rate,att_range)
        
    def lance_ecarlate(self,target):
        puissance = 40
        precision = 0.90
        crit_rate = 0.02
        att_range=1
        self.attack(target,puissance,precision,crit_rate,att_range)
        #ajouter effet chute
        
    def lance_celeste(self,target):
        puissance=80
        precision=0.70
        att_range=1
        crit_rate=0.05
        self.attack(target,puissance,precision,crit_rate,att_range)
        
    def salve_divine(self,target):
        puissance = 110
        precision = 1
        crit_rate = 0.02
        att_range=1
        self.attack(target,puissance,precision,crit_rate,att_range)
        #ajouter zone d'effet
        # faut ajouter un effet de brulure sur l'ennemi touché pour toutes les attaques

class Mio (Unit):
    #Classe pour l'unité Mio
 
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path)

    def crocs_aeriens(self,target):
        puissance = 45
        precision = 0.95
        crit_rate = 0.02
        att_range=1
        self.attack(target,puissance,precision,crit_rate,att_range)
        
    def Large_entaille(self,target):
        puissance=60
        precision=0.80
        att_range=1
        crit_rate=0.02
        self.attack(target,puissance,precision,crit_rate,att_range)
    
    def demon_de_la_vitesse(self,target):
      ##  Augmente l’esquive de Mio de 5 pts pendant 2 tours et sa defense de 5 pts pendant 3 tours. Cette compétence ne peut etre encore utilisé qu’apres 3 tours
        pass
    
    def attaque_jumelee(self,target):
        puissance=80
        precision=1
        att_range=1
        crit_rate=0.01
        self.attack(target,puissance,precision,crit_rate,att_range)
        pass
    ## augaugmente l’esquive de Mio de 10 points pendant 2 tours


class Ashera(Unit):
    #Classe pour l'unité Ashera
 
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path)

    def tueurs_de_demons(self,target):
        puissance = 50
        precision = 0.95
        crit_rate = 0.02
        att_range=1
        self.attack(target,puissance,precision,crit_rate,att_range)
        
    def roue_infernale(self,target):
        puissance=70
        precision=0.80
        att_range=1
        crit_rate=0.02
        self.attack(target,puissance,precision,crit_rate,att_range)
    
    def lame_d_ascension(self,target):
        puissance = 45
        precision = 0.90
        crit_rate = 0.02
        att_range=1
        self.attack(target,puissance,precision,crit_rate,att_range)
        #ajouter l'effet d’ejection
    
    def fleur_de_la_mort(self,target):
        puissance=100
        precision = 1
        att_range=1
        crit_rate=0.01
        #augmente l’attaque de Ashera pendant 3 tours (dont celui où elle fait l’attaque, donc le bonus se fait juste avant qu’elle attaque l’ennemi)

        self.attack(target,puissance,precision,crit_rate,att_range)
        
class Zeon(Unit):
    #Classe pour l'unité Zeon
 
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path)

    def lame_glorieuse(self,target):
        puissance = 50
        precision = 0.95
        crit_rate = 0.02
        att_range=1
        self.attack(target,puissance,precision,crit_rate,att_range)
        
    def coup_de_bouclier(self,target):
        puissance=40
        precision=0.90
        att_range=1
        crit_rate=0.02
        self.attack(target,puissance,precision,crit_rate,att_range)
	  #ajout effet chute
    
    def frappe_celeste(self,target):
        puissance = 80
        precision = 0.80
        crit_rate = 0.02
        att_range=1
        self.attack(target,puissance,precision,crit_rate,att_range)
        
    
    def SP_Champ_déflecteur(self,target):
         # Zeon est invulnérable pendant 1 tour et augmente son attaque de 10 pts pendant 3 tours

        pass
class Alexandria (Unit):
    #Classe pour l'unité Alexandria
 
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path)

    def coup_de_cote (self,target):
        puissance = 50
        precision = 0.95
        crit_rate = 0.15
        att_range=1
        self.attack(target,puissance,precision,crit_rate,att_range)
        
    def gravure_profonde(self,target):
        puissance = 30
        precision = 0.95
        crit_rate = 0.15
        att_range=1
        self.attack(target,puissance,precision,crit_rate,att_range)
        #ajouter destabilisation
        
    def illusion_lumineuse(self,target):
        puissance=70
        precision=0.80
        att_range=1
        crit_rate=0.15
        self.attack(target,puissance,precision,crit_rate,att_range)
        
    def epee_de_legende(self,target):
        puissance = 100
        precision = 1
        crit_rate = 0.05
        att_range=1
        self.attack(target,puissance,precision,crit_rate,att_range)
        #ajouter effet commotion









""" La fonction qui génère un cercle pour la fonction marche de rayon speed et ... """
