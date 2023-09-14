# classes/Buttons/MoveMenuButton.py

import pygame
from typing import Callable, Optional


class MoveMenuButton:
    """
    Represents a clickable and interactive button on a menu.

    Attributes:
        image (pygame.Surface): The image representing the button.
        rect (pygame.Rect): The rectangle defining the button's
        position and dimensions.
        action (Callable[[], None]): The action to execute when the
        button is clicked.
        hovered (bool): A flag indicating whether the mouse is hovering
        over the button.
        current_image (pygame.Surface): The current image being displayed,
        affected by hovering.
    """

    # [REPERE 10 - 1]: Illustrat° de callback
    #       parametre 'action' qui sera 1 methode.
    # [REPERE 10 - 2]: (ici ds la methode handle_event())
    # [REPERE 10 - 3]: Fichier game/game.py
    # [REPERE 10 - 4]: Fichier game/game.py
    def __init__(self,
                 x: int,
                 y: int,
                 image_path: str,
                 width: int,
                 height: int,
                 action: Optional[Callable[[], None]],
                 angle: float = 0):
        """
        Initialize a MoveMenuButton instance.

        Parameters:
            x (int): The x-coordinate of the button center.
            y (int): The y-coordinate of the button center.
            image_path (str): The path to the image to use for the button.
            width (int): The width of the button.
            height (int): The height of the button.
            action (Callable[[], None], optional): The function to call when
            the button is clicked.
            angle (float, optional): The angle to rotate the button image.
            Default is 0.
        """

        original_image = pygame.image.load(image_path)

        # Scale and rotate the image
        scaled_image = pygame.transform.scale(original_image, (width, height))
        self.image = pygame.transform.rotate(scaled_image, angle)

        self.rect = self.image.get_rect(center=(x, y))
        self.action = action
        self.hovered = False
        self.current_image = self.image

    # =========================================================================

    def render(self,
               screen: pygame.Surface) -> None:
        """
        Render the button on the given screen.

        Parameters:
            screen (pygame.Surface): The screen to render the button on.
        """

        #
        screen.blit(self.current_image, self.rect.topleft)

    # =========================================================================

    def handle_event(self,
                     event: pygame.event.Event) -> None:
        """
        Handle user interaction events like mouse movements and clicks.

        Parameters:
            event (pygame.event.Event): The event to handle.
        """

        #
        if event.type == pygame.MOUSEMOTION:
            # Check if mouse is over the button
            if self.rect.collidepoint(event.pos):
                self.hovered = True
            else:
                self.hovered = False

        # [REPERE 10 - 2]:
        # On clique sur le bouton et on execute la methode 'action()'
        # qui est un des parametre du consttucteur
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos) and self.action:
                self.action()
