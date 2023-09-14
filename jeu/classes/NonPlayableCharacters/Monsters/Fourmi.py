# classes/NonPlayableCharacters/Monsters/Fourmi.py

from typing import Tuple

from classes.NonPlayableCharacters.Monsters.Insects import Insects

"""
NOTES:
    01:
        Le *args et **kwargs
        sont des conventions utilisées en Python pour permettre à
        une fonction de prendre un nombre variable d'arguments.
        *args

        *args est utilisé pour passer une liste variable
        d'arguments non-clé/valeur à une fonction.
        Il permet de passer un nombre arbitraire d'arguments à la fonction
        et de les manipuler comme une liste à l'intérieur de la fonction
        Exemple :
        def fonction_args(*args):
            for arg in args:
                print(arg)

        fonction_args(1, 2, 3, 4)

        Cela affichera :
        1
        2
        3
        4

        ==================================================================

        **kwargs

        **kwargs est utilisé pour passer un dictionnaire d'arguments
        clé/valeur à une fonction. Vous pouvez passer un nombre arbitraire
        d'arguments clé/valeur à une fonction en utilisant **kwargs.
        Exemple :
        def fonction_kwargs(**kwargs):
            for key, value in kwargs.items():
                print(f"La clé est {key} et la valeur est {value}")

        fonction_kwargs(arg1=1, arg2=2, arg3=3)

        Cela affichera :
        La clé est arg1 et la valeur est 1
        La clé est arg2 et la valeur est 2
        La clé est arg3 et la valeur est 3

        ==================================================================

        Utilisation combinée

        Vous pouvez utiliser *args et **kwargs dans la même fonction,
        mais *args doit apparaître avant **kwargs.
        Exemple :
        def fonction_args_et_kwargs(arg1, arg2, *args, kwarg1=None, **kwargs):
            print(f"arg1: {arg1}")
            print(f"arg2: {arg2}")
            print(f"*args: {args}")
            print(f"kwarg1: {kwarg1}")
            print(f"**kwargs: {kwargs}")

        fonction_args_et_kwargs(1, 2, 3, 4, 5, kwarg1=6, kwarg2=7, kwarg3=8)

        Cela affichera :
        arg1: 1
        arg2: 2
        *args: (3, 4, 5)
        kwarg1: 6
        **kwargs: {'kwarg2': 7, 'kwarg3': 8}

        Ces techniques sont souvent utilisées pour écrire des fonctions
        plus flexibles qui peuvent accepter un nombre varié d'arguments.
"""


class Fourmi(Insects):
    """
    Classe Fourmi héritant de la classe Insects.

    Cette classe représente une fourmi en tant qu'entité dans le jeu. Elle
    a des propriétés et des méthodes spécifiques aux fourmis.
    """

    # ===============================================================

    def __init__(self,
                 position: Tuple[int, int],
                 *args,
                 **kwargs) -> None:
        """
        Constructeur de la classe Fourmi.

        :param position: Position initiale de la fourmi dans le jeu.
        :type position: dict
        :param sprite_paths: Les chemins vers les fichiers image du sprite de la fourmi.
        :type sprite_paths: None | dict
        :param args: Arguments positionnels supplémentaires.
        :param kwargs: Arguments clé/valeur supplémentaires.
        """

        # Appel du constructeur de la classe parente.
        super().__init__(position=position,
                         **kwargs)

        # Mise à jour du type de monstre spécifique à cette classe
        self.monster_type = "Fourmi_rouge"

        # Attributes and methods specific to the Fourmi class.
        self.ant_specific_attribute = "Some value"

    # ===============================================================

    # You can add methods specific to the Fourmi class.
    def ant_specific_method(self) -> None:
        """
        Méthode spécifique à la classe Fourmi.

        Cette méthode peut être utilisée pour implémenter une fonctionnalité
        qui est spécifique aux fourmis.
        """

        pass
