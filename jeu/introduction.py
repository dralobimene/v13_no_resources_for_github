# introduction.py

import tkinter as tk
import subprocess
import sys

"""
Voici la ligne de commande que l'on doit executer pour lancer le programme.
Sinon les imports de classe ne fonctionneront pas.
Cela permet de ne pas toucher au PYTHONPATH ds le ~.bashrc
PYTHONPATH="/home/sambano/Documents/python/jeu/v2/jeu"
        python3.11 /home/sambano/Documents/python/jeu/v2/jeu/introduction.py
"""

from classes.ToolTip import ToolTip
from classes.utilitaires_01 import Utilitaires01
# usage:
# Utilitaires01.directory_exists('/some/path')


class Application(tk.Frame):
    """
    A class representing the main application window.

    Attributes:
        master (tk.Frame): The root window of the application.
        testing (bool): A flag to enable testing mode.
        image (ImageTk.PhotoImage): The image to be displayed on the button.
        button (tk.Button): A button widget containing the image.
    """

    def __init__(self,
                 master=None,
                 testing=False):
        """
        Initialize the Application.

        Parameters:
            master (tk.Frame): The root window of the application.
            testing (bool): A flag to enable testing mode.
        """

        super().__init__(master)
        self.master = master
        self.master.geometry('800x600')
        self.master.title('screen01 - introduction.py')
        self.grid(padx=5,
                  pady=5)

        self.testing = testing

        self.utils_01 = Utilitaires01()

        # =====================================================================

        self.button = tk.Button(self,
                                text='Go to screen 02', command=self.goto_screen02)

        self.button.grid(row=0,
                         column=0)

        # Add the tooltip to the button
        ToolTip(self.button,
                "Next step: Choose.")

        # =====================================================================

    def goto_screen02(self):
        """
        Close the current window and open the second screen.
        """

        if not self.testing:
            self.master.destroy()
        subprocess.run([sys.executable, 'screen02.py'], check=True)
        # self.utils_01.exit_and_run_script("screen02.py")


def main():
    """
    Entry point for the application.
    """

    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
