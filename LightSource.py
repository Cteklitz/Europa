import pygame
import math
import random
class LightSource(pygame.sprite.Sprite):
    def __init__(self, x, y, radius = 120, color = (255, 200, 150), strength = 200, shape = "circle"):
        super().__init__()
        
        self.x = x
        self.y = y
        self.radius = radius
        self.strength = strength
        self.color = color
        self.shape = shape # "circle", "oval", "cone"
        self.light_surface = self.create_light_surface()


    def create_light_surface(self):
        light_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        r, g, b = self.color
        for rad in range(self.radius, 0, -1):
            falloff = (rad / self.radius) ** 1.8
            alpha = int(self.strength * (1 - falloff))
            if alpha <= 0:
                continue
            pygame.draw.circle(light_surface, (r, g, b, alpha), (self.radius, self.radius), rad)
        if self.shape == "oval":
            scaled_x = self.radius * 2
            scaled_y = int(self.radius * 1.5) # vertical stretch
            light_surface = pygame.transform.smoothscale(light_surface, (scaled_x, scaled_y))
        elif self.shape == "cone":
            scaled_x = self.radius * 2
            scaled_y = int(self.radius * 1.8)
            light_surface = pygame.transform.smoothscale(light_surface, (scaled_x, scaled_y))
            mask = pygame.Surface((scaled_x, scaled_y), pygame.SRCALPHA)
            mask.fill((0, 0, 0, 255))
            pygame.draw.polygon(mask, (0, 0, 0, 0), [
                (0, scaled_y // 3),
                (scaled_x, scaled_y // 3),
                (scaled_x, scaled_y),
                (0, scaled_y)
            ])
            light_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return light_surface

    
    def add_ambient_light(surface, darkness=200):
        ambient = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        ambient.fill((0, 0, 0, darkness))
        surface.blit(ambient, (0, 0))

    def draw(self, surface):
        rect = self.light_surface.get_rect(center = (self.x, self.y))
        surface.blit(self.light_surface, rect, special_flags = pygame.BLEND_RGBA_SUB)