# classes/KeyHandler.py

import pygame

from classes.FileProcessor import FileProcessor
from classes.utilitaires_01 import Utilitaires01


class KeyHandler:
    def __init__(self,
                 player=None,
                 game=None,
                 utilitaires_05_for_canvas04_informations=None,
                 scrollable_menu=None):

        # =====================================================================

        # servent de parametres aux methodes, dc pas besoin d'importer les
        # modules (classes)

        #
        self.game = game

        #
        self.player = player

        #
        self.utilitaires_05_for_canvas04_informations = utilitaires_05_for_canvas04_informations

        #
        self.scrollable_menu = scrollable_menu

        # =====================================================================

        # Create a FileProcessor instance
        self.processor = FileProcessor(Utilitaires01.list_files("monoplayer/save/stairs_json"))

        #
        self.key_state = {
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False
        }

    # =========================================================================

    # [REPERE 4 - 2]
    # setter pour l'instance de player.
    # utilisée ds game/game.py [REPERE 4 - 1]
    def set_player(self, player):
        self.player = player

    # =========================================================================

    def handle_key_up(self, key):
        if key in self.key_state:
            self.key_state[key] = False

    # =========================================================================

    def handle_key_down(self, key):
        if key in self.key_state:
            self.key_state[key] = True

    # =========================================================================

    def handle_F1_pressed(self):
        print("F1 pressed")

    def handle_F2_pressed(self):
        print("F2 pressed")

    def handle_F3_pressed(self):
        print("F3 pressed")

    def handle_F4_pressed(self):
        print("F4 pressed")

    # =========================================================================

    def handle_F1_released(self):
        print("F1 released")
        # print player attributes
        print("player attributes from class Player.py")
        print(self.player)
        print("")

    def handle_F2_released(self):
        print("F2 released")

        self.player.life += 1

    # Définir et faire apparaitre 1 bouton défini ds sa propre classe
    # avec un callback (defini ds classes/Utilitaires04Callbacks.py)
    # avec le classes/KeyHandler.py qui fait apparaitre le btn qd
    # on appuie sur F3
    # [REPERE 5 - etape 5]
    # run method to instantiate the btn when F3 released
    def handle_F3_released(self):
        print("F3 released")

        # Instantiate the square button when F3 is released
        # using the game and utilitaires_05 instances
        if self.game:
            if self.utilitaires_05_for_canvas04_informations:

                self.utilitaires_05_for_canvas04_informations.instantiate_square01_button()
                self.game.square01_button = \
                    self.utilitaires_05_for_canvas04_informations.instantiate_square01_button()

                self.utilitaires_05_for_canvas04_informations.instantiate_circle01_button()
                self.game.circle01_button = \
                    self.utilitaires_05_for_canvas04_informations.instantiate_circle01_button()

                self.utilitaires_05_for_canvas04_informations.instantiate_triangle01_button()
                self.game.triangle01_button = \
                    self.utilitaires_05_for_canvas04_informations.instantiate_triangle01_button()

                self.utilitaires_05_for_canvas04_informations.instantiate_square02_button()
                self.game.square02_button = \
                    self.utilitaires_05_for_canvas04_informations.instantiate_square02_button()

    def handle_F4_released(self, scrollable_menu):
        print("F4 released")
        if scrollable_menu:
            print("menu visible")
            scrollable_menu.update_option_position()

