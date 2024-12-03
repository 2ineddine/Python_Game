import pygame
import random

# Constantes
GRID_SIZE = 8
CELL_SIZE = 60
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


##TEMPORAIRE NORMALEMENT-----------------------------------------------------
current_unit_index=0 #correspond à l'unité qui joue actuellement, à chaque tour(donc quand c'est le tour d'une autre unité) elle augmente . qd > 7 ca repart a 0
#la dynamique de i se fait normalement dans le main() de game.py





##---------------------------------------------------

class Unit:
    """
    Classe pour représenter une unité.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    health : int
        La santé de l'unité.
    attack_power : int
        La puissance d'attaque de l'unité.
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    is_selected : bool
        Si l'unité est sélectionnée ou non.

    Méthodes
    --------
    move(dx, dy)
        Déplace l'unité de dx, dy.
    attack(target)
        Attaque une unité cible.
    draw(screen)
        Dessine l'unité sur la grille.
    """

    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team):
        """
        Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.

        Paramètres
        ----------
        x : int
            La position x de l'unité sur la grille.
        y : int
            La position y de l'unité sur la grille.
        health : int
            La santé de l'unité.
        attack_power : int
            La puissance d'attaque de l'unité.
        team : str
            L'équipe de l'unité ('player' ou 'enemy').
        """
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.magic_power = magic_power
        self.defence = defence
        self.speed = speed
        self.agility = agility
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False
        self.max_stats = {
            "health_max": health,
            "attack_power_max": attack_power,
            "magic_power_max": magic_power,
            "defence_max": defence,
            "speed_max": speed,
            "agility_max": agility
        }
        self.effects = {} #{"stat_name":{"value":float,"duration":int}}

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy

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
            
#PHASE DE TEST ---------------------------------------------------------------         
    def apply_effects(self):
        for stat, effect in list(self.effects.items()):
            # Retirer l'effet actuel si déjà appliqué
            if effect["applied"]:
                if stat!="guerison":
                    setattr(self, stat, getattr(self, stat) - effect["value"])
                effect["applied"] = False

            # Appliquer à nouveau l'effet pour ce tour
            if stat=="guerison":
                healing_amount = self.max_stats["health_max"] * effect["value"]
                self.health +=healing_amount
                if self.health>self.max_stats["health_max"]:
                    self.health=self.max_stats["health_max"]
            else:
                setattr(self, stat, getattr(self, stat) + effect["value"])
            effect["applied"] = True
            effect["duration"] -= 1
            if effect["duration"] < 0:
                if stat!="guerison":
                    setattr(self, stat, getattr(self,stat) - effect["value"])
                del self.effects[stat]
    
    def add_effect(self,target, stat, value, duration):
        if stat not in target.effects:
            target.effects[stat] = {"value": value, "duration": duration, "applied": False}
        else:
            target.effects[stat]["duration"] += duration
    
    
    ##DOIT ETRE IMPLEMENTER DANS LE GAME.PY
    def next_turn():
        global current_unit_index
        current_unit = units[current_unit_index]
        current_unit.apply_effects()
        print(f"{current_unit} joue son tour.")
        #ACTION
        print(f"Fin du tour de {current_unit}.")
        current_unit_index = (current_unit_index + 1) % len(units)

#-----------------------------------------------------------------------------

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        color = BLUE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
                           2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)


def calcul_precision_total(esquive_adv,precision_att):
    precision_totale = (100-esquive_adv)/100 * precision_att
    return 1 if random.random() < precision_totale else 0

class Noah(Unit): #noah=Noah(x,y,110,90,0,50,3,10,'team')
    #Classe pour l'unité Noah
 
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team)
    
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
 
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team)

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
        self.add_effect(self,"defence",10,2)
        pass
    
class Eunie(Unit): #eunie=Eunie(x,y,90,30,80,50,3,7,'team')
    #Classe pour l'unité Eunie
     
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team)

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
        self.add_effect(target,"attack_power",10,3)
        #ajouter la portée et la précision (direct dans add_effect)
        #fonction pour le buff d'attaque de 10 pts pdt 3 tours
        
    def anneau_de_guerison(self,target):
        precision = 1
        att_range=100
        target.effects["guerison"] = {"value": 0.1, "duration": 4, "applied": False}
        #rajouter la range

class Taion(Unit):
    #Classe pour l'unité Taion
     
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team)

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
     
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team)

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
     
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team)

    def exterminateur(self,target):
        puissance = 90
        precision = 0.80
        crit_rate = 0.02
        att_range=1
        self.attack(target,puissance,precision,crit_rate,att_range)
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

unit1=Noah(0,0,110,90,0,50,3,10,'player')
unit2=Lanz(0,1,200,80,0,80,3,5,'enemy')
unit3=Eunie(1,0,90,30,80,50,3,7,'player')
units = [unit1, unit2, unit3]