# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 20:13:14 2023

@author: Jules JOUVIN; Martin PICHON
"""

import pygame, sys
from parametre_general import *
from jeu import Jeu
from creation_jeu import Creation_jeu
import Button
import login
from time import sleep
from debug import debug
import pickle




class Arrow:

    def __init__(self):
        
        self.ecran = ecran
        self.order = 1
        self.bouton = pygame.sprite.Group()
        self.fleche_up = Button.Bouton_Image((1433, 865), "../Graphique/Temple/fleche_up.png", self.bouton, True, survolable = True, image_path_survolee = "../Graphique/Temple/fleche_up_survolee.png")
        self.fleche_down = Button.Bouton_Image((1433, 921), "../Graphique/Temple/fleche_down.png", self.bouton, True, survolable = True, image_path_survolee = "../Graphique/Temple/fleche_down_survolee.png")
        self.page = pygame.image.load(f"../Regles/page{self.order}.png").convert()

        self.rule_rect = self.page.get_rect(center = POSITION_REGLES)

    def update(self):

        if self.fleche_up.check_click():
            if self.order > 1:
                self.order -= 1
                self.page = pygame.image.load(f"../Regles/page{self.order}.png").convert()

        if self.fleche_down.check_click():
            if self.order < 8:
                self.order += 1
                self.page = pygame.image.load(f"../Regles/page{self.order}.png").convert()

        

    def afficher(self):

        self.ecran.blit(self.page, self.rule_rect)

        self.bouton.draw(self.ecran)

        


    def run(self):

        self.afficher()
        self.update()



# fonction affichant le menu
def display_menu():
    
    global game_state
    global stat_state

    if bouton_menu_jouer.click():
        game_state = "creation jeu"
    if bouton_menu_continuer.click():
        None
    if bouton_menu_stat.click():
        game_state = "stat"
        stat_state = False
        pygame.display.update()
    if bouton_menu_rules.click():
        game_state = "rules"
    if bouton_menu_about.click():
        None
    if bouton_menu_exit.click():
        pygame.quit()
        sys.exit()

    # affichage
    ecran.blit(illustration, POSITION_MENU["illustration"])
    ecran.blit(logo, POSITION_MENU["logo"])
    bouton_menu_jouer.draw()
    bouton_menu_continuer.draw()
    bouton_menu_stat.draw()
    bouton_menu_rules.draw()
    bouton_menu_about.draw()
    bouton_menu_exit.draw()
    
    pygame.display.update()

def display_rules():

    global game_state

    fleche_regles.run()

    if close2.click():
        game_state = "menu"

    close2.draw()

    pygame.display.update()



def print_stat(pseudo):

    global game_state

    font = pygame.font.Font("../Font/edosz.ttf", 50)

    stat_file = open(f"../Data/Player/{pseudo}", "rb")
    stat_list = pickle.load(stat_file)
    stat_file.close()
    victoire = stat_list[0]
    defaite = stat_list[1]

    wood_surf = pygame.image.load("../Graphique/Wood_Assets/large_wood_plank.png")
    wood_surf_resize = pygame.transform.scale(wood_surf, (1100, 630))
    wood_rect = wood_surf_resize.get_rect(center = (960, 540))

    text_surf_win = font.render("Nombre de victoires de "+pseudo+" : "+str(victoire), True, 'Black')
    text_rect_win = text_surf_win.get_rect(midleft = (550, 500))

    text_surf_loose = font.render("Nombre de défaites : "+str(defaite), True, 'Black')
    text_rect_loose = text_surf_loose.get_rect(midleft = (550, 580))
    
    ecran.blit(wood_surf_resize, wood_rect)
    ecran.blit(text_surf_win, text_rect_win)
    ecran.blit(text_surf_loose, text_rect_loose)
    close1.draw()

    if close1.click():
        game_state = "menu"
    
    pygame.display.update()
    
    


# paramètres général
pygame.init()
ecran = pygame.display.set_mode((LONGUEUR,LARGEUR))
pygame.display.set_caption("Tokaido")
icon = pygame.image.load("../Graphique/icon.png").convert_alpha()
pygame.display.set_icon(icon)

# création des viariables
clock = pygame.time.Clock()
game_active = False
game_state = "menu"
liste_pseudo_joueur = []

# création instances
jeu = Jeu()
creation_jeu = Creation_jeu()
fleche_regles = Arrow()
bouton_menu_jouer = Button.Text_Button(BOUTONS_MENU_X, BOUTON_JOUER_Y, ecran, '- Jouer', 60)
bouton_menu_continuer = Button.Text_Button(BOUTONS_MENU_X, BOUTON_CONTINUER_Y, ecran, '- Continuer', 60)
bouton_menu_stat = Button.Text_Button(BOUTONS_MENU_X, BOUTON_STAT_Y, ecran, '- Carrière', 60)
bouton_menu_rules = Button.Text_Button(BOUTONS_MENU_X, BOUTON_RULES_Y, ecran, '- Règles', 60)
bouton_menu_about = Button.Text_Button(BOUTONS_MENU_X, BOUTON_ABOUT_Y, ecran, '- A propos', 60)
bouton_menu_exit = Button.Text_Button(BOUTONS_MENU_X, BOUTON_EXIT_Y, ecran, '- Quitter', 60)
close1 = Button.Close_Button(1400, 340, ecran)
close2 = Button.Close_Button(1920, 0, ecran)

# création de ce qui va être affichés sur le menu
ecran.fill(COULEUR["beige"])
illustration = pygame.image.load("../Graphique/Menu/illustration.png").convert()
logo = pygame.image.load("../Graphique/Menu/logo.png").convert()


while 1:
    
    # on gère les évenments
    for event in pygame.event.get():
        
        # si l'utilisateur clique sur fermer on ferme la fenetre
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # si l'utilisateur clique sur echap
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            
    # gérer les différents game state
    if not game_active:
        if game_state == "menu":
            ecran.fill(COULEUR["beige"])
            display_menu()

        if game_state == "creation jeu" :
            lancer_jeu = creation_jeu.run(jeu)
            if lancer_jeu:
                game_active = True
                game_state = "jeu"

        if game_state == "stat":
            if not stat_state:
                
                pseudo = login.login()
                stat_state = True
            print_stat(pseudo)

        if game_state == "rules":
            display_rules()
            

    if game_active:
        if game_state == "jeu":
            jeu.run()
            if jeu.end_game:
                del(jeu)
                jeu = Jeu()
                del(creation_jeu)
                creation_jeu = Creation_jeu()
                game_active = False
                game_state = "menu"
                ecran.fill(COULEUR["beige"])
        
    # bloquer les fps a 60
    clock.tick(60)
