# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 21:47:09 2023

@author: Jules JOUVIN
"""

import pygame
from parametre_general import *
from Button import Bouton_Image
from choix_2_cartes import Choix_2_Cartes


class Station(pygame.sprite.Sprite):
    

    def __init__(self, types = None, station_double = False, position = None, coordonnee = None, direction = 0):
        
        super().__init__()

        # définit la station
        self.type = types
        self.station_double = station_double
        self.position = position                # tuple avec [0] le jour et [1] positon par rapport aux relais

        # affichage
        self.direction = direction   # ±1
        
        self.decalage = self.direction * DECALAGE_STATION_DOUBLE
        self.coordonee = (coordonnee[0] - 23, coordonnee[1] - 23)
        self.coordonee_center = (coordonnee[0], coordonnee[1])
        self.images_animation = [pygame.image.load("../Graphique/Jeu/station_selectionable.png").convert_alpha(),
                                 pygame.image.load("../Graphique/Jeu/station_survolee.png").convert_alpha()]
        self.image = self.images_animation[0]
        self.rect = self.image.get_rect(topleft = self.coordonee)
        self.pressed = False

        # si la station est un relai alors permet de gerer le nombre de passage
        if self.type == "relais":
            self.relai = None


    # methode quand le bouton est non survolee
    def idle(self):

        self.image = self.images_animation[0]


    # methode reagissant quand le bouton survolée
    def survolee(self):

        self.image = self.images_animation[1]


    # quand le bouton est clické
    def clicked(self, liste_joueur, joueur_jouant, ui_joueur, decks_cartes, relai):

        # deplace le pion
        joueur_jouant.change_pos(liste_joueur, self.coordonee_center, self.position)

        # effectué actions de la case
        if self.type == "relais":
            relai.run(joueur_jouant, liste_joueur, decks_cartes)
            ui_joueur.update(updated_pieces = joueur_jouant.pieces, updated_points = joueur_jouant.points, updated_pano_riziere = joueur_jouant.collection["p_riziere"], updated_temple = joueur_jouant.collection["temple"],
                             updated_pano_montagne = joueur_jouant.collection["p_montagne"], updated_pano_mer = joueur_jouant.collection["p_mer"])

        elif self.type == "echoppe":
            echoppe = Echoppe(joueur_jouant, decks_cartes["souvenirs"])
            echoppe.run(joueur_jouant)
            del(echoppe)
            ui_joueur.update(updated_pieces = joueur_jouant.pieces, updated_points = joueur_jouant.points)

        elif self.type == "temple":
            temple = Temple(joueur_jouant)
            temple.run(joueur_jouant)
            del(temple)
            ui_joueur.update(updated_pieces = joueur_jouant.pieces, updated_temple = joueur_jouant.collection["temple"], updated_points = joueur_jouant.points)

        elif self.type == "rencontre":
            rencontre = Rencontre(joueur_jouant, decks_cartes)
            rencontre.run(joueur_jouant, liste_joueur)
            del(rencontre)
            ui_joueur.update(updated_pieces = joueur_jouant.pieces, updated_points = joueur_jouant.points, updated_pano_riziere = joueur_jouant.collection["p_riziere"], updated_temple = joueur_jouant.collection["temple"],
                             updated_pano_montagne = joueur_jouant.collection["p_montagne"], updated_pano_mer = joueur_jouant.collection["p_mer"])

        elif self.type == "source chaude":
            points = decks_cartes["sources_chaudes"].pop(0)
            joueur_jouant.add_points(points)
            if joueur_jouant.voyageur == "mitsukuni":
                joueur_jouant.add_points(1)
            joueur_jouant.collection["n_source_chaude"] += 1
            ui_joueur.update(updated_points = joueur_jouant.points)

        elif self.type == "ferme":
            joueur_jouant.add_pieces(3)
            ui_joueur.update(updated_pieces = joueur_jouant.pieces)

        elif self.type == "pano riziere":
            accomplissement = False
            points_ac = 0
            if joueur_jouant.collection["p_riziere"] == 2:
                accomplissement = True
                points_ac = 3
                for joueur in liste_joueur:
                    if joueur.collection["a_riziere"]:
                        accomplissement = False
                        points_ac = 0
            joueur_jouant.add_pano("riziere", accomplissement)
            joueur_jouant.add_points(joueur_jouant.collection["p_riziere"] + points_ac)
            if joueur_jouant.voyageur == "mitsukuni" and joueur_jouant.collection["a_riziere"]:
                joueur_jouant.add_points(1)
            ui_joueur.update(updated_pano_riziere = joueur_jouant.collection["p_riziere"], updated_points = joueur_jouant.points)

        elif self.type == "pano montagne":
            accomplissement = False
            points_ac = 0
            if joueur_jouant.collection["p_montagne"] == 3:
                accomplissement = True
                points_ac = 3
                for joueur in liste_joueur:
                    if joueur.collection["a_montagne"]:
                        accomplissement = False
                        points_ac = 0
            joueur_jouant.add_pano("montagne", accomplissement)
            joueur_jouant.add_points(joueur_jouant.collection["p_montagne"] + points_ac)
            if joueur_jouant.voyageur == "mitsukuni" and joueur_jouant.collection["a_montagne"]:
                joueur_jouant.add_points(1)
            ui_joueur.update(updated_pano_montagne = joueur_jouant.collection["p_montagne"], updated_points = joueur_jouant.points)

        elif self.type == "pano mer":
            accomplissement = False
            points_ac = 0
            if joueur_jouant.collection["p_mer"] == 4:
                accomplissement = True
                points_ac = 3
                for joueur in liste_joueur:
                    if joueur.collection["a_mer"]:
                        accomplissement = False
                        points_ac = 0
            joueur_jouant.add_pano("mer", accomplissement)
            joueur_jouant.add_points(joueur_jouant.collection["p_mer"] + points_ac)
            if joueur_jouant.voyageur == "mitsukuni" and joueur_jouant.collection["a_mer"]:
                joueur_jouant.add_points(1)
            ui_joueur.update(updated_pano_mer = joueur_jouant.collection["p_mer"], updated_points = joueur_jouant.points)



class Temple:

    def __init__(self, joueur):

        # general
        self.ecran = pygame.display.get_surface()
        self.continuer = True
        self.pieces_donnees = 1

        # groupe
        self.bouton = pygame.sprite.Group()
        self.fleche_up = Bouton_Image(POSITION_TEMPLE["bouton up"], "../Graphique/Temple/fleche_up.png", self.bouton, True, survolable = True, image_path_survolee = "../Graphique/Temple/fleche_up_survolee.png")
        self.fleche_down = Bouton_Image(POSITION_TEMPLE["bouton down"], "../Graphique/Temple/fleche_down.png", self.bouton, True, survolable = True, image_path_survolee = "../Graphique/Temple/fleche_down_survolee.png")
        self.confirmer = Bouton_Image(POSITION_TEMPLE["bouton confirmer"], "../Graphique/Bouttons/confirmer.png", self.bouton, True, survolable = True, image_path_survolee = "../Graphique/Bouttons/confirmer_survolee.png")

        # affichage
        self.font_edos = pygame.font.Font('../Font/edosz.ttf', FONT_SIZE_TEMPLE)
        self.font_edos_petit = pygame.font.Font('../Font/edosz.ttf', FONT_SIZE_TEMPLE_PETIT)
        self.fond_im = pygame.image.load("../Graphique/Temple/fond.png").convert_alpha()
        self.fond_rect = self.fond_im.get_rect(topleft = POSITION_TEMPLE["fond"])
        if joueur.voyageur:
            self.avatar_im = pygame.image.load(f"../Graphique/Avatar/{joueur.voyageur}.png").convert_alpha()
            self.avatar_rect = self.avatar_im.get_rect(center = POSITION_TEMPLE["couleur"])
        else: self.avatar_im = None
        self.baniere_im = pygame.image.load("../Graphique/Temple/baniere.png").convert_alpha()
        self.baniere_rect = self.baniere_im.get_rect(topleft = POSITION_TEMPLE["baniere"])
        self.text_pieces_joueurs = self.font_edos_petit.render(str(joueur.pieces), True, COULEUR["couleur font"])
        self.text_pieces_joueurs_rect = self.text_pieces_joueurs.get_rect(center = POSITION_TEMPLE["nbr pieces joueurs"])
        self.text_pieces_donee = self.font_edos.render("x 1", True, COULEUR["couleur font"])
        self.text_pieces_donee_rect = self.text_pieces_donee.get_rect(center = POSITION_TEMPLE["pieces donnes"])

        # transparent background
        self.transp_surface = pygame.Surface((1920,1080), pygame.SRCALPHA)
        self.transp_surface.fill((251, 253, 248, 150))


    # methode qui va enlever les pieces du joueurs et ajouter les pieces au temple
    def finito_pepito(self, joueur):

        joueur.add_pieces(-self.pieces_donnees)
        joueur.add_temple(self.pieces_donnees)
        joueur.add_points(self.pieces_donnees)
        if joueur.voyageur == "hirotada":
            joueur.add_temple(1)
            joueur.add_points(1)
        self.continuer = False


    def update(self, joueur):

        if self.fleche_up.check_click():
            if self.pieces_donnees < 3 and self.pieces_donnees < joueur.pieces:
                self.pieces_donnees += 1
                self.text_pieces_donee = self.font_edos.render(f"x {self.pieces_donnees}", True, COULEUR["couleur font"])
        if self.fleche_down.check_click():
            if self.pieces_donnees > 1:
                self.pieces_donnees -= 1
                self.text_pieces_donee = self.font_edos.render(f"x {self.pieces_donnees}", True, COULEUR["couleur font"])
        if self.confirmer.check_click():
            self.finito_pepito(joueur)


    def afficher(self, joueur):

        self.ecran.blit(self.fond_im, self.fond_rect)
        pygame.draw.circle(self.ecran, COULEUR[joueur.couleur], POSITION_TEMPLE["couleur"], 110)
        if self.avatar_im: self.ecran.blit(self.avatar_im, self.avatar_rect)
        self.ecran.blit(self.baniere_im, self.baniere_rect)
        self.bouton.draw(self.ecran)
        self.ecran.blit(self.text_pieces_donee, self.text_pieces_donee_rect)
        self.ecran.blit(self.text_pieces_joueurs, self.text_pieces_joueurs_rect)


    def run(self, joueur):

        self.ecran.blit(self.transp_surface, (0, 0))

        while self.continuer:

            # on gère les évenments
            for event in pygame.event.get():
        
                # si l'utilisateur clique sur echap
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.continuer = False

            # afficher
            self.update(joueur)
            self.afficher(joueur)

            pygame.display.update()



class Echoppe:

    def __init__(self, joueur, decks_cartes):

        # general
        self.ecran = pygame.display.get_surface()
        self.continuer = True

        self.carte1 = decks_cartes.pop(0)
        self.carte2 = decks_cartes.pop(0)
        self.carte3 = decks_cartes.pop(0)

        self.carte_achete = []

        # groupe
        self.bouton = pygame.sprite.Group()
        self.confirmer = Bouton_Image(POSITION_ECHOPPE["bouton confirmer"], "../Graphique/Bouttons/confirmer.png", group = self.bouton, clickable = True, survolable = True, 
                                      image_path_survolee = "../Graphique/Bouttons/confirmer_survolee.png")

        # affichage
        self.font_edos = pygame.font.Font('../Font/edosz.ttf', FONT_SIZE_ECHOPPE)
        self.fond_im = pygame.image.load("../Graphique/Echoppe/fond.png").convert_alpha()
        self.fond_rect = self.fond_im.get_rect(topleft = POSITION_ECHOPPE["fond"])
        if joueur.voyageur:
            self.avatar_im = pygame.image.load(f"../Graphique/Avatar/{joueur.voyageur}.png").convert_alpha()
            self.avatar_rect = self.avatar_im.get_rect(center = POSITION_ECHOPPE["couleur"])
        else: self.avatar_im = None
        self.baniere_im = pygame.image.load("../Graphique/Temple/baniere.png").convert_alpha()
        self.baniere_rect = self.baniere_im.get_rect(topleft = POSITION_ECHOPPE["baniere"])
        self.text_petit_souvenir = self.font_edos.render(str(joueur.collection["echoppe"]["petit souvenir"]), True, COULEUR["couleur font"])
        self.text_petit_souvenir_rect = self.text_petit_souvenir.get_rect(center = POSITION_ECHOPPE["text petit souvenir"])
        self.text_nouriture = self.font_edos.render(str(joueur.collection["echoppe"]["nouriture"]), True, COULEUR["couleur font"])
        self.text_nouriture_rect = self.text_nouriture.get_rect(center = POSITION_ECHOPPE["text nouriture"])
        self.text_gros_souvenir = self.font_edos.render(str(joueur.collection["echoppe"]["gros souvenir"]), True, COULEUR["couleur font"])
        self.text_gros_souvenir_rect = self.text_gros_souvenir.get_rect(center = POSITION_ECHOPPE["text gros souvenir"])
        self.text_vetement = self.font_edos.render(str(joueur.collection["echoppe"]["vetement"]), True, COULEUR["couleur font"])
        self.text_vetement_rect = self.text_vetement.get_rect(center = POSITION_ECHOPPE["text vetement"])
        self.text_pieces_joueurs = self.font_edos.render(str(joueur.pieces), True, COULEUR["couleur font"])
        self.text_pieces_joueurs_rect = self.text_pieces_joueurs.get_rect(center = POSITION_ECHOPPE["pieces joueurs"])

        self.carte1_bouton = Bouton_Image(POSITION_ECHOPPE["carte 1"], f"../Graphique/Echoppe/c_{self.carte1}.png", group = self.bouton, clickable = True, survolable = True, 
                                         resize = SURVOLEE_SIZE_CARTE_ECHOPPE, point_position = "center")
        self.carte2_bouton = Bouton_Image(POSITION_ECHOPPE["carte 2"], f"../Graphique/Echoppe/c_{self.carte2}.png", group = self.bouton, clickable = True, survolable = True, 
                                         resize = SURVOLEE_SIZE_CARTE_ECHOPPE, point_position = "center")
        self.carte3_bouton = Bouton_Image(POSITION_ECHOPPE["carte 3"], f"../Graphique/Echoppe/c_{self.carte3}.png", group = self.bouton, clickable = True, survolable = True, 
                                         resize = SURVOLEE_SIZE_CARTE_ECHOPPE, point_position = "center")

        # transparent background
        self.transp_surface = pygame.Surface((1920,1080), pygame.SRCALPHA)
        self.transp_surface.fill((251, 253, 248, 150))


    def update_text(self, joueur, type_souvenir):

        if type_souvenir == "petit souvenir":
            self.text_petit_souvenir = self.font_edos.render(str(joueur.collection["echoppe"]["petit souvenir"]), True, COULEUR["couleur font"])
        elif type_souvenir == "nouriture":
            self.text_nouriture = self.font_edos.render(str(joueur.collection["echoppe"]["nouriture"]), True, COULEUR["couleur font"])
        elif type_souvenir == "gros souvenir":
            self.text_gros_souvenir = self.font_edos.render(str(joueur.collection["echoppe"]["gros souvenir"]), True, COULEUR["couleur font"])
        elif type_souvenir == "vetement":
            self.text_vetement = self.font_edos.render(str(joueur.collection["echoppe"]["vetement"]), True, COULEUR["couleur font"])

        self.text_pieces_joueurs = self.font_edos.render(str(joueur.pieces), True, COULEUR["couleur font"])
        self.text_pieces_joueurs_rect = self.text_pieces_joueurs.get_rect(center = POSITION_ECHOPPE["pieces joueurs"])


    def update(self, joueur):

        if self.confirmer.check_click():

            if joueur.voyageur == "sasayakko" and len(self.carte_achete) >= 2:
                cout_min = 4
                for souvenir in self.carte_achete:
                    if cout_min > CARTES_SOUVENIRS[souvenir][1]:
                        cout_min = CARTES_SOUVENIRS[souvenir][1]
                joueur.add_pieces(cout_min)

            self.continuer = False

        if self.carte1_bouton.check_click():

            if joueur.voyageur == "zen-emon" and not self.carte_achete:
                joueur.add_echoppe(CARTES_SOUVENIRS[self.carte1][0], 1)
                self.carte1_bouton.kill()
                self.carte1_bouton.killed = True
                self.update_text(joueur, CARTES_SOUVENIRS[self.carte1][0])
                self.carte_achete.append(self.carte1)

            elif joueur.pieces >= CARTES_SOUVENIRS[self.carte1][1]:
                joueur.add_echoppe(CARTES_SOUVENIRS[self.carte1][0], CARTES_SOUVENIRS[self.carte1][1])
                self.carte1_bouton.kill()
                self.carte1_bouton.killed = True
                self.update_text(joueur, CARTES_SOUVENIRS[self.carte1][0])
                self.carte_achete.append(self.carte1)

        if self.carte2_bouton.check_click():

            if joueur.voyageur == "zen-emon" and not self.carte_achete:
                joueur.add_echoppe(CARTES_SOUVENIRS[self.carte2][0], 1)
                self.carte2_bouton.kill()
                self.carte2_bouton.killed = True
                self.update_text(joueur, CARTES_SOUVENIRS[self.carte2][0])
                self.carte_achete.append(self.carte2)

            elif joueur.pieces >= CARTES_SOUVENIRS[self.carte2][1]:
                joueur.add_echoppe(CARTES_SOUVENIRS[self.carte2][0], CARTES_SOUVENIRS[self.carte2][1])
                self.carte2_bouton.kill()
                self.carte2_bouton.killed = True
                self.update_text(joueur, CARTES_SOUVENIRS[self.carte2][0])
                self.carte_achete.append(self.carte2)

        if self.carte3_bouton.check_click():

            if joueur.voyageur == "zen-emon" and not self.carte_achete:
                joueur.add_echoppe(CARTES_SOUVENIRS[self.carte3][0], 1)
                self.carte3_bouton.kill()
                self.carte3_bouton.killed = True
                self.update_text(joueur, CARTES_SOUVENIRS[self.carte3][0])
                self.carte_achete.append(self.carte3)

            elif joueur.pieces >= CARTES_SOUVENIRS[self.carte2][1]:
                joueur.add_echoppe(CARTES_SOUVENIRS[self.carte3][0], CARTES_SOUVENIRS[self.carte3][1])
                self.carte3_bouton.kill()
                self.carte3_bouton.killed = True
                self.update_text(joueur, CARTES_SOUVENIRS[self.carte3][0])
                self.carte_achete.append(self.carte3)


    def afficher(self, joueur):

        self.ecran.blit(self.fond_im, self.fond_rect)
        pygame.draw.circle(self.ecran, COULEUR[joueur.couleur], POSITION_ECHOPPE["couleur"], 110)
        if self.avatar_im: self.ecran.blit(self.avatar_im, self.avatar_rect)
        self.ecran.blit(self.baniere_im, self.baniere_rect)
        self.ecran.blit(self.text_pieces_joueurs, self.text_pieces_joueurs_rect)
        self.bouton.draw(self.ecran)
        self.ecran.blit(self.text_petit_souvenir, self.text_petit_souvenir_rect)
        self.ecran.blit(self.text_nouriture, self.text_nouriture_rect)
        self.ecran.blit(self.text_gros_souvenir, self.text_gros_souvenir_rect)
        self.ecran.blit(self.text_vetement, self.text_vetement_rect)


    def run(self, joueur):

        self.ecran.blit(self.transp_surface, (0, 0))

        while self.continuer:

            # on gère les évenments
            for event in pygame.event.get():
        
                # si l'utilisateur clique sur echap
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.continuer = False

            # afficher
            self.update(joueur)
            self.afficher(joueur)

            pygame.display.update()



class Relai:

    def __init__(self):

        # general
        self.ecran = pygame.display.get_surface()
        self.continuer = True
        self.text_repas_joueur = []
        self.cartes = []

        # groupe
        self.visible_sprite = pygame.sprite.Group()
        self.bouton = pygame.sprite.Group()
        self.confirmer = Bouton_Image(POSITION_RELAI["bouton confirmer"], "../Graphique/Bouttons/annuler.png", group = self.visible_sprite, clickable = True, survolable = True, 
                                      image_path_survolee = "../Graphique/Bouttons/annuler_survolee.png")

        # affichage
        self.font_edos = pygame.font.Font('../Font/edosz.ttf', FONT_SIZE_RELAI)
        self.font_edos_text = pygame.font.Font('../Font/edosz.ttf', FONT_SIZE_RELAI_TEXT)
        self.fond_im = pygame.image.load("../Graphique/Relai/fond.png").convert_alpha()
        self.fond_rect = self.fond_im.get_rect(topleft = POSITION_RELAI["fond"])
        self.baniere_im = pygame.image.load("../Graphique/Temple/baniere.png").convert_alpha()
        self.baniere_rect = self.baniere_im.get_rect(topleft = POSITION_RELAI["baniere"])

        # transparent background
        self.transp_surface = pygame.Surface((1920,1080), pygame.SRCALPHA)
        self.transp_surface.fill((251, 253, 248, 150))

    # initialise l'affichage
    def initialisation_affichage(self, joueur_jouant, liste_joueur, decks_cartes):

        self.continuer = True

        # perso lui avant car mise à jour affishage pièce etc...
        if joueur_jouant.voyageur == "chuubei":
            rencontre = Rencontre(joueur_jouant, decks_cartes)
            rencontre.run(joueur_jouant, liste_joueur)
            del(rencontre)

        if joueur_jouant.voyageur == "hiroshige":
            continu = True
            c1 = "rizière"
            c2 = "montagne"
            c3 = "mer"

            while continu:
                
                choix_2_cartes = Choix_2_Cartes(c1, c2, "../Graphique/Rencontre/pano_riziere.png", "../Graphique/Rencontre/pano_montagne.png", c3, "../Graphique/Rencontre/pano_mer.png")
                carte = choix_2_cartes.run()

                if carte == c1 and joueur_jouant.collection["p_riziere"] < 3:
                    accomplissement = False
                    p_ac = 0
                    if joueur_jouant.collection["p_riziere"] == 2:
                        accomplissement = True
                        p_ac = 3
                        for joueurs in liste_joueur:
                            if joueurs.collection["a_riziere"]:
                                accomplissement = False
                                p_ac = 0
                    joueur_jouant.add_pano("riziere", accomplissement)
                    joueur_jouant.add_points(joueur_jouant.collection["p_riziere"] + p_ac)
                    continu = False
                elif carte == c2 and joueur_jouant.collection["p_montagne"] < 4:
                    accomplissement = False
                    p_ac = 0
                    if joueur_jouant.collection["p_montagne"] == 3:
                        accomplissement = True
                        p_ac = 3
                        for joueurs in liste_joueur:
                            if joueurs.collection["a_montagne"]:
                                accomplissement = False
                                p_ac = 0
                    joueur_jouant.add_pano("montagne", accomplissement)
                    joueur_jouant.add_points(joueur_jouant.collection["p_montagne"] + p_ac)
                    continu = False
                elif carte == c3 and joueur_jouant.collection["p_mer"] < 5:
                    accomplissement = False
                    p_ac = 0
                    if joueur_jouant.collection["p_mer"] == 4:
                        accomplissement = True
                        p_ac = 3
                        for joueurs in liste_joueur:
                            if joueurs.collection["a_mer"]:
                                accomplissement = False
                                p_ac = 0
                    joueur_jouant.add_pano("mer", accomplissement)
                    joueur_jouant.add_points(joueur_jouant.collection["p_mer"] + p_ac)
                    continu = False

                del(choix_2_cartes)



        # compte nombre de joueur a la station
        self.nbr_joueur_relai = 0
        for joueur in liste_joueur:
            if joueur.position[0] == joueur_jouant.position[0] and joueur.position[1] == 0:
                self.nbr_joueur_relai += 1

        # initialisation affichage
        #joueur
        if joueur_jouant.voyageur:
            self.avatar_im = pygame.image.load(f"../Graphique/Avatar/{joueur_jouant.voyageur}.png").convert_alpha()
            self.avatar_rect = self.avatar_im.get_rect(center = POSITION_RELAI["couleur"])
        else: self.avatar_im = None
        self.text_pieces_joueurs = self.font_edos.render(str(joueur_jouant.pieces), True, COULEUR["couleur font"])
        self.text_pieces_joueurs_rect = self.text_pieces_joueurs.get_rect(center = POSITION_RELAI["pieces joueurs"])
        index = 0
        self.text_repas_joueur.clear()
        for nom_repas in joueur_jouant.collection["repas"]:
            nom_repas = nom_repas.replace("_", " ")
            text = self.font_edos_text.render(nom_repas.capitalize(), True, COULEUR["couleur font"])
            text_rect = text.get_rect(center = (POSITION_RELAI["text"][0], POSITION_RELAI["text"][1] + index * 40))
            self.text_repas_joueur.append([text, text_rect])
            index += 1
        # cartes reinitialise ssi le joueur est suele sur la nouvelle station
        if self.nbr_joueur_relai == 1:
            self.cartes.clear()
            self.bouton.empty()
            self.visible_sprite.empty()
            self.visible_sprite.add(self.confirmer)
            for i in range(len(liste_joueur)+1):
                self.cartes.append(decks_cartes["repas"].pop(0))
            for index in range(len(self.cartes)):
                Bouton_Image(POSITION_RELAI[f"carte {index + 1}"], f"../Graphique/Relai/{self.cartes[index]}.png", group = (self.bouton, self.visible_sprite), clickable = True, survolable = True, 
                             resize = SURVOLEE_SIZE_CARTE_RELAI, point_position = "center", name = self.cartes[index])

        # perso après car si prend pas continue normal mais si prend alors on s'en fiche avant ou apres
        if joueur_jouant.voyageur == "satsuki":

            c1 = decks_cartes["repas"].pop(0)
            c2 = "None"

            choix_2_cartes = Choix_2_Cartes(c1, c2, f"../Graphique/Relai/{self.cartes[index]}.png", "../Graphique/Relai/derriere_carte.png")
            carte_choisi = choix_2_cartes.run()
            if carte_choisi == c1:
                self.continuer = False
                joueur_jouant.add_points(6)
                joueur.collection["repas"].append(c1)
            elif carte_choisi == c2:
                decks_cartes["repas"].append(c1)


    def finito_pepito(self, joueur, nom_plat):

        joueur.add_points(6)
        if joueur.voyageur == "kinko":
            joueur.add_pieces(-CARTES_REPAS[nom_plat] + 1)
            joueur.collection["budget_repas"] += CARTES_REPAS[nom_plat] - 1
        else:
            joueur.add_pieces(-CARTES_REPAS[nom_plat])
            joueur.collection["budget_repas"] += CARTES_REPAS[nom_plat]
        joueur.collection["repas"].append(nom_plat)
        self.continuer = False


    def update(self, joueur):

        if self.confirmer.check_click():
            self.continuer = False

        for sprite in self.bouton:
            if sprite.check_click():
                if joueur.pieces >= CARTES_REPAS[sprite.name] and sprite.name not in joueur.collection["repas"]:
                    sprite.kill()
                    del(self.cartes[self.cartes.index(sprite.name)])
                    self.finito_pepito(joueur, sprite.name)


    def afficher(self, joueur):

        self.ecran.blit(self.fond_im, self.fond_rect)
        pygame.draw.circle(self.ecran, COULEUR[joueur.couleur], POSITION_ECHOPPE["couleur"], 110)
        if self.avatar_im: self.ecran.blit(self.avatar_im, self.avatar_rect)
        self.ecran.blit(self.baniere_im, self.baniere_rect)
        self.ecran.blit(self.text_pieces_joueurs, self.text_pieces_joueurs_rect)
        self.visible_sprite.draw(self.ecran)
        for text in self.text_repas_joueur:
            self.ecran.blit(text[0], text[1])


    def run(self, joueur, liste_joueur, decks_cartes):

        self.ecran.blit(self.transp_surface, (0, 0))

        self.initialisation_affichage(joueur, liste_joueur, decks_cartes)

        while self.continuer:

            # on gère les évenments
            for event in pygame.event.get():
        
                # si l'utilisateur clique sur echap
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.continuer = False

            # afficher
            self.update(joueur)
            self.afficher(joueur)

            pygame.display.update()

        if self.nbr_joueur_relai == len(liste_joueur):
            for carte in self.cartes:
                decks_cartes["repas"].append(carte)



class Rencontre:

    def __init__(self, joueur, decks_cartes):

        if joueur.voyageur == "yoshiyasu":
            c1 = decks_cartes["rencontres"][0]
            c2 = decks_cartes["rencontres"][1]
            if c1[:5] == "guide": c1 = "guide"
            if c2[:5] == "guide": c2 = "guide"

            choix_2_cartes = Choix_2_Cartes(c1, c2, f"../Graphique/Carte_rencontre/{c1}.png", f"../Graphique/Carte_rencontre/{c2}.png")
            carte = choix_2_cartes.run()
            if carte == c1: 
                personnage = decks_cartes["rencontres"].pop(0)
            elif carte == c2:
                personnage = decks_cartes["rencontres"].pop(1)
            del(choix_2_cartes)

        else:
            personnage = decks_cartes["rencontres"].pop(0)

        # general
        self.ecran = pygame.display.get_surface()
        self.continuer = True
        self.carte = personnage
        self.rencontre_state = "rencontre"
        self.font_edos = pygame.font.Font('../Font/edosz.ttf', FONT_SIZE_RENCONTRE)

        # groupe
        self.bouton = pygame.sprite.Group()
        self.carte_buton = pygame.sprite.Group()
        self.confirmer = Bouton_Image(POSITION_RENCONTRE["bouton confirmer"], "../Graphique/Bouttons/confirmer.png", self.bouton, True, survolable = True, image_path_survolee = "../Graphique/Bouttons/confirmer_survolee.png")
        if self.carte == "artisan":
            self.carte_souvenir = decks_cartes["souvenirs"].pop(0)
            text_remplacement = self.carte_souvenir
        elif self.carte[:5] == "guide":
            self.carte1_bouton = Bouton_Image(POSITION_RENCONTRE["pano 1"], f"../Graphique/Rencontre/pano_riziere.png", group = self.carte_buton, clickable = True, survolable = True, 
                                              resize = SURVOLEE_SIZE_CARTE_RECONTRE, point_position = "center")
            self.carte2_bouton = Bouton_Image(POSITION_RENCONTRE["pano 2"], f"../Graphique/Rencontre/pano_montagne.png", group = self.carte_buton, clickable = True, survolable = True, 
                                              resize = SURVOLEE_SIZE_CARTE_RECONTRE, point_position = "center")
            self.carte3_bouton = Bouton_Image(POSITION_RENCONTRE["pano 3"], f"../Graphique/Rencontre/pano_mer.png", group = self.carte_buton, clickable = True, survolable = True, 
                                              resize = SURVOLEE_SIZE_CARTE_RECONTRE, point_position = "center")
            if self.carte == "guide_riz":
                text_remplacement = "rizière"
            if self.carte == "guide_montagne":
                text_remplacement = "montagne"
            if self.carte == "guide_mer":
                text_remplacement = "mer"

        # affichage
        self.fond_im = pygame.image.load("../Graphique/Rencontre/fond.png").convert_alpha()
        self.fond_rect = self.fond_im.get_rect(topleft = POSITION_RENCONTRE["fond"])
        if self.carte[:5] == "guide": carte = "guide"
        else: carte = self.carte
        self.personnage_im = pygame.image.load(f"../Graphique/Rencontre/{carte}.png").convert_alpha()
        self.personnage_rect = self.personnage_im.get_rect(bottomright = POSITION_RENCONTRE["personnage"])

        self.text = []
        if "_" in personnage: personnage = personnage.split("_")[0]
        # permet de centrer le text au milieu
        position = list(POSITION_RENCONTRE["text"])
        position[1] -= len(TEXT_RENCONTRE[personnage])/2 * TEXT_DECALAGE_RENCONTRE
        i = 0
        for ligne in TEXT_RENCONTRE[personnage]:
            if "__replace__" in ligne:
                ligne_aff = ligne.replace("__replace__", text_remplacement)
            else: ligne_aff = ligne
            text_im = self.font_edos.render(ligne_aff, True, COULEUR["couleur font"])
            text_rect = text_im.get_rect(center = position)
            text_rect.y += TEXT_DECALAGE_RENCONTRE * i
            self.text.append([text_im, text_rect])
            i += 1

        # transparent background
        self.transp_surface = pygame.Surface((1920,1080), pygame.SRCALPHA)
        self.transp_surface.fill((251, 253, 248, 150))


    def update(self, joueur, liste_joueur):

        if self.confirmer.check_click():

            self.continuer = False

            if joueur.voyageur == "umegae":
                joueur.add_points(1)
                joueur.add_pieces(1)

            if self.carte == "artisan":
                joueur.add_pieces(CARTES_SOUVENIRS[self.carte_souvenir][1])
                joueur.add_echoppe(CARTES_SOUVENIRS[self.carte_souvenir][0], CARTES_SOUVENIRS[self.carte_souvenir][1])

            elif self.carte[:5] == "guide":
                if self.carte == "guide_riz" and joueur.collection["p_riziere"] < 3:
                    accomplissement = False
                    p_ac = 0
                    if joueur.collection["p_riziere"] == 2:
                        accomplissement = True
                        p_ac = 3
                        for joueurs in liste_joueur:
                            if joueurs.collection["a_riziere"]:
                                accomplissement = False
                                p_ac = 0
                    joueur.add_pano("riziere", accomplissement)
                    joueur.add_points(joueur.collection["p_riziere"] + p_ac)
                    if joueur.voyageur == "mitsukuni" and joueur.collection["a_riziere"]:
                        joueur.add_points(1)
                elif self.carte == "guide_montagne" and joueur.collection["p_montagne"] < 4:
                    accomplissement = False
                    p_ac = 0
                    if joueur.collection["p_montagne"] == 3:
                        accomplissement = True
                        p_ac = 3
                        for joueurs in liste_joueur:
                            if joueurs.collection["a_montagne"]:
                                accomplissement = False
                                p_ac = 0
                    joueur.add_pano("montagne", accomplissement)
                    joueur.add_points(joueur.collection["p_montagne"] + p_ac)
                    if joueur.voyageur == "mitsukuni" and joueur.collection["a_montagne"]:
                        joueur.add_points(1)
                elif self.carte == "guide_mer" and joueur.collection["p_mer"] < 5:
                    accomplissement = False
                    p_ac = 0
                    if joueur.collection["p_mer"] == 4:
                        accomplissement = True
                        p_ac = 3
                        for joueurs in liste_joueur:
                            if joueurs.collection["a_mer"]:
                                accomplissement = False
                                p_ac = 0
                    joueur.add_pano("mer", accomplissement)
                    joueur.add_points(joueur.collection["p_mer"] + p_ac)
                    if joueur.voyageur == "mitsukuni" and joueur.collection["a_mer"]:
                        joueur.add_points(1)
                else:
                    self.continuer = True
                    self.rencontre_state = "choix pano"

            elif self.carte == "samourai":
                joueur.add_points(3)

            elif self.carte == "noble":
                joueur.add_pieces(3)

            elif self.carte == "pretre":
                joueur.add_temple(1)
                joueur.add_points(1)

            joueur.collection["n_rencontre"] += 1


    def afficher(self):

        self.ecran.blit(self.fond_im, self.fond_rect)
        self.ecran.blit(self.personnage_im, self.personnage_rect)
        for ligne in self.text: self.ecran.blit(ligne[0], ligne[1])
        self.bouton.draw(self.ecran)


    def run(self, joueur, liste_joueur):

        self.ecran.blit(self.transp_surface, (0, 0))

        while self.continuer:

            # on gère les évenments
            for event in pygame.event.get():
        
                # si l'utilisateur clique sur echap
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.continuer = False

            if self.rencontre_state == "rencontre":

                # afficher
                self.afficher()
                self.update(joueur, liste_joueur)

            if self.rencontre_state == "choix pano":

                # affichage
                self.ecran.fill(COULEUR["beige"])
                self.carte_buton.draw(self.ecran)

                #gere si clique
                if self.carte1_bouton.check_click() and joueur.collection["p_riziere"] < 3:

                    accomplissement = False
                    p_ac = 0
                    if joueur.collection["p_riziere"] == 2:
                        accomplissement = True
                        p_ac = 3
                        for joueurs in liste_joueur:
                            if joueurs.collection["a_riziere"]:
                                accomplissement = False
                                p_ac = 0
                    joueur.add_pano("riziere", accomplissement)
                    joueur.add_points(joueur.collection["p_riziere"] + p_ac)
                    if joueur.voyageur == "mitsukuni" and joueur.collection["a_riziere"]:
                        joueur.add_points(1)

                    self.continuer = False

                if self.carte2_bouton.check_click() and joueur.collection["p_montagne"] < 4:

                    accomplissement = False
                    p_ac = 0
                    if joueur.collection["p_montagne"] == 3:
                        accomplissement = True
                        p_ac = 3
                        for joueurs in liste_joueur:
                            if joueurs.collection["a_montagne"]:
                                accomplissement = False
                                p_ac = 3
                    joueur.add_pano("montagne", accomplissement)
                    joueur.add_points(joueur.collection["p_montagne"] + p_ac)
                    if joueur.voyageur == "mitsukuni" and joueur.collection["a_montagne"]:
                        joueur.add_points(1)

                    self.continuer = False

                if self.carte3_bouton.check_click() and joueur.collection["p_mer"] < 5:

                    accomplissement = False
                    p_ac = 0
                    if joueur.collection["p_mer"] == 4:
                        accomplissement = True
                        p_ac = 3
                        for joueurs in liste_joueur:
                            if joueurs.collection["a_mer"]:
                                accomplissement = False
                                p_ac =0
                    joueur.add_pano("mer", accomplissement)
                    joueur.add_points(joueur.collection["p_mer"] + p_ac)
                    if joueur.voyageur == "mitsukuni" and joueur.collection["a_mer"]:
                        joueur.add_points(1)

                    self.continuer = False

            pygame.display.update()