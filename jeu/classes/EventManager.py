# classes/EventManager.py

import pygame_gui


class EventManager:

    # =========================================================================

    def __init__(self, game):
        self.game = game

    # =========================================================================

    def process_event(self, event, player_attributes):
        """
        Cette méthode gère les événements en fonction de leur type.
        Si l'événement est le bouton 'Save' pressé, elle sauvegarde
        les attributs du joueur.
        """
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            print("EventManager invoqué")
            # if self.game.save_button and event.ui_element == self.game.save_button:
