# utilitaires_01.py

import pygame

import os
import sys
import shutil
import json
import subprocess

from PIL import Image, ImageTk
from typing import Any, Optional, List

from classes.Tiles.Exit import Exit
from classes.Tiles.Entry import Entry


"""
N'oubliez pas que lorsque vous utilisez des méthodes statiques,
vous n'aurez pas accès aux variables
d'instance ou aux autres méthodes d'instance de la classe dans ces méthodes.
Si vous avez besoin
d'accéder à des données spécifiques à l'instance, vous devez envisager
d'utiliser des méthodes
d'instance à la place.
"""


class Utilitaires01:
    """
    pydoc de Utilitaires01:

    NOTE:
        01:
            PAS DE def __init__() ???
    """

    TILE_SIZE = 16

    # =========================================================================

    @staticmethod
    def directory_exists(self,
                         dir_path: str) -> bool:
        """
        Checks if the provided directory exists.

        Args:
            dir_path (str): The path to the directory.

        Returns:
            bool: True if the directory exists, False otherwise.
        usage:
            if directory_exists("/path/to/directory"):
                print("Directory exists.")
            else:
                print("Directory does not exist.")
        """
        return os.path.isdir(dir_path)

    # =========================================================================

    @staticmethod
    def create_folder(self,
                      path: str) -> None:
        """
        Creates a folder at the specified path.

        :param path: The path where the folder should be created
        :type path: str
        :raises FileExistsError: If the folder already exists
        :raises Exception: If any other exception occurs

        Usage
        path = 'my_folder'
        Utilitaires01.create_folder(path)
        """
        try:
            os.makedirs(path)
            print(f"Folder '{path}' created successfully")
        except FileExistsError as error1:
            print(f"Folder '{path}' already exists")
            raise error1
        except Exception as error2:
            print(f"An error occurred while creating the folder: {error2}")

    # =========================================================================

    @staticmethod
    def is_folder_empty(self,
                        folder_path: str) -> bool:
        """
        Checks whether the specified folder is empty or not.

        :param folder_path: Path to the directory to be checked.
        :type folder_path: str
        :return: True if the folder is empty, False otherwise.
        :rtype: bool
        :raises FileNotFoundError: If the specified folder does not exist.

        usage:
        if Utilitaires01.is_folder_empty("/path/to/folder"):
            print("The folder is empty")
        else:
            print("The folder is not empty")
        """

        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder {folder_path} does not exist.")

        return not bool(os.listdir(folder_path))

    # =========================================================================

    @staticmethod
    def empty_folder(self,
                     path: str) -> None:
        """
        Empties the contents of the specified folder.

        This function will remove all files and subdirectories inside the given
        folder without deleting the folder itself.

        :param path: The path to the folder that should be emptied.
        :type path: str
        :raises ValueError: If the path does not exist or is not a directory.
        :raises PermissionError: If the permissions on the file system
        do not allow deletion.

        usage
        Utilitaires01.empty_folder('/path/to/folder')
        """

        if not os.path.exists(path):
            raise ValueError("Path does not exist: " + path)

        if not os.path.isdir(path):
            raise ValueError("Path is not a directory: " + path)

        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    print("File deleted:", file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print("Directory deleted:", file_path)
            except Exception as error1:
                print('Failed to delete %s. Reason: %s' % (file_path, error1))

    # =========================================================================

    @staticmethod
    def draw_map_from_json(self,
                           file_path: str,
                           canvas) -> None:
        """
        Dessine une carte à partir d'un fichier JSON.

        :param file_path: Le chemin du fichier JSON à lire.
        :param canvas: Le canvas sur lequel dessiner la carte.
        """

        """
        Cette méthode dessine une carte à partir d'un fichier JSON.
        Elle vérifie d'abord si le dossier et le fichier spécifiés existent.
        Si ce n'est pas le cas, elle affiche un message d'erreur et quitte
        le programme. Ensuite, elle lit les données du fichier JSON et les
        dessine sur le canvas.

        - Dessine les tiles blanches et bleues.
        - Dessine la tile de sortie (classes/Tiles/Exit.py)
        - Affiche un fichier png qui represente une dalle.
        """

        folder_path = os.path.dirname(file_path)

        if not os.path.exists(folder_path):
            print("")
            print(f"The folder '{folder_path}' does not exist.")
            print("14101: Exit program")

            pygame.quit()
            sys.exit()

        if not os.path.exists(file_path):
            print("")
            print(f"The file '{file_path}' does not exist.")
            print("14050: Exit program")

            pygame.quit()
            sys.exit()

        with open(file_path, 'r') as file:
            data = json.load(file)

        #
        self.total_tiles_array = data["total_tiles_array"]

        for tile in self.total_tiles_array:
            x = tile['x']
            y = tile['y']
            w = tile['w']
            h = tile['h']
            if tile['color'] == 'white':
                pygame.draw.rect(canvas, self.WHITE, pygame.Rect(x, y, w, h))
            elif tile['color'] == 'blue':
                pygame.draw.rect(canvas, self.BLUE, pygame.Rect(x, y, w, h))

            # [REPERE 7 - 2]
            # Affiche le fichier .png de la dalle.
            # IL n'a y a pas de preload de l'image ce qui entraine
            # 1 ralentissement
            # Check if there's a 'image_path' key for the tile
            if 'dalle_png_path' in tile and os.path.exists(tile['dalle_png_path']):
                image = pygame.image.load(tile['dalle_png_path'])
                # Rescale the image if it doesn't match the tile's dimensions
                if image.get_width() != w or image.get_height() != h:
                    image = pygame.transform.scale(image, (w, h))
                canvas.blit(image, (x, y))

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # definir des tiles particulieres

        # tile sortie qui permet de passer au prochain stair
        # Check if "exit_tile" is in "data" variable
        if "exit_tile" in data:
            # Extract 'x' and 'y' from JSON
            x = data['exit_tile']['x']
            y = data['exit_tile']['y']

            # Create a Sortie instance
            sortie = Exit((x, y))

            # Draw sortie
            sortie.draw()
            canvas.blit(sortie.surface, sortie.position)
        else:
            print("")
            print("no exit_tile found in stair json file")
            print("13451: Exit program")

            pygame.quit()
            sys.exit()

        # tile entry qui permet de revenir au précédent stair
        # Check if "entry_tile" is in the data
        if "entry_tile" in data:
            # Extract 'x' and 'y' from JSON
            x = data['entry_tile']['x']
            y = data['entry_tile']['y']

            # Create a Entree instance
            entree = Entry((x, y))

            # Draw entree
            entree.draw()
            canvas.blit(entree.surface, entree.position)
        else:
            print("")
            print("no entry_tile found in stair json file")
            print("13452: Exit program")

            pygame.quit()
            sys.exit()
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # =========================================================================

    @staticmethod
    def load_image(self,
                   path: str,
                   size: tuple) -> ImageTk.PhotoImage:
        """
        Load and resize an image.

        Parameters:
            path (str): Path to the image file.
            size (tuple): Desired size of the image.

        Returns:
            ImageTk.PhotoImage: The resized image.
        """
        image = Image.open(path)
        image_resized = image.resize(size)
        photo = ImageTk.PhotoImage(image_resized)
        return photo

    # =========================================================================

    @staticmethod
    def get_key_value_from_json(file_path: str,
                                key: str) -> Optional[Any]:
        """
        Lit un fichier json et en extrait toutes les valeurs
        comprises ds la clé spécifiée.

        usage:
            file_path = "monoplayer/save/stairs_json/stair_10.json"
            key = "attributes_rooms_array"

            value = Utilitaires.get_key_value_from_json(file_path, key)

            print(value)
        """

        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get(key, None)

    # =========================================================================

    @staticmethod
    def list_files(directory: str) -> List[str]:
        """
        Cette méthode renvoie une liste des fichiers dans un répertoire.

        Paramètre:
        - directory: Le chemin du répertoire dont lister les fichiers.

        Renvoie une liste des noms des fichiers dans le répertoire,
        triés par la partie numérique de leur nom.
        """

        file_paths = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                # Ignore directories, only consider files
                if os.path.isfile(os.path.join(root, file)):
                    # Extract the filename without path
                    filename = os.path.basename(file)
                    file_paths.append(filename)

        ordered_file_paths = sorted(file_paths,
                                    key=Utilitaires01.sort_by_numeric_part)

        return ordered_file_paths

    # =========================================================================

    @staticmethod
    def sort_by_numeric_part(filename: str) -> int:
        """
        Cette méthode extrait la partie numérique d'un nom de
        fichier et la renvoie.

        Paramètre:
        - filename: Le nom de fichier à partir duquel extraire
        la partie numérique.

        Renvoie la partie numérique du nom de fichier en tant qu'entier.
        """

        # Extract the numeric part from the file name
        numeric_part = int(filename.split("_")[1].split(".")[0])

        #
        return numeric_part

    # =========================================================================

    @staticmethod
    def update_json_file_player(self,
                                key,
                                new_value) -> None:
        """
        Met à jour une clé dans le fichier "save_player.json"
        avec une nouvelle valeur.

        :param key: La clé à mettre à jour.
        :param new_value: La nouvelle valeur à définir.

        Cette méthode met à jour une clé dans le fichier "player.json" avec
        une nouvelle valeur. Elle vérifie d'abord si la clé existe dans le
        fichier. Si c'est le cas, elle met à jour la valeur de la clé et
        sauvegarde le fichier. Si la clé n'existe pas, elle affiche un message
        indiquant que la clé n'existe pas.
        """

        # Lire le fichier 'save_player.json'
        with open('monoplayer/save/save_player.json', 'r') as file:
            data = json.load(file)

        # Vérifier si la clé existe
        if key in data:
            # Mettre à jour la valeur de la clé
            data[key] = new_value

            # Réécrire le fichier 'save_player.json' avec la nouvelle valeur
            with open('monoplayer/save/save_player.json', 'w') as file:
                json.dump(data,
                          file,
                          indent=4)
                # print(f"'{key}' a été mis à jour avec la nouvelle valeur : {new_value}")
        else:
            print(f"La clé '{key}' n'existe pas dans 'save_player.json'.")
            print("On quitte le programme")
            pygame.quit()
            sys.exit()

    # =========================================================================
    @staticmethod
    def update_json_file_player_multiple_keys(key_value_pairs: dict) -> None:
        """
        Met à jour toutes clés dans le fichier "save_player.json"
        avec de nouvelles valeurs.

        :param key_value_pairs: Dictionnaire contenant les clés à mettre
        à jour et leurs nouvelles valeurs.

        Usage:
            Utilitaires01.update_multiple_keys(
                    {'key1': 'new_value1',
                     'key2': 'new_value2'}
                    )
        """

        # Lire le fichier 'save_player.json'
        with open('monoplayer/save/save_player.json', 'r') as file:
            data = json.load(file)

        updated_keys = []
        missing_keys = []

        for key, new_value in key_value_pairs.items():
            # Vérifier si la clé existe
            if key in data:
                # Mettre à jour la valeur de la clé
                data[key] = new_value
                updated_keys.append(key)
            else:
                missing_keys.append(key)

        # Réécrire le fichier 'save_player.json' avec les nouvelles valeurs
        with open('monoplayer/save/save_player.json', 'w') as file:
            json.dump(data,
                      file,
                      indent=4)

        # Print update summary
        if updated_keys:
            # print(f"Les clés suivantes ont été mises à jour: {', '.join(updated_keys)}")
            pass
        if missing_keys:
            # print(f"Les clés suivantes n'existent pas: {', '.join(missing_keys)}")

            pygame.quit()
            sys.exit()

    # =========================================================================

    def exit_and_run_script(self, script_name):
        print(f"Exécution du script : {script_name}")
        self.running = False
        pygame.quit()

        python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
        subprocess.run([python_version, script_name], check=True)

        sys.exit()
