# classes/Player.py

import pygame
from typing import Tuple, Dict, Union, List
from pygame import Color
from typing import Optional
import random
import time

from classes.utilitaires_01 import Utilitaires01
# usage:
# Utilitaires01.directory_exists('/some/path')

"""
NOTE:
    01:
        chatGPT:
            Issue with Position Setter:
                In the constructor (__init__), you have:
                [CODE]
                self.__position = pygame.Vector2(position['x'], position['y'])
                [/CODE]
                But the type hint for position is Tuple[int, int],
                and you're accessing it like a dictionary.
                You should unify the handling and type hints.
                Here's the fixed position setter and the relevant part
                from the constructor:
                [CODE]
                @property
                def position(self) -> Tuple[int, int]:
                    return int(self.__position.x), int(self.__position.y)

                @position.setter
                def position(self, position: Tuple[int, int]) -> None:
                    self.__position = pygame.Vector2(*position)
                [/CODE]
                And in the constructor:
                [CODE]
                self.__position = pygame.Vector2(*position)
                [/CODE]
    ===========================================================================
    ===========================================================================
    ===========================================================================
"""


# Constants
TRANSPARENT_COLOR = (0, 0, 0, 0)
PLAYER_COLOR = (0, 255, 0, 255)
TILE_SIZE = 16

# Constants for the different directions
VA_EN_HAUT = 'va_en_haut'
VA_A_DROITE = 'va_a_droite'
VA_EN_BAS = 'va_en_bas'
VA_A_GAUCHE = 'va_a_gauche'


