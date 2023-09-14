# monoplayer/ExitGameFromFirstStair.py

import pygame
import pygame_gui

import sys
import subprocess


class GameWindow:
    def __init__(self, width, height, title):
        pygame.init()
        pygame.mixer.init()
        self.size = (width, height)
        self.title = title
        self.window_surface = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)
        self.manager = pygame_gui.UIManager(self.size)
        self.clock = pygame.time.Clock()
        self.is_running = True

        # Boutons
        self.button_start = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 550), (200, 50)),
                                                         text='Start new game',
                                                         manager=self.manager)

        self.button_exit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 550), (200, 50)),
                                                        text='See you soon',
                                                        manager=self.manager)

        # Chargement de l'image
        # Assurez-vous que le chemin d'accès est correct
        self.image = pygame.image.load('images/dessin01.png')

        # Redimensionner l'image
        self.image = pygame.transform.scale(self.image, (500, 500))

    def run(self):
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                self.manager.process_events(event)

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.button_start:
                        print('Start new game')
                        self.is_running = False
                        pygame.quit()
                        subprocess.run(
                            ["python3.9", "introduction.py"])
                        sys.exit()
                    if event.ui_element == self.button_exit:
                        print('See you soon')
                        self.is_running = False
                        pygame.quit()
                        sys.exit()

            self.manager.update(time_delta)

            self.window_surface.fill((0, 0, 0))

            # Dessiner l'image sur le canvas
            self.window_surface.blit(self.image, (150, 25))

            self.manager.draw_ui(self.window_surface)

            pygame.display.update()


if __name__ == "__main__":
    game_window = GameWindow(800, 600, "Exit game from first stair")
    game_window.run()
