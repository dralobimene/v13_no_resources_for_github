# classes/ShapedButton.py

import pygame

from typing import Tuple, Optional


# Constants
TRANSPARENT_COLOR = (0, 0, 0, 0)


class ShapedButton:
    def __init__(self,
                 canvas_target,
                 width: int,
                 height: int,
                 offset_y: int = 0,
                 color: Optional[Tuple[int, int, int, int]] = None,
                 image_path: Optional[str] = None,
                 callback=None) -> None:
        self.__canvas_target = canvas_target
        self.__width = width
        self.__height = height
        self.__offset_y = offset_y
        self.__color = color
        self.__position = (0, 0)
        self.__image_path = image_path
        self.__callback = callback

        self.__surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.__surface.fill(TRANSPARENT_COLOR)

        self._draw()

    # =========================================================================

    @property
    def width(self) -> int:
        return self.__width

    @width.setter
    def width(self,
              width: int) -> None:
        self.__width = width
        self._draw()

    @property
    def height(self) -> int:
        return self.__height

    @height.setter
    def height(self,
               height: int) -> None:
        self.__height = height
        self._draw()

    @property
    def color(self) -> Optional[Tuple[int, int, int, int]]:
        return self.__color

    @color.setter
    def color(self,
              color: Optional[Tuple[int, int, int, int]]) -> None:
        self.__color = color
        self._draw()

    @property
    def position(self) -> Tuple[int, int]:
        return self.__position

    @position.setter
    def position(self,
                 position: Tuple[int, int]) -> None:
        self.__position = position

    @property
    def image_path(self) -> Optional[str]:
        return self.__image_path

    @image_path.setter
    def image_path(self,
                   path: Optional[str]) -> None:
        self.__image_path = path
        self._draw()

    # =========================================================================

    def _draw(self) -> None:
        """
        Methode protegée, destinée a être redéfinie ds les classes enfant.
        This will be overridden by the child classes to draw
        their respective shapes.
        """
        pass

    # =========================================================================

    def draw(self,
             target_surface: pygame.Surface) -> None:
        """
        Methode publique
        """

        #
        target_surface.blit(self.__surface, self.__position)

    # =========================================================================

    def move(self,
             dx: int,
             dy: int) -> None:

        x, y = self.__position
        x += dx
        y += dy
        self.__position = (x, y)

    # =========================================================================
    """
    def handle_event_SAUV(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            adjusted_y = 0
            if (self._ShapedButton__position[0] <= x <= self._ShapedButton__position[0] + self._ShapedButton__width and 
                self._ShapedButton__position[1] <= adjusted_y <= self._ShapedButton__position[1] + self._ShapedButton__height):
                return True
        return False
    """

    # =========================================================================

    def handle_event(self,
                     event: pygame.event.Event) -> bool:
        """
        Handle mouse button down events.

        Parameters:
            event (pygame.event.Event): The event to handle.

        Returns:
            bool: True if the event has been successfully handled;
            otherwise False.
        """

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            adjusted_y = 0
            x_condition = (
                self._ShapedButton__position[0] <= x <=
                self._ShapedButton__position[0] + self._ShapedButton__width
            )
            y_condition = (
                self._ShapedButton__position[1] <= adjusted_y <=
                self._ShapedButton__position[1] + self._ShapedButton__height
            )
            if x_condition and y_condition:
                return True
        return False
