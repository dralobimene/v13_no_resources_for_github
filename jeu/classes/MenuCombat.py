# classes/MenuCombat.py

import pygame
import pygame_gui

from classes.Player import Player
from classes.Monster import Monster

from pygame_gui.core import UIContainer


class MenuCombat:
    """
    Classe gérant l'interface utilisateur du menu de combat dans le jeu.

    Attributs:
        screen (pygame.Surface): Surface de l'écran du jeu.
        manager (pygame_gui.UIManager): Gestionnaire de l'interface
        utilisateur.
        relative_rect (pygame.Rect): Rectangle relatif définissant
        la position et la taille du menu.
        container (UIContainer): Conteneur de l'interface utilisateur
        pour les éléments du menu.
        monster (Monster): Le monstre avec lequel le joueur est en combat.
        player (Player): Le joueur en combat.
    """

    def __init__(self,
                 screen: pygame.Surface,
                 manager: pygame_gui.UIManager,
                 relative_rect: pygame.Rect,
                 container: UIContainer,
                 monster: Monster,
                 player: Player) -> None:
        """
        Initialise un nouveau menu de combat.

        Args:
            screen (pygame.Surface): Surface de l'écran du jeu.
            manager (pygame_gui.UIManager): Gestionnaire de
            l'interface utilisateur.
            relative_rect (pygame.Rect): Rectangle relatif pour le menu.
            container (UIContainer): Conteneur pour les éléments du menu.
            monster (Monster): Monstre en combat.
            player (Player): Joueur en combat.
        """

        self.__screen = screen
        self.__manager = manager
        self.__relative_rect = relative_rect
        self.__container = container
        self.__monster = monster
        self.__player = player

        # Attributs qui ne st pas des arguments du constructeur
        self.__x = relative_rect.x
        self.__y = relative_rect.y
        self.__attack_timer = 0.0
        self.__button1_disabled_timer = 0.0
        self.__button2_disabled_timer = 0.0
        self.__button1 = None
        self.__button2 = None
        self.__monster_label = None

        # Appel de methode ds le def __init__()
        self.setup_ui()

    # =========================================================================

    @property
    def screen(self) -> pygame.Surface:
        return self.__screen

    @screen.setter
    def screen(self,
               screen: pygame.Surface) -> None:
        self.__screen = screen

    @property
    def manager(self) -> pygame_gui.UIManager:
        return self.__manager

    @manager.setter
    def manager(self,
                manager: pygame_gui.UIManager) -> None:
        self.__manager = manager

    @property
    def relative_rect(self) -> pygame.Rect:
        return self.__relative_rect

    @relative_rect.setter
    def relative_rect(self,
                      relative_rect: pygame.Rect) -> None:
        self.__relative_rect = relative_rect

    @property
    def container(self) -> UIContainer:
        return self.__container

    @container.setter
    def container(self,
                  container: UIContainer) -> None:
        self.__container = container

    @property
    def monster(self) -> Monster:
        return self.__monster

    @monster.setter
    def monster(self,
                monster: Monster) -> None:
        self.__monster = monster

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self,
          x: int) -> None:
        self.__x = x

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self,
          y: int) -> None:
        self.__y = y

    @property
    def player(self) -> Player:
        return self.__player

    @player.setter
    def player(self,
               player: Player) -> None:
        self.__player = player

    @property
    def attack_timer(self) -> float:
        return self.__attack_timer

    @attack_timer.setter
    def attack_timer(self,
                     attack_timer: float) -> None:
        self.__attack_timer = attack_timer

    @property
    def button1_disabled_timer(self) -> float:
        return self.__button1_disabled_timer

    @button1_disabled_timer.setter
    def button1_disabled_timer(self,
                               button1_disabled_timer: float) -> None:
        self.__button1_disabled_timer = button1_disabled_timer

    @property
    def button2_disabled_timer(self) -> float:
        return self.__button2_disabled_timer

    @button2_disabled_timer.setter
    def button2_disabled_timer(self,
                               button2_disabled_timer: float) -> None:
        self.__button2_disabled_timer = button2_disabled_timer

    @property
    def button1(self) -> pygame_gui.elements.UIButton:
        return self.__button1

    @button1.setter
    def button1(self,
                button1: pygame_gui.elements.UIButton) -> None:
        self.__button1 = button1

    @property
    def button2(self) -> pygame_gui.elements.UIButton:
        return self.__button2

    @button2.setter
    def button2(self,
                button2: pygame_gui.elements.UIButton) -> None:
        self.__button2 = button2

    @property
    def monster_label(self) -> pygame_gui.elements.UILabel:
        return self.__monster_label

    @monster_label.setter
    def monster_label(self,
                      monster_label: pygame_gui.elements.UILabel) -> None:
        self.__monster_label = monster_label

    # =========================================================================

    def setup_ui(self) -> None:
        """
        Initialise les éléments de l'interface utilisateur pour le menu
        de combat.
        """

        btn1_rect = pygame.Rect((0, 0), (100, 25))
        btn2_rect = pygame.Rect((110, 0), (100, 25))

        monster_label_rect = pygame.Rect((220, 10), (110, 30))

        self.__button1 = pygame_gui.elements.UIButton(
            relative_rect=btn1_rect,
            text='Attaquer',
            manager=self.__manager,
            container=self.__container)

        self.__button2 = pygame_gui.elements.UIButton(
            relative_rect=btn2_rect,
            text='Defendre',
            manager=self.__manager,
            container=self.__container)

        self.__monster_label = pygame_gui.elements.UILabel(
            relative_rect=monster_label_rect,
            text=str(self.__monster.life) +
            " / " + str(self.__monster.attack) +
            " / " + str(self.__monster.defense),
            manager=self.__manager,
            container=self.__container)

        self.update_position()

    # =========================================================================

    # NOTE:
    # ne pas mettre de type fort a l'argument: event
    # ne trouve pas le module ou se trouve le UIEvent
    def handle_button_press(self,
                            event) -> None:
        """
        Gère les actions des boutons lorsqu'ils sont pressés.

        Args:
            event: Événement de l'interface utilisateur.

        Note:
            Le type de l'argument event n'est pas strictement défini car
            le module correspondant
            n'a pas été trouvé.
        """

        if event.ui_element == self.__button1:
            self.__button1.disable()
            self.__button1_disabled_timer = 1
            self.__player.attaquer(self.__monster)

            # print(f"\n--- After Attack ---")
            # print(f"Joueur Life: {self.__player.life}")
            # print(f"Monster Life: {self.__monster.life}")

        if event.ui_element == self.__button2:

            self.__button2.disable()
            self.__button2_disabled_timer = 1
            self.__player.defendre()

    # =========================================================================

    def kill(self) -> None:
        """
        Supprime tous les éléments de l'interface utilisateur
        associés à ce menu.
        """

        self.__button1.kill()
        self.__button2.kill()
        self.__monster_label.kill()

    # =========================================================================

    def move(self,
             new_y: int) -> None:
        """
        Déplace le menu à une nouvelle position en y.

        Args:
            new_y (int): Nouvelle position en y.
        """

        self.__y = new_y
        self.update_position()

    # =========================================================================

    def update_position(self) -> None:
        """
        Met à jour la position des éléments de l'interface utilisateur.
        """

        btn1_position = (self.__x, self.__y)
        btn2_position = (self.__x + 110, self.__y)
        monster_label_position = (self.__x + 220, self.__y)
        self.__button1.set_relative_position(btn1_position)
        self.__button2.set_relative_position(btn2_position)
        self.__monster_label.set_relative_position(monster_label_position)

    # =========================================================================

    def update(self,
               time_passed: float) -> None:
        """
        Met à jour l'état du menu de combat, y compris les compteurs de
        temps et les couleurs.

        Args:
            time_passed (float): Le temps écoulé depuis la dernière
            mise à jour.
        """

        if self.__monster.is_attacking:
            self.__monster_label.text_colour = pygame.Color('red')
            self.__monster_label.rebuild()
            self.__attack_timer += time_passed
            if self.__attack_timer >= 1:  # 1 seconde écoulée
                self.__monster.is_attacking = False
                self.__attack_timer = 0
                self.__monster_label.text_colour = pygame.Color('white')
                self.__monster_label.rebuild()

        if self.__button1_disabled_timer > 0:
            self.__button1_disabled_timer -= time_passed
            if self.__button1_disabled_timer <= 0:
                self.__button1.enable()

        if self.__button2_disabled_timer > 0:
            self.__button2_disabled_timer -= time_passed
            if self.__button2_disabled_timer <= 0:
                self.__button2.enable()

        # permet de mettre a jour la valeur de l'attribut life de
        # l'instance de classes/Monster.py
        self.__monster_label.set_text(str(self.__monster.life) +
                                      " / " +
                                      str(self.__monster.attack) +
                                      " / " +
                                      str(self.__monster.defense))
