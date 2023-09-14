# classes/Tiles/Exit.py

import pygame
from typing import Tuple


class Exit:
    TILE_SIZE = 16
    RED = pygame.Color(255, 0, 0)
    TRANSPARENT_COLOR = pygame.Color(0, 0, 0, 0)

    def __init__(self,
                 position: Tuple[int, int]) -> None:
        self.__position = position

        self.__surface = pygame.Surface((Exit.TILE_SIZE, Exit.TILE_SIZE), pygame.SRCALPHA)
        self.__surface.fill(Exit.RED)

    # Getter
    @property
    def position(self) -> Tuple[int, int]:
        return self.__position

    @property
    def surface(self):
        return self.__surface

    # Setter
    @position.setter
    def position(self, position: Tuple[int, int]) -> None:
        self.__position = position

    def draw(self) -> None:
        # clear the surface with transparency
        self.__surface.fill(self.TRANSPARENT_COLOR)
        # Draw the square
        pygame.draw.rect(self.__surface, self.RED, (0, 0, self.TILE_SIZE, self.TILE_SIZE))

    def to_dict(self):
        return {
            'position': self.__position
        }

    def __str__(self):
        return f"Exit: position={self.__position}"
