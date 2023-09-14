# classes/Buttons/shaped_button_square.py

from classes.ShapedButton import ShapedButton
import pygame


class ShapedButtonSquare(ShapedButton):

    # =========================================================================

    def _draw(self) -> None:
        print("Drawing square button")
        if self.image_path:
            image = pygame.image.load(self.image_path)
            image = pygame.transform.scale(image, (self.width,
                                                   self.height))
            self._ShappedButton__surface.blit(image, (0, 0))
        elif self.color:
            pygame.draw.rect(self._ShapedButton__surface, self.color, (0,
                                                                       0,
                                                                       self.width,
                                                                       self.height))
    # =========================================================================

    def handle_event(self, event: pygame.event.Event) -> bool:
        clicked = super().handle_event(event)
        if clicked:
            print(f"Square button received click: {clicked}")
            if self._ShapedButton__callback:
                self._ShapedButton__callback()
        return clicked
