# screen02.py

import tkinter as tk
import subprocess
import sys
import os
from PIL import Image, ImageTk

from classes.ToolTip import ToolTip
from classes.utilitaires_01 import Utilitaires01
# usage:
# Utilitaires01.directory_exists('/some/path')

"""
Voici la ligne de commande que l'on doit executer pour lancer le programme.
Sinon les imports de classe ne fonctionneront pas.
Cela permet de ne pas toucher au PYTHONPATH ds le ~.bashrc
PYTHONPATH="/home/sambano/Documents/python/jeu/v2/jeu" python3.9
                    /home/sambano/Documents/python/jeu/v2/jeu/introduction.py
"""


class Application(tk.Frame):
    """
    The main application class for managing the tkinter GUI.

    Attributes:
        master : The root window for the tkinter application.
        button : The button widget to go back to the previous screen.
        monoplayer_button : The button widget to navigate to
        the monoplayer screen.
        multiplayer_button : The button widget to navigate to
        the multiplayer screen.
    """

    def __init__(self,
                 master=None):
        """
        Constructor for the Application class.

        Parameters:
            master (tkinter.Tk, optional): The parent window. Defaults to None.
        """

        super().__init__(master)
        self.master = master
        self.master.geometry('800x600')
        self.master.title('screen02.py')
        self.grid(padx=5,
                  pady=5)

        self.empty_space = tk.Label(self,
                                    width=2)

        self.empty_space.grid(row=0,
                              column=0,
                              sticky='w')

        # =====================================================================

        # Add a button which will close the current window and open
        # the introduction screen

        self.button = tk.Button(self,
                                text="Go back to introduction",
                                command=self.goto_screen01)

        self.button.grid(row=0,
                         column=1,
                         padx=15,
                         sticky='w')

        #
        ToolTip(self.button,
                "Go back to introduction")

        # =====================================================================

        # Add a button which will close the current window and
        # open the monoplayer screen

        self.monoplayer_button = tk.Button(self,
                                           text='Go to screen 02',
                                           command=self.goto_monoplayer_screen01)

        self.monoplayer_button.grid(row=1,
                                    column=1,
                                    padx=15,
                                    sticky='w')

        ToolTip(self.monoplayer_button,
                "Mode: monoplayer")

        # =====================================================================

    def goto_screen01(self):
        """
        Closes the current window and opens the introduction screen.
        """

        self.master.destroy()
        subprocess.run([sys.executable, 'introduction.py'],
                       check=True)

    # =========================================================================

    def goto_monoplayer_screen01(self):
        """
        Closes the current window and opens the monoplayer screen.
        """
        self.master.destroy()
        # assuming the monoplayer folder is in the same directory as your
        # current script
        subprocess.run([sys.executable,
                        os.path.join('monoplayer', 'monoplayer_screen01.py')],
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
