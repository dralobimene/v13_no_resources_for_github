# classes/Monster.py
# On ne peut pas importer classes/utilitaires_03.py ici

import sys
import pygame
import random
import time

from pygame import Color
from typing import Tuple, Dict, Union, List, Optional, TYPE_CHECKING

from classes.utilitaires_01 import Utilitaires01
# usage:
# Utilitaires01.directory_exists('/some/path')

# Constants
TRANSPARENT_COLOR = (0, 0, 0, 0)
MONSTER_COLOR = (0, 0, 0, 255)
TILE_SIZE = 16

# Constants for the different directions
VA_EN_HAUT = 'va_en_haut'
VA_A_DROITE = 'va_a_droite'
VA_EN_BAS = 'va_en_bas'
VA_A_GAUCHE = 'va_a_gauche'

# permet les imports circulaires
# voir le type fort ds le constructeur
if TYPE_CHECKING:
    from classes.MenuCombatScrollableArea03 import MenuCombatScrollableArea03

"""
NOTES:
    01:
        Présente 1 bug avec les png des fourmis. Elles st blanches
        qd elles vont vers la droite ou le haut.

    02:
        cls: paramètre conventionnel utilisé dans les méthodes
        de classe pour se référer à la classe elle-même, plutôt que à une
        instance de la classe

    03:
        lazy loading: ne charge la ressource qu'en cas de besoin.
        Exemple ds la methode de classe load_monsters_pictures().
        __monsters_pictures est initialement définie comme None.
        La méthode vérifie ensuite si cette variable est toujours None
        avant de tenter de charger les données depuis un fichier JSON.
        Si __monsters_pictures est déjà initialisée (c'est-à-dire, non-None),
        la méthode n'effectuera pas un autre chargement,
        ce qui est en fait le concept de Lazy Loading :
        charger la ressource seulement si elle est nécessaire.
"""


