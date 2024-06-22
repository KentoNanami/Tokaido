# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 15:15:55 2023

@author: 36796932
"""

import pygame
from parametre_general import *



class Joueur(pygame.sprite.Sprite):
    
    def __init__(self, index_joueur, couleur, position = [0, 0, 0], pseudo = None, statistic = None, voyageur = None, piece = 7, points = 0, collection = None, IA = False):
        
        super().__init__()
        
        # attribues du joueur
        
        # compte
        self.pseudo = pseudo
        self.statistic = statistic
        self.IA = IA
        
        # caract du joueur
        self.voyageur = voyageur
        self.couleur = couleur
        self.index_joueur = index_joueur

        # jeux
        self.pieces = piece
        self.points = points
        self.position = position                      # avec [0] le jour, [1] la postion de la station par rapport aux relais et [2] sa place (pour station double/relais)
        if collection: self.collection = collection
        else: 
            echoppe = {"petit souvenir": 0, "nouriture": 0, "gros souvenir": 0, "vetement": 0}
            self.collection = {"echoppe": echoppe, "compteur_points_echoppe": [], "repas" : list(), "p_mer" : 0, "p_montagne" : 0, "p_riziere" : 0, 
                               "a_mer" : False, "a_montagne": False, "a_riziere" : False, "n_rencontre" : 0, "n_source_chaude" : 0, "temple" : 0, "budget_repas": 0,
                               "a_gourmet": False, "a_baigneur": False, "a_bavard": False, "a_collectionneur": False, "points_temple": 0}
            
        # affichage
        coordonee_centre = PLATEAU[self.position[0]][self.position[1]][2]
        decalage = self.position[2]
        decalage_station = PLATEAU[self.position[0]][self.position[1]][3]
        if self.position[1] == 0:
            if self.position[2] == 1: decalage = decalage_station * DECALAGE_STATION_RELAIS
            else: decalage = decalage_station * DECALAGE_STATION_RELAIS + (decalage - 1) * decalage_station * 67
        else: decalage = (decalage - 1) * decalage_station * DECALAGE_STATION_DOUBLE
        self.coordonee = [coordonee_centre[0] + decalage, coordonee_centre[1] - 30]
        self.image = pygame.image.load(f"../Graphique/Jeu/pion_{self.couleur}.png").convert_alpha()
        self.rect = self.image.get_rect(center = self.coordonee)


    # methode pour changer le joueur et son pion de position
    def change_pos(self, liste_joueur, coordonee_station, position_station):

        self.coordonee = [coordonee_station[0], coordonee_station[1] - 30]
        self.rect.center = self.coordonee
        position_sur_station = 1
        for joueur in liste_joueur:
            if joueur.position[:2] == list(position_station):
                position_sur_station += 1
        self.position = [position_station[0], position_station[1], position_sur_station]


    # methode ajoutant nombre de pieces au joueur
    def add_pieces(self, pieces):

        self.pieces += pieces


    # methode ajoutantun nombre de points au joueur
    def add_points(self, points):

        self.points += points


    # methode ajoutant des pieces au temple
    def add_temple(self, pieces):

        self.collection["temple"] += pieces


    # methode ajoutant un souvenir a la collection et comptant les points
    def add_echoppe(self, type_souvenir, cout):

        # permet de trouver la meilleure liste famille differente pour ajouter max de points
        liste_famille_diff_plus_grande = list()
        longueur_liste = 0
        index = 0
        index_ajout = -1
        for liste_famille_diff in self.collection["compteur_points_echoppe"]:
            if type_souvenir not in liste_famille_diff:
                if len(liste_famille_diff) > longueur_liste:
                    liste_famille_diff_plus_grande = liste_famille_diff
                    longueur_liste = len(liste_famille_diff)
                    index_ajout = index
            index += 1

        # calcul le nombre de point a ajoute et enleve l'argent
        if longueur_liste == 0: self.add_points(1)
        elif longueur_liste == 1: self.add_points(3)
        elif longueur_liste == 2: self.add_points(5)
        elif longueur_liste == 3: self.add_points(7)
        self.add_pieces(-cout)

        # ajoute aux collection
        self.collection["echoppe"][type_souvenir] += 1
        if index_ajout == -1:
            self.collection["compteur_points_echoppe"].append([type_souvenir])
        else:
            self.collection["compteur_points_echoppe"][index_ajout].append(type_souvenir)

        ech = self.collection["echoppe"]
        coll = self.collection["compteur_points_echoppe"]


    # methode ajoutant un pano au joueur
    def add_pano(self, type_pano, accomplissement):

        self.collection[f"p_{type_pano}"] += 1
        if accomplissement: self.collection[f"a_{type_pano}"] = True