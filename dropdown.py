import pygame
import os

class DropDown():
    def __init__(self, x, y, lp, rp, width, height, font=os.path.join("pixel.ttf"), main=None, options=None, color_menu=None, color_option=None):
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = pygame.Rect((width - x)//2 - lp, (height - y) - rp , x, y)
        self.font = pygame.font.Font(font, 28)
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, screen):
        pygame.draw.rect(screen, self.color_menu[self.menu_active], self.rect, border_radius=5)
        
        text = self.font.render(self.main, True, "white")
        screen.blit(text, text.get_rect(center = self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(screen, self.color_option[1 if i == self.active_option else 0], rect, 0)
                text = self.font.render(text, 1, "grey20")
                screen.blit(text, text.get_rect(center = rect.center))

    def update(self, event_list):
        mouse_pos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mouse_pos)
        
        self.active_option = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mouse_pos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.draw_menu = False
                    return self.active_option
        return -1