class Monster:

    # ---------------------------------------------------------------------

    def __init__(self,
                 attack: Optional[int] = None,
                 defense: Optional[int] = None,
                 life: Optional[int] = None,
                 position: Tuple[int, int] = (0, 0),
                 color: Tuple[int, int, int, int] = MONSTER_COLOR,
                 radius: int = 8,
                 speed: int = 16,
                 monster_type: Optional[str] = None,
                 name: Optional[str] = None) -> None:

        self.__attack = attack if attack is not None else random.randint(
            10, 100)
        self.__defense = defense if defense is not None else random.randint(
            10, 100)
        self.__life = life if life is not None else random.randint(10, 100)
        self.__position = pygame.Vector2(position['x'], position['y'])
        self.__color = color
        self.__radius = radius
        self.__speed = speed
        self.__name = name

        # ---------------------------------------------------------------------
        # Attributs qui ne font pas partie des parametres
        # du constructeur

        # pour dessiner l'instance
        self.__surface = pygame.Surface((2*self.__radius, 2*self.__radius),
                                        pygame.SRCALPHA)
        self.__surface.fill(TRANSPARENT_COLOR)

        # ---------------------------------------------------------------------

        # tps écoulé depuis le dernier mvt
        self.__last_move_time = time.time()

        # Détermine si cette instance peut se déplacer ou pas
        # utilisée ds la methode move()
        self.__can_move = True

        # ---------------------------------------------------------------------
        # Pour faire apparaitre les monstres à chaque stair.

        # Etape 1:
        # On recupere la paire clé => valeur
        # '__stair_actuel' du fichier monoplayer/save/save_player.json
        # pr pvoir ensuite ouvrir le fichier
        # monoplayer/save/stairs_json/stair_x.json concerné et dt on
        # récupère en dessous la paire 'total_tiles_array => value'.
        self.__stair_actuel = Utilitaires01.get_key_value_from_json(
            "monoplayer/save/save_player.json",
            "stair_actuel"
        )

        # Etape 2:
        # Contient toutes les tiles contenus ds la clé 'total_tiles_array'
        # du fichier 'monoplayer/save/stairs_json/stair_X.json' lu.
        # Les instances de classes/Monster.py ne pourront se déplacer
        # que sur ces tiles.
        # Le fichier json dt il faut extraire la paire est défini par
        # __srair_actuel.
        self.__allowed_tiles = Utilitaires01.get_key_value_from_json(
            self.__stair_actuel,
            "total_tiles_array"
        )

        # ---------------------------------------------------------------------

        # Définit une direct° par défaut à la creat° de l'instance.
        self.__current_direction = VA_EN_HAUT

        # ---------------------------------------------------------------------

        #
        self.__animation_imgs = None

        # ---------------------------------------------------------------------

        self.__last_attack_time = 0
        self.__is_attacking = False
        self.__attack_delay_timer = 0
        self.__should_attack = False

        # ---------------------------------------------------------------------

        # [REPERE 11 - 1]:
        # Posit° précédente qui permet de savoir si l'instance du monstre
        # va en haut, a droite, en bas ou  a gauche.
        # [REPERE 11 - 2] & [REPERE 11 - 3] ds la methode move() de ce fichier
        # [REPERE 11 - 4] ds le fichier classes/utilitaires_03.py
        self.__previous_position = pygame.Vector2(0, 0)

        #
        # if Monster.__monsters_pictures is None:
        #     Monster.load_monsters_pictures()

        self.__monster_type = monster_type

    # =========================================================================

    # =========================================================================
    # getters et setters des parametres et attributs (instance)

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
        self.__position = pygame.Vector2(position[0], position[1])

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
    def can_move(self) -> bool:
        return self.__can_move

    @can_move.setter
    def can_move(self, can_move: bool) -> None:
        self.__can_move = can_move

    @property
    def last_move_time(self) -> float:
        return self.__last_move_time

    @last_move_time.setter
    def last_move_time(self, last_move_time: float) -> None:
        self.__last_move_time = last_move_time

    @property
    def stair_actuel(self) -> str:
        return self.__stair_actuel

    @stair_actuel.setter
    def stair_actuel(self, stair_actuel: str) -> None:
        self.__stair_actuel = stair_actuel

    @property
    def allowed_tiles(self) -> List[Dict[str, int]]:
        return self.__allowed_tiles

    @allowed_tiles.setter
    def allowed_tiles(self, allowed_tiles: List[Dict[str, int]]) -> None:
        self.__allowed_tiles = allowed_tiles

    @property
    def current_direction(self) -> str:
        return self.__current_direction

    @current_direction.setter
    def current_direction(self, current_direction: str) -> None:
        self.__current_direction = current_direction

    @property
    def animation_imgs(self) -> Dict[str, List[pygame.Surface]]:
        return self.__animation_imgs

    @animation_imgs.setter
    def animation_imgs(self, animation_imgs: Dict[str, List[pygame.Surface]]) -> None:
        self.__animation_imgs = animation_imgs

    @property
    def current_frame(self) -> int:
        return self.__current_frame

    @current_frame.setter
    def current_frame(self, current_frame: int) -> None:
        self.__current_frame = current_frame

    @property
    def frame_count(self) -> int:
        return self.__frame_count

    @frame_count.setter
    def frame_count(self, frame_count: int) -> None:
        self.__frame_count = frame_count

    @property
    def frame_delay(self) -> int:
        return self.__frame_delay

    @frame_delay.setter
    def frame_delay(self, frame_delay: int) -> None:
        self.__frame_delay = frame_delay

    @property
    def name(self) -> Optional[str]:
        return self.__name

    @name.setter
    def name(self,
             name: Optional[str]) -> None:
        self.__name = name

    @property
    def last_attack_time(self) -> int:
        return self.__last_attack_time

    @last_attack_time.setter
    def last_attack_time(self,
                         last_attack_time: int) -> None:
        self.__last_attack_time = last_attack_time

    @property
    def is_attacking(self) -> bool:
        return self.__is_attacking

    @is_attacking.setter
    def is_attacking(self,
                     is_attacking: bool) -> None:
        self.__is_attacking = is_attacking

    @property
    def attack_delay_timer(self) -> int:
        return self.__attack_delay_timer

    @attack_delay_timer.setter
    def attack_delay_timer(self,
                           attack_delay_timer: int) -> None:
        self.__attack_delay_timer = attack_delay_timer

    @property
    def should_attack(self) -> bool:
        return self.__should_attack

    @should_attack.setter
    def should_attack(self,
                      should_attack: bool) -> None:
        self.__should_attack = should_attack

    # =========================================================================

    def draw(self,
             surface: pygame.Surface) -> None:
        """
        Draw the monster on the given Pygame surface.

        The method first clears the surface with transparency and then draws
        the monster as a circle on the surface.

        :param surface: Pygame surface on which the monster will be drawn
        """

        self.__surface.fill(TRANSPARENT_COLOR)

        pygame.draw.circle(self.__surface,
                           self.__color,
                           (self.__radius, self.__radius),
                           self.__radius)

    # =========================================================================

    def move(self) -> None:
        """
        Move the monster on the screen.

        The monster moves randomly within its allowed tiles, changing its
        position once every second. The new position is validated to be
        within the allowed tiles. If it can't find a valid position within
        100 attempts, the game exits.
        """

        # check if the monster can move
        if not self.__can_move:
            return

        # check if 1 second has passed
        if time.time() - self.__last_move_time >= 1:
            if self.__allowed_tiles is None:
                pygame.quit()
                sys.exit()

            # Define the range of movement
            move_range = TILE_SIZE

            # [REPERE 11 - 2]: Store the previous position
            self.__previous_position = self.__position.copy()

            # Limit number of tries to 100
            for _ in range(100):
                # Try to randomly change the Monster's position
                new_position = self.__position.copy()
                new_position.x += random.randint(-move_range, move_range)
                new_position.y += random.randint(-move_range, move_range)

                # Check if the new position is inside the allowed tiles
                for tile in self.__allowed_tiles:
                    if tile['x'] == new_position.x \
                            and tile['y'] == new_position.y:
                        # If it is, update the position and the time
                        # of the last movement
                        self.__position = new_position
                        self.__last_move_time = time.time()

                        # [REPERE 11 - 3]
                        # Now we compare the new and previous positions
                        delta_x = self.__position.x - self.__previous_position.x
                        delta_y = self.__position.y - self.__previous_position.y

                        if delta_x > 0:
                            # print(f"{self.name} va à droite.")
                            self.__current_direction = "va_a_droite"
                        elif delta_x < 0:
                            # print(f"{self.name} va à gauche.")
                            self.__current_direction = "va_a_gauche"
                        elif delta_y > 0:
                            # print(f"{self.name} va en bas.")
                            self.__current_direction = "va_en_bas"
                        elif delta_y < 0:
                            # print(f"{self.name} va en haut.")
                            self.__current_direction = "va_en_haut"

                        return

    # =========================================================================

    def attaquer(self,
                 other_player) -> None:
        print("==============================================================")
        print("Attaque de " + str(self.__name))
        self.__is_attacking = True
        if self.__attack <= other_player.defense:
            print("Attaque échouée")
            print("attaque: " + str(self.__attack) +
                  ", defense: " + str(other_player.defense))
        else:
            print("Attaque réussie")
            print("attaque: " + str(self.__attack) +
                  ", defense: " + str(other_player.defense))
            damage_dealt = random.randint(1, 10)
            other_player.life -= damage_dealt
            print("PV: " + str(other_player.life))
        print("==============================================================")

    # =========================================================================

    def decision_attaque(self,
                         player_instance) -> None:
        choix = random.randint(1, 2)
        if choix == 1:
            self.__should_attack = True
            self.__attack_delay_timer = 0
        elif choix == 2:
            pass
        else:
            print("PROBLEME 02:")
            raise ValueError("Choix non reconnu.")
            print("Fichier: classes/Monster.py")
            print("methode: decision_attaque()")

    # =========================================================================

    def update(self,
               time_passed,
               player_instance) -> None:
        self.__last_attack_time += time_passed
        if self.__should_attack:
            self.__attack_delay_timer += time_passed
            if self.__attack_delay_timer >= 1:
                self.attaquer(player_instance)
                self.__should_attack = False
                self.__attack_delay_timer = 0
        if self.__last_attack_time >= random.randint(2, 10):
            self.decision_attaque(player_instance)
            self.__last_attack_time = 0

    # =========================================================================

    def check_life(self) -> bool:
        if self.__life <= 0:
            print(f"{self.name} mort!")
            self.__life = 0
            # Ici, vous pouvez également ajouter d'autres logiques comme
            # retirer le monstre du jeu, etc
            return True
        return False

    # =========================================================================

    def to_dict(self) -> Dict[str, Union[int, Tuple[int, int], str]]:
        """
        Return a dictionary representation of the monster.

        The dictionary contains key-value pairs representing properties of
        the monster such as attack, defense, life, position, color, radius,
        and speed.

        :return: Dictionary containing monster's properties
        """

        return {
            'attack': self.__attack,
            'defense': self.__defense,
            'life': self.__life,
            'position': self.position,
            'color': self.__color,
            'radius': self.__radius,
            'sprite_paths': self.__sprite_paths,
            'speed': self.__speed,
            'can_move': self.__can_move,
        }

    # =========================================================================

    def __str__(self) -> str:
        """
        Return a string representation of the monster.

        The string includes the monster's attack, defense, life, position,
        color, radius, and speed, making it easy to print and log.

        :return: String representing the monster
        """

        return f"Monster(attack={self.__attack}, \n\
                defense={self.__defense}, \n\
                life={self.__life}, \n\
                position={self.position}, \n\
                color={self.__color}, \n\
                radius={self.__radius}, \n\
                speed={self.__speed}, \n\
                can_move={self.__can_move}, \n\
                name={self.__name}"
