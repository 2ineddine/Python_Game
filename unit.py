import pygame
import math
import random

FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRID_SIZE = 18
CELL_SIZE = 50
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
        self.is_moving = False
        self.is_attacking = False
        self.bonus_damage = 1 #Sert pour les bonus de dégats liés à l'éjection et à la commotion
        self.cumul_damage=0
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
        return[self.x,self.y]
    
    def changes (self, x=None, y=None, health=None, attack_power=None,magic_power=None, defence=None, speed=None, agility=None, team=None,icon_path = None):
        if (x and y) is not None:
            self.x= x
            self.y = y
            self.team = team
            
    def generate_circle(self, x, y, walls_coordinates,attack_range=None):
        """
        Génère les coordonnées dans la portée de déplacement d'une unité sous forme de losange.
    
        :param x: Coordonnée x du centre.
        :param y: Coordonnée y du centre.
        :param walls_instances: Liste ou ensemble des coordonnées des murs (obstacles) sous forme de tuples (x, y).
        :return: Liste de tuples (x, y) représentant les coordonnées des cases accessibles dans le losange.
        """
        # Liste pour stocker les coordonnées
        range_coordinates = []
        valid_coordinates = []
        
        radium = self.speed if attack_range is None else attack_range
        
        # Parcourir les décalages possibles dans le carré englobant
        for dx in range(-radium, radium+ 1):
            for dy in range(-radium, radium + 1):
                # Vérifier si le point est dans le losange (|dx| + |dy| <= self.speed)
                if abs(dx) + abs(dy) <= radium and 0<=dx+x<GRID_SIZE and 0<=dy+y<GRID_SIZE :
                    # Ajouter les coordonnées au résultat
                    range_coordinates.append((x + dx, y + dy))
                    
        
        # Retirer les coordonnées qui sont des murs
        valid_coordinates = [
            coordinate for coordinate in range_coordinates if coordinate not in walls_coordinates
        ]
    
        return valid_coordinates

    
        
    
        
        
        

    def attack(self, target,puissance_comp,precision_comp,crit_rate,att_range):
        """Attaque une unité cible."""
        if self.team != target.team:
            damage = int((self.attack_power/100)*puissance_comp*(50/target.defence)*target.bonus_damage)
            if calcul_precision_total(target.agility,precision_comp) ==1:
                if random.random() < crit_rate :
                    damage = int(damage*1.7)
                    print("Coup Critique !!!")
                target.health -= damage
                target.cumul_damage += damage
                if target.health <0:
                    target.health == 0
                print(f"{target.__class__.__name__} prend {damage} points de dégats")
                print(f"{target.__class__.__name__} a donc {target.health} PVs !")
            else :
                target.health -= 0
                print(f"{target.__class__.__name__} a esquivé l'attaque !!")
    
    def verif_limit(self): #verifie si l'unté peut utiliser son attaque SP
        return 1 if self.cumul_damage >= (1.5 * self.max_stats["health_max"]) else 0
    
    def heal(self, target,soin_comp,precision_comp,crit_rate,att_range):
        """Soigne une unité cible."""
        if self.team == target.team:
            soin = int((self.magic_power/130)*soin_comp)
            if random.random() < precision_comp :
                if random.random() < crit_rate :
                    soin = int(soin*1.7)
                    print("Soin Critique !!!")
                target.health += soin
                if target.health>target.max_stats["health_max"]:
                    target.health=target.max_stats["health_max"]
                print(f"{target.__class__.__name__} récupère {soin} PVs !")
                print(f"{target.__class__.__name__} a donc {target.health} PVs !")
            else :
                target.health -= 0
                print("Le soin a échoué !!")
        
    def apply_effects(self):
        for stat, effect in list(self.effects.items()):
            # Retirer l'effet actuel si déjà appliqué
            self.bonus_damage = 1
            if effect["applied"]:
                if stat!="guerison" and stat!= "desta" and stat!="chute" and stat!="ejection" and stat!="commotion" and stat!="brulure":
                    setattr(self, stat, getattr(self, stat) - effect["value"])
                effect["applied"] = False

            # Appliquer à nouveau l'effet pour ce tour
            if stat=="guerison":
                healing_amount = self.max_stats["health_max"] * effect["value"]
                self.health +=healing_amount
                print(f"La guérison fait effet ! Régénération de {healing_amount} PVs !")
                if self.health>self.max_stats["health_max"]:
                    self.health=self.max_stats["health_max"]
            if stat =="brulure":
                burning_amount = self.max_stats["health_max"] * effect["value"]
                self.health -=burning_amount
                print(f"La brûlure fait effet ! Perte de {burning_amount} PVs !")
            if stat!="guerison" and stat!= "desta" and stat!="chute" and stat!="ejection" and stat!="commotion" and stat!="brulure":
                setattr(self, stat, getattr(self, stat) + effect["value"])
            effect["applied"] = True
            effect["duration"] -= 1
            if effect["duration"] < 0:
                if stat!="guerison" and stat!= "desta" and stat!="chute" and stat!="ejection" and stat!="commotion" and stat!="brulure":
                    setattr(self, stat, getattr(self,stat) - effect["value"])
                del self.effects[stat]
    
    def add_effect(self,target, stat, value, duration):
        if stat not in target.effects:
            target.effects[stat] = {"value": value, "duration": duration, "applied": True}
        else:
            target.effects[stat]["duration"] += duration
            
    def chance_brulure(self,target):
        if random.random() < 0.15 :
            print("L'adversaire est brûlé !")
            self.add_effect(target,"brulure",0.05,2)
    
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
    
    
    #def attack_range (self,)

