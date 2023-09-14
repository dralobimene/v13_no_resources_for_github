# classes/utilitaires_05_instantiate_buttons_callbacks.py

import pygame

from classes.utilitaires_04_callbacks import Utilitaires04Callbacks
from classes.Buttons.shaped_button_square import ShapedButtonSquare
from classes.Buttons.shaped_button_circle import ShapedButtonCircle
from classes.Buttons.shaped_button_triangle import ShapedButtonTriangle


class Utilitaires_05:
    """
    Classe qui définit la configuration de chacun des boutons
    crées avec pygame
    """

    # constants
    TRANSPARENT = pygame.Color(0, 0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)
    BLACK = pygame.Color(0, 0, 0)
    GREEN = pygame.Color(0, 255, 0)
    BLUE = pygame.Color(0, 0, 255)
    YELLOW = pygame.Color(255, 255, 0)
    RED = pygame.Color(255, 0, 0)
    GREY = pygame.Color(128, 128, 128)

    # =========================================================================

    def __init__(self, canvas_target):

        #
        self.canvas_target = canvas_target

        # Définir et faire apparaitre 1 bouton défini ds sa propre classe
        # avec un callback (defini ds classes/Utilitaires04Callbacks.py)
        # avec le classes/KeyHandler.py qui fait apparaitre le btn qd
        # on appuie sur F3.
        # [REPERE 5 - etape 1]
        # Définir à None.
        self.square01_button = None
        self.circle01_button = None
        self.triangle01_button = None
        self.square02_button = None

    # =========================================================================

    def instantiate_square01_button(self):
        # print("Instantiating square01 button")
        self.square01_button = ShapedButtonSquare(
            self.canvas_target,
            50,
            50,
            offset_y=self.canvas_target.get_height(),
            color=self.BLUE,
            callback=Utilitaires04Callbacks.on_square01_button_click
        )
        self.square01_button.position = (0, 0)
        return self.square01_button

    # =========================================================================

    def instantiate_circle01_button(self):
        # print("Instantiating circle01 button")
        self.circle01_button = ShapedButtonCircle(
            self.canvas_target,
            50,
            50,
            offset_y=self.canvas_target.get_height(),
            color=self.GREEN,
            callback=Utilitaires04Callbacks.on_circle01_button_click
        )
        self.circle01_button.position = (150, 0)
        return self.circle01_button

    # =========================================================================

    def instantiate_triangle01_button(self):
        # print("Instantiating triangle01 button")
        self.triangle01_button = ShapedButtonTriangle(
            self.canvas_target,
            50,
            50,
            offset_y=self.canvas_target.get_height(),
            color=self.RED,
            callback=Utilitaires04Callbacks.on_triangle01_button_click
        )
        self.triangle01_button.position = (250, 0)
        return self.triangle01_button

    # =========================================================================

    def instantiate_square02_button(self):
        # print("Instantiating square02 button")
        self.square02_button = ShapedButtonSquare(
            self.canvas_target,
            50,
            50,
            offset_y=self.canvas_target.get_height(),
            color=self.GREY,
            callback=Utilitaires04Callbacks.on_square02_button_click
        )
        self.square02_button.position = (350, 0)
        return self.square02_button

    # =========================================================================
