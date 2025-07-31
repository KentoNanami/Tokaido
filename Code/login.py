import FreeSimpleGUI as sg
import pickle


def login():
	layout_login = [
	[sg.Text("Insérez votre pseudo : ")],
	[sg.Input(key = "PSEUDO_INPUT_l")],
	[sg.Text("Inserez votre mot de passe : ")],
	[sg.Input(key = "MDP_INPUT_l")],
	[sg.Button("Se connecter")],
	[sg.Text("", key = "OUTPUT")],
	[sg.Text("Si vous n'avez pas encore de compte c'est par ici ->"), sg.Button("S'inscire ! ")],
	[sg.Text("Astuce : Si vous ne souhaitez pas avoir de compte fermer la fenêtre")]
	]
	fenetre_login = sg.Window("Login", layout_login)
	event = True
	while event != sg.WIN_CLOSED:
		combo_file = open("../Data/combo_data", "rb")
		combo_dict = pickle.load(combo_file)
		combo_file.close()
		event, values = fenetre_login.read()

		if event == sg.WIN_CLOSED:
			break
		if event == "S'inscire ! ":
			signin()
		if event == "Se connecter":
			if values["PSEUDO_INPUT_l"] in combo_dict:
				if combo_dict[values["PSEUDO_INPUT_l"]] == values["MDP_INPUT_l"]:
					fenetre_login["OUTPUT"].update("Bienvenu " + values["PSEUDO_INPUT_l"])
					break		
				else:
					fenetre_login["OUTPUT"].update("Mot de passe incorrect")
			if values["PSEUDO_INPUT_l"] not in combo_dict:
				fenetre_login["OUTPUT"].update("Créeez vous un compte pour jouer !")
				
	fenetre_login.close()
	return values["PSEUDO_INPUT_l"]

def signin():
	layout_signin = [
	[sg.Text("Insérez votre pseudo : ")],
	[sg.Input(key = "PSEUDO_INPUT_s")],
	[sg.Text("Inserez un mot de passe : ")],
	[sg.Input(key = "MDP_INPUT_s")],
	[sg.Button("S'inscrire")],
	[sg.Text("", key = "OUTPUT")]
	]
	combo_file = open("../Data/combo_data", "rb")
	combo_dict = pickle.load(combo_file)
	combo_file.close()
	fenetre_signin = sg.Window("Inscription", layout_signin)
	while True:
		event, values = fenetre_signin.read()
		if event == sg.WIN_CLOSED:
			exit()
		if event == "S'inscrire":
			if values["PSEUDO_INPUT_s"] in combo_dict:
				fenetre_signin["OUTPUT"].update("Ce pseudo est deja pris !")
			else:
				if values["PSEUDO_INPUT_s"] == "":
					fenetre_signin["OUTPUT"].update("Merci d'entrer un pseudo")#il faudrait être vachement con mais bon.....
				else : 
					combo_dict[values["PSEUDO_INPUT_s"]] = values["MDP_INPUT_s"]
					pseudo = values["PSEUDO_INPUT_s"]
					stat_file = open(f"../Data/Player/{pseudo}", "wb")
					pickle.dump([0,0,0], stat_file) # 1=victoire 2=défaite 3=temps de jeu(optionnel)
					stat_file.close()
					break
	combo_file = open("../Data/combo_data", "wb")
	pickle.dump(combo_dict, combo_file)
	combo_file.close()

	fenetre_signin.close()


