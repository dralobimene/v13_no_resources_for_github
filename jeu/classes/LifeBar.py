# Fichier: classes/LifeBar.py

import pygame
import pygame.font

from classes.utilitaires_01 import Utilitaires01
# usage:
# Utilitaires01.directory_exists('/some/path')


class LifeBar:
    """
    Classe représentant la barre de vie d'une entité dans un jeu.

    Attributs:
        screen (pygame.Surface): La surface sur laquelle la barre de vie sera dessinée.
        x (int): La position X de la barre de vie.
        y (int): La position Y de la barre de vie.
        entity: L'entité dont la vie est représentée.
    """

    # constants
    BLACK = pygame.Color(0, 0, 0)
    ESPACEMENT = 15

    def __init__(self,
                 screen: pygame.Surface,
                 x: int,
                 y: int,
                 entity) -> None:
        """
        Initialise une nouvelle instance de la classe LifeBar.

        Paramètres:
            screen (pygame.Surface): La surface sur laquelle la barre de vie sera dessinée.
            x (int): La position X de la barre de vie.
            y (int): La position Y de la barre de vie.
            entity: L'entité dont la vie est représentée.
        """

        self.__screen = screen
        self.__x = x
        self.__y = y
        self.__entity = entity

        # Utilisation de la méthode get_key_value_from_json pour obtenir
        # la valeur de 'life'
        self.__width = Utilitaires01.get_key_value_from_json(
            "monoplayer/save/save_player.json", "life")

        # suppose que la largeur est proportionnelle à la vie
        self.__max_width = 100
        self.__height = 10
        self.__color = pygame.Color('green')

        self.__life_value = Utilitaires01.get_key_value_from_json(
            "monoplayer/save/save_player.json", "life")

        # Créer une nouvelle variable qui prendra la même valeur
        # que self.__life_value
        self.__max_life_authorized = Utilitaires01.get_key_value_from_json(
            "monoplayer/save/save_player.json", "max_life_authorized")

        self.__text = None

    # =======================================================================

    @property
    def screen(self) -> pygame.Surface:
        """Retourne la surface sur laquelle la barre de vie est dessinée."""
        return self.__screen

    @screen.setter
    def screen(self, screen: pygame.Surface) -> None:
        """Définit la surface sur laquelle la barre de vie sera dessinée."""
        self.__screen = screen

    @property
    def x(self) -> int:
        """Retourne la position X de la barre de vie."""
        return self.__x

    @x.setter
    def x(self, x: int) -> None:
        """Définit la position X de la barre de vie."""
        self.__x = x

    @property
    def y(self) -> int:
        """Retourne la position Y de la barre de vie."""
        return self.__y

    @y.setter
    def y(self, y: int) -> None:
        """Définit la position Y de la barre de vie."""
        self.__y = y

    @property
    def entity(self):
        """Retourne l'entité associée à cette barre de vie."""
        return self.__entity

    @entity.setter
    def entity(self, entity) -> None:
        """Définit l'entité associée à cette barre de vie."""
        self.__entity = entity

    @property
    def width(self) -> int:
        """Retourne la largeur de la barre de vie."""
        return self.__width

    @width.setter
    def width(self, width: int) -> None:
        """Définit la largeur de la barre de vie."""
        self.__width = width

    @property
    def max_width(self) -> int:
        """Retourne la largeur maximale de la barre de vie."""
        return self.__max_width

    @max_width.setter
    def max_width(self, max_width: int) -> None:
        """Définit la largeur maximale de la barre de vie."""
        self.__max_width = max_width

    @property
    def height(self) -> int:
        """Retourne la hauteur de la barre de vie."""
        return self.__height

    @height.setter
    def height(self, height: int) -> None:
        """Définit la hauteur de la barre de vie."""
        self.__height = height

    @property
    def color(self) -> pygame.Color:
        """Retourne la couleur de la barre de vie."""
        return self.__color

    @color.setter
    def color(self, color: pygame.Color) -> None:
        """Définit la couleur de la barre de vie."""
        self.__color = color

    @property
    def life_value(self) -> int:
        """Retourne la valeur de vie actuelle de l'entité."""
        return self.__life_value

    @life_value.setter
    def life_value(self, life_value: int) -> None:
        """Définit la valeur de vie actuelle de l'entité."""
        self.__life_value = life_value

    @property
    def max_life_authorized(self) -> int:
        """Retourne la valeur maximale autorisée de la vie de l'entité."""
        return self.__max_life_authorized

    @max_life_authorized.setter
    def max_life_authorized(self, max_life_authorized: int) -> None:
        """Définit la valeur maximale autorisée de la vie de l'entité."""
        self.__max_life_authorized = max_life_authorized

    @property
    def text(self):
        """Retourne le texte associé à la barre de vie."""
        return self.__text

    @text.setter
    def text(self, text) -> None:
        """Définit le texte associé à la barre de vie."""
        self.__text = text

    # =======================================================================

    """
    def set_entity(self, entity):
        self.__entity = entity
        self.update()
    """

    # =======================================================================

    def kill(self):
        """
        Supprime toutes les références pour permettre le nettoyage par le ramasse-miettes.
        """

        self.__text = None
        self.__entity.life = None
        self.__entity = None
        self.__screen = None
        self.__x = None
        self.__y = None
        self.__max_life_authorized = None
        self.__life_value = None
        self.__width = None
        self.__height = None
        self.__max_width = None

    # =======================================================================

    def draw(self) -> None:
        """
        Dessine la barre de vie sur la surface définie.
        """

        # Créer une police
        font = pygame.font.Font(None, 20)

        pygame.draw.rect(self.__screen, self.__color,
                         (self.__x, self.__y, self.__width, self.__height))

        self.__text = font.render(f"Life: {self.__max_life_authorized} / {self.__life_value}",
                                  True, self.BLACK)

        # Dessiner le texte
        # -40 déplace le texte vers le haut par rapport à la barre de vie
        self.__screen.blit(self.__text, (self.__x, self.__y - self.ESPACEMENT))

    # =======================================================================

    def update(self) -> None:
        """
        Met à jour la barre de vie en fonction de la vie de l'entité.
        """

        # Calculer le pourcentage de vie
        life_percentage = (self.__entity.life /
                           self.__entity.max_life_authorized) * 100

        # Mettre à jour self.__life_value avec la nouvelle valeur
        self.__life_value = self.__entity.life

        # Mettre à jour la largeur en fonction du pourcentage de vie
        self.__width = int(self.__max_width * (life_percentage / 100))

        # Changer la couleur en fonction du pourcentage de vie
        if 100 >= life_percentage >= 75:
            self.__color = pygame.Color('green')
        elif 75 > life_percentage >= 45:
            self.__color = pygame.Color('yellow')
        elif 45 > life_percentage >= 15:
            self.__color = pygame.Color('orange')
        elif 15 > life_percentage >= 1:
            self.__color = pygame.Color('red')

        font = pygame.font.Font(None, 20)
        self.__text = font.render(f"Life: {self.__max_life_authorized} / {self.__entity.life}",
                                  True, self.BLACK)
        self.__screen.blit(self.__text, (self.__x, self.__y - self.ESPACEMENT))

        pygame.draw.rect(self.__screen, self.__color,
                         (self.__x, self.__y, self.__width, self.__height))
