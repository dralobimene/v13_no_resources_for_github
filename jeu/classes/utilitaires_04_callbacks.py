# classes/utilitaires_04_callbacks.py


"""
N'oubliez pas que lorsque vous utilisez des méthodes statiques,
vous n'aurez pas accès aux variables
d'instance ou aux autres méthodes d'instance de la classe dans ces méthodes.
Si vous avez besoin
d'accéder à des données spécifiques à l'instance, vous devez envisager
d'utiliser des méthodes d'instance à la place.
"""


class Utilitaires04Callbacks:
    """
    Classe qui Définit toutes les methodes callback des boutons
    dessinés avec pygame.
    exemple:
        On a définit une classe parente:
            classes/ShapedButton.py qui est la classe parente.
            Elle définit des formes sur lesquelles on pourra cliquer.
            Ces formes cliquables sont réutilisables grâce aux callbacks.
            classes/Buttons/shaped_button_XXX.py st les classes enfant.
    """

    # =========================================================================

    # Définir et faire apparaitre 1 bouton défini ds sa propre classe.
    # Le bouton est défini grâce aux fichiers:
    #   - classes/ShapedButton.py (classe parente).
    #   - classes/Buttons/shaped_button_XXX.py (classe enfant).
    #   Possède un callback (defini ds classes/Utilitaires04Callbacks.py)
    # avec le classes/KeyHandler.py qui fait apparaitre le btn qd
    # on appuie sur F3.
    # [REPERE 5 - etape 6]
    # Définir la méthode qui sera executée qd on cliquera sur ce btn.
    @staticmethod
    def on_square01_button_click():
        print("square01 clicked")

    # =========================================================================

    @staticmethod
    def on_circle01_button_click():
        print("circle01 clicked")

    # =========================================================================

    @staticmethod
    def on_triangle01_button_click():
        print("triangle02 clicked")

    # =========================================================================

    @staticmethod
    def on_square02_button_click():
        print("square02 clicked")

    # =========================================================================
