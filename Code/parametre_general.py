# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 14:14:41 2023

@author: 36796932
"""


# parametre ecran
LONGUEUR = 1920
LARGEUR = 1080

LONGUEUR_MID = 960
LARGEUR_MID = 540

POSITION_REGLES = (LONGUEUR_MID, LARGEUR_MID)
# les différentes sations
PLATEAU = [
            [["relais", False, (1313, 3397), 1], ["echoppe", True, (1322, 3312), -1], ["temple", False, (1324, 3257), 0], ["rencontre", False, (1298, 3194), 0], 
             ["pano riziere", False, (1309, 3127), 0], ["source chaude", True, (1350, 3057), -1], ["pano montagne", True, (1382, 2994), 1],
             ["ferme", True, (1427, 2934), -1], ["echoppe", False, (1482, 2882), 0], ["temple", True, (1486, 2811), -1], ["rencontre", False, (1448, 2742), 0], 
             ["pano mer", True, (1407, 2689), -1], ["pano montagne", False, (1327, 2619), 0], ["source chaude", False, (1271, 2590), 0]],
            
            [["relais", False, (1255, 2507), 1], ["pano mer", False, (1313, 2425), 0], ["temple", False, (1347, 2379), 0], ["ferme", True, (1399, 2334), 1],
             ["pano riziere", True, (1436, 2286), -1], ["pano montagne", True, (1486, 2237), 1], ["rencontre", True , (1546, 2179), -1], ["temple", False, (1595, 2141), 0], 
             ["source chaude", True, (1675, 2093), -1], ["pano montagne", False, (1702, 2044), 0], ["pano mer", True, (1699, 1991), -1], ["echoppe", False, (1705, 1933), 0],
             ["ferme", False, (1696, 1881), 0]],

            [["relais", False, (1668, 1790), -1], ["pano riziere", False, (1673, 1708), 0], ["echoppe", False, (1666, 1658), 0], ["rencontre", True, (1670, 1607), 1], 
             ["ferme", False, (1653, 1549), 0], ["pano montagne", True, (1650, 1494), 1], ["source chaude", False, (1628, 1445), 0], ["pano mer", True, (1579, 1378), 1], 
             ["pano riziere", False, (1549, 1331), 0], ["temple", True, (1535, 1277), 1], ["ferme", True, (1510, 1231), -1], ["rencontre", False, (1470, 1178), 0], 
             ["pano mer", False, (1425, 1132), 0], ["echoppe", True, (1421, 1079), 1]],

            [["relais", False, (1399, 996), -1], ["source chaude", False, (1394, 913), 0], ["temple", True, (1384, 862), 1], ["rencontre", False, (1356, 813), 0], 
             ["echoppe", True, (1332, 759), 1], ["pano mer", False, (1302, 714), 0], ["ferme", True, (1281, 659), 1], ["source chaude", True, (1250, 598), -1], 
             ["rencontre", False, (1252, 539), 0], ["pano montagne", False, (1246, 482), 0], ["pano riziere", True, (1264, 421), 1], ["pano mer", True, (1264, 352), -1], 
             ["echoppe", False, (1210, 277), 0]],
            
            [["relais", False, (1119, 170), 1]]
          ]

# cartes et leur prix et/ou type
CARTES_SOUVENIRS = {
                    "koma": ["petit souvenir", 1], "gofu": ["petit souvenir", 1], "washi": ["petit souvenir", 1], "hashi": ["petit souvenir", 1], "uchiwa": ["petit souvenir", 1], 
                    "yunomi": ["petit souvenir", 1],

                    "ocha": ["nouriture", 2], "sake": ["nouriture", 2], "konpeito": ["nouriture", 1], "kamaboko": ["nouriture", 1], "daifuku": ["nouriture", 2], "manju": ["nouriture", 1],

                    "netsuke": ["gros souvenir", 2], "shamisen": ["gros souvenir", 3], "jubako": ["gros souvenir", 2], "sumie": ["gros souvenir", 3], "shikki": ["gros souvenir", 2],
                    "ukiyoe": ["gros souvenir", 3],

                    "kan_zashi": ["vetement", 2], "sandogasa": ["vetement", 2], "geta": ["vetement", 2], "haori": ["vetement", 2], "yukata": ["vetement", 2], "furoshiki": ["vetement", 2]
                   }
CARTES_REPAS = {
                "tai_meshi": 3, "udon": 3, "unagi": 3, "tempura": 2, "soba": 2, "misoshiru": 1, "tofu": 2, "sushi": 2, "dango": 1, "donburi": 3, "fugu": 3, "sashimi": 3,
                "yakitori": 2, "nigirimeshi": 1
                }
CARTES_PERSONNAGES = {
                      "chuubei": 4, "hiroshige": 3, "hirotada": 8, "kinko": 7, "mitsukuni": 6, "sasayakko": 6, "satsuki": 2, "umegae": 5, "yoshiyasu": 9, "zen-emon": 6
                     }

# decalage de la coordonee an x des stations avec plusieurs placves
DECALAGE_STATION_DOUBLE = 90
DECALAGE_STATION_RELAIS = 82

# position des différents sprites du menu
POSITION_MENU = {"illustration" : (295,310), "logo" : (70,70)}
POSITION_CARTE_J = [                                                                                             # pour avatar et Ttemple/pieces/points situe au centre
                    {"fond": (100, 80), "banieres": (74 ,172), "avatar": (197, 147), "souvenirs": (373, 193), "T temple": (120, 296), "T pieces": (200, 317), "T points": (277, 289),
                     "T pano riziere": (338,305), "T pano montagne": (397, 305), "T pano mer": (454, 305), "pseudo": (290, 106)},

                    {"fond": (550, 258), "banieres": (524, 350), "avatar": (647, 324), "souvenirs": (823, 371), "T temple": (570, 474), "T pieces": (650, 495), "T points": (727, 467),
                     "T pano riziere": (788, 483), "T pano montagne": (847, 483), "T pano mer": (904, 483), "pseudo": (742, 284)},

                    {"fond": (100, 408), "banieres": (74, 500), "avatar": (197, 474), "souvenirs": (373, 521), "T temple": (120, 624), "T pieces": (200, 645), "T points": (277, 627),
                     "T pano riziere": (338, 633), "T pano montagne": (397, 633), "T pano mer": (454, 633), "pseudo": (290, 434)},

                    {"fond": (550, 586), "banieres": (524, 678), "avatar": (647, 652), "souvenirs": (823, 699), "T temple": (570, 802), "T pieces": (650, 823), "T points": (727, 795),
                     "T pano riziere": (788, 811), "T pano montagne": (847, 811), "T pano mer": (904, 811), "pseudo": (742, 612)},

                    {"fond": (100, 736), "banieres": (74, 828), "avatar": (197, 802), "souvenirs": (373, 849), "T temple": (120, 952), "T pieces": (200, 973), "T points": (277, 945),
                     "T pano riziere": (338, 961), "T pano montagne": (397, 961), "T pano mer": (454, 961), "pseudo": (290, 762)}
                   ]
POSITION_TEMPLE = {"fond": (163, 66), "nbr pieces joueurs": (374, 538), "pieces donnes": (920, 913), "bouton up": (1033, 865), "bouton down": (1033, 921), 
                   "bouton confirmer" : (1163, 868), "couleur": (304, 308), "baniere": (301, 345)}           #nbr pieces joueure, donee, couleur = coord center
POSITION_ECHOPPE = {"fond": (141, 0), "text petit souvenir": (334, 370), "text nouriture": (334, 444), "text gros souvenir": (334, 516), "text vetement": (334, 588),
                    "carte 1": (701, 665), "carte 2": (957, 665), "carte 3": (1213, 663), "bouton confirmer": (1376, 766), "couleur": (294, 189), "baniere": (95, 201),
                    "pieces joueurs": (167, 396)}     # carte coord, couleur, text = center
POSITION_RELAI = {"fond": (141, 0), "carte 1": (658, 759), "carte 2": (858, 759), "carte 3": (1058, 759), "carte 4": (1258, 759), "carte 5": (758, 520), "carte 6": (958, 520), 
                  "text": (292, 370), "bouton confirmer": (1376, 766), "couleur": (294, 189), "baniere": (95, 201), "pieces joueurs": (167, 396)}      # carte coord, couleur, text = center
POSITION_RENCONTRE = {"fond": (88, 118), "personnage": (2057, 1269), "bouton confirmer": (939, 637), "pano 1": (360, 540), "pano 2": (960, 540), "pano 3": (1560, 540), "text": (580, 475)}
TEXT_RENCONTRE = {"pretre": ["Bonjour voyageur, je suis Miko", "la prêtresse.", "Je vais donner une pièce au", "temple pour toi."],
                  "guide": ["Salut, je suis Annaibito le guide.", "Laissez moi vous aider à compléter", "le panorama de la __replace__.", "Si vous l'avez déjà complété,", 
                            "je vous laisse choisir le panorama", "que vous souhaitez."],
                  "samourai":["Salut, je suis un samourai.", "Laissez mon épée vous guider" ,"vers la victoire.", "Prenez ces 3 points."],
                  "artisan": ["Bonjour voyageur, je suis", "Shokunin un marchand ambuland.", "Prenez ce __replace__ en guise", "de souvenir de notre rencontre."],
                  "noble": ["Enchanté voyageur, je suis", "Kuge le noble.", "C'est toujours", "un plaisir d'aider un voyageur", "dans le besoin.", "Prenez ces 3 pièces."]}
POSITION_FIN_JEU = {"fond": (277, 49), "couleur": (485, 485), "points totals": (582, 485), "baigneur": (721, 485), "bavard": (849, 485), "collectionneur": (1031, 485),
                    "accomplissement pano": (1280, 485), "temple": (1458, 485), "bouton confirmer": (1488, 894)}
POSITION_CREATION_JEU = {"fond": (271, 45),"text nbr total joueur": (1242, 469), "text nbr IA": (1242, 630), "text mode": (1298, 775),"fleche up total": (1343, 415), "fleche down total": (1343, 471),
                         "fleche up IA": (1343, 568), "fleche down IA": (1343, 624), "fleche up mode": (1343, 713), "fleche down mode": (1343, 769), "bouton confirmer": (1423, 822)}
POSITION_CHOIX_2_CARTES = {"carte 1": (675, 540), "carte 2": (1245, 540), "3.carte 1": (360, 540), "3.carte 2": (960, 540), "3.carte 3": (1560, 540)}

# autre
COULEUR = {"beige": (251, 253, 248), "bleu": (71, 134, 207), "gris": (139, 139, 139), "vert": (68, 177, 92), "jaune": (198, 189, 52), "rose": (196, 99, 141),
           "gris fonce": (40, 40, 40), "couleur font": (23, 23, 23)}
ROBOT_NAME = ["Jotaro", "Unizoka", "Sasuke", "Mia", "David", "Kazuya", "Musashi", "Akira", "Omoikane", "Tsukuyomi", "Izanagi", "Amaterasu", "Fujin", "Raiden", "Uzume"]
GAME_MOD = ["classique", "voyage initiatique"]

# taille font
FONT_SIZE_CARTE_J = 45
FONT_SIZE_TEMPLE = 100
FONT_SIZE_TEMPLE_PETIT = 80
FONT_SIZE_ECHOPPE = 60
FONT_SIZE_RELAI = 60
FONT_SIZE_RELAI_TEXT = 25
FONT_SIZE_RENCONTRE = 50
FONT_SIZE_FIN = 50
FONT_SIZE_CREATION_JEU = 70
FONT_SIZE_CREATION_JEU_PETIT = 50
TEXT_DECALAGE_RENCONTRE = 60

#taille carte
SURVOLEE_SIZE_CARTE_ECHOPPE = (240, 370)
SURVOLEE_SIZE_CARTE_RELAI = (163, 245)
SURVOLEE_SIZE_CARTE_RECONTRE = (511, 781)
SURVOLEE_SIZE_CHOIX_2_CARTES = (605, 803)

################################################################################################################################################
BOUTONS_MENU_X = 127
BOUTON_JOUER_Y = 425
BOUTON_CONTINUER_Y = 504
BOUTON_STAT_Y = 587
BOUTON_RULES_Y = 670
BOUTON_ABOUT_Y = 751
BOUTON_EXIT_Y = 832
################################################################################################################################################