class Player:
    """
    Represents a Player in the game.

    Attributes:
    - name: Player's name.
    - attack: Player's attack strength.
    - defense: Player's defense strength.
    - life: Player's life points.
    - position: 2D position of the player.
    - color: Player's color.
    - radius: Radius for the circle representation.
    - sprite_paths: Dictionary containing paths for player's
    movement animations.
    - speed: Player's movement speed.
    - stair_actuel: The current stair the player is on.
    """

    def __init__(self,
                 name: str,
                 attack: int,
                 defense: int,
                 life: int,
                 max_life_authorized: int,
                 position: Tuple[int, int] = (0, 0),
                 color: Tuple[int, int, int, int] = PLAYER_COLOR,
                 radius: int = 8,
                 speed: int = 16,
                 stair_actuel: str = "monoplayer/save/stairs_json/stair_1.json") -> None:
        self.__name = name
        self.__attack = attack
        self.__defense = defense
        self.__life = life

        # Sert pour la lifebar du player a l'initialisat° de celui-ci
        # ms aussi par exemple qd il boit une health potion.
        # L'attribut __life ne peut pas en tps normal, dépasser cette
        # valeur qui peut croitre ou decroitre selon que le self.player
        # gagne des niveaux, change de nature (race, ou espece ou autre).
        self.__max_life_authorized = max_life_authorized

        self.__position = pygame.Vector2(position['x'], position['y'])
        self.__color = color
        self.__radius = radius
        self.__speed = speed
        self.__stair_actuel = stair_actuel

        """
        Initialize the Player with given parameters.

        :param name: Player's name.
        :param attack: Player's attack strength.
        :param defense: Player's defense strength.
        :param life: Player's life points.
        :param position: Dictionary representing 2D position of the player.
        :param color: Player's color.
        :param radius: Radius for the circle representation.
        :param sprite_paths: Dictionary containing paths for player's movement animations.
        :param speed: Player's movement speed.
        :param stair_actuel: The current stair the player is on.
        """

        # ---------------------------------------------------------------------

        # Attributs qui ne font pas partie des parametres
        # du constructeur

        # pour dessiner l'instance
        self.__surface = pygame.Surface((2*self.__radius, 2*self.__radius),
                                        pygame.SRCALPHA)
        self.__surface.fill(TRANSPARENT_COLOR)

        # définit un tableau qui contient toutes les tiles
        # de la carte en récupérant la valeur de la clé "total_tiles_array"
        allowed_tiles_list = \
            Utilitaires01.get_key_value_from_json(self.__stair_actuel,
                                                  "total_tiles_array")
        self.__allowed_tiles = {(tile['x'], tile['y']) for
                                tile in allowed_tiles_list}

        # ---------------------------------------------------------------------

        # Définit si l'instance est en mvt.
        self.__moving = False

        # Définit une direct° par défaut à la creat° de l'instance.
        self.__current_direction = VA_EN_HAUT

        # ---------------------------------------------------------------------

        self.__original_defense = defense
        self.__defense_boostee = 100
        self.__defend_start_time: Optional[float] = None

        # ---------------------------------------------------------------------
    # =========================================================================

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self,
             name: str):
        self.__name = name

    @property
    def attack(self):
        return self.__attack

    @attack.setter
    def attack(self,
               attack: int):
        self.__attack = attack

    @property
    def defense(self):
        return self.__defense

    @defense.setter
    def defense(self,
                defense: int):
        self.__defense = defense

    @property
    def life(self):
        return self.__life

    @life.setter
    def life(self,
             life: int):
        self.__life = life

    @property
    def position(self) -> Tuple[int, int]:
        return int(self.__position.x), int(self.__position.y)

    @position.setter
    def position(self,
                 position: Tuple[int, int]) -> None:
        self.__position = position

    @property
    def color(self) -> Color:
        return self.__color

    @color.setter
    def color(self,
              color: Tuple[int, int, int, int]) -> None:
        self.__color = color

    @property
    def transparency(self) -> int:
        return self.__color[3]

    @transparency.setter
    def transparency(self,
                     alpha: int) -> None:
        self.color = (self.color[0], self.color[1], self.color[2], alpha)

    @property
    def radius(self) -> int:
        return self.__radius

    @radius.setter
    def radius(self,
               radius: int) -> None:
        self.__radius = radius

    @property
    def surface(self) -> pygame.Surface:
        return self.__surface

    @property
    def speed(self) -> int:
        return self.__speed

    @speed.setter
    def speed(self,
              speed: int) -> None:
        self.__speed = speed

    @property
    def stair_actuel(self) -> str:
        return self.__stair_actuel

    @stair_actuel.setter
    def stair_actuel(self,
                     stair_actuel: str) -> None:
        self.__stair_actuel = stair_actuel

    @property
    def allowed_tiles(self):
        return self.__allowed_tiles

    @allowed_tiles.setter
    def allowed_tiles(self,
                      allowed_tiled) -> None:
        self.__allowed_tiles = allowed_tiled

    @property
    def original_defense(self) -> int:
        return self.__original_defense

    @original_defense.setter
    def original_defense(self,
                         original_defense: int) -> None:
        self.__original_defense = original_defense

    @property
    def defense_boostee(self) -> int:
        return self.__defense_boostee

    @defense_boostee.setter
    def defense_boostee(self,
                        defense_boostee: int) -> None:
        self.__defense_boostee = defense_boostee

    @property
    def defend_start_time(self) -> Optional[float]:
        return self.__defend_start_time

    @defend_start_time.setter
    def defend_start_time(self,
                          defend_start_time: float) -> None:
        self.__defend_start_time = defend_start_time

    @property
    def max_life_authorized(self):
        return self.__max_life_authorized

    @max_life_authorized.setter
    def max_life_authorized(self,
                            max_life_authorized: int):
        self.__max_life_authorized = max_life_authorized

    # =========================================================================

    def va_en_haut(self):
        self.__moving = True
        self.__current_direction = VA_EN_HAUT
        new_position = self.__position.copy()
        new_position.y -= self.__speed
        return new_position

    def va_a_droite(self):
        self.__moving = True
        self.__current_direction = VA_A_DROITE
        new_position = self.__position.copy()
        new_position.x += self.__speed
        return new_position

    def va_en_bas(self):
        self.__moving = True
        self.__current_direction = VA_EN_BAS
        new_position = self.__position.copy()
        new_position.y += self.__speed
        return new_position

    def va_a_gauche(self):
        self.__moving = True
        self.__current_direction = VA_A_GAUCHE
        new_position = self.__position.copy()
        new_position.x -= self.__speed
        return new_position

    # =========================================================================

    def handle_events(self, event):
        """
        Handle movement based on key events.

        :param event: Pygame event to process.
        """

        #
        self.__moving = False

        if event.type == pygame.KEYDOWN:
            # Fait une copie de self.__position afin de permettre
            # le deplacement par comparaison
            new_position = self.__position.copy()

            # gest° des déplacements
            if event.key == pygame.K_UP:
                new_position = self.va_en_haut()
            elif event.key == pygame.K_DOWN:
                new_position = self.va_en_bas()
            elif event.key == pygame.K_LEFT:
                new_position = self.va_a_gauche()
            elif event.key == pygame.K_RIGHT:
                new_position = self.va_a_droite()

            # If you want to check for collisions or validate the new position,
            # you can do it here.

            # Check if the new position is inside self.__allowed_tiles.
            # Forbid to accross walls
            if (new_position.x, new_position.y) in self.__allowed_tiles:
                self.__position = new_position

    # =========================================================================

    def draw(self,
             surface: pygame.Surface) -> None:
        """
        Draw the player on the given surface.

        :param surface: Pygame surface to draw the player on.
        """

        # Clear the main surface
        surface.fill(TRANSPARENT_COLOR)

        # draw the circle
        pygame.draw.circle(surface,
                           self.__color,
                           (self.__radius, self.__radius),
                           self.__radius)

    # =========================================================================

    def attaquer(self,
                 other_player) -> None:
        damage_dealt = self.__attack - other_player.defense
        if damage_dealt > 0:
            damage = random.randint(1, 20)
            print("==========================================================")
            print(f"{self.__class__.__name__} attaque\n\
                    {other_player.__class__.__name__}:\n\
                    attaque: {self.attack}, \n\
                    defense: {other_player.defense}, \n\
                    attaque réussie, \n\
                    nom l'adversaire: {other_player.name},\n\
                    PV de l'adversaire avt dommage: {other_player.life}")
            other_player.life -= damage
            print(f"PV de l'adversaire apres dommage: {other_player.life}")
        else:
            print("==========================================================")
            print(f"{self.__class__.__name__} attaque\n\
                    {other_player.__class__.__name__}:\n\
                    attaque: {self.attack}, \n\
                    defense: {other_player.defense}, \n\
                    attaque échouée, \n\
                    nom l'adversaire: {other_player.name},\n\
                    PV de l'adversaire: {other_player.life}")

    def defendre(self) -> None:
        print("methode defendre de classes/Player.py")
        print("Boosting defense from", self.__defense,
              "to", self.__defense_boostee)
        self.__defense = self.__defense_boostee
        self.__defend_start_time = time.time()

    def update(self) -> None:
        if self.__defend_start_time and time.time() - self.__defend_start_time >= 1:
            self.__defense = self.__original_defense
            self.__defend_start_time = None

    # =========================================================================

    def to_dict(self) -> Dict[str, Union[int, Tuple[int, int], str]]:
        return {
            'name': self.__name,
            'attack': self.__attack,
            'defense': self.__defense,
            'life': self.__life,
            'max_life_authorized': self.__max_life_authorized,
            'position': self.position,
            'color': self.__color,
            'radius': self.__radius,
            'speed': self.__speed,
            'stair_actuel': self.__stair_actuel,
        }

    # =========================================================================

    def __str__(self) -> str:
        return f"Player(name={self.__name}, \n\
                attack={self.__attack}, \n\
                defense={self.__defense}, \n\
                life={self.__life}, \n\
                max_life_authorized={self.__max_life_authorized}, \n\
                position={self.position}, \n\
                color={self.__color}, \n\
                radius={self.__radius}, \n\
                speed={self.__speed}, \n\
                stair_actuel={self.__stair_actuel}"
