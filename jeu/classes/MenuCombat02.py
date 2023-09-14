# classes/MenuCombat02.py
import pygame
import pygame_gui

from classes.Player import Player
from classes.Monster import Monster

from pygame_gui.core import UIContainer


class MenuCombat02:
    """
    Classe représentant le menu de combat en jeu.

    Attributes:
        screen (pygame.Surface): La surface de jeu.
        manager (pygame_gui.UIManager): Le gestionnaire d'interface utilisateur.
        relative_rect (pygame.Rect): La position et la taille du conteneur.
        container (UIContainer): Le conteneur d'éléments d'interface utilisateur.
        monster (Monster): Le monstre en combat.
        player (Player): Le joueur en combat.
    """

    def __init__(self,
                 screen: pygame.Surface,
                 manager: pygame_gui.UIManager,
                 relative_rect: pygame.Rect,
                 container: UIContainer,
                 monster: Monster,
                 player: Player):
        """
        Initialise une nouvelle instance de la classe MenuCombat02.

        ...
        """

        self.__screen = screen
        self.__manager = manager
        self.__relative_rect = relative_rect
        self.__container = container
        self.__monster = monster
        self.__player = player

        #  --------------------------------------------------------------------
        # Attributs qui ne st pas des arguments du contructeur.

        self.__x = relative_rect.x
        self.__y = relative_rect.y
        self.__attack_timer = 0.0
        self.__button1_disabled_timer = 0.0
        self.__button2_disabled_timer = 0.0
        self.__button1 = None
        self.__button2 = None
        self.__monster_label = None
        self.__needs_setup = True

        # Appel de methode depuis le constructeur.
        self.setup_ui()

    # ========================================================================

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

    @property
    def needs_setup(self):
        return self.__needs_setup

    @needs_setup.setter
    def needs_setup(self,
                    needs_setup: bool) -> None:
        self.__needs_setup = needs_setup

    # ========================================================================

    def setup_ui(self) -> None:
        """
        Configure l'interface utilisateur pour le menu de combat.
        """

        if not self.__needs_setup:
            return

        btn1_rect = pygame.Rect((0, 0), (100, 25))
        btn2_rect = pygame.Rect((110, 0), (100, 25))

        monster_label_rect = pygame.Rect((220, 10), (100, 30))

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
            text=self.__monster.name,
            manager=self.__manager,
            container=self.__container)

        self.update_position()

        self.__needs_setup = False

    # ========================================================================

    # NOTE:
    # ne pas mettre de type fort a l'argument: event
    # ne trouve pas le module ou se trouve le UIEvent
    def handle_button_press(self,
                            event) -> None:
        """
        Gère les événements de pression de bouton dans l'interface utilisateur.

        :param event: L'événement déclenché.
        """

        if event.ui_element == self.__button1:
            print("self_button1 presse")

        if event.ui_element == self.__button2:
            print("self.button2 presse")

    # ========================================================================

    def kill(self) -> None:
        self.__button1.kill()
        self.__button2.kill()
        self.__monster_label.kill()

    # ========================================================================

    def move(self,
             new_y: int) -> None:
        self.__y = new_y
        self.update_position()

    # ========================================================================

    def update_position(self) -> None:
        btn1_position = (self.__x, self.__y)
        btn2_position = (self.__x + 110, self.__y)
        monster_label_position = (self.__x + 220, self.__y)
        self.__button1.set_relative_position(btn1_position)
        self.__button2.set_relative_position(btn2_position)
        self.__monster_label.set_relative_position(monster_label_position)

    # ========================================================================

    def update(self,
               time_passed: float) -> None:
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