def calcul_precision_total(esquive_adv,precision_att):
    precision_totale = (100-esquive_adv)/100 * precision_att
    return 1 if random.random() < precision_totale else 0

class Noah(Unit): #noah=Noah(x,y,110,90,0,50,3,10,'team')
    #Classe pour l'unité Noah
 
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path)
        self.attack_range=[1,0,1,1]
        self.effect_zone=[1,2,1,3]
        self.effect_shape=["square","square","square","line"]
    def coup_d_epee(self,target):
        puissance = 50
        precision = 0.95
        crit_rate = 0.02
        att_range=1
        hp=target.health
        self.attack(target,puissance,precision,crit_rate,att_range)
        if hp != target.health and self.team != target.team: #verifie si l'attaque a bien touché l'adv avant d'appliquer l'effet
            target.effects["desta"] = {"value": None, "duration": 0, "applied": True}
        
    def frappe_au_sol(self,target):
        puissance = 40
        precision = 0.95
        crit_rate = 0.02
        att_range=1
        if "ejection" in target.effects and target.effects["ejection"]["applied"] and self.team != target.team:
            target.effects["commotion"] = {"value": None, "duration": 1, "applied": True}
            target.bonus_damage=3
            precision=2 #Si il y a possibilité de commotion, obligé de réussir l'attaque
        self.attack(target,puissance,precision,crit_rate,att_range)
        
        
    def entaille_aerienne(self,target):
        puissance=75
        precision=0.75
        att_range=1
        crit_rate=0.02
        self.attack(target,puissance,precision,crit_rate,att_range)
        
    def ravage_fulgurant(self,target): #attaque SP
        puissance = 100
        precision = 1
        crit_rate = 0.01
        att_range=3
        if self.verif_limit()==1:
            self.attack(target,puissance,precision,crit_rate,att_range)
        else : 
            print("La jauge de Limite n'est pas assez remplie pour utiliser la capacité SP !")

class Lanz(Unit): #lanz=Lanz(x,y,200,80,0,80,3,5,'team')
    #Classe pour l'unité Lanz 
 
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path)
        self.attack_range=[1,1,0,0] 
        self.effect_zone=[1,1,2,20]
        self.effect_shape=["square","square","square","rhombus"]
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
        hp=target.health
        self.attack(target,puissance,precision,crit_rate,att_range)
        if hp!=target.health:
            if "desta" in target.effects and target.effects["desta"]["applied"] and self.team != target.team:
                target.effects["chute"] = {"value": None, "duration": 0, "applied": True}
    
    def aplatissement(self,target):
        puissance = 40
        precision = 0.95
        crit_rate = 0.02
        att_range=1
        if "ejection" in target.effects and target.effects["ejection"]["applied"] and self.team != target.team:
            target.effects["commotion"] = {"value": None, "duration": 0, "applied": True}
            target.bonus_damage=3
            precision=2
        self.attack(target,puissance,precision,crit_rate,att_range)
        #ajouter l'effet de commotion
    
    def provocation_furieuse(self,target):
        #créer un effet de focus sur le personnage
        
        if self.verif_limit()==1:
            self.add_effect(self,"defence",10,2)
            self.defence=self.max_stats["defence_max"]
            self.defence +=10
        else : 
            print("La jauge de Limite n'est pas assez remplie pour utiliser la capacité SP !")
        pass
    
