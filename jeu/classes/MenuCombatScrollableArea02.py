import pygame
import pygame_gui
from typing import Tuple
from classes.MenuCombat02 import MenuCombat02
class MenuCombatScrollableArea02:
    def __init__(self,
                 window_surface: pygame.Surface,
                 manager: pygame_gui.UIManager,
                 container_rect_dimensions: Tuple[int, int, int, int],
                 content_rect_size: Tuple[int, int],
                 menu_height: int):

            self.__window_surface = window_surface
            self.__manager = manager
            self.__container_rect = pygame.Rect(*container_rect_dimensions)
            self.__menu_height = menu_height
            self.__menu_y = 0
            self.__container_background = pygame.Surface(self.__container_rect.size)
            self.__container_background.fill(pygame.Color('blue'))
            self.__content_rect = pygame.Rect((0, 0), content_rect_size)
            self.__scrollable_container = pygame_gui.elements.UIScrollingContainer(
                relative_rect=self.__container_rect,
                manager=self.__manager)
            self.__scrollable_container.set_scrollable_area_dimensions(
                    self.__content_rect.size)
            self.__menu_combats = []
            self.text_label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((10, 10), (280, 30)),  # Position and size
                text="",
                manager=manager,
                container=self.scrollable_container
            )
            self.__needs_redraw = True

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
    def menu_combats(self) -> list[MenuCombat02]:
        return self.__menu_combats

    def reorganise_menus(self,
                         number_of_menus):
        total_menu_height = (self.__menu_height + 10) * number_of_menus - 10
        self.__content_rect = pygame.Rect(
                (0, 0),
                (self.__content_rect.width, total_menu_height))
        self.__scrollable_container.set_scrollable_area_dimensions(
                self.__content_rect.size)
    def get_next_menu_position(self):
        y_position = self.__menu_y
        self.__menu_y += self.__menu_height + 10
        return y_position
    def draw(self):
        if self.__needs_redraw:
            self.__window_surface.blit(self.__container_background,
                                       self.__container_rect.topleft)
            self.__needs_redraw = False
    def show(self):
        self.__scrollable_container.show()
    def hide(self, surface):
        self.__scrollable_container.hide()
        surface.fill((0, 0, 0, 0), self.__container_rect)
    def reset_menu_y_position(self):
        self.__menu_y = 0
    def kill(self):
        self.__scrollable_container.kill()
        self.__window_surface = None
        self.__manager = None
        self.__content_rect = None
    def is_empty(self):
        return len(self.__menu_combats) == 0
    def update_text(self, new_text, monsters):
        self.text_label.set_text(new_text)
    def add_combats(self,
                player,
                monsters,
                menu_height):

        print("test")
        """
        self.__needs_redraw = True
        for menu_combat in self.__menu_combats:
            menu_combat.kill()
        self.__menu_combats = []
        self.reset_menu_y_position()
        for monster in monsters:
            y_position = self.get_next_menu_position()
            menu_combat = MenuCombat02(
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
        """
