# Import the required libraries
import subprocess
import sys
import tkinter as tk

"""
Voici la ligne de commande que l'on doit executer pour lancer le programme.
Sinon les imports de classe ne fonctionneront pas.
Cela permet de ne pas toucher au PYTHONPATH ds le ~.bashrc
PYTHONPATH="/home/sambano/Documents/python/jeu/v2/jeu" python3.11 /home/sambano/Documents/python/jeu/v2/jeu/introduction.py
"""


# Define a class for your application
class Application(tk.Frame):
    """
    This is the main Application class for a tkinter GUI.
    It represents the multiplayer screen.

    Attributes:
        master (tkinter.Tk): The root window for the tkinter application.
        button (tkinter.Button): The button widget that navigates back to
        the introduction screen.
    """

    def __init__(self, master=None):
        """
        Constructor for the Application class.

        Parameters:
            master (tkinter.Tk, optional): The parent window. Defaults to None.
        """

        super().__init__(master)
        self.master = master
        self.master.geometry("800x600")
        self.master.title("multiplayer_screen01.py")
        self.grid(padx=5, pady=5)

        # Add a button which will close the current window and open
        # the introducti,n screen
        self.button = tk.Button(self,
                                text="Back to introduction",
                                command=self.goto_screen01)
        self.button.grid(row=0,
                         column=0)

    def goto_screen01(self):
        """
        Destroys the current window and opens the introduction screen.
        """

        self.master.destroy()
        subprocess.Popen([sys.executable, "introduction.py"])


def main():
    """
    The main entry point for the application.
    It creates an Application instance and starts the Tkinter event loop.
    """

    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
