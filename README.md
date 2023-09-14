FRENCH:  
installer le projet:  
Procédure depuis Linux Debian Bookworm.  

NOTES  

01:  
Le projet a été crée avec Python3.9.0  
Il a été testé (rapidement) avec:  
	- Python3.9.0  
	- Python3.10.0  
	- Python3.11.0  
	
02:  
Pour des questions de droit, le projet ne contient pas les musiques, bruitages ou fichiers graphiques.  
Graphiquement, il est épuré.  

License: Faîtes ce que vous voulez avec.  
Aucune garantie pour quoi que ce soit.  
BSP trouvé sur: https://github.com/fsd66/py-dungeon/  
(Aucune license trouvée)  

==========================================================================================

01: Verifier votre version de python.  
	01A:  
	python3 -V  

02: Installer sur votre systeme la bibliotheque tkinter pr python.  
	02A:  
	# apt install python3-tk  

03: Installer pip pour pouvoir plus tard installer les librairies necessaires au projet.  
	03A:  
	# apt install pip (ou apt install python3-pip)  

04: Installer python3-venv pour être capable de créer des environnements virtuels python.  
(cela évitera de polluer votre installation système avec des librairies non désirées)  
	04A:  
	# apt install python3-venv  

05: Créer un environnement virtuel Python.  
	05A:  
	$ python3.9 -m venv test  

06: Executer l'environnement virtuel Python.  
	06A:  
	$ cd test  
	$ source bin/activate  

07: Cloner le repo.  
	07A:  
	$ git clone https://github.com/dralobimene/v13_no_resources_for_github.git  

08: Déplacer les fichiers dans le repertoire précédent.  
	08A:  
	Copier le rep "jeu" et le script pip_install.sh ds le rep "test".  
		$ cp -R v13_no_resources_for_github/jeu/ /home/XXX/Documents/test/  
		$ cp v13_no_resources_for_github/pip_install.sh /home/XXX/Documents/test/  
	08B:  
	Effacer le rep v13... et son contenu. (ATTENTION AVEC CETTE COMMANDE)  
		$ rm -rf v13_no_resources_for_github  
	08C:  
	Executer le script shell ./pip_install.  
		$ ./pip_install.sh  

09: Se placer ds le rep "jeu".  
	$ cd jeu  

08: Executer le projet.  
	08A:  
	$ cd jeu  
	$ PYTHONPATH="/home/XXX/Documents/test/jeu" python3.9 /home/XXX/Documents/test/jeu/introduction.py  

QUAND VOUS AVEZ TERMINÉ DE VOUS AMUSER  

09: Quitter l'environnement virtuel Python.  
	$ deactivate  

10: supprimer le repertoire "test"  
	$rm -rf test (ATTENTION AVEC CETTE COMMANDE)  

******************************************************************************************************
******************************************************************************************************
******************************************************************************************************

ENGLISH:  
Install the project:  
Procedure from Debian Linux Bookworm.  

NOTES  

01:  
The project was created with Python3.9.0.  
It has been quickly tested with:  
- Python3.9.0  
- Python3.10.0  
- Python3.11.0  

02:  
Due to legal reasons, the project does not contain any music, sound effects, or graphic files.  
The graphics are minimalistic.  

License: Do whatever you want with it.  
No warranties for anything.  
BSP found on: https://github.com/fsd66/py-dungeon/  
(No license found)  

==========================================================================================

01: Check your Python version.  
  01A:  
  python3 -V  

02: Install the Tkinter library for Python on your system.  
  02A:  
  # apt install python3-tk  

03: Install pip to later install the necessary libraries for the project.  
  03A:  
  # apt install pip (or apt install python3-pip)  

04: Install python3-venv to be able to create Python virtual environments.  
(This will avoid polluting your system installation with undesired libraries)  
  04A:  
  # apt install python3-venv  

05: Create a Python virtual environment.  
  05A:  
  $ python3.9 -m venv test  

06: Execute the Python virtual environment.  
  06A:  
  $ cd test  
  $ source bin/activate  

07: Clone the repository.  
  07A:  
  $ git clone https://github.com/dralobimene/v13_no_resources_for_github.git  

08: Move the files to the previous directory.  
  08A:  
  Copy the "jeu" folder and the pip_install.sh script into the "test" folder.  
  $ cp -R v13_no_resources_for_github/jeu/ /home/XXX/Documents/test/  
  $ cp v13_no_resources_for_github/pip_install.sh /home/XXX/Documents/test/  
  08B:  
  Delete the v13... directory and its contents. (BE CAREFUL WITH THIS COMMAND)  
  $ rm -rf v13_no_resources_for_github  
  08C:  
  Run the shell script ./pip_install.  
  $ ./pip_install.sh  

  09: Go to the "jeu" directory.  
  $ cd jeu  

  08: Execute the project.  
  08A:  
  $ cd jeu  
  $ PYTHONPATH="/home/XXX/Documents/test/jeu" python3.9 /home/XXX/Documents/test/jeu/introduction.py  

WHEN YOU ARE DONE HAVING FUN  

09: Exit the Python virtual environment.  
  $ deactivate  

10: Delete the "test" directory.  
  $ rm -rf test (BE CAREFUL WITH THIS COMMAND)  
