# Import the required library
import tkinter as tk
import subprocess
import sys

"""
Voici la ligne de commande que l'on doit executer pour lancer le programme.
Sinon les imports de classe ne fonctionneront pas.
Cela permet de ne pas toucher au PYTHONPATH ds le ~.bashrc
PYTHONPATH="/home/sambano/Documents/python/jeu/v2/jeu" python3.11 /home/sambano/Documents/python/jeu/v2/jeu/introduction.py
l'erreur ci-dessous par le linter n'est pas d'actualité
"""

# Define a class for your application
class Application(tk.Frame):
    """
    This is the main application class for a tkinter GUI.

    Attributes:
        master (tkinter.Tk): The root window for the tkinter application.
        button (tkinter.Button): The button widget that navigates back
        to the introduction screen.

    master = typiquement le widget racine (la fenetre)
    """

    def __init__(self, master=None):
        """
        Constructor for the Application class.

        Parameters:
            master (tkinter.Tk, optional): The parent window. Defaults to None.
        """

        super().__init__(master)
        self.master = master
        self.master.geometry('800x600')
        self.master.title('monoplayer_screen03_run_save.py')
        self.grid(padx=5, pady=5)

        # Add a button which will close the current window and open the
        # second screen
        self.button = tk.Button(self,
                                text='Go to introduction',
                                command=self.goto_introduction)
        self.button.grid(row=0,
                         column=0)

    def goto_introduction(self):
        """
        Destroys the current window and opens the introduction screen.
        """

        self.master.destroy()
        subprocess.run([sys.executable, 'introduction.py'],
                       check=True)

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
