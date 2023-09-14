# monoplayer_screen02_create_character.py

import tkinter as tk
import subprocess
import sys
import os
import secrets
import json

"""
Voici la ligne de commande que l'on doit executer pour lancer le programme.
Sinon les imports de classe ne fonctionneront pas.
Cela permet de ne pas toucher au PYTHONPATH ds le ~.bashrc
PYTHONPATH="/home/sambano/Documents/python/jeu/v2/jeu"
        python3.11 /home/sambano/Documents/python/jeu/v2/jeu/introduction.py
"""

from classes.ToolTip import ToolTip
from classes.utilitaires_01 import Utilitaires01
# usage:
# Utilitaires01.directory_exists('/some/path')


class Application(tk.Frame):
    """
    The Application class represents the main interface of the game.
    It provides GUI elements to create a character, roll dice for attributes,
    and navigate between different screens.
    """

    # =========================================================================

    def __init__(self, master=None):
        """
        Initializes the application, setting up the main frame and widgets.

        :param master: The parent widget
        """

        super().__init__(master)
        self.master = master
        self.master.geometry('800x600')
        self.master.title('monoplayer_screen02_create_character.py')
        self.grid(padx=5,
                  pady=5)

        # Define variables
        self.character_name = tk.StringVar()
        self.attack = tk.IntVar()
        self.defense = tk.IntVar()
        self.life = tk.IntVar()

        # =====================================================================

        self.empty_space_01 = tk.Label(self,
                                       width=2)

        self.empty_space_01.grid(row=0,
                                 column=0,
                                 sticky='w')

        # =====================================================================

        # Add a button which will close the current window
        # and open the introduction screen

        self.button = tk.Button(self,
                                text="Go back to introduction",
                                command=self.goto_screen01)

        self.button.grid(row=0,
                         column=2,
                         padx=15,
                         sticky='w')

        ToolTip(self.button,
                "Go back to introduction")

        # =====================================================================

        # Add a button which will close the current window and
        # open the monoplayer screen

        self.monoplayer_button = tk.Button(self,
                                           text="Go back 1 step",
                                           command=self.goto_monoplayer_screen01)

        self.monoplayer_button.grid(row=0,
                                    column=1,
                                    padx=15,
                                    sticky='w')

        ToolTip(self.monoplayer_button,
                "Go back 1 step")

        # =====================================================================

        self.empty_space_02 = tk.Label(self,
                                       width=10,
                                       height=4)

        self.empty_space_02.grid(row=1,
                                 column=0,
                                 sticky='w')

        # =====================================================================

        # Add the labels and text entry
        self.label_create_character = tk.Label(self,
                                               text='Create your character')
        self.label_create_character.grid(row=2,
                                         column=1,
                                         padx=15,
                                         sticky='w')

        self.label_enter_name = tk.Label(self,
                                         text='Please enter the name of your character')

        self.label_enter_name.grid(row=3,
                                   column=1,
                                   padx=15,
                                   sticky='w')

        self.entry_name = tk.Entry(self,
                                   textvariable=self.character_name)

        self.entry_name.grid(row=4,
                             column=1,
                             padx=15,
                             sticky='w')

        self.entry_name.bind('<KeyRelease>',
                             self.check_and_update_button)

        self.label_guideline = tk.Label(self,
                                        text='Only letters and or numbers, min 5 and max 15')

        self.label_guideline.grid(row=5,
                                  column=1,
                                  padx=15,
                                  sticky='w')

        # =====================================================================

        self.roll_dice_button = tk.Button(self,
                                          text="Please roll dice to define your skills",
                                          command=self.roll_dice)

        self.roll_dice_button.grid(row=6,
                                   column=1,
                                   padx=15,
                                   sticky='w')

        ToolTip(self.roll_dice_button,
                "Please roll dices to define your skills")

        # =====================================================================

        self.label_attack = tk.Label(self,
                                     text='The attack of your character will be: ')

        self.label_attack.grid(row=7,
                               column=1,
                               padx=15,
                               sticky='w')

        # Label to show attack value
        self.label_attack_value = tk.Label(self,
                                           textvariable=self.attack)

        self.label_attack_value.grid(row=7,
                                     column=2,
                                     padx=15,
                                     sticky='w')

        self.label_defense = tk.Label(self,
                                      text='The defense of your character will be: ')

        self.label_defense.grid(row=8,
                                column=1,
                                padx=15,
                                sticky='w')

        # Label to show defense value
        self.label_defense_value = tk.Label(self,
                                            textvariable=self.defense)

        self.label_defense_value.grid(row=8,
                                      column=2,
                                      padx=15,
                                      sticky='w')

        self.label_life = tk.Label(self,
                                   text='The life of your character will be: ')

        self.label_life.grid(row=9,
                             column=1,
                             padx=15,
                             sticky='w')

        # Label to show life value
        self.label_life_value = tk.Label(self,
                                         textvariable=self.life)

        self.label_life_value.grid(row=9,
                                   column=2,
                                   padx=15,
                                   sticky='w')

        # =====================================================================

        self.empty_space_03 = tk.Label(self,
                                       width=10,
                                       height=3)

        self.empty_space_03.grid(row=10,
                                 column=0,
                                 sticky='w')

        # =====================================================================

        # New button that will be hidden until character name,
        # attack, defense and life are set

        self.buttonToCreateCharacter = tk.Button(self,
                                                 text="Create your character and start the game",
                                                 command=self.start_game)

        self.buttonToCreateCharacter.grid(row=11,
                                          column=1,
                                          padx=15,
                                          sticky='w')

        # initially hidden
        self.buttonToCreateCharacter.grid_remove()

        ToolTip(self.buttonToCreateCharacter,
                "Create your character and start the game")

    # =========================================================================

    def goto_screen01(self):
        """
        Closes the current window and opens the introduction screen.
        """

        self.master.destroy()
        subprocess.run([sys.executable, 'introduction.py'],
                       check=True)

    # =========================================================================

    def goto_monoplayer_screen01(self):
        """
        Closes the current window and opens the monoplayer screen.
        """

        self.master.destroy()
        subprocess.run([sys.executable,
                        os.path.join('monoplayer', 'monoplayer_screen01.py')],
                       check=True)

    # =========================================================================

    def roll_dice(self):
        """
        Randomly sets the attack and defense attributes of the character.
        """

        self.attack.set(secrets.randbelow(100) + 1)
        self.defense.set(secrets.randbelow(100) + 1)
        self.life.set(secrets.randbelow(100) + 1)
        self.check_and_update_button()

    # =========================================================================

    def start_game(self):
        """
        - Checks for the existence of a save folder and
        creates it if necessary.
        - Check if this folder is empty or not
        no? so empty this folder.
        - Create a json dictionary about the player skills defined.
        - Write this json dictionary to the empty folder.
        - Check for the existence of a save/stairs_json folder and
        creates it if necessary.
        - Check if this folder is empty or not
        no? So empty this folder.
        will take you to next screen to start the game
        """
        # ---------------------------------------------------------------------
        # on verifie si le dossier monoplayer/save existe ou pas.
        # s'il existe
        # s'il n'existe pas on le crée
        if Utilitaires01.directory_exists(self, 'monoplayer/save'):
            print("Folder monoplayer/save already exists, we continue")
        else:
            print("Folder monoplayer/save does not exists")
            Utilitaires01.create_folder(self, "monoplayer/save")
            print("creation before going on")
        # ---------------------------------------------------------------------
        # on verifie si le dossier monoplayer/save (dt on a déja verifié
        # l'existence') contient
        # des fichiers ou pas. On commence une nvelle partie.
        # Dc si le dossier est vide, c'est bon.
        # Si le dossier n'est pas vide, on le vide
        if Utilitaires01.is_folder_empty(self, "monoplayer/save"):
            print("Folder monoplayer/save empty, we continue")
        else:
            print("Folder monoplayer/save not empty, need to empty it")
            Utilitaires01.empty_folder(self, "monoplayer/save")
            print("folder now empty, we are going on")
        # ---------------------------------------------------------------------
        # Create a JSON dictionary with the values
        json_dict = {
            "name": self.character_name.get(),
            "attack": self.attack.get(),
            "defense": self.defense.get(),
            "NOTE_for_dev_about_key_life": "Représente la vie actuelle du self.player",
            "life": self.life.get(),
            "NOTE_for_dev_about_key_max_life_authorized": "Représente la vie max authorisée pour le self.player. Cette valeur ne peut pas etre dépassée ms elle peut augmentée (ou diminiuée) si par exemple, la nature du joueur change ou s'il boit une pot° de 'super vie' qui lui permet d'augmenter cette valeur.",
            "max_life_authorized": self.life.get(),
            "position": (0, 0),
            "color": (0, 255, 0),
            "radius": 8,
            "sprite_paths": {
                "va_en_haut": [
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_haut/01.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_haut/02.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_haut/03.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_haut/04.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_haut/05.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_haut/06.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_haut/07.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_haut/08.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_haut/09.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_haut/10.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_haut/11.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_haut/12.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_haut/13.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_haut/14.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_haut/15.png"],
                "va_a_droite": [
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_droite/01.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_droite/02.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_droite/03.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_droite/04.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_droite/05.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_droite/06.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_droite/07.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_droite/08.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_droite/09.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_droite/10.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_droite/11.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_droite/12.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_droite/13.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_droite/14.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_droite/15.png"
                ],
                "va_en_bas": [
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_bas/01.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_bas/02.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_bas/03.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_bas/04.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_bas/05.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_bas/06.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_bas/07.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_bas/08.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_bas/09.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_bas/10.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_bas/11.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_bas/12.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_bas/13.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_bas/14.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_en_bas/15.png"
                ],
                "va_a_gauche": [
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_gauche/01.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_gauche/02.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_gauche/03.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_gauche/04.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_gauche/05.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_gauche/06.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_gauche/07.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_gauche/08.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_gauche/09.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_gauche/10.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_gauche/11.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_gauche/12.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_gauche/13.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_gauche/14.png",
                    "images/mante_religieuse/sequence_animation_mante_religieuse_03_16x16/va_a_gauche/15.png"
                ],
            },
            "speed": 16,
            "stair_actuel": "monoplayer/save/stairs_json/stair_1.json",
        }

        # Define the path for the JSON file
        save_path = "monoplayer/save/save_player.json"

        # Write the JSON dictionary to the file
        with open(save_path, 'w') as json_file:
            json.dump(json_dict,
                      json_file,
                      indent=4)

        print("Player data saved successfully.")
        print("to monoplayer/save/save_player.json")
        # ---------------------------------------------------------------------
        # on verifie si le dossier monoplayer/save/stairs_json existe ou pas.
        # s'il existe
        # s'il n'existe pas on le crée
        # PROBLEME:
        # cette etape pose probleme, le dossier monoplayer/save/stairs_json
        # est crée qu'il existe déjà ou pas
        if Utilitaires01.directory_exists(self, 'monoplayer/save/stairs_json'):
            print("Folder monoplayer/save/stairs_json already exists, we continue")
        else:
            print("Folder monoplayer/save/stairs_json does not exists")
            Utilitaires01.create_folder(self, "monoplayer/save/stairs_json")
            print("creation before going on")
        # ---------------------------------------------------------------------
        # on verifie si le dossier monoplayer/save/stairs_json (dt on a
        # déja verifié l'existence') contient
        # des fichiers ou pas. On commence une nvelle partie.
        # Dc si le dossier est vide, c'est bon.
        # Si le dossier n'est pas vide, on le vide
        if Utilitaires01.is_folder_empty(self, "monoplayer/save/stairs_json"):
            print("Folder monoplayer/save/stairs_json empty, we continue")
        else:
            print("Folder monoplayer/save/stairs_json not empty, need to empty it")
            Utilitaires01.empty_folder(self, "monoplayer/save/stairs_json")
            print("folder now empty, we are going on")
        # ---------------------------------------------------------------------

        self.master.destroy()
        subprocess.run([sys.executable,
                        os.path.join('game', 'game.py')],
                       check=True)

    # =========================================================================

    def check_and_update_button(self,
                                event=None):
        """
        Validates the character name, attack, and defense attributes,
        and enables or disables the start game button accordingly.

        :param event: The event object (default is None)
        """

        if self.character_name.get() and \
                len(self.character_name.get()) >= 5 and \
                self.character_name.get().isalnum() and \
                self.attack.get() != 0 and \
                self.defense.get() != 0 and \
                self.life.get() != 0:
            # make button visible
            self.buttonToCreateCharacter.grid()
        else:
            # hide button
            self.buttonToCreateCharacter.grid_remove()


def main():
    """
    Entry point for the application. Creates the root window and runs
    the main loop.
    """

    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