class Eunie(Unit): #eunie=Eunie(x,y,90,30,80,50,3,7,'team')
    #Classe pour l'unité Eunie
     
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path)
        self.attack_range=[3,3,4,10] 
        self.effect_zone=[1,1,1,20]
        self.effect_shape=["square","square","square","rhombus"]
    
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
            
    def anneau_de_puissance(self,target):
        att_range=3
        if self.team == target.team : 
            self.add_effect(target,"attack_power",10,3)
            target.attack_power=target.max_stats["attack_power_max"]
            target.attack_power +=10
        #ajouter la portée et la précision (direct dans add_effect)
        #fonction pour le buff d'attaque de 10 pts pdt 3 tours
        
    def anneau_de_guerison(self,target):
        att_range=100
        if self.verif_limit()==1 and self.team == target.team:
            self.add_effect(target,"guerison",0.1,3) #C'est bien 4 tours mais je sais pas pk avec 4 ca fait 5
        else : 
            print("La jauge de Limite n'est pas assez remplie pour utiliser la capacité SP !")
        

class Taion(Unit):
    #Classe pour l'unité Taion
     
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path)
        self.attack_range=[3,2,3,3]
        self.effect_zone=[3,1,3,3]
        self.effect_shape=["rhombus","square","rhombus","rhombus"]
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
        if "chute" in target.effects and target.effects["chute"]["applied"] and self.team != target.team:
            target.effects["ejection"] = {"value": None, "duration": 0, "applied": True}
            target.bonus_damage=1.3
            precision=2 #100% de chance de caler l'ejection si deja chuté
        self.attack(target,puissance,precision,crit_rate,att_range)
        
        
    def silhouette_brumeuse(self,target):
        att_range=3
        #effet de zone a ajouter
        if self.team == target.team :
            self.add_effect(target,"agility",10,2)
            target.agility=target.max_stats["agility_max"]
            target.agility+=10
        
    def onde_deferlante(self,target):
        soin = 40
        puissance = 100
        precision = 1
        att_range=3
        crit_rate=0.01
        
        if self.verif_limit()==1:
            self.attack(target,puissance,precision,crit_rate,att_range)
            self.heal(target,soin,precision,crit_rate,att_range)
        else : 
            print("La jauge de Limite n'est pas assez remplie pour utiliser la capacité SP !")
        #soigne tout les alliés dans un rayon de 3 cases de l'ennemi touché
        
class Valdi(Unit):
    #Classe pour l'unité Valdi
     
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path)
        self.attack_range=[3,3,3,4]
        self.effect_zone=[1,1,2,1]
        self.effect_shape=["square","square","rhombus","square"]
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
        att_range=3
        #effet de zone de rayon 2 cases a ajouter
        if self.team == target.team :
            self.add_effect(target,"defence",10,3)
            target.defence=target.max_stats["defence_max"]
            target.defence+=10
        
    def soin_technique(self,target):
        soin = 80
        precision = 1
        att_range=3
        crit_rate=0.01
        
        if self.verif_limit()==1:
            self.heal(target,soin,precision,crit_rate,att_range)
        else : 
            print("La jauge de Limite n'est pas assez remplie pour utiliser la capacité SP !")
    
    
