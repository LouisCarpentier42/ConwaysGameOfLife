
import pygame

class Settings:

    def __init__(self,
                 background_color = pygame.color.Color(0,0,0),
                 automatic_mode = False):
        self.background_color = background_color
        self.frame_rate = 20
        self.automatic_mode = automatic_mode

    def change_frame_rate(self, delta):
        self.frame_rate = max(1, self.frame_rate + delta)

    def change_automatic_mode(self):
        self.automatic_mode = not self.automatic_mode
