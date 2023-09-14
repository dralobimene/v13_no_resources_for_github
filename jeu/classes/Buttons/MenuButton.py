# classes/Buttons/MenuButton.py

import pygame
from typing import Callable, Optional

BLACK = (0, 0, 0)
GREY = (128, 128, 128)


class Button:
    """
    Represents a clickable and interactive text button.

    Attributes:
        rect (pygame.Rect): Rectangle defining the button's position
        and dimensions.
        text (str): The text displayed on the button.
        action (Optional[Callable[[], None]]): The action to execute
        when the button is clicked.
        hovered (bool): Flag indicating whether the mouse is hovering over
        the button.
    """

    def __init__(self,
                 x: int,
                 y: int,
                 w: int,
                 h: int,
                 text: str,
                 action: Optional[Callable[[], None]] = None) -> None:
        """
        Initialize a Button instance.

        Parameters:
            x (int): The x-coordinate of the top-left corner of the button.
            y (int): The y-coordinate of the top-left corner of the button.
            w (int): The width of the button.
            h (int): The height of the button.
            text (str): The text to display on the button.
            action (Optional[Callable[[], None]]): The function to call when
            the button is clicked.
        """

        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action

        # Attributs qui ne st pas des arguments du constructeur.
        # Attribute to track if the button is hovered or not.
        self.hovered = False

    # =========================================================================

    def render(self, screen: pygame.Surface) -> None:
        """
        Render the button on the given screen.

        Parameters:
            screen (pygame.Surface): The screen to render the button on.
        """
        # Draw a border around the button to simulate UIButton's style.
        border_color = (200, 200, 200)  # Light gray
        pygame.draw.rect(screen, border_color, self.rect.inflate(4, 4))

        # Use RED for the button background
        pygame.draw.rect(screen, GREY, self.rect)

        # Render the text
        font = pygame.font.SysFont(None, 20)
        label = font.render(self.text, True, BLACK)
        screen.blit(label,
                    (self.rect.x + (self.rect.w - label.get_width()) // 2,
                     self.rect.y + (self.rect.h - label.get_height()) // 2)
                    )

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

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and self.action:
                self.action()
