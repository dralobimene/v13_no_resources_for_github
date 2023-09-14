import pygame
import pygame_gui
from typing import Tuple, List
class MenuCombatScrollableArea03:
    def __init__(self,
                 window_surface: pygame.Surface,
                 manager: pygame_gui.UIManager,
                 container_rect_dimensions: Tuple[int, int, int, int],
                 content_rect_size: Tuple[int, int],
                 menu_height: int):

            self.__window_surface = window_surface
            self.__manager = manager
            self.__container_rect = pygame.Rect(*container_rect_dimensions)
            self.__menu_height = menu_height
            self.__menu_y = 0
            self.__container_background = pygame.Surface(self.__container_rect.size)
            self.__container_background.fill(pygame.Color('blue'))
            self.__content_rect = pygame.Rect((0, 0), content_rect_size)
            self.__scrollable_container = pygame_gui.elements.UIScrollingContainer(
                relative_rect=self.__container_rect,
                manager=self.__manager)
            self.__scrollable_container.set_scrollable_area_dimensions(
                    self.__content_rect.size)
            self.text_label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((10, 10), (280, 30)),
                text="",
                manager=manager,
                container=self.scrollable_container
            )
            self.__menu_combats = []
            self.__monster_labels = []
            self.__button_to_monster = {}

    @property
    def window_surface(self) -> pygame.Surface:
        return self.__window_surface

    @window_surface.setter
    def window_surface(self,
                       window_surface: pygame.Surface) -> None:
        self.__window_surface = window_surface

    @property
    def manager(self) -> pygame_gui.UIManager:
        return self.__manager

    @manager.setter
    def manager(self,
                manager: pygame_gui.UIManager) -> None:
        self.__manager = manager

    @property
    def container_rect(self) -> pygame.Rect:
        return self.__container_rect

    @container_rect.setter
    def container_rect(self,
                       container_rect: pygame.Rect) -> None:
        self.__container_rect = container_rect

    @property
    def menu_height(self) -> int:
        return self.__menu_height

    @menu_height.setter
    def menu_height(self,
                    menu_height: int) -> None:
        self.__menu_height = menu_height

    @property
    def menu_y(self) -> int:
        return self.__menu_y

    @menu_y.setter
    def menu_y(self,
               menu_y: int) -> None:
        self.__menu_y = menu_y

    @property
    def container_background(self) -> pygame.Surface:
        return self.__container_background

    @container_background.setter
    def container_background(self,
                             container_background: pygame.Surface) -> None:
        self.__container_background = container_background

    @property
    def content_rect(self) -> pygame.Rect:
        return self.__content_rect

    @content_rect.setter
    def content_rect(self,
                     content_rect: pygame.Rect) -> None:
        self.__content_rect = content_rect

    @property
    def scrollable_container(self) -> pygame_gui.elements.UIScrollingContainer:
        return self.__scrollable_container

    @scrollable_container.setter
    def scrollable_container(self,
                             scrollable_container: pygame_gui.elements.UIScrollingContainer) -> None:
        self.__scrollable_container = scrollable_container
    @property
    def menu_combats(self) -> List[pygame_gui.elements.UIButton]:
        return self.__menu_combats

    @menu_combats.setter
    def menu_combats(self, value: List[pygame_gui.elements.UIButton]):
        if not isinstance(value, list) or not all(isinstance(item, pygame_gui.elements.UIButton) for item in value):
            raise TypeError("La valeur doit être une liste de boutons UIButton.")
        self.__menu_combats = value
    def print_collision_number(self, number_of_collisions: int):
        print("Number of monsters in collision with the player:", number_of_collisions)
        collision_text = "Collisions: " + str(number_of_collisions)
        self.text_label.set_text(collision_text)
    def show(self):
        print("methode show appelee")
        self.__scrollable_container.show()
    def hide(self, surface):
        print("methode hide appelee")
        self.__scrollable_container.hide()
        surface.fill((0, 0, 0, 0), self.__container_rect)
    def clear_content(self):
        for button in self.__menu_combats:
            button.kill()
        for label in self.__monster_labels:
            label.kill()
        self.__menu_combats.clear()
        self.__monster_labels.clear()
        self.__scrollable_container.set_scrollable_area_dimensions(self.__content_rect.size)
    def get_monster_name(self, button):
        return self.__button_to_monster.get(button, None)
    def create_additional_options(self, collision_count: int, monster_name: str):
        print("Contenu de self.__menu_combats")
        print("AVANT de créer le menu")
        print(self.__menu_combats)
        y = collision_count * self.__menu_height
        button1 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, y), (90, 30)),
            text="Attaquer",
            manager=self.__manager,
            container=self.__scrollable_container
        )
        self.__button_to_monster[button1] = monster_name
        button2 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((100, y), (90, 30)),
            text="Défendre",
            manager=self.__manager,
            container=self.__scrollable_container
        )
        self.__button_to_monster[button2] = monster_name
        self.__menu_combats.extend([button1, button2])
        monster_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((190, y), (200, 30)),
            text=f"{monster_name}",
            manager=self.__manager,
            container=self.__scrollable_container
        )
        self.__monster_labels.append(monster_label)
        print("Contenu de self.__menu_combats")
        print("APRES avoir crée le menu")
        print(self.__menu_combats)
    def remove_additional_options(self, monster_name: str):
        # Trouvez les boutons à supprimer
        buttons_to_remove = [button for button, name in self.__button_to_monster.items() if name == monster_name]
        for button in buttons_to_remove:
            # Supprimez les boutons du dictionnaire
            if button in self.__button_to_monster:
                self.__button_to_monster.pop(button)
            else:
                print("probleme 01:")
                print("classes/MenuCombatScrollableArea03.py")
                print("methode: remove_additional_options()")
            # Supprimez les boutons de la liste __menu_combats
            if button in self.__menu_combats:
                self.__menu_combats.remove(button)
            else:
                print("probleme 02:")
                print("classes/MenuCombatScrollableArea03.py")
                print("methode: remove_additional_options()")
            # Tuez le bouton pour le supprimer du gestionnaire d'interface utilisateur
            button.kill()
        # Trouvez les labels à supprimer
        labels_to_remove = [label for label in self.__monster_labels if label.text == monster_name]
        for label in labels_to_remove:
            # Supprimez les labels de la liste __monster_labels
            self.__monster_labels.remove(label)
            # Tuez le label pour le supprimer du gestionnaire d'interface utilisateur
            label.kill()
    def is_empty(self):
        return len(self.__menu_combats) == 0
    def kill(self):
        self.__scrollable_container.kill()
        self.__window_surface = None
        self.__manager = None
        self.__content_rect = None
    def get_next_menu_position(self):
        y_position = self.__menu_y
        self.__menu_y += self.__menu_height + 10
        return y_position

    def reset_menu_y_position(self):
        self.__menu_y = 0
    def draw(self):
        self.__window_surface.blit(self.__container_background,
                                   self.__container_rect.topleft)

    def update_option_position(self, new_y, monster_name):
        print("methode APPELEE")
        # Trouver les boutons correspondants au monstre.
        buttons_to_update = [button for button, name in self.__button_to_monster.items() if name == monster_name]
        # Mettre à jour la position en y des boutons et des labels.
        for button in buttons_to_update:
            button.relative_rect.y = new_y
