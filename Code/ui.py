# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 15:25:32 2023

@author: 36796932
"""

import pygame
from parametre_general import *



class UI:
    

    def __init__(self, joueur):
        
        # general
        self.ecran = pygame.display.get_surface()
        self.font_edos = pygame.font.Font('../Font/edosz.ttf', FONT_SIZE_CARTE_J)
        self.couleur = joueur.couleur   
        self.index = joueur.index_joueur

        # image carte
        self.fond_im = pygame.image.load("../Graphique/Carte_joueur/fond_carte.png").convert_alpha()
        self.fond_rect = self.fond_im.get_rect(topleft = POSITION_CARTE_J[self.index]["fond"])

        if joueur.voyageur:
            self.avatar_im = pygame.image.load(f"../Graphique/Avatar/{joueur.voyageur}.png").convert_alpha()
            self.avatar_rect = self.avatar_im.get_rect(center = POSITION_CARTE_J[self.index]["avatar"])
        else: self.avatar_im = None

        self.position_cercle = (POSITION_CARTE_J[self.index]["avatar"][0] + 1, POSITION_CARTE_J[self.index]["avatar"][1] + 20)

        self.banieres_im = pygame.image.load("../Graphique/Carte_joueur/banieres.png").convert_alpha()
        self.banieres_rect = self.banieres_im.get_rect(topleft = POSITION_CARTE_J[self.index]["banieres"])
        # texte 
        self.text_pseudo = self.font_edos.render(joueur.pseudo, True, COULEUR["couleur font"])
        self.text_pseudo_rect = self.text_pseudo.get_rect(topleft = POSITION_CARTE_J[self.index]["pseudo"])
        self.text_temple = self.font_edos.render(str(joueur.collection["temple"]), True, COULEUR["couleur font"])
        self.text_temple_rect = self.text_temple.get_rect(center = POSITION_CARTE_J[self.index]["T temple"])
        self.text_piece = self.font_edos.render(str(joueur.pieces), True, COULEUR["couleur font"])
        self.text_piece_rect = self.text_piece.get_rect(center = POSITION_CARTE_J[self.index]["T pieces"])
        self.text_points = self.font_edos.render(str(joueur.points), True, COULEUR["couleur font"])
        self.text_points_rect = self.text_points.get_rect(center = POSITION_CARTE_J[self.index]["T points"])
        self.text_mer = self.font_edos.render(str(joueur.collection["p_mer"]), True, COULEUR["couleur font"])
        self.text_mer_rect = self.text_mer.get_rect(topleft = POSITION_CARTE_J[self.index]["T pano mer"])
        self.text_montagne = self.font_edos.render(str(joueur.collection["p_montagne"]), True, COULEUR["couleur font"])
        self.text_montagne_rect = self.text_montagne.get_rect(topleft = POSITION_CARTE_J[self.index]["T pano montagne"])
        self.text_riziere = self.font_edos.render(str(joueur.collection["p_riziere"]), True, COULEUR["couleur font"])
        self.text_riziere_rect = self.text_riziere.get_rect(topleft = POSITION_CARTE_J[self.index]["T pano riziere"])
        

    # méthode permettant d'update les informations du joueurs pour les afficher
    def update(self, updated_pieces = None, updated_points = None, updated_pano_riziere = None, updated_pano_montagne = None, updated_pano_mer = None, updated_temple = None):

        if updated_pieces != None:
            self.text_piece = self.font_edos.render(str(updated_pieces), True, COULEUR["couleur font"])
            self.text_piece_rect = self.text_piece.get_rect(center = POSITION_CARTE_J[self.index]["T pieces"])

        if updated_points:
            self.text_points = self.font_edos.render(str(updated_points), True, COULEUR["couleur font"])
            self.text_points_rect = self.text_points.get_rect(center = POSITION_CARTE_J[self.index]["T points"])

        if updated_pano_riziere:
            self.text_riziere = self.font_edos.render(str(updated_pano_riziere), True, COULEUR["couleur font"])

        if updated_pano_montagne:
            self.text_montagne = self.font_edos.render(str(updated_pano_montagne), True, COULEUR["couleur font"])

        if updated_pano_mer:
            self.text_mer = self.font_edos.render(str(updated_pano_mer), True, COULEUR["couleur font"])

        if updated_temple:
            self.text_temple = self.font_edos.render(str(updated_temple), True, COULEUR["couleur font"])


    def afficher(self):

        self.ecran.blit(self.fond_im, self.fond_rect)
        self.ecran.blit(self.text_pseudo, self.text_pseudo_rect)
        pygame.draw.circle(self.ecran, COULEUR[self.couleur], self.position_cercle, 80)
        if self.avatar_im: self.ecran.blit(self.avatar_im, self.avatar_rect)

        self.ecran.blit(self.banieres_im, self.banieres_rect)
        self.ecran.blit(self.text_temple, self.text_temple_rect)
        self.ecran.blit(self.text_piece, self.text_piece_rect)
        self.ecran.blit(self.text_points, self.text_points_rect)

        self.ecran.blit(self.text_riziere, self.text_riziere_rect)
        self.ecran.blit(self.text_montagne, self.text_montagne_rect)
        self.ecran.blit(self.text_mer, self.text_mer_rect)
