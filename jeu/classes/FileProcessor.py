# classes/FileProcessor.py


class FileProcessor:
    """
    permet de connaitre ds 1 liste d'elts (des fichiers ds 1 dossier)
    - l'elt courant sur lequel l'instance de la classe pointe
    - l'elt précedent
    - le prochain elt
    """

    def __init__(self, file_list):
        self.file_list = file_list
        self.current_index = 0

    def process_next(self, liste_fichiers, p_current_element):
        try:
            current_index = liste_fichiers.index(p_current_element)

            previous_element = (
                    liste_fichiers[current_index - 1]
                    if current_index > 0 else 'No previous element')

            current_element = liste_fichiers[current_index]

            next_element = (
                    liste_fichiers[current_index + 1]
                    if current_index < len(liste_fichiers) - 1 else 'No next element')

            # print(f"Previous element is {previous_element}, "
                  # f"current element is {current_element}, "
                  # f"next element is {next_element}")

            return previous_element, current_element, next_element

        except ValueError:
            print("--The provided element is not in the list.")
            return None

    def process_previous(self, liste_fichiers, p_current_element):
        try:
            current_index = liste_fichiers.index(p_current_element)

            previous_element = (liste_fichiers[current_index - 1]
                                if current_index > 0 else 'No previous element')

            current_element = liste_fichiers[current_index]

            next_element = (liste_fichiers[current_index + 1]
                            if current_index < len(liste_fichiers) - 1 else 'No next element'
                            )

            # print(f"Previous element is {previous_element}, "
                  # f"current element is {current_element}, "
                  # f"next element is {next_element}")

            return previous_element, current_element, next_element

        except ValueError:
            print("-The provided element is not in the list.")
            return None
