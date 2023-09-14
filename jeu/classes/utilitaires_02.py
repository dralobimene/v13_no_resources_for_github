# utilitaires_02.py
# la classe Utilitaires02 ne peut pas être importée
# ds la classe Player

import pygame

import os

import json
import sys

from classes.Player import Player

"""
N'oubliez pas que lorsque vous utilisez des méthodes statiques,
vous n'aurez pas accès aux variables
d'instance ou aux autres méthodes d'instance de la classe dans ces méthodes.
Si vous avez besoin
d'accéder à des données spécifiques à l'instance, vous devez envisager
d'utiliser des méthodes d'instance à la place.
"""


class Utilitaires02:

    # =========================================================================

    @staticmethod
    def create_player_from_saved_player_json(self,
                                             canvas,
                                             position_override=None,
                                             stair_actuel_override=None):
        """
        Cette méthode crée et renvoie un objet Player à partir des données
        enregistrées dans un fichier JSON.

        Paramètres:
        - self: Une référence à l'objet qui appelle cette méthode (normalement,
        un objet de la classe qui contient cette méthode).
        - position_override: Si fourni, cette position sera utilisée pour le
        joueur au lieu de la position enregistrée dans le fichier.

        Si le fichier "monoplayer/save/player.json" n'existe pas,
        la méthode affiche un
        message d'erreur et arrête le programme.

        Renvoie un objet Player initialisé avec les données du fichier.
        """

        # verificat° de l'existence du fichier
        if not os.path.exists("monoplayer/save/save_player.json"):
            pygame.quit()
            sys.exit()

        # Open the JSON file
        with open("monoplayer/save/save_player.json", 'r') as file:
            # Load the JSON data
            player_data = json.load(file)

        # Extract position from the data or use override
        if position_override:
            position = position_override
        else:
            position_data = player_data['position']
            # Handle both list and dictionary formats
            if isinstance(position_data, dict) and 'x' in position_data and 'y' in position_data:
                position = (int(position_data['x']), int(position_data['y']))
            elif isinstance(position_data, (list, tuple)) and len(position_data) == 2:
                position = (int(position_data[0]), int(position_data[1]))
            else:
                raise ValueError(f"Invalid position format: {position_data}")

        #
        stair_actuel = stair_actuel_override \
            if stair_actuel_override is not None \
            else player_data['stair_actuel']

        # Initialize a Player object with the data from the file
        player = Player(
            player_data['name'],
            player_data['attack'],
            player_data['defense'],
            player_data['life'],
            player_data['max_life_authorized'],
            position,
            player_data['color'],
            player_data['radius'],
            player_data['speed'],
            stair_actuel,
        )

        # Save the new player data back to the JSON file
        with open("monoplayer/save/save_player.json", 'w') as file:
            json.dump(player.to_dict(), file, indent=4)

        return player
