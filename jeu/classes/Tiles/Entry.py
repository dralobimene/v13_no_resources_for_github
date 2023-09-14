# classes/Tiles/Entry.py

import pygame
from typing import Tuple


class Entry:
    TILE_SIZE = 16
    BLUE = pygame.Color(0, 0, 255)
    TRANSPARENT_COLOR = pygame.Color(0, 0, 0, 0)

    def __init__(self,
                 position: Tuple[int, int]) -> None:
        self.__position = position

        self.__surface = pygame.Surface((Entry.TILE_SIZE, Entry.TILE_SIZE), pygame.SRCALPHA)
        self.__surface.fill(Entry.BLUE)

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
        pygame.draw.rect(self.__surface, self.BLUE, (0, 0, self.TILE_SIZE, self.TILE_SIZE))

    def to_dict(self):
        return {
            'position': self.__position
        }

    def __str__(self):
        return f"Entry: position={self.__position}"