class Maitre(Unit):
    #Classe pour l'unité Maître
     
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path)
        self.attack_range=[1,1,3,1]
        self.effect_zone=[1,2,2,1]
        self.effect_shape=["square","square","rhombus","square"]
    def exterminateur(self,target):
        puissance = 90
        precision = 0.80
        crit_rate = 0.02
        att_range=1
        if "ejection" in target.effects and target.effects["ejection"]["applied"] and self.team != target.team:
            target.effects["commotion"] = {"value": None, "duration": 0, "applied": True}
            target.bonus_damage=3
            precision=2
        self.attack(target,puissance,precision,crit_rate,att_range)
        #effet commotion
        
    def briseur_de_rang(self,target):
        soin=50
        puissance = 50
        precision = 0.90
        crit_rate = 0.02
        att_range=1
        hp = target.health
        self.attack(target,puissance,precision,crit_rate,att_range)
        if hp != target.health : #si l'attaque touche l'ennemi, soigne les alliés autour avec 100% de chance
            self.heal(target,soin,2,crit_rate,att_range)
        
    def force_interieur(self,target):
        att_range=3
        #effet de zone de rayon 2 cases a ajouter
        if self.team == target.team :
            self.add_effect(target,"attack_power",10,3)
            target.attack_power=target.max_stats["attack_power_max"]
            target.attack_power+=10
        
        
    def estocade_du_trepas(self,target):
        puissance = 110
        precision = 1
        att_range=1
        crit_rate=0.01
        hp=target.health
        if self.verif_limit()==1 and self.team != target.team:
            self.attack(target,puissance,precision,crit_rate,att_range)
            if hp != target.health: #verifie si l'attaque a touché
                target.effects["chute"] = {"value": None, "duration": 0, "applied": True}
        else : 
            print("La jauge de Limite n'est pas assez remplie pour utiliser la capacité SP !")
        
        
class Sena(Unit):
    #Classe pour l'unité Sena
 
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path)
        self.attack_range=[1,1,0,1]
        self.effect_zone=[1,1,2,1]
        self.effect_shape=["square","square","square","square"]
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
        hp=target.health
        if self.verif_limit()==1 and self.team != target.team:
            self.attack(target,puissance,precision,crit_rate,att_range)
            if hp != target.health:
                target.effects["ejection"] = {"value": None, "duration": 0, "applied": True}
                target.bonus_damage=1.3
        else : 
            print("La jauge de Limite n'est pas assez remplie pour utiliser la capacité SP !")
        #ajouter effet ejection
        
class Cammuravi (Unit):
    #Classe pour l'unité Cammuravi
 
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path)
        self.attack_range=[1,1,1,1]
        self.effect_zone=[1,1,1,1]
        self.effect_shape=["square","square","square","square"]
    def tempete_frenetique (self,target):
        puissance = 50
        precision = 0.95
        crit_rate = 0.02
        att_range=1
        hp = target.health
        self.attack(target,puissance,precision,crit_rate,att_range)
        if hp != target.health and self.team != target.team:
            self.chance_brulure(target)
        
    def lance_ecarlate(self,target):
        puissance = 40
        precision = 0.90
        crit_rate = 0.02
        att_range=1
        hp=target.health
        self.attack(target,puissance,precision,crit_rate,att_range)
        if hp!=target.health and self.team != target.team:
            self.chance_brulure(target)
            if "desta" in target.effects and target.effects["desta"]["applied"]:
                target.effects["chute"] = {"value": None, "duration": 0, "applied": True}
        
        
    def lance_celeste(self,target):
        puissance=80
        precision=0.70
        att_range=1
        crit_rate=0.05
        hp=target.health
        self.attack(target,puissance,precision,crit_rate,att_range)
        if hp != target.health and self.team != target.team:
            self.chance_brulure(target)
        
    def salve_divine(self,target):
        puissance = 110
        precision = 1
        crit_rate = 0.02
        att_range=1
        hp=target.health
        if self.verif_limit()==1 and self.team != target.team:
            self.attack(target,puissance,precision,crit_rate,att_range)
            if hp != target.health:
                self.chance_brulure(target)
        else : 
            print("La jauge de Limite n'est pas assez remplie pour utiliser la capacité SP !")
        #ajouter zone d'effet
        # faut ajouter un effet de brulure sur l'ennemi touché pour toutes les attaques

