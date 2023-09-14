# classes/utilitaires_03.py
# la classe classes/Utilitaires03 ne peut pas être importée
# ds la classe classes/Monster.py

import sys
import random
from copy import deepcopy
from typing import Union, List

import pygame

from classes.NonPlayableCharacters.Monsters.Fourmi import Fourmi

from classes.utilitaires_01 import Utilitaires01
# usage:
# Utilitaires01.directory_exists('/some/path')


"""
N'oubliez pas que lorsque vous utilisez des méthodes statiques,
vous n'aurez pas accès aux variables
d'instance ou aux autres méthodes d'instance de la classe dans ces méthodes.
Si vous avez besoin
d'accéder à des données spécifiques à l'instance, vous devez envisager
d'utiliser des méthodes d'instance à la place.
"""


class Utilitaires03:
    """
    Classe utilitaire pour diverses fonctions liées aux monstres
    et autres éléments du jeu.
    """

    def create_monsters(self,
                        stair_actuel: str) -> List[Union[Fourmi]]:
        """
        Crée une liste de monstres sur les tuiles blanches du niveau.

        :param stair_actuel: Le niveau actuel.
        :return: Une liste contenant des objets monstre.
        """

        tile_player = Utilitaires01.get_key_value_from_json(
            stair_actuel, "entry_tile")
        tiles_blanches = Utilitaires01.get_key_value_from_json(
            stair_actuel, "white_tiles_array")
        tiles_blanches_copy = deepcopy(tiles_blanches)

        monsters_number = random.randint(15, 35)
        liste_monsters = []

        if tile_player not in tiles_blanches:
            print("la tile_player n'est pas ds tiles_blanches")
            print("32651: Erreur program")
            pygame.quit()
            sys.exit()

        monster_classes = {
            "Fourmi_rouge": Fourmi,
        }

        for i in range(monsters_number):
            element_chosen = random.choice(tiles_blanches_copy)
            x = element_chosen['x']
            y = element_chosen['y']

            monster_type = random.choice(list(monster_classes.keys()))
            monster_class = monster_classes[monster_type]

            monster = monster_class(
                position={'x': x, 'y': y},
                name=f"monster{i+1}",
                monster_type=monster_type
            )

            tiles_blanches_copy.remove(element_chosen)
            liste_monsters.append(monster)

        return liste_monsters

    # =========================================================================
