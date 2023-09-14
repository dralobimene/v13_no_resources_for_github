# Import the required libraries
import tkinter as tk
import subprocess
import sys
import os

from classes.ToolTip import ToolTip
from classes.utilitaires_01 import Utilitaires01

"""
Voici la ligne de commande que l'on doit executer pour lancer le programme.
Sinon les imports de classe ne fonctionneront pas.
Cela permet de ne pas toucher au PYTHONPATH ds le ~.bashrc
PYTHONPATH="/home/sambano/Documents/python/jeu/v2/jeu"
        python3.11 /home/sambano/Documents/python/jeu/v2/jeu/introduction.py
l'erreur ci-dessous par le linter n'est pas d'actualité
"""

"""
fenetre qui presente le menu du mode monoplayer
on peut
- retourner a l'introduct°
- creer son personnage
- lancer sa sauvegarde
"""


class Application(tk.Frame):
    """
    The main application class for managing the tkinter GUI for a
    monoplayer game.

    Attributes:
        master : The root window for the tkinter application.
        testing : Boolean variable for testing mode.
        button : The button widget to go back to the introduction screen.
        buttonToCreateCharacter : The button widget to navigate to the
        character creation screen.
        buttonToRunSave : The button widget to navigate to the save game
        screen.
    """

    def __init__(self,
                 master=None,
                 testing=False):
        """
        Constructor for the Application class.

        Parameters:
            master (tkinter.Tk, optional): The parent window. Defaults to None.
            testing (bool, optional): The mode of operation, True for
            testing mode, False for normal execution. Defaults to False.
        """

        super().__init__(master)
        self.master = master
        self.master.geometry('800x600')
        self.master.title('monoplayer_screen01.py')
        self.grid(padx=5,
                  pady=5)

        self.testing = testing

        # =====================================================================

        self.button = tk.Button(self,
                                text="Go back to introduction",
                                command=self.goto_screen01)

        self.button.grid(row=0,
                         column=0,
                         sticky='w')

        ToolTip(self.button,
                "Go back to introduction")

        # =====================================================================

        # Add a button which will close the current window and open the screen
        # to create the character

        self.buttonToCreateCharacter = tk.Button(self,
                                                 text="Create your character",
                                                 command=self.goto_monoplayer_screen02)

        self.buttonToCreateCharacter.grid(row=1,
                                          column=0,
                                          sticky='w')

        ToolTip(self.buttonToCreateCharacter,
                'Create your character')

        # =====================================================================

    def goto_screen01(self):
        """
        Closes the current window and opens the introduction screen.
        """

        if not self.testing:
            self.master.destroy()
        subprocess.run([sys.executable, 'introduction.py'],
                       check=True)

    # =========================================================================

    def goto_monoplayer_screen02(self):
        """
        Closes the current window and opens the character creation screen.
        """

        if not self.testing:
            self.master.destroy()
        subprocess.run([sys.executable,
                        os.path.join('monoplayer', 'monoplayer_screen02_create_character.py')],
                       check=True)

    # =========================================================================


def main():
    """
    The main entry point for the application.
    Creates an Application instance and starts the Tkinter event loop.
    """

    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
