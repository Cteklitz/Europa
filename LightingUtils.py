import pygame

def apply_lighting(surface, lights, darkness = 200, ambient_strength = 40, ambient_color = (40, 30, 30)):  
    light_map = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    light_map.fill((0, 0, 0, darkness))
    for light in lights:
        light.draw(light_map) 
    surface.blit(light_map, (0, 0))
    ambient_overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    r, g, b = ambient_color
    ambient_overlay.fill((r, g, b, ambient_strength))
    surface.blit(ambient_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)