import pygame
import os

class Button:
    def __init__(self, x, y, lp, rp, width, height, text, font_size=18, bg_color="lightpink3", text_color="white", font=os.path.join("pixel.ttf"), visible=None,action=None):
        self.rect = pygame.Rect((width - x)//2 - lp, (height - y) - rp , x, y)
        self.font = pygame.font.Font(font, font_size)
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.visible = visible
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=5)
        text_font = self.font.render(self.text, True, self.text_color)
        text_rect = text_font.get_rect(center=self.rect.center)
        screen.blit(text_font, text_rect)
    
    def hide(self, screen):
        pygame.draw.rect(screen, "white", self.rect, border_radius=5)
        text_font = self.font.render(self.text, True, "white")
        text_rect = text_font.get_rect(center=self.rect.center)
        screen.blit(text_font, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.rect.collidepoint(mouse_x, mouse_y) and self.action:
                    self.action()  