class Mio (Unit):
    #Classe pour l'unité Mio
 
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path)
        self.attack_range=[1,1,0,1]
        self.effect_zone=[1,1,1,1]
        self.effect_shape=["square","square","rhombus","rhombus"]
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
        self.add_effect(self, "agility", 10, 2)
        self.add_effect(self, "defence", 10, 3)
        self.agility=self.max_stats["agility_max"]
        self.defence=self.max_stats["defence_max"]
        self.agility+=10
        self.defence+=10
    
    def attaque_jumelee(self,target):
        puissance=80
        precision=1
        att_range=1
        crit_rate=0.01
        hp = target.health
        if self.verif_limit()==1:
            self.attack(target,puissance,precision,crit_rate,att_range)
            if hp != target.health : 
                self.add_effect(self,"agility",10,2)
                self.agility=self.max_stats["agility_max"]
                self.agility +=10
        else : 
            print("La jauge de Limite n'est pas assez remplie pour utiliser la capacité SP !")
    ## augaugmente l’esquive de Mio de 10 points pendant 2 tours


class Ashera(Unit):
    #Classe pour l'unité Ashera
 
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path)
        self.attack_range=[1,1,1,1]
        self.effect_zone=[1,1,1,1]
        self.effect_shape=["square","square","square","square"]
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
        if "chute" in target.effects and target.effects["chute"]["applied"] and self.team != target.team:
            target.effects["ejection"] = {"value": None, "duration": 0, "applied": True}
            target.bonus_damage=1.3
            precision=2
        self.attack(target,puissance,precision,crit_rate,att_range)
        
    
    def fleur_de_la_mort(self,target):
        puissance=100
        precision = 1
        att_range=1
        crit_rate=0.01
        #augmente l’attaque de Ashera pendant 3 tours (dont celui où elle fait l’attaque, donc le bonus se fait juste avant qu’elle attaque l’ennemi)
        
        if self.verif_limit()==1:
            self.attack_power=self.max_stats["attack_power_max"]
            self.attack_power = self.attack_power_max + 10
            self.attack(target,puissance,precision,crit_rate,att_range)
            self.add_effect(self,"attack_power",10,3)
        else : 
            print("La jauge de Limite n'est pas assez remplie pour utiliser la capacité SP !")
        
class Zeon(Unit):
    
    #Classe pour l'unité Zeon
 
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path)
        self.attack_range=[1,1,1,0]
        self.effect_zone=[1,1,1,1]
        self.effect_shape=["square","square","square","square"]
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
        hp=target.health
        self.attack(target,puissance,precision,crit_rate,att_range)
        if hp!=target.health:
            if "desta" in target.effects and target.effects["desta"]["applied"] and self.team != target.team:
                target.effects["chute"] = {"value": None, "duration": 0, "applied": True}
    
    def frappe_celeste(self,target):
        puissance = 80
        precision = 0.80
        crit_rate = 0.02
        att_range=1
        self.attack(target,puissance,precision,crit_rate,att_range)
        
    
    def SP_Champ_déflecteur(self,target):
         # Zeon est invulnérable pendant 1 tour et augmente son attaque de 10 pts pendant 3 tours
         
         if self.verif_limit()==1:
             self.add_effect(self,"attack_power",10,3)
             self.attack_power=self.max_stats["attack_power_max"]
             self.attack_power+=10
         else : 
             print("La jauge de Limite n'est pas assez remplie pour utiliser la capacité SP !")
             
class Alexandria (Unit):
    #Classe pour l'unité Alexandria
 
    def __init__(self, x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path):
        super().__init__(x, y, health, attack_power,magic_power, defence, speed, agility, team,icon_path)
        self.attack_range=[1,1,1,1]
        self.effect_zone=[1,1,1,1]
        self.effect_shape=["square","square","square","square"]
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
        hp=target.health
        self.attack(target,puissance,precision,crit_rate,att_range)
        if hp!=target.health and self.team != target.team:
            target.effects["desta"] = {"value": None, "duration": 0, "applied": True} 
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
        
        if self.verif_limit()==1:
            if "ejection" in target.effects and target.effects["ejection"]["applied"] and self.team != target.team:
                target.effects["commotion"] = {"value": None, "duration": 0, "applied": True}
                target.bonus_damage=3
                precision=2
            self.attack(target,puissance,precision,crit_rate,att_range)
        else : 
            print("La jauge de Limite n'est pas assez remplie pour utiliser la capacité SP !")
        #ajouter effet commotion









""" La fonction qui génère un cercle pour la fonction marche de rayon speed et ... """
