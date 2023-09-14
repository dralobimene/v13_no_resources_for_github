# classes/Buttons/shaped_button_triangle.py

from classes.ShapedButton import ShapedButton
import pygame


class ShapedButtonTriangle(ShapedButton):
    def _draw(self) -> None:
        if self.image_path:
            image = pygame.image.load(self.image_path)
            image = pygame.transform.scale(image, (self.width,
                                                   self.height))
            self._ShapedButton__surface.blit(image, (0, 0))
        elif self.color:
            points = [(self.width // 2, 0),
                      (0, self.height),
                      (self.width, self.height)]
            pygame.draw.polygon(self._ShapedButton__surface,
                                self.color,
                                points)

    def handle_event(self, event: pygame.event.Event) -> bool:
        clicked = super().handle_event(event)
        if clicked:
            print(f"Triangle button received click: {clicked}")
            if self._ShapedButton__callback:
                self._ShapedButton__callback()
        return clicked
