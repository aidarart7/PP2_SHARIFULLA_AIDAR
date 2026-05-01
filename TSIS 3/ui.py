import pygame

# ---------- BUTTON ----------
class Button:
    def __init__(self, x, y, w, h, text,
                 color=(200, 200, 200),
                 hover_color=(150, 150, 150),
                 text_color=(0, 0, 0)):

        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color

        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()

        # hover effect
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color

        pygame.draw.rect(surface, current_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=8)

        # centered text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN and
            event.button == 1 and
            self.rect.collidepoint(event.pos)
        )


# ---------- TEXT INPUT ----------
class TextInput:
    def __init__(self, x, y, w, h, placeholder="Enter name..."):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.placeholder = placeholder

        self.font = pygame.font.Font(None, 36)
        self.active = True  # always active (можно расширить)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]

            elif event.key == pygame.K_RETURN:
                return self.text

            elif event.unicode.isprintable() and len(self.text) < 15:
                self.text += event.unicode

        return None

    def draw(self, surface):
        # box
        pygame.draw.rect(surface, (255, 255, 255), self.rect, border_radius=6)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=6)

        # text or placeholder
        display_text = self.text if self.text else self.placeholder
        color = (0, 0, 0) if self.text else (150, 150, 150)

        text_surf = self.font.render(display_text, True, color)

        # vertical center align
        text_rect = text_surf.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        surface.blit(text_surf, text_rect)