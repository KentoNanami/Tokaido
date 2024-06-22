# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 22:37:40 2023

@author: Jules JOUVIN
"""

import pygame
from parametre_general import *
from random import shuffle
from joueur import Joueur
from Button import Bouton_Image
from choix_2_cartes import Choix_2_Cartes
import login



class Creation_jeu:
    
    def __init__(self):
        
        # general
        self.ecran = pygame.display.get_surface()
        self.liste_joueur = []
        self.nbr_total = 2
        self.nbr_IA = 0
        self.indice_mode = 0
        self.liste_voyageur_joueur = []
        self.liste_voyageur = []
        for carte in CARTES_PERSONNAGES:
            self.liste_voyageur.append(carte)
        shuffle(self.liste_voyageur)

        self.sprite_visible = pygame.sprite.Group()

        # affichage
        self.font_edos = pygame.font.Font('../Font/edosz.ttf', FONT_SIZE_CREATION_JEU)
        self.font_edos_petit = pygame.font.Font('../Font/edosz.ttf', FONT_SIZE_CREATION_JEU_PETIT)
        self.fond_im = pygame.image.load("../Graphique/Creation_jeu/fond.png").convert_alpha()
        self.fond_rect = self.fond_im.get_rect(topleft = POSITION_FIN_JEU["fond"])
        self.confirmer = Bouton_Image(POSITION_CREATION_JEU["bouton confirmer"], "../Graphique/Bouttons/annuler.png", group = self.sprite_visible, clickable = True, survolable = True, 
                                      image_path_survolee = "../Graphique/Bouttons/annuler_survolee.png")
        self.fleche_up_total = Bouton_Image(POSITION_CREATION_JEU["fleche up total"], "../Graphique/Temple/fleche_up.png", self.sprite_visible, True, survolable = True, image_path_survolee = "../Graphique/Temple/fleche_up_survolee.png")
        self.fleche_down_total = Bouton_Image(POSITION_CREATION_JEU["fleche down total"], "../Graphique/Temple/fleche_down.png", self.sprite_visible, True, survolable = True, image_path_survolee = "../Graphique/Temple/fleche_down_survolee.png")
        self.fleche_up_IA= Bouton_Image(POSITION_CREATION_JEU["fleche up IA"], "../Graphique/Temple/fleche_up.png", self.sprite_visible, True, survolable = True, image_path_survolee = "../Graphique/Temple/fleche_up_survolee.png")
        self.fleche_down_IA = Bouton_Image(POSITION_CREATION_JEU["fleche down IA"], "../Graphique/Temple/fleche_down.png", self.sprite_visible, True, survolable = True, image_path_survolee = "../Graphique/Temple/fleche_down_survolee.png")
        self.fleche_up_mode = Bouton_Image(POSITION_CREATION_JEU["fleche up mode"], "../Graphique/Temple/fleche_up.png", self.sprite_visible, True, survolable = True, image_path_survolee = "../Graphique/Temple/fleche_up_survolee.png")
        self.fleche_down_mode = Bouton_Image(POSITION_CREATION_JEU["fleche down mode"], "../Graphique/Temple/fleche_down.png", self.sprite_visible, True, survolable = True, image_path_survolee = "../Graphique/Temple/fleche_down_survolee.png")
        self.text_total = self.font_edos.render("2", True, COULEUR["couleur font"])
        self.text_total_rect = self.text_total.get_rect(center = POSITION_CREATION_JEU["text nbr total joueur"])
        self.text_IA = self.font_edos.render("0", True, COULEUR["couleur font"])
        self.text_IA_rect = self.text_IA.get_rect(center = POSITION_CREATION_JEU["text nbr IA"])
        self.text_mode = self.font_edos_petit.render(GAME_MOD[self.indice_mode], True, COULEUR["couleur font"])
        self.text_mode_rect = self.text_mode.get_rect(midright = POSITION_CREATION_JEU["text mode"])

        # transparent background
        self.transp_surface = pygame.Surface((1920,1080), pygame.SRCALPHA)
        self.transp_surface.fill((251, 253, 248, 150))


    # login de Martin
    def display_login(self, j):

        liste_pseudo_joueur = []

        i = 1
        while i <= j:
            self.ecran.fill(COULEUR["beige"])
            text_surf = self.font_edos.render("Joueur "+ str(i), True, 'Black')
            text_rect = text_surf.get_rect(midbottom = (960, 300))
            self.ecran.blit(text_surf, text_rect)
            pygame.display.update()
            pseudo = login.login()
            liste_pseudo_joueur.append(pseudo)
            i+= 1

            if GAME_MOD[self.indice_mode] == "classique":
                c1 = self.liste_voyageur.pop(0)
                c2 = self.liste_voyageur.pop(0)

                choix_2_cartes = Choix_2_Cartes(c1, c2, f"../Graphique/Carte_personage/{c1}.png", f"../Graphique/Carte_personage/{c2}.png")
                voyageur = choix_2_cartes.run()
                self.liste_voyageur_joueur.append(voyageur)
                del(choix_2_cartes)

        return liste_pseudo_joueur

        
    # va initier la partie avec les parametres choisi
    def init_jeu(self, jeu):

        # creation liste joueur
        liste_pseudo = self.display_login(self.nbr_total - self.nbr_IA)

        # definit couleur et non robot perso aléatoirement
        couleur = ["bleu", "gris", "vert", "jaune", "rose"]
        shuffle(couleur)
        # oblige de faire comme ca sinon modifie la liste des noms de robots
        robot_name = []
        for name in ROBOT_NAME:
            robot_name.append(name)
        shuffle(robot_name)

        #creation joueur

        index_jouers = list(range(1, self.nbr_total+1))
        shuffle(index_jouers)
        index = 0
        if GAME_MOD[self.indice_mode] == "classique":
            for pseudo in liste_pseudo:
                if pseudo:
                    self.liste_joueur.append(Joueur(index, couleur[index], pseudo = pseudo, position = [0, 0, index_jouers[index]], voyageur = self.liste_voyageur_joueur[index], piece = CARTES_PERSONNAGES[self.liste_voyageur_joueur[index]]))
                else:
                    self.liste_joueur.append(Joueur(index, couleur[index], pseudo = robot_name.pop(0), position = [0, 0, index_jouers[index]], voyageur = self.liste_voyageur_joueur[index], piece = CARTES_PERSONNAGES[self.liste_voyageur_joueur[index]]))
                index += 1
            for robot in range(self.nbr_IA):
                voyageur = self.liste_voyageur.pop(0)
                self.liste_joueur.append(Joueur(index, couleur[index], pseudo = robot_name.pop(0), IA = True, position = [0, 0, index_jouers[index]], voyageur = voyageur, piece = CARTES_PERSONNAGES[voyageur]))
                index += 1

        elif GAME_MOD[self.indice_mode] == "voyage initiatique":
            for pseudo in liste_pseudo:
                if pseudo:
                    self.liste_joueur.append(Joueur(index, couleur[index], pseudo = pseudo, position = [0, 0, index_jouers[index]]))
                else:
                    self.liste_joueur.append(Joueur(index, couleur[index], pseudo = robot_name.pop(0), position = [0, 0, index_jouers[index]]))
                index += 1
            for robot in range(self.nbr_IA):
                self.liste_joueur.append(Joueur(index, couleur[index], pseudo = robot_name.pop(0), IA = True, position = [0, 0, index_jouers[index]]))
                index += 1
        
        jeu.liste_joueur = self.liste_joueur
        
        for joueur in jeu.liste_joueur:
            jeu.sprite_visible.add(joueur)

        return True


    def update(self, jeu):

        if self.fleche_up_total.check_click():
            if self.nbr_total < 5:
                self.nbr_total += 1
                self.text_total = self.font_edos.render(str(self.nbr_total), True, COULEUR["couleur font"])
        if self.fleche_down_total.check_click():
            if self.nbr_total > 2 and self.nbr_total > self.nbr_IA + 1:
                self.nbr_total -= 1
                self.text_total = self.font_edos.render(str(self.nbr_total), True, COULEUR["couleur font"])
        if self.fleche_up_IA.check_click():
            if self.nbr_IA < self.nbr_total - 1:
                self.nbr_IA += 1
                self.text_IA = self.font_edos.render(str(self.nbr_IA), True, COULEUR["couleur font"])
        if self.fleche_down_IA.check_click():
            if self.nbr_IA > 0:
                self.nbr_IA -= 1
                self.text_IA = self.font_edos.render(str(self.nbr_IA), True, COULEUR["couleur font"])
        if self.fleche_up_mode.check_click():
            if self.indice_mode < len(GAME_MOD) - 1:
                self.indice_mode += 1
                self.text_mode = self.font_edos_petit.render(GAME_MOD[self.indice_mode], True, COULEUR["couleur font"])
                self.text_mode_rect = self.text_mode.get_rect(midright = POSITION_CREATION_JEU["text mode"])
        if self.fleche_down_mode.check_click():
            if self.indice_mode > 0:
                self.indice_mode -= 1
                self.text_mode = self.font_edos_petit.render(GAME_MOD[self.indice_mode], True, COULEUR["couleur font"])
                self.text_mode_rect = self.text_mode.get_rect(midright = POSITION_CREATION_JEU["text mode"])
        if self.confirmer.check_click():
            return self.init_jeu(jeu)


    def afficher(self):

        self.ecran.blit(self.fond_im, self.fond_rect)
        self.sprite_visible.draw(self.ecran)
        self.ecran.blit(self.text_total, self.text_total_rect)
        self.ecran.blit(self.text_IA, self.text_IA_rect)
        self.ecran.blit(self.text_mode, self.text_mode_rect)


    def run(self, jeu):

        self.ecran.blit(self.transp_surface, (0, 0))

        # afficher
        lancer_jeu = self.update(jeu)
        self.afficher()

        if lancer_jeu:
            return True

        pygame.display.update()