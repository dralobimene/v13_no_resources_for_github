# classes/Buttons/button_shaped_circle.py

from classes.ShapedButton import ShapedButton
import pygame


class ShapedButtonCircle(ShapedButton):

    # =========================================================================

    def _draw(self) -> None:
        print("Drawing circle button")
        if self.image_path:
            image = pygame.image.load(self.image_path)
            image = pygame.transform.scale(image, (self.width, self.height))
            self._ShapedButton__surface.blit(image, (0, 0))
        elif self.color:
            pygame.draw.ellipse(self._ShapedButton__surface,
                                self.color, (0, 0, self.width, self.height))

    # =========================================================================

    def handle_event(self, event: pygame.event.Event) -> bool:
        clicked = super().handle_event(event)
        if clicked:
            print(f"Circle button received click: {clicked}")
            if self._ShapedButton__callback:
                self._ShapedButton__callback()
        return clicked
