
import pygame_gui
import pygame


class MainMenu:
    def __init__(self,
                 manager,
                 surface):
        self.manager = manager
        self.surface = surface

        self.panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((800,
                                                                            0),
                                                                           (200,
                                                                            300)), 
                                                 manager=self.manager)

        self.button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,
                                                                              0),
                                                                             (50,
                                                                              50)),
                                                   text='Cliquez-moi',
                                                   manager=self.manager, 
                                                   container=self.panel)

    def handle_event(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.button:
                    print("bonjour")
