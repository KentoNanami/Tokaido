# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 15:15:55 2023

@author: 36796932
"""

import pygame
from random import shuffle
from ui import UI
from parametre_general import *
from debug import debug
from station import Station, Relai
from Button import Bouton_Image
import pickle



class Jeu:
    
    def __init__(self):
        
        # general
        self.ecran = pygame.display.get_surface()
        
        self.liste_joueur = []
        self.index_joueur_jouant = 0
        self.stations_jouable = []
        self.UI_joueurs = []
        
        self.deroulement_partie_state = "debut de partie"
        self.end_game = False

        self.relai = Relai()      # seule station ou les joueurs influences sur d'autres:: evite de faire 100 return

        # deck de carte
        cartes_sources_chaudes = [2] * 8 + [3] * 4
        shuffle(cartes_sources_chaudes)
        cartes_rencontres = ["artisan"] * 2 + ["guide_riz"] * 2 + ["guide_montagne"] * 2 + ["guide_mer"] * 2 + ["samourai"] * 2 + ["noble"] * 2 + ["pretre"] * 2
        shuffle(cartes_rencontres)
        cartes_souvenirs = []
        for carte in CARTES_SOUVENIRS.keys():
            cartes_souvenirs.append(carte)
        shuffle(cartes_souvenirs)
        cartes_repas = []
        for carte in CARTES_REPAS.keys():
            if CARTES_REPAS[carte] == 3:
                cartes_repas.append(carte)
            if CARTES_REPAS[carte] <= 2:
                cartes_repas.append(carte)
            if CARTES_REPAS[carte] <= 1:
                cartes_repas.append(carte)
        shuffle(cartes_repas)
        self.decks_cartes = {"sources_chaudes": cartes_sources_chaudes, "rencontres": cartes_rencontres, "souvenirs": cartes_souvenirs, "repas": cartes_repas}
        self.choix_repas = []
        
        # mise en place du jeu
        self.plateau = []
        self.creer_plateau()
        
        # création groupe groupe
        self.sprite_visible = YScrollGroup()
        self.bouttons_stations = pygame.sprite.Group()
        
        
    # crétion du plateau
    def creer_plateau(self):
        
        # creer une boucle qui va prendre chaque element du plateau predefini et creer une instance classe
        j = 0
        s = 0
        for jour in PLATEAU:
            stations_par_jour = []
            for infos_station in jour:
                stations_par_jour.append(Station(infos_station[0], infos_station[1], (j, s), infos_station[2], infos_station[3]))
                s += 1
            s = 0
            j += 1
            self.plateau.append(stations_par_jour)


    # methode qui intialise le jeu
    def init_jeu(self):

        # affiche UI
        for joueur in self.liste_joueur:
            self.UI_joueurs.append(UI(joueur))
     
        
    # méthode qui va trouver a qui c'est le tour de jouer
    def tour_du_joueur(self):
        
        index_joueur_plus_loin = 0
        index = 1
        for joueur in self.liste_joueur[1:]:
            if joueur.position[0] < self.liste_joueur[index_joueur_plus_loin].position[0]:
                index_joueur_plus_loin = index
            elif joueur.position[0] == self.liste_joueur[index_joueur_plus_loin].position[0]:
                if joueur.position[1] < self.liste_joueur[index_joueur_plus_loin].position[1]:
                    index_joueur_plus_loin = index
                elif joueur.position[1] == self.liste_joueur[index_joueur_plus_loin].position[1]:
                    if joueur.position[2] > self.liste_joueur[index_joueur_plus_loin].position[2]:
                        index_joueur_plus_loin = index
            index += 1
        
        self.index_joueur_jouant = index_joueur_plus_loin
            
            
    # méthode trouvant toute les stations ou le joueur peut jouer
    def stations_jouable_finder(self):
        
        joueur_jouant = self.liste_joueur[self.index_joueur_jouant]
        index_stations_jouable = []
        
        # liste des stations le meme jour ou se trouve le joueur dans la meme journée (sauf relais)
        for station in self.plateau[joueur_jouant.position[0]]:
            # regarde les stations apres le joueur
            if station.position[1] > joueur_jouant.position[1]:
                # en fonction de la station regarde si le joueur a plus d'une piece
                if not (station.type == "temple" or station.type == "echoppe") or joueur_jouant.pieces >= 1:
                    # si c'est un pano on regarde si le joueur a complete le pano
                    if not (station.type == "pano riziere" and joueur_jouant.collection["p_riziere"] == 3):
                        if not (station.type == "pano montagne" and joueur_jouant.collection["p_montagne"] == 4):
                            if not (station.type == "pano mer" and joueur_jouant.collection["p_mer"] == 5):
                                # si c'est une station double ajoute 2 fois
                                if station.station_double and len(self.liste_joueur) > 2:
                                    index_stations_jouable.append(station.position[1])
                                    index_stations_jouable.append(station.position[1])
                                else: index_stations_jouable.append(station.position[1])
                
        # enleve les stations prisent par les autres joueur
        for joueur in self.liste_joueur:
            if joueur.position[1] in index_stations_jouable:
                del index_stations_jouable[index_stations_jouable.index(joueur.position[1])]
        
        # enleve les doublons
        index_stations_jouable = list(set(index_stations_jouable))
        index_stations_jouable.sort()
        
        self.stations_jouable.clear()
        for index_stations in index_stations_jouable:
            self.stations_jouable.append(self.plateau[joueur_jouant.position[0]][index_stations])
        self.stations_jouable.append(self.plateau[joueur_jouant.position[0] + 1][0])
    

    # méthode qui va update les stations affiché
    def update_stations_affichage(self):

        # supprime les sprites deja present pour les remplacer
        for sprite in self.sprite_visible:
            if isinstance(sprite, Station):
                sprite.kill()
        self.bouttons_stations.empty()

        positions_joueur = []
        position_station = 1

        # recupere positions des joueurs
        for joueur in self.liste_joueur:
            positions_joueur.append(joueur.position)

        # va afficher les sprites avec ou pas un decalage
        for sprite in self.stations_jouable:

            position_station = 1
            joueur_jouant = self.liste_joueur[self.index_joueur_jouant]

            # gere le decalage pour une station relais
            if sprite.type == "relais":
                for position in positions_joueur:
                    if (position[0], position[1]) == (joueur_jouant.position[0] + 1, 0):
                        position_station += 1

                if sprite.direction == -1: decalage = sprite.decalage + 47
                else: decalage = sprite.decalage

                if position_station == 1:
                    coordonee = (sprite.coordonee[0] + sprite.direction * 16 + decalage, sprite.coordonee[1] + 23)
                else:
                    coordonee = (sprite.coordonee[0] + sprite.direction * 16 + decalage + sprite.direction * (position_station - 1) * 68, sprite.coordonee[1] + 23)
                station_ajoute = Station(sprite.type, sprite.station_double, sprite.position, coordonee, decalage)
                self.sprite_visible.add(station_ajoute)
                self.bouttons_stations.add(station_ajoute)

            # gere le decalage pour les autre types de stations
            else:
                position_station = 0
                for position in positions_joueur:
                    if (position[0], position[1]) == sprite.position:
                        position_station += 1

                coordonee = (sprite.coordonee[0] + 23 + sprite.decalage * position_station, sprite.coordonee[1] + 23)
                station_ajoute = Station(sprite.type, sprite.station_double, sprite.position, coordonee, sprite.decalage)
                self.sprite_visible.add(station_ajoute)
                self.bouttons_stations.add(station_ajoute)


    # methode qui va regarder si une des stations est clickée
    def check_click(self):

        mouse_pos = pygame.mouse.get_pos()

        for sprite in self.bouttons_stations:
            if sprite.rect.collidepoint(mouse_pos):
                sprite.survolee()
                if pygame.mouse.get_pressed()[0]:
                    sprite.pressed = True
                else:
                    if sprite.pressed == True:
                        sprite.pressed = False
                        sprite.clicked(self.liste_joueur, self.liste_joueur[self.index_joueur_jouant], self.UI_joueurs[self.index_joueur_jouant], self.decks_cartes, self.relai)
                        self.deroulement_partie_state = "qui joue"
            else:
                self.pressed = False
                sprite.idle()


    # methode qui va assigner les accomplissemnts aux différents joueurs
    def accomplissement(self):

        gourmet = []
        baigneur = []
        bavard = []
        collectionneur = []
        temple = []
        max_gourmet = 0
        max_baigneur = 0
        max_bavard = 0
        max_collectionneur = 0

        for joueur in self.liste_joueur:

            if joueur.collection["budget_repas"] > max_gourmet: 
                gourmet = [joueur]
                max_gourmet = joueur.collection["budget_repas"]
            elif joueur.collection["budget_repas"] == max_gourmet: gourmet.append(joueur)

            if joueur.collection["n_source_chaude"] > max_baigneur: 
                baigneur = [joueur]
                max_baigneur = joueur.collection["n_source_chaude"]
            elif joueur.collection["n_source_chaude"] == max_baigneur: baigneur.append(joueur)

            if joueur.collection["n_rencontre"] > max_bavard: 
                bavard = [joueur]
                max_bavard = joueur.collection["n_rencontre"]
            elif joueur.collection["n_rencontre"] == max_bavard: bavard.append(joueur)

            n_souvenir = joueur.collection["echoppe"]["petit souvenir"] + joueur.collection["echoppe"]["nouriture"] + joueur.collection["echoppe"]["gros souvenir"] + joueur.collection["echoppe"]["vetement"]

            if n_souvenir > max_collectionneur: 
                collectionneur = [joueur]
                max_collectionneur = n_souvenir
            elif n_souvenir == max_collectionneur: collectionneur.append(joueur)

        liste_temple = list(range(len(self.liste_joueur)))

        n = len(liste_temple)
        inverse = False

        for i in range(n-1):

            for j in range(0, n-i-1):
                if self.liste_joueur[liste_temple[j]].collection["temple"] < self.liste_joueur[liste_temple[j + 1]].collection["temple"]:
                    inverse = True
                    liste_temple[j], liste_temple[j + 1] = liste_temple[j + 1], liste_temple[j]
             
            if not inverse:
                break

        for joueur in gourmet:
            joueur.add_points(3)
            if joueur.voyageur == "mitsukuni":
                joueur.add_points(1)
            joueur.collection["a_gourmet"] = True
        for joueur in baigneur:
            joueur.add_points(3)
            if joueur.voyageur == "mitsukuni":
                joueur.add_points(1)
            joueur.collection["a_baigneur"] = True
        for joueur in bavard:
            joueur.add_points(3)
            if joueur.voyageur == "mitsukuni":
                joueur.add_points(1)
            joueur.collection["a_bavard"] = True
        for joueur in collectionneur:
            joueur.add_points(3)
            if joueur.voyageur == "mitsukuni":
                joueur.add_points(1)
            joueur.collection["a_collectionneur"] = True

        self.liste_joueur[liste_temple[0]].add_points(10)
        self.liste_joueur[liste_temple[0]].collection["points_temple"] = 10
        pts_gagne = 10
        for index in range(1, len(liste_temple)):
            if self.liste_joueur[liste_temple[index]].collection["temple"] == self.liste_joueur[liste_temple[index - 1]].collection["temple"]:
                self.liste_joueur[liste_temple[index]].add_points(pts_gagne)
            else:
                if pts_gagne >= 7:
                    pts_gagne += -3
                else: 
                    pts_gagne = 2
                if self.liste_joueur[liste_temple[index]].collection["temple"] == 0:
                    pts_gagne = 0
                self.liste_joueur[liste_temple[index]].add_points(pts_gagne)
                self.liste_joueur[liste_temple[index]].collection["points_temple"] = pts_gagne
    

    # méthode qui va afficher le jeu
    def run(self):
        
        #gere le state du jeu
        if self.deroulement_partie_state == "debut de partie":
            # choix des cartes
            # initialisation de la partie
            self.init_jeu()
            self.deroulement_partie_state = "qui joue"

        elif self.deroulement_partie_state == "qui joue":
            n_perso_derniere_station = 0
            for joueur in self.liste_joueur:
                if joueur.position[0] == 4: 
                    n_perso_derniere_station += 1
            if n_perso_derniere_station == len(self.liste_joueur): self.deroulement_partie_state = "fin du jeu"
            else:
                self.tour_du_joueur()
                self.deroulement_partie_state = "stations jouable"

        elif self.deroulement_partie_state == "stations jouable":
            self.stations_jouable_finder()
            self.update_stations_affichage()
            self.deroulement_partie_state = "choix stations"

        elif self.deroulement_partie_state == "choix stations":
            self.check_click()

        elif self.deroulement_partie_state == "fin du jeu":
            self.accomplissement()
            fin_partie = Affichage_Fin(self.liste_joueur)
            self.end_game = fin_partie.run(self.liste_joueur)

        # update l'affichage
        self.sprite_visible.custom_draw()

        for ui in self.UI_joueurs:
            ui.afficher()

        pygame.display.update()
        


class YScrollGroup(pygame.sprite.Group):
    
    
    def __init__(self):
        
        # general 
        super().__init__()
        self.ecran = pygame.display.get_surface()
        self.mouse_speed = [0, 0]
        self.decalage_y = - 3530 + LARGEUR
        
        # l'image de fond
        self.carte_im = pygame.image.load("../Graphique/Jeu/carte.png").convert()
        self.carte_rect = self.carte_im.get_rect(topleft = (0,0))
        
        
    # methode gerant la methode d'affichage pourvant
    def custom_draw(self):

        self.mouse_speed = pygame.mouse.get_rel()

        # deplace le fond en fonction de la vitesse de la sourie
        if pygame.mouse.get_pressed()[2]: self.decalage_y += self.mouse_speed[1]

        # gere quand l'ecran est en dehors /!\ avec la vitesse peut deplacer doit le remettre a un endroit
        if self.decalage_y > 0: self.decalage_y = 0
        if self.decalage_y < - 3530 + LARGEUR: self.decalage_y = - 3530 + LARGEUR

        # decale la carte
        self.carte_rect.y = self.decalage_y
        
        # affiche la carte
        self.ecran.blit(self.carte_im, self.carte_rect)
                                                                                
        # affiche tout les sprites de la meme maniere
        for sprite in self.sprites():
            sprite.rect.y = sprite.coordonee[1] + self.decalage_y
            self.ecran.blit(sprite.image, sprite.rect)



class Affichage_Fin:

    def __init__(self, liste_joueur):

        # general
        self.ecran = pygame.display.get_surface()
        self.continuer = True

        # affichage
        self.font_edos = pygame.font.Font('../Font/edosz.ttf', FONT_SIZE_FIN)
        self.fond_im = pygame.image.load("../Graphique/Fin/panneau.png").convert_alpha()
        self.fond_rect = self.fond_im.get_rect(topleft = POSITION_FIN_JEU["fond"])
        self.bouton = pygame.sprite.Group()
        self.confirmer = Bouton_Image(POSITION_FIN_JEU["bouton confirmer"], "../Graphique/Bouttons/annuler.png", group = self.bouton, clickable = True, survolable = True, 
                                      image_path_survolee = "../Graphique/Bouttons/annuler_survolee.png")

        self.liste_joueur_affichage = []
        index = 0
        for joueur in liste_joueur:
            a_baigneur = 0
            a_bavard = 0
            a_collectionneur = 0
            a_panorama = 0

            if joueur.voyageur:
                avatar_im = pygame.image.load(f"../Graphique/Avatar/{joueur.voyageur}.png").convert_alpha()
                avatar_rect = avatar_im.get_rect(center = POSITION_FIN_JEU["couleur"])
                avatar_rect.y += index * 100
                self.liste_joueur_affichage.append([avatar_im, avatar_rect])

            t_total_points = self.font_edos.render(str(joueur.points), True, COULEUR["couleur font"])
            t_total_points_rect = t_total_points.get_rect(center = POSITION_FIN_JEU["points totals"])
            t_total_points_rect.y += index * 100
            self.liste_joueur_affichage.append([t_total_points, t_total_points_rect])

            if joueur.collection["a_baigneur"]: a_baigneur = 3
            t_baigneur = self.font_edos.render(str(a_baigneur), True, COULEUR["couleur font"])
            t_baigneur_rect = t_baigneur.get_rect(center = POSITION_FIN_JEU["baigneur"])
            t_baigneur_rect.y += index * 100
            self.liste_joueur_affichage.append([t_baigneur, t_baigneur_rect])

            if joueur.collection["a_bavard"]: a_bavard = 3
            t_bavard = self.font_edos.render(str(a_bavard), True, COULEUR["couleur font"])
            t_bavard_rect = t_bavard.get_rect(center = POSITION_FIN_JEU["bavard"])
            t_bavard_rect.y += index * 100
            self.liste_joueur_affichage.append([t_bavard, t_bavard_rect])

            if joueur.collection["a_collectionneur"]: a_collectionneur = 3
            t_collectionneur = self.font_edos.render(str(a_collectionneur), True, COULEUR["couleur font"])
            t_collectionneur_rect = t_collectionneur.get_rect(center = POSITION_FIN_JEU["collectionneur"])
            t_collectionneur_rect.y += index * 100
            self.liste_joueur_affichage.append([t_collectionneur, t_collectionneur_rect])

            if joueur.collection["a_riziere"]: a_panorama += 3
            if joueur.collection["a_montagne"]: a_panorama += 3
            if joueur.collection["a_mer"]: a_panorama += 3
            t_panorama = self.font_edos.render(str(a_panorama), True, COULEUR["couleur font"])
            t_panorama_rect = t_panorama.get_rect(center = POSITION_FIN_JEU["accomplissement pano"])
            t_panorama_rect.y += index * 100
            self.liste_joueur_affichage.append([t_panorama, t_panorama_rect])

            t_temple = self.font_edos.render(str(joueur.collection["points_temple"]), True, COULEUR["couleur font"])
            t_temple_rect = t_temple.get_rect(center = POSITION_FIN_JEU["temple"])
            t_temple_rect.y += index * 100
            self.liste_joueur_affichage.append([t_temple, t_temple_rect])

            index += 1

        # transparent background
            self.transp_surface = pygame.Surface((1920,1080), pygame.SRCALPHA)
            self.transp_surface.fill((251, 253, 248, 150))


    def update(self, liste_joueur):

        if self.confirmer.check_click():
            self.continuer = False

            gagnant = []
            max_point = 0
            for joueur in liste_joueur:
                if joueur.points > max_point: 
                    gagnant = [joueur]
                    max_point = joueur.points
                elif joueur.points == max_point: gagnant.append(joueur)

            for e in gagnant:
                if e.pseudo not in ROBOT_NAME:

                    combo_file = open(f"../Data/Player/{e.pseudo}", "rb")
                    stats_list = pickle.load(combo_file) # 1=victoire 2=défaite 3=temps de jeu(optionnel)
                    combo_file.close()

                    stats_list[0] += 1

                    combo_file = open(f"../Data/Player/{e.pseudo}", "wb")
                    stats_list = pickle.dump(stats_list, combo_file) # 1=victoire 2=défaite 3=temps de jeu(optionnel)
                    combo_file.close()

            for joueur in liste_joueur:

                if joueur not in gagnant:
                    if joueur.pseudo not in ROBOT_NAME:

                        combo_file = open(f"../Data/Player/{joueur.pseudo}", "rb")
                        stats_list = pickle.load(combo_file) # 1=victoire 2=défaite 3=temps de jeu(optionnel)
                        combo_file.close()

                        stats_list[1] += 1

                        combo_file = open(f"../Data/Player/{joueur.pseudo}", "wb")
                        stats_list = pickle.dump(stats_list, combo_file) # 1=victoire 2=défaite 3=temps de jeu(optionnel)
                        combo_file.close()


    def afficher(self, liste_joueur):

        self.ecran.blit(self.fond_im, self.fond_rect)
        for i in range(len(liste_joueur)):
            pygame.draw.circle(self.ecran, COULEUR[liste_joueur[i].couleur], (POSITION_FIN_JEU["couleur"][0], POSITION_FIN_JEU["couleur"][1] + i*100), 40)
        for sprite in self.liste_joueur_affichage:
            self.ecran.blit(sprite[0], sprite[1])
        self.bouton.draw(self.ecran)


    def run(self, liste_joueur):

        self.ecran.blit(self.transp_surface, (0, 0))

        while self.continuer:

            # on gère les évenments
            for event in pygame.event.get():
        
                # si l'utilisateur clique sur echap
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.continuer = False

            # afficher
            self.afficher(liste_joueur)
            self.update(liste_joueur)

            pygame.display.update()

        return True