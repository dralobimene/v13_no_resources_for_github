# classes/MenuCombatScrollableArea.py

import pygame
import pygame_gui
from typing import Tuple, List, Union

from classes.Player import Player
from classes.Monster import Monster
from classes.MenuCombat import MenuCombat


class MenuCombatScrollableArea:
    """
    Classe qui gère un conteneur scrollable pour afficher des menus de combat.

    Attributs:
        window_surface (pygame.Surface): La surface sur laquelle le conteneur
        est dessiné.
        manager (pygame_gui.UIManager): Le gestionnaire d'interface
        utilisateur pour pygame_gui.
        container_rect (pygame.Rect): Le rectangle définissant la taille
        et la position du conteneur.
        content_rect (pygame.Rect): Le rectangle définissant la taille et
        la position du contenu.
        menu_combats (list[MenuCombat]): Liste des menus de combat à afficher.
        ... (autres attributs privés)
    """

    def __init__(self,
                 window_surface: pygame.Surface,
                 manager: pygame_gui.UIManager,
                 container_rect_dimensions: Tuple[int, int, int, int],
                 content_rect_size: Tuple[int, int],
                 menu_height: int) -> None:
        """
        Initialise un nouvel objet de type MenuCombatScrollableArea.

        Paramètres :
        - window_surface : Surface Pygame où le menu sera affiché.
        - manager : Gestionnaire d'interface utilisateur de pygame_gui.
        - container_rect_dimensions : Dimensions du rectangle conteneur.
        - content_rect_size : Taille du rectangle de contenu.
        - menu_height : Hauteur du menu.
        """

        self.__window_surface = window_surface
        self.__manager = manager
        self.__container_rect = pygame.Rect(*container_rect_dimensions)
        self.__menu_height = menu_height

        self.__menu_y = 0
        self.__container_background = pygame.Surface(
            self.__container_rect.size)
        self.__container_background.fill(pygame.Color('blue'))
        self.__content_rect = pygame.Rect((0, 0), content_rect_size)
        self.__scrollable_container = pygame_gui.elements.UIScrollingContainer(
            relative_rect=self.__container_rect,
            manager=self.__manager)
        self.__scrollable_container.set_scrollable_area_dimensions(
            self.__content_rect.size)
        self.__menu_combats = []

    # =========================================================================

    @property
    def window_surface(self) -> pygame.Surface:
        return self.__window_surface

    @window_surface.setter
    def window_surface(self,
                       window_surface: pygame.Surface) -> None:
        self.__window_surface = window_surface

    @property
    def manager(self) -> pygame_gui.UIManager:
        return self.__manager

    @manager.setter
    def manager(self,
                manager: pygame_gui.UIManager) -> None:
        self.__manager = manager

    @property
    def container_rect(self) -> pygame.Rect:
        return self.__container_rect

    @container_rect.setter
    def container_rect(self,
                       container_rect: pygame.Rect) -> None:
        self.__container_rect = container_rect

    @property
    def menu_height(self) -> int:
        return self.__menu_height

    @menu_height.setter
    def menu_height(self,
                    menu_height: int) -> None:
        self.__menu_height = menu_height

    @property
    def menu_y(self) -> int:
        return self.__menu_y

    @menu_y.setter
    def menu_y(self,
               menu_y: int) -> None:
        self.__menu_y = menu_y

    @property
    def container_background(self) -> pygame.Surface:
        return self.__container_background

    @container_background.setter
    def container_background(self,
                             container_background: pygame.Surface) -> None:
        self.__container_background = container_background

    @property
    def content_rect(self) -> pygame.Rect:
        return self.__content_rect

    @content_rect.setter
    def content_rect(self,
                     content_rect: pygame.Rect) -> None:
        self.__content_rect = content_rect

    @property
    def scrollable_container(self) -> pygame_gui.elements.UIScrollingContainer:
        return self.__scrollable_container

    @scrollable_container.setter
    def scrollable_container(self,
                             scrollable_container: pygame_gui.elements.UIScrollingContainer) -> None:
        self.__scrollable_container = scrollable_container

    @property
    def menu_combats(self) -> list[MenuCombat]:
        return self.__menu_combats

    # =========================================================================

    def reorganise_menus(self,
                         number_of_menus: int) -> None:
        """
        Réorganise les menus de combat en fonction du nombre de menus donné.

        Paramètres :
        - number_of_menus : Nombre total de menus à organiser.
        """

        total_menu_height = (self.__menu_height + 10) * number_of_menus - 10

        self.__content_rect = pygame.Rect(
            (0, 0),
            (self.__content_rect.width, total_menu_height))

        self.__scrollable_container.set_scrollable_area_dimensions(
            self.__content_rect.size)

    # =========================================================================

    def get_next_menu_position(self) -> int:
        """
        Obtient la position y du prochain menu dans le conteneur.

        Retour :
        - int : Position y du prochain menu.
        """

        y_position = self.__menu_y
        self.__menu_y += self.__menu_height + 10

        return y_position

    # =========================================================================

    def draw(self) -> None:
        """
        Dessine le fond du conteneur sur la surface de la fenêtre.
        """

        self.__window_surface.blit(self.__container_background,
                                   self.__container_rect.topleft)

    # =========================================================================

    def reset_menu_y_position(self) -> None:
        """
        Réinitialise la position y du menu à 0.
        """

        self.__menu_y = 0

    # =========================================================================

    def kill(self) -> None:
        """
        Supprime le conteneur et nettoie les ressources.
        """

        self.__scrollable_container.kill()
        self.__window_surface = None
        self.__manager = None
        self.__content_rect = None

    # =========================================================================

    def add_combats_02(self,
                       player: Player,
                       monsters: List['Monster'],
                       menu_height: int) -> None:
        """
        Ajoute des menus de combat pour chaque monstre donné qui n'est pas
        déjà dans le menu.

        Paramètres :
        - player : L'objet joueur.
        - monsters : Liste des monstres.
        - menu_height : Hauteur du menu.
        """

        # syntaxe qui permet ..?
        existing_monsters = {menu.monster for menu in self.__menu_combats}

        for monster in monsters:
            if monster not in existing_monsters:
                y_position = self.get_next_menu_position()
                menu_combat = MenuCombat(
                    self.__window_surface,
                    manager=self.__manager,
                    relative_rect=pygame.Rect(
                        (10, y_position),
                        (210, menu_height)),
                    container=self.__scrollable_container,
                    monster=monster,
                    player=player)

                self.__menu_combats.append(menu_combat)

        self.reorganise_menus(len(monsters))

    # =========================================================================

    def remove_dead_monsters_02(self,
                                dead_monsters: List['Monster']) -> None:
        """
        Supprime les menus de combat des monstres morts.

        Paramètres :
        - dead_monsters : Liste des monstres morts.
        """

        to_remove_menus = []

        for monster in dead_monsters:
            for menu_combat in self.__menu_combats:
                if menu_combat.monster == monster:
                    menu_combat.kill()
                    to_remove_menus.append(menu_combat)
                    break

        for menu in to_remove_menus:
            if menu in self.__menu_combats:
                self.__menu_combats.remove(menu)

        self.reset_menu_y_position()

        for menu in self.__menu_combats:
            y_position = self.get_next_menu_position()
            menu.move(y_position)

    # =========================================================================

    def is_empty(self) -> bool:
        """
        Vérifie si le conteneur est vide.

        Retour :
        - bool : True si le conteneur est vide, False sinon.
        """

        return len(self.__menu_combats) == 0
