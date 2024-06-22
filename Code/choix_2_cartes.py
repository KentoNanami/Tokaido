# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 15:15:55 2023

@author: 36796932
"""

import pygame
from parametre_general import *
from Button import Bouton_Image



# classe permettant au joueur de choisir entre 2 cartes
class Choix_2_Cartes:

    def __init__(self, carte_1, carte_2, path_1, path_2, carte_3 = None, path_3 = None):

        # general
        self.ecran = pygame.display.get_surface()
        self.bouton = pygame.sprite.Group()
        self.continuer = True

        self.carte1 = carte_1
        self.carte2 = carte_2
        self.carte3 = carte_3

        if self.carte3:
            pos1 = POSITION_CHOIX_2_CARTES["3.carte 1"]
            pos2 = POSITION_CHOIX_2_CARTES["3.carte 2"]
        else:
            pos1 = POSITION_CHOIX_2_CARTES["carte 1"]
            pos2 = POSITION_CHOIX_2_CARTES["carte 2"]

        # affichage
        self.carte1_bouton = Bouton_Image(pos1, path_1, group = self.bouton, clickable = True, survolable = True, resize = SURVOLEE_SIZE_CHOIX_2_CARTES, point_position = "center")
        self.carte2_bouton = Bouton_Image(pos2, path_2, group = self.bouton, clickable = True, survolable = True, resize = SURVOLEE_SIZE_CHOIX_2_CARTES, point_position = "center")
        if self.carte3:
          self.carte3_bouton = Bouton_Image(POSITION_CHOIX_2_CARTES["3.carte 3"], path_3, group = self.bouton, clickable = True, survolable = True, 
                                              resize = SURVOLEE_SIZE_CHOIX_2_CARTES, point_position = "center")


    def run(self):


        while self.continuer:

            # on gère les évenments
            for event in pygame.event.get():
        
                # si l'utilisateur clique sur echap
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.continuer = False

            self.ecran.fill(COULEUR["beige"])

            if self.carte1_bouton.check_click():
                voyageur_choisi = self.carte1
                self.continuer = False
            elif self.carte2_bouton.check_click():
                voyageur_choisi = self.carte2
                self.continuer = False
            if self.carte3:
              if self.carte3_bouton.check_click():
                voyageur_choisi = self.carte3
                self.continuer = False

            self.bouton.draw(self.ecran)

            pygame.display.update()

        return voyageur_choisi