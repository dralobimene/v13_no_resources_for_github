import pygame
import pygame_gui

import sys
import os
import random
import math
import json
from collections import deque
from copy import deepcopy


from classes.DungeonGame import DungeonGame
from classes.KeyHandler import KeyHandler
from classes.FileProcessor import FileProcessor
from classes.EventManager import EventManager
from classes.Buttons.MenuButton import Button
from classes.Buttons.MoveMenuButton import MoveMenuButton
from classes.MenuCombatScrollableArea03 import MenuCombatScrollableArea03

from classes.utilitaires_01 import Utilitaires01
# usage:
# Utilitaires01.directory_exists('/some/path')

from classes.utilitaires_02 import Utilitaires02
from classes.utilitaires_03 import Utilitaires03
from classes.utilitaires_05_instantiate_buttons_callbacks import Utilitaires_05


"""
Voici la ligne de commande que l'on doit executer pour lancer le programme.
Sinon les imports de classe ne fonctionneront pas.
Cela permet de ne pas toucher au PYTHONPATH ds le ~.bashrc
PYTHONPATH="/home/sambano/Documents/python/jeu/v2/jeu"
        python3.11 /home/sambano/Documents/python/jeu/v2/jeu/introduction.py
"""


class Game:
    """
    A class representing the main game loop and operations for a dungeon game.

    Attributes:
        TRANSPARENT: A pygame Color object representing transparency.
        WHITE: A pygame Color object representing white color.
        BLACK: A pygame Color object representing black color.
        GREEN: A pygame Color object representing green color.
        BLUE: A pygame Color object representing blue color.
        YELLOW: A pygame Color object representing yellow color.
        RED: A pygame Color object representing red color.
        GREY: A pygame Color object representing grey color.
        TILE_SIZE: An integer representing the size of each tile in the game.
        SCREEN_WIDTH: An integer representing the width of window
        SCREEN_HEIGHT: An integer representing the height of window
        CANVASES_PRINCIPAUX_WIDTH: an integer representing the width of
            main canvases (maps, player, others)
        CANVASES_PRINCIPAUX_HEIGHT: an integer representing the height of
            main canvases (maps, player, others)
    """

    # colors
    TRANSPARENT = pygame.Color(0, 0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)
    BLACK = pygame.Color(0, 0, 0)
    GREEN = pygame.Color(0, 255, 0)
    BLUE = pygame.Color(0, 0, 255)
    YELLOW = pygame.Color(255, 255, 0)
    RED = pygame.Color(255, 0, 0)
    GREY = pygame.Color(128, 128, 128)
    GREY_LIGHT_01 = pygame.Color(224, 224, 224, 0)

    TILE_SIZE = 16

    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800

    CANVASES_PRINCIPAUX_WIDTH = 800
    CANVASES_PRINCIPAUX_HEIGHT = 600

    # =========================================================================

    def __init__(self):
        """
        Initializes the Game object with required attributes and pygame setup.
        """

        # Initialise tous les modules importés de Pygame.
        pygame.init()

        # Définit le titre de la fenêtre.
        pygame.display.set_caption('game/game.py')

        # Crée une fenêtre de 1200x800 pixels.
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,
                                               self.SCREEN_HEIGHT))

        # Initialise le gestionnaire d'interface utilisateur de pygame_gui,
        # qui permet de gérer les éléments de l'interface utilisateur.
        self.manager = pygame_gui.UIManager((self.SCREEN_WIDTH,
                                             self.SCREEN_HEIGHT))

        # Crée un objet d'horloge qui peut être utilisé pour
        # contrôler le taux de rafraîchissement du jeu
        self.clock = pygame.time.Clock()

        #
        self.player = None
        self.player_attributes = None

        #
        self.event_manager = EventManager(self)

        # definit le canvas chargé d'afficher la carte
        self.canvas01_maps = pygame.Surface((self.CANVASES_PRINCIPAUX_WIDTH,
                                             self.CANVASES_PRINCIPAUX_HEIGHT))
        self.canvas01_maps.fill(self.GREY)

        # définit le canvas chargé d'afficher l'instance du player
        self.canvas02_player = \
            pygame.Surface((self.CANVASES_PRINCIPAUX_WIDTH,
                            self.CANVASES_PRINCIPAUX_HEIGHT),
                           pygame.SRCALPHA, 32).convert_alpha()

        # définit le canvas chargé d'afficher les instances de
        # classes/Monster.py
        self.canvas03_monsters = \
            pygame.Surface((self.CANVASES_PRINCIPAUX_WIDTH,
                            self.CANVASES_PRINCIPAUX_HEIGHT),
                           pygame.SRCALPHA, 32).convert_alpha()

        # définit le canvas chargé d'afficher les instances de
        # classes/Monster.py
        self.canvas05_infos_diverses = \
            pygame.Surface((self.CANVASES_PRINCIPAUX_WIDTH,
                            self.CANVASES_PRINCIPAUX_HEIGHT),
                           pygame.SRCALPHA, 32).convert_alpha()

        # Définit le canvas chargé d'afficher les informat°.
        self.canvas04_informations = \
            pygame.Surface((self.CANVASES_PRINCIPAUX_WIDTH,
                            200))
        self.canvas04_informations.fill(self.WHITE)

        # ---------------------------------------------------------------------

        #
        self.utilitaires_05_for_canvas04_informations = \
                Utilitaires_05(self.canvas04_informations)

        # initialise une instance de classes/KeyHandler.py
        # pour la gest° d'evenements clavier qui ne st pas rattachés
        # à l'instance de classes/Player.py.
        self.key_handler = KeyHandler(
                self.player,
                game=self,
                utilitaires_05_for_canvas04_informations=self.utilitaires_05_for_canvas04_informations
                )

        # ---------------------------------------------------------------------

        #
        self.dungeon_map = None
        self.map_width = None

        # structures chargées de contenir les tiles selon
        # certaines spécificités
        self.total_tiles_array = None
        self.white_tiles_array = None
        self.blue_tiles_array = None
        self.rooms_tiles_array = None
        self.attributes_rooms_array = None

        # Initialise la 1° carte, le fichier du 1° stair
        # qd le player débute la partie (c'est forcément celui-ci)
        # [REPERE - 3 - étape 1]
        self.current_stair_path = "monoplayer/save/stairs_json/stair_1.json"

        # contient la liste des monstres
        self.liste_monsters = None

        # utilisées ds la methode 'check_collisions()'
        self.collision_detected = False
        self.previous_overlapping_monsters = []

        # ---------------------------------------------------------------------

        # Définir et faire apparaitre 1 bouton défini ds sa propre classe
        # avec un callback (defini ds classes/Utilitaires04Callbacks.py)
        # avec le classes/KeyHandler.py qui fait apparaitre le btn qd
        # on appuie sur F3.
        # [REPERE 5 - etape 1]
        # Définir à None.
        # Représentent des réfs aux boutons qui st définis ds
        # classes/utilitaires_05_instantiate_buttons_callbacks.py
        self.square01_button = None
        self.circle01_button = None
        self.triangle01_button = None
        self.square02_button = None

        # ---------------------------------------------------------------------

        # Initialise le menu courant a l'execution du programme.
        # Concerne le menu de test.
        self.current_menu = 'MENU01'

        # Définit le 1° menu de test.
        # Concerne le menu de test.
        self.menu01_buttons = [
            Button(820, 10, 100, 30, "BoutonA1", self.go_to_menu02),
            Button(820, 50, 100, 30, "BoutonA2", self.quit_program),
            Button(820, 90, 100, 30, "BoutonA3")
        ]

        # Définit le 2° menu de test.
        # Concerne le menu de test.
        self.menu02_buttons = [
            Button(820, 10, 100, 30, "BoutonB1"),
            Button(820, 50, 100, 30, "BoutonB2"),
            Button(820, 90, 100, 30, "BoutonB3", self.go_to_menu01)
        ]

        # ---------------------------------------------------------------------

        # Définit le move menu avec ses boutons.
        # Boutons:
        # avec 1 fleche qui va a droite
        # avec 1 fleche qui va en haut
        # avec 1 fleche qui va a gauche
        # avec 1 fleche qui va en bas

        # [REPERE - 6 - 1]
        # Définir le move menu avec ses boutons.
        # [REPERE - 6 - 2]
        # Rédiger les méthodes helper (wrapper)
        # [REPERE - 6 - 3]
        # Passez l'événement au gestionnaire d'événements de move_menu_button
        # [REPERE - 6 - 4]
        # Dessine le move menu avec ses boutons.

        self.move_menu_buttons = [MoveMenuButton(1100,
                                                 75,
                                                 "images/fleche_droite_01.png",
                                                 50,
                                                 50,
                                                 0,
                                                 self.player_move_right),
                                  MoveMenuButton(1050,
                                                 40,
                                                 "images/fleche_droite_01.png",
                                                 50,
                                                 50,
                                                 90,
                                                 self.player_move_up),
                                  MoveMenuButton(1000,
                                                 75,
                                                 "images/fleche_droite_01.png",
                                                 50,
                                                 50,
                                                 180,
                                                 self.player_move_left),
                                  MoveMenuButton(1050,
                                                 110,
                                                 "images/fleche_droite_01.png",
                                                 50,
                                                 50,
                                                 270,
                                                 self.player_move_down)
                                  ]

        # ---------------------------------------------------------------------

        # [REPERE - 8 - 1]
        # Etablir 1 menu de combat. 1 scroll area composée de menu de combat.
        # Pour chaque monstre rencontré. Les menus de combat sont chacun
        # composé de 2 boutons: "attaquer" et "défendre".
        self.is_updated_once = False
        self.container_rect = (810, 300, 380, 300)
        self.content_rect = (580, 800)
        self.menu_height = 60
        self.overlapping_monsters = set()
        self.current_collisions = set()
        self.current_collisions1 = set()
        self.previous_collisions = set()
        self.collision_count = 0
        self.current_collision_count = 0
        self.previous_collision_count = 0
        self.to_remove_monsters_menu_combat = []
        self.scrollable_menu = MenuCombatScrollableArea03(
                self.screen,
                self.manager,
                self.container_rect,
                self.content_rect,
                self.menu_height)

        # Rendre le menu invisible à l'execut° du programme.
        self.scrollable_menu_visible = False
        self.scrollable_menu.clear_content()

    # =========================================================================

    def go_to_menu01(self):
        self.current_menu = 'MENU01'

    def quit_program(self):
        self.running = False
        pygame.quit()
        sys.exit()

    def go_to_menu02(self):
        self.current_menu = 'MENU02'

    # =========================================================================

    # [REPERE - 6 - 2]

    def player_move_right(self):
        # This is a helper function to call the player's va_a_droite() method
        # On appelle ça un wrapper. Cela permet de s'assurer que..?

        # Ensure player exists
        if self.player:
            new_position = self.player.va_a_droite()
            if (new_position.x, new_position.y) in self.player.allowed_tiles:
                self.player.position = new_position

    def player_move_up(self):
        # This is a helper function to call the player's va_en_haut() method
        # On appelle ça un wrapper. Cela permet de s'assurer que..?

        # Ensure player exists
        if self.player:
            new_position = self.player.va_en_haut()
            if (new_position.x, new_position.y) in self.player.allowed_tiles:
                self.player.position = new_position

    def player_move_left(self):
        # This is a helper function to call the player's va_a_gauche() method
        # On appelle ça un wrapper. Cela permet de s'assurer que..?

        # Ensure player exists
        if self.player:
            new_position = self.player.va_a_gauche()
            if (new_position.x, new_position.y) in self.player.allowed_tiles:
                self.player.position = new_position

    def player_move_down(self):
        # This is a helper function to call the player's va_en_bas() method
        # On appelle ça un wrapper. Cela permet de s'assurer que..?

        # Ensure player exists
        if self.player:
            new_position = self.player.va_en_bas()
            if (new_position.x, new_position.y) in self.player.allowed_tiles:
                self.player.position = new_position

    # =========================================================================

    def is_reachable(self):
        """
        Cette méthode vérifie si toutes les tuiles dans `total_tiles_array`
        sont atteignables à partir d'une tuile choisie au hasard.
        Elle utilise un algorithme de remplissage par diffusion (flood fill)
        pour parcourir toutes les tuiles atteignables à partir de
        la tuile de départ.

        Retourne:
            True si toutes les tuiles sont atteignables, sinon False.
        """

        #
        if not self.total_tiles_array:
            return False

        # Choisis une tuile au hasard
        start_tile = random.choice(self.total_tiles_array)

        # Crée un ensemble de toutes les tuiles pour une recherche rapide
        all_tiles = set((tile["x"], tile["y"]) for tile
                        in self.total_tiles_array)

        # jeu de tuiles qui ont été atteintes
        # ensemble vide appelé reached_tiles.
        # un ensemble est une collection non ordonnée d'éléments uniques
        reached_tiles = set()

        # File d'attente pour le remplissage par diffusion
        # classe de la bibliothèque collections
        queue = deque([start_tile])

        while queue:
            # supprime le 1° elt de la 'queue'
            current_tile = queue.popleft()
            # si cette tile n'est pas ds le set reached_tile
            # alors elle est ajoutée au set (normal, à la 1° iteration,
            # la 1° tile ne peut pas etre ds le set)
            if (current_tile["x"], current_tile["y"]) not in reached_tiles:
                reached_tiles.add((current_tile["x"], current_tile["y"]))

                # Ajoute les voisins à la file d'attente
                for neighbor in self.get_neighbors(current_tile):
                    # si la tile est bien ds all_tiles alors
                    # on l'ajoute à la queue
                    if (neighbor["x"], neighbor["y"]) in all_tiles:
                        queue.append(neighbor)

        # Verifie si toutes les tuiles ont été atteintes
        return len(reached_tiles) == len(all_tiles)

    # =========================================================================

    def get_neighbors(self, tile):
        """
        Returns the neighboring tiles for a given tile.

        Args:
            tile (dict): A dictionary containing information about the tile.

        Returns:
            list: A list of dictionaries representing neighboring tiles.
        """

        x, y = tile['x'], tile['y']
        return [{"x": x - self.TILE_SIZE, "y": y},
                {"x": x + self.TILE_SIZE, "y": y},
                {"x": x, "y": y - self.TILE_SIZE},
                {"x": x, "y": y + self.TILE_SIZE}]

    # =========================================================================

    def get_rooms_tiles(self, white_tiles_array):
        """
        Retrieves room tiles from white tiles.

        Args:
            white_tiles_array (list): A list of dictionaries containing
            information about white tiles.

        Returns:
            list: A list of room tiles.
        """

        if not white_tiles_array:
            return []

        all_tiles = set((tile["x"], tile["y"]) for tile in white_tiles_array)
        visited_tiles = set()
        rooms = []

        for tile in white_tiles_array:
            if (tile["x"], tile["y"]) not in visited_tiles:
                room_tiles = set()
                queue = deque([tile])
                while queue:
                    current_tile = queue.popleft()
                    if (current_tile["x"], current_tile["y"]) not in visited_tiles:
                        visited_tiles.add((current_tile["x"], current_tile["y"]))
                        room_tiles.add((current_tile["x"], current_tile["y"]))

                        for neighbor in self.get_neighbors(current_tile):
                            if (neighbor["x"], neighbor["y"]) in all_tiles:
                                queue.append(neighbor)

                rooms.append(list(room_tiles))

        return rooms

    # =========================================================================

    def get_attributes_rooms(self, white_tiles_array):
        """
        Retrieves attributes of rooms from white tiles.

        Args:
            white_tiles_array (list): A list of dictionaries containing
            information about white tiles.

        Returns:
            list: A list of dictionaries containing attributes of rooms.
        """

        if not white_tiles_array:
            return []

        all_tiles = set((tile["x"], tile["y"]) for tile in white_tiles_array)
        visited_tiles = set()
        rooms = []

        for tile in white_tiles_array:
            if (tile["x"], tile["y"]) not in visited_tiles:
                room_tiles = set()
                queue = deque([tile])
                while queue:
                    current_tile = queue.popleft()
                    if (current_tile["x"], current_tile["y"]) not in visited_tiles:
                        visited_tiles.add((current_tile["x"], current_tile["y"]))
                        room_tiles.add((current_tile["x"], current_tile["y"]))

                        for neighbor in self.get_neighbors(current_tile):
                            if (neighbor["x"], neighbor["y"]) in all_tiles:
                                queue.append(neighbor)

                min_x = min(tile[0] for tile in room_tiles)
                max_x = max(tile[0] for tile in room_tiles)
                min_y = min(tile[1] for tile in room_tiles)
                max_y = max(tile[1] for tile in room_tiles)

                room_width = max_x - min_x + self.TILE_SIZE
                room_height = max_y - min_y + self.TILE_SIZE

                center_x = min_x + room_width / 2
                center_y = min_y + room_height / 2

                rooms.append({
                    "x": min_x,
                    "y": min_y,
                    "width": room_width,
                    "height": room_height,
                    "center": (center_x, center_y),
                    "tiles": list(room_tiles)
                })

        return rooms

    # =========================================================================

    def get_tile_arrays(self, tile_size=(TILE_SIZE, TILE_SIZE)):
        """
        Gets tile arrays for different tile colors.

        Args:
            tile_size (tuple): The size of the tile, defaults to TILE_SIZE.

        Returns:
            tuple: Three lists representing white tiles, blue tiles,
                    and total tiles.
        """

        white_tiles = []
        blue_tiles = []
        total_tiles = []

        for i in range(len(self.dungeon_map)):
            if self.dungeon_map[i] == 0:
                continue

            #
            map_x, map_y = (i % self.map_width, math.trunc(i / self.map_width))

            # Tableau qui va contenir ts les chemins des fichiers png
            # qui doivent être collés sur chacun des tuiles du donjon.
            icons_dalles_array = []

            # le nom et chemin des fichiers qui sont les .png des
            # dalles du donjon.
            icons_dalles_array.append("images/floor/dalle01.png")
            icons_dalles_array.append("images/floor/dalle02.png")
            icons_dalles_array.append("images/floor/dalle03.png")
            icons_dalles_array.append("images/floor/dalle04.png")

            # Choix aléatoire qui va définir la dalle qui sera collée
            # à la tile.
            random_chosen_dalle = random.choice(icons_dalles_array)

            # [REPERE 7 - 1]:
            # Constitution des paires clé => valeur
            # des 3 tableaux (avec l'ajout d'un fichier png aléatoire)
            # (voir ci-dessus)
            # total_tiles_array
            # white_tiles_array
            # blue_tiles_array
            # [ REPERE 7 - 2]:
            #           fichier: classes/Utilitaires01.py
            #           methode: draw_map_from_json()
            tile_info = {"x": map_x * tile_size[0],
                         "y": map_y * tile_size[1],
                         "w": tile_size[0],
                         "h": tile_size[1],
                         "center": ((map_x * tile_size[0]) + tile_size[0] / 2,
                                    (map_y * tile_size[1]) + tile_size[1] / 2),
                         "dalle_png_path": random_chosen_dalle,
                         }

            if self.dungeon_map[i] == 1:
                tile_info["color"] = "white"
                white_tiles.append(tile_info)
                total_tiles.append(tile_info)
            elif self.dungeon_map[i] == 2:
                tile_info["color"] = "blue"
                blue_tiles.append(tile_info)
                total_tiles.append(tile_info)

        return white_tiles, blue_tiles, total_tiles

    # =========================================================================
    def check_collisions(self):

        # Initialize flag for detecting collision in this frame
        collision_detected_this_frame = False

        # List to store monsters that overlap with the player in this frame
        current_collisions = set()

        # Check each monster's position against the player's position
        for monster in self.liste_monsters:
            if self.player.position == monster.position:
                collision_detected_this_frame = True
                current_collisions.add(monster)
                self.current_collisions1 = current_collisions
                monster.can_move = False

        print("current_collisions")
        print(current_collisions)
        print("self.current_collisions1")
        print(self.current_collisions1)

        # Increment collision count for new collisions and add to menu
        for monster in current_collisions:
            if monster not in self.previous_collisions:
                self.collision_count += 1
                self.scrollable_menu.create_additional_options(self.collision_count, monster.name)

        # Decrement collision count for collisions that no longer exist and remove from menu
        for monster in self.previous_collisions:
            if monster not in current_collisions:
                self.collision_count -= 1
                self.scrollable_menu.remove_additional_options(monster.name)

                # Réorganiser le menu.
                new_y = 0  # Initialiser la nouvelle position en y
                for remaining_monster in current_collisions:
                    print("BOUVLE FOR")
                    print("liste des monstres en collision")
                    print(remaining_monster.name)
                    self.scrollable_menu.update_option_position(new_y, remaining_monster.name)
                    new_y += self.scrollable_menu.menu_height
                    #self.manager.draw_ui(self.screen)
                    #pygame.display.update()

        # Update the previous_collisions set for the next frame
        self.previous_collisions = current_collisions

        # You may need to add additional logic here for handling the collision effects
        if self.collision_count <= 0:
            print("hide panel")
            self.scrollable_menu_visible = False
        else:
            print("display panel")
            self.scrollable_menu.draw()
            self.scrollable_menu_visible = True

        return collision_detected_this_frame
    # =========================================================================

    def process_player_movement(self,
                                direction):
        """
        QD ON APPUIE SUR LA BARRE ESPACE
        Methode qui permet selon que le player descend ds un stair inférieur
        ou remonte ds 1 stair supérieur de:
            - lire le fichier monoplayer/save/stairs_json/stair_X.json
            correspondant grâce à la classes/FileProcessor.
            - definir 2 override des attributs 'position' et 'stair_actuel'
            de l'instance de player
            - de récupérer ts les attributs de l'instance de classes/Player.py
            - de MAJ le fichier monoplayer/save/save_player.json
            - de creer 1 nvelle instance de classes/Player.py pour la placer
            sur la tile_entry définie ds le fichier
            'monoplayer/save/stairs_json_stair_1.json' du prochain stair
            visité
        """

        # Retrieve the names of all files located in
        # 'monoplayer/save/stairs_json'
        liste_fichiers_stairs = Utilitaires01.list_files("monoplayer/save/stairs_json")
        # liste_fichiers_stairs

        # Extract previous_element, current_element, next_element
        # with the File Processor
        # elts contains, for example,
        # ('No previous element', 'stair_1.json', 'stair_2.json')
        elts = (
                FileProcessor.process_next(
                    self,
                    liste_fichiers_stairs,
                    os.path.basename(self.player.stair_actuel)
                )
                if direction == "next"
                else FileProcessor.process_previous(
                    self,
                    liste_fichiers_stairs,
                    os.path.basename(self.player.stair_actuel)
                )
            )

        # Retrieve the name of the file representing the next or
        # previous element depending on the direction
        # elts[2]: next stair, le player descend d'1 stair
        # or
        # elts[0]: previous stair: le player remonte d'1 stair
        file_name = elts[2] if direction == "next" else elts[0]

        # Prefix it with the folder names
        # i.e., 'monoplayer/save/stairs_json'
        # print it
        complete_path = os.path.join('monoplayer/save/stairs_json', file_name)
        # complete_path

        # Redefine the variable which now contains
        # the address of the file describing the next stair.
        # [REPERE - 3 - étape 2]
        self.current_stair_path = complete_path

        # Update the file monoplayer/save/player.json
        # clé: "stair_actuel"
        # valeur: complete_path
        Utilitaires01.update_json_file_player(self,
                                              "stair_actuel",
                                              complete_path)

        # Read the file representing the next stair
        with open(complete_path, 'r') as f:
            data = json.load(f)

        # Get the value of the key 'exit_tile'
        next_exit_tile_value = data.get('exit_tile',
                                        'Key not found')
        # Value of next_exit_tile_value
        # next_exit_tile_value

        # Get the value of the key 'entry_tile'
        next_entry_tile_value = data.get('entry_tile',
                                         'Key not found')
        # value of next_entry_tile_value
        # next_entry_tile_value

        # Clear the canvas
        # The new stair is drawn in the method
        # render()
        # [REPERE - 3 - étape 3]
        self.canvas01_maps.fill((self.GREY))
        self.canvas02_player.fill((0, 0, 0, 0))
        self.canvas03_monsters.fill((0, 0, 0, 0))
        self.canvas04_informations.fill((self.WHITE))

        # ---------------------------------------------------------------------
        # etape 1
        # Définir un override de l'attribut 'position'
        # de l'instance de classes/Player.py
        position_override = {'x': next_entry_tile_value['x'],
                             'y': next_entry_tile_value['y']} \
                                     if direction == "next" else {'x': next_exit_tile_value['x'],
                                                                  'y': next_exit_tile_value['y']}

        # etape 2
        # On récupère tous les attributs de l'instance classes/Player.py
        player_attributes = self.player.to_dict()

        # etape 3
        # On MAJ le fichier monoplayer/save/save_player.json
        Utilitaires01.update_json_file_player_multiple_keys(player_attributes)

        # etape 4
        # On crée 1 instance de classes/Player.py
        # Create player with 2 overriding
        # overriden attributes:
        #   - position
        #   - stair_actuel
        self.player = Utilitaires02.create_player_from_saved_player_json(self,
                                                                         self.canvas02_player,
                                                                         position_override,
                                                                         complete_path)
        # ---------------------------------------------------------------------

        # MONSTERS
        self.liste_monsters = Utilitaires03.create_monsters(self,
                                                            complete_path,
                                                            menu_combat=self.scrollable_menu)
        print("Liste des monstres du stair")
        print("nbre d'elts: " + str(len(self.liste_monsters)))
        for monster in self.liste_monsters:
            print(monster.name)

        # ---------------------------------------------------------------------
        # Update the player in classes/key_handler.py.
        # this ensures that self.player in
        # classes/KeyHandler.py is a reference to the same object
        # as player in the handle_events() method, not
        # a separate object
        # methode set_player définie ds classes/KeyHandler.py [REPERE 4 - 2]
        # [REPERE 4 - 1]
        self.key_handler.set_player(self.player)

    # =========================================================================

    def handle_events(self):
        """
        Handles all the event handling during the game loop.
        """

        for event in pygame.event.get():

            # [REPERE - 8 - 2]
            self.manager.process_events(event)

            # -----------------------------------------------------------------
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # -----------------------------------------------------------------

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                # Gérer les actions de l'interface utilisateur ici
                # typiquement les collis° avec des boutons pygame pr le menu
                button = event.ui_element
                monster_name = self.scrollable_menu.get_monster_name(button)
                monster = None
                if monster_name:
                    monster = next((m for m in self.liste_monsters if m.name == monster_name), None)
                    if monster:
                        index = self.scrollable_menu.menu_combats.index(button)
                    if index % 2 == 0: # Cela suppose que les boutons d'attaque sont en premier
                        print(f"Monstre {monster_name} attaqué!")
                        self.player.attaquer(monster) # Appeler la méthode attaquer
                        if monster.check_life():
                            self.scrollable_menu.remove_additional_options(monster_name)
                            self.liste_monsters.remove(monster)
                            print("Liste des monstres du stair")
                            print("nbre d'elts: " + str(len(self.liste_monsters)))
                            for monster in self.liste_monsters:
                                print(monster.name)

                    else:
                        print(f"Le joueur défend contre le monstre {monster_name}")

            # -----------------------------------------------------------------
            if event.type == pygame.KEYDOWN:
                self.key_handler.handle_key_down(event.key)
                if event.key == pygame.K_F1:
                    self.key_handler.handle_F1_pressed()
                if event.key == pygame.K_F2:
                    self.key_handler.handle_F2_pressed()
                if event.key == pygame.K_F3:
                    self.key_handler.handle_F3_pressed()
                if event.key == pygame.K_F4:
                    self.key_handler.handle_F4_pressed()
                if event.key == pygame.K_SPACE:
                    print("SPACE key pressed from game/game.py")
            # -----------------------------------------------------------------
            if event.type == pygame.KEYUP:
                self.key_handler.handle_key_up(event.key)
                # -------------------------------------------------------------
                if event.key == pygame.K_F1:
                    self.key_handler.handle_F1_released()
                # -------------------------------------------------------------
                if event.key == pygame.K_F2:
                    self.key_handler.handle_F2_released()
                # -------------------------------------------------------------
                if event.key == pygame.K_F3:
                    self.key_handler.handle_F3_released()
                # -------------------------------------------------------------
                if event.key == pygame.K_F4:
                    self.key_handler.handle_F4_released(self.scrollable_menu)
                if event.key == pygame.K_a:
                    print("a presse")
                    if self.scrollable_menu_visible:
                        print("menu combat visible")
                        new_y = 10  # Mettez la valeur initiale de y ici
                        for monster in self.current_collisions1:
                            self.scrollable_menu.update_option_position(new_y, monster.name)
                            new_y += self.scrollable_menu.menu_height
                    else:
                        print("menu combat pas visible")
                # -------------------------------------------------------------
                if event.key == pygame.K_SPACE:
                    if self.player is not None:
                        # self.player pas None:
                        # player attributes from __str__ method
                        # str(self.player)
                        # le fichier " + self.player.stair_actuel
                        # est logiquement le fichier qui decrit le stair"

                        # ouvrir le fichier
                        # monoplayer/save/stairs_json/stair_X.json
                        # défini par l'attribut self.player.stair_actuel
                        # crée 1 variable "data" qui contient ttes les
                        # clé du fichier json lu
                        with open(self.player.stair_actuel, 'r') as f:
                            data = json.load(f)

                        # Obtenir depuis "data", la valeur de la clé
                        # "exit_tile"
                        exit_tile = data.get('exit_tile', 'Key not found')
                        # valeur de exit_tile"
                        # exit_tile

                        # Obtenir les coords comprises ds les valeurs
                        # contenues de la clé "exit_tile"
                        exit_tile_coords = [exit_tile['x'], exit_tile['y']]
                        # Coordonnées de l'actuelle exit_tile"
                        # exit_tile_coords

                        # Obtenir depuis "data", la valeur de la clé
                        # "entry_tile"
                        entry_tile = data.get('entry_tile', 'Key not found')
                        # valeur de entry_tile"
                        # entry_tile

                        # Obtenir les coords comprises ds les valeurs
                        # contenues de la clé "entry_tile"
                        entry_tile_coords = [entry_tile['x'], entry_tile['y']]
                        # Coordonnées de l'actuelle entry_tile"
                        # entry_tile_coord

                        # comparaison entre 1 tuple et 1 list,
                        # Il faut en convertir l'1 des 2 ds le
                        # format de l'autre (ici comparaison de 2 list)
                        if list(self.player.position) == exit_tile_coords:
                            print("Player on the exit_tile.")
                            self.process_player_movement("next")

                        # comparaison entre 1 tuple et 1 list,
                        # Il faut en convertir l'1 des 2 ds le
                        # format de l'autre (ici comparaison de 2 list)
                        elif list(self.player.position) == entry_tile_coords:
                            print("Player on the entry_tile.")
                            self.process_player_movement("previous")
                        else:
                            print("Player is on a regular tile.")
                    else:
                        print("player None")
                        print("86303: Erreur program")

                        pygame.quit()
                        sys.exit()

            # -----------------------------------------------------------------

            # Autres gestionnaires d'événements
            if self.player is not None:
                # Update the player_attributes dictionary
                # with the updated position
                # MAJ la position du player des le debut du jeu
                # [REPERE - 1]
                self.player_attributes['position'] = self.player.position

                # importe le gestionnaire des touches défini
                # ds classes/Player.py
                self.player.handle_events(event)

            # -----------------------------------------------------------------

            # pour les menus du jeu
            if self.current_menu == 'MENU01':
                for button in self.menu01_buttons:
                    button.handle_event(event)
            elif self.current_menu == 'MENU02':
                for button in self.menu02_buttons:
                    button.handle_event(event)

            # -----------------------------------------------------------------

            # Définir et faire apparaitre 1 bouton défini ds sa propre classe
            # avec un callback (defini ds classes/Utilitaires04Callbacks.py)
            # avec le classes/KeyHandler.py qui fait apparaitre le btn qd
            # on appuie sur F3
            # [REPERE 5 - etape 3]
            # checker existence du btn avt de gérer ses events
            if self.square01_button and self.square01_button.handle_event(event):
                continue
            if self.circle01_button and self.circle01_button.handle_event(event):
                continue
            if self.triangle01_button and self.triangle01_button.handle_event(event):
                continue
            if self.square02_button and self.square02_button.handle_event(event):
                continue

            # -----------------------------------------------------------------
            # Pass the event to the move_menu_button's event handler
            # Passez l'événement au gestionnaire d'événements de move_menu_button
            # [REPERE - 6 - 3]
            for button in self.move_menu_buttons:
                button.handle_event(event)
    # =========================================================================

    def update(self, time_delta):
        self.manager.update(time_delta)

        self.check_collisions()
        #pygame.display.update()
        #self.manager.draw_ui(self.screen)

    # =========================================================================

    def render(self):
        """
        Renders the game to the screen.
        """

        # afficher l'ecran, fond noir
        self.screen.fill(self.GREY_LIGHT_01)

        # ---------------------------------------------------------------------

        # dessiner le stair en fonction du fichier qui décrit le stair.
        # (il s'agit du 2nd parametre, définit ds le __init__ et
        # redéfinit ensuite dans la méthode handle_events())
        # [REPERE - 3 - étape 4]
        Utilitaires01.draw_map_from_json(self,
                                         self.current_stair_path,
                                         self.canvas01_maps)

        # Dessiner les objets du jeu, les sprites, etc.

        # ---------------------------------------------------------------------
        # blit le canvas01_maps sur le screen
        self.screen.blit(self.canvas01_maps, (0, 0))
        # ---------------------------------------------------------------------
        # Draw the player onto the specific canvas
        self.player_x, self.player_y = self.player.position
        self.player.draw(self.canvas02_player)
        # ---------------------------------------------------------------------
        # Blit the player's canvas onto the main screen at
        # the player's position
        self.screen.blit(self.canvas02_player, (self.player_x, self.player_y))
        # ---------------------------------------------------------------------
        # Clear the monster surface
        self.canvas03_monsters.fill((0, 0, 0, 0))

        #
        for monster in self.liste_monsters:
            monster.move()
            monster.draw(self.canvas03_monsters)
            self.canvas03_monsters.blit(monster.surface, monster.position)
        #
        self.screen.blit(self.canvas03_monsters, (0, 0))
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        # Définir et faire apparaitre 1 bouton défini ds sa propre classe
        # avec un callback (defini ds classes/Utilitaires04Callbacks.py)
        # avec le classes/KeyHandler.py qui fait apparaitre le btn qd
        # on appuie sur F3
        # [REPERE 5 - etape 4]
        # Checker existence du btn avt de le dessiner et de la blitter
        # sur son canvas
        if self.square01_button:
            self.square01_button.draw(self.canvas04_informations)

        if self.circle01_button:
            self.circle01_button.draw(self.canvas04_informations)

        if self.triangle01_button:
            self.triangle01_button.draw(self.canvas04_informations)

        if self.square02_button:
            self.square02_button.draw(self.canvas04_informations)

        self.screen.blit(self.canvas04_informations,
                         (0, self.canvas01_maps.get_height()))
        # ---------------------------------------------------------------------

        # Dessine les boutons du menu générique de test.
        if self.current_menu == 'MENU01':
            for button in self.menu01_buttons:
                button.render(self.screen)
        elif self.current_menu == 'MENU02':
            for button in self.menu02_buttons:
                button.render(self.screen)

        # ---------------------------------------------------------------------

        # [REPERE - 6 - 4]
        # Dessine le move menu avec ses boutons.
        for button in self.move_menu_buttons:
            button.render(self.screen)

        # ---------------------------------------------------------------------
        if self.scrollable_menu_visible is False:
            pass
        else:
            self.manager.draw_ui(self.screen)
            pygame.display.update()
        #self.manager.draw_ui(self.screen)
        #pygame.display.update()

    # =========================================================================

    def run_game(self):
        """
        Main game loop that initializes, updates, and renders the game.
        - 3 verifs
        - efface eventuellement des fichiers qui ne devraient plus exister
        - genere les fichiers json de chacun des stairs
        - 1 vérif
        - cree et place l'instance de classes/Player.py sur une tile blanche
        - boucle principale
        """

        # ---------------------------------------------------------------------
        # verifier que le dossier monoplayer/save existe
        if Utilitaires01.directory_exists(self, 'monoplayer/save'):
            print("Folder monoplayer/save exists, we continue")
        else:
            print("Folder monoplayer/save/stairs_json does not exists")
            print("QUIT GAME")
            pygame.quit()
            sys.exit()
        # ---------------------------------------------------------------------
        # Check if file monoplayer/save/save_player.json exists
        if os.path.isfile("monoplayer/save/save_player.json"):
            print("File monoplayer/save/save_player.json already exists.")
        else:
            print("File monoplayer/save/save_player.json does not exist.")
            print("QUIT GAME")
            pygame.quit()
            sys.exit()
        # ---------------------------------------------------------------------
        # verifier que le dossier monoplayer/save/stairs_json" existe
        if os.path.exists("monoplayer/save/stairs_json"):
            print("The monoplayer/save/stairs_json directory exists.")
        else:
            print("The monoplayer/save/stairs_json directory does not exist.")
            print("QUIT GAME")
            pygame.quit()
            sys.exit()
        # ---------------------------------------------------------------------
        # effacer les eventuels fichiers presents
        # ds le dossier monoplayer/save/stairs_json
        files_in_save_folder = os.listdir('monoplayer/save/stairs_json')

        if len(files_in_save_folder) == 0:
            print("The monoplayer/save/stairs_json folder is empty.")
        else:
            print("The monoplayer/save/stairs_json folder is not empty.")
            print("content deletion")

            for file in files_in_save_folder:
                file_path = os.path.join('monoplayer/save/stairs_json', file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            print("All files have been removed")
            print("from the 'monoplayer/save/stairs_json' folder.")
        # ---------------------------------------------------------------------
        # generat° des fichiers json de chacun des stairs
        # localisat° dans monoplayer/save/stairs_json
        # index_fichiers:
        #   sert a nommer les fichiers json sous forme stair_X.json
        # created_files:
        #   contient le nom de chacun des fichier généré
        #   sert pour verificat°
        # not_created_files:
        #   contient le nom de chacun des fichier qui n'a pas été généré
        #   (a cause de is_reachable())

        # variables
        index_fichiers = 1
        created_files = []
        not_created_files = []

        # la boucle qui génère les fichiers json
        for i in range(1, 11):
            # définit les cartes (les fichiers json de chacun des stairs)
            dungeon_game = DungeonGame(self.CANVASES_PRINCIPAUX_WIDTH,
                                       self.CANVASES_PRINCIPAUX_HEIGHT)

            #
            self.dungeon_map, self.map_width, _ = dungeon_game.generate_next_map()

            #
            self.white_tiles_array, self.blue_tiles_array, self.total_tiles_array = self.get_tile_arrays()
            self.rooms_tiles_array = self.get_rooms_tiles(self.white_tiles_array)
            self.attributes_rooms_array = self.get_attributes_rooms(self.white_tiles_array)

            # fait 1 copie exacte de self.white_tiles_array pr ds la
            # prochaine boucle pvoir definir la tile entree
            # de chacun des stairs
            # [REPERE - 2]
            white_tiles_array_copy = deepcopy(self.white_tiles_array)

            # crée le json dict si ttes les tuiles du stair st atteignables
            if self.is_reachable():

                # Choose a random element to set exit for each stair
                # from self.white_tiles_array
                chosen_dict_to_set_exit_tile = random.choice(self.white_tiles_array)

                # pr definir l'entree, il faut etre sur que les tiles entree
                # et sortie ne soient pas les memes. Dc pr definir la tile
                # entree, il faut d'abord faire une copie exacte du tableau
                # self.white_tiles_array, (fait au-dessus, en dehors de la
                # boucle, qd on definit les array([REPERE - 2]))
                # supprimer la tile qui a servi a definir la sortie
                # choisir alors 1 tile au hasard pr definir la tile entree
                white_tiles_array_copy.remove(chosen_dict_to_set_exit_tile)
                chosen_dict_to_set_entry_tile = random.choice(white_tiles_array_copy)

                # on cree 1 variable particuliere pr le 1° stair qui
                # permet de positionner + tard, le joueur au meme
                # emplacement que la "entry_tile"
                if index_fichiers == 1:
                    tile_spe_entry_tile_first_stair = chosen_dict_to_set_entry_tile

                # Creer le json dict qui décrit le stair
                json_dict = {
                    "file": f"monoplayer/save/stairs_json/stair_{index_fichiers}.json",
                    "name": f"stair_{index_fichiers}",
                    "level": f"{index_fichiers}",
                    "exit_tile": chosen_dict_to_set_exit_tile,
                    "entry_tile": chosen_dict_to_set_entry_tile,
                    "total_tiles_array": self.total_tiles_array,
                    "white_tiles_array": self.white_tiles_array,
                    "blue_tiles_array": self.blue_tiles_array,
                    "rooms_tiles_array": self.rooms_tiles_array,
                    "attributes_rooms_array": self.attributes_rooms_array,
                    }

                # définition des noms de chacun des fichiers
                file_name = f'monoplayer/save/stairs_json/stair_{index_fichiers}.json'

                # ecriture de chacun des fichiers
                with open(file_name, 'w') as f:
                    json.dump(json_dict,
                              f,
                              indent=4)

                # si le fichier json est crée,
                # ajout de son nom au tableau
                created_files.append(file_name)

                # incrémentat° pr permettre un nom de fichier unique
                # exemple monoplayer/save/stairs_json/stair_X.json
                index_fichiers += 1
            else:
                # si le fichier json n'est pas crée,
                # ajout de son nom au tableau
                not_created_file = f'stair_{index_fichiers}'
                not_created_files.append(not_created_file)
        # ---------------------------------------------------------------------
        # Vérificat°:
        # le tableau created_files doit contenir au - 1 elt
        # sinon, on quitte le jeu
        if len(created_files) == 0:
            pygame.quit()
            sys.exit()
        else:
            print("Created files:")
            for file_name in created_files:
                print(file_name)
        # ---------------------------------------------------------------------
        # Creer et placer l'instance de player

        # Get the white_tiles_array_from_json using the method
        # on placera ensuite l'instance de player sur une tile tirée au hasard
        # depuis ce tableau
        white_tiles_array_from_json = Utilitaires01.get_key_value_from_json(
                        file_path="monoplayer/save/stairs_json/stair_1.json",
                        key="white_tiles_array")

        # Check if the array is not empty
        if white_tiles_array_from_json \
                and len(white_tiles_array_from_json) > 0:

            # Use 'position_override'when creating the instance
            # of the player to place the instance onto 'entry_tile' to
            # first stair
            position_override = {'x': tile_spe_entry_tile_first_stair['x'],
                                 'y': tile_spe_entry_tile_first_stair['y']}
            self.player = Utilitaires02.create_player_from_saved_player_json(
                                        self,
                                        self.canvas02_player,
                                        position_override)

            # On doit déclarer un
            # dictionnaire json vide pour à la prochaine itérat° de la
            # boucle principale
            # pouvoir stocker l'attribut 'position' de
            # self.player_attributes['position'] (defini au [REPERE - 1]).
            # Déclare un dictionnaire json vide pour contenir les
            # attributs de l'instance de classes/Player.py
            self.player_attributes = {}

            # Accède à l'attribut player de la classe classes/KeyHandler.py
            # et lui fournit les attributs de l'instance self.player
            # de cette manière depuis classes/KeyHandler.py, on peut
            # afficher les attributs de l'instance du player
            self.key_handler.player = self.player

        else:
            print("Error: Could not find valid start tile.")
            pygame.quit()
            sys.exit()

        # ---------------------------------------------------------------------
        # creer la liste des monstres pour le 1° stair
        self.liste_monsters = Utilitaires03.create_monsters(
                self,
                "monoplayer/save/stairs_json/stair_1.json",
                menu_combat=self.scrollable_menu
                )
        print("Liste des monstres du stair")
        print("nbre d'elts: " + str(len(self.liste_monsters)))
        for monster in self.liste_monsters:
            print(monster.name)

        # BOUCLE PRINCIPALE
        running = True
        while running:
            time_delta = self.clock.tick(60) / 1000.0
            self.handle_events()
            self.update(time_delta)
            self.render()
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run_game()
