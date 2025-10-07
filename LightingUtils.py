# To use in room: define light_pos variable with value tuple of desired light position (x , y)
# create list of LightSource(light_pos[0], light_pos[1]) objects. Radius, color, strength can be changed if desired.
# create list of LightFalloff(screen_size) objects in room. radius and darkness can be changed if desired.
# In loop, use apply_lighting(screen, list_of_lights) apply_falloff(falloff, screen, light_pos) for each light

import pygame

def apply_lighting(surface, lights, darkness = 200, ambient_strength = 40, ambient_color = (40, 30, 30)):  
    # Creates dark surface to fill with light
    light_map = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    light_map.fill((0, 0, 0, darkness))
    
    # Draw each light on light_map
    for light in lights:
        light.draw(light_map) 
    
    # Blit light_map to screen
    surface.blit(light_map, (0, 0))
    
    # Create ambient light overlay
    ambient_overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    r, g, b = ambient_color
    ambient_overlay.fill((r, g, b, ambient_strength))
    
    # Blend ambient light on top of the surface
    surface.blit(ambient_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

def apply_falloff(falloff, surface, light_pos):
    for shadow in falloff:
        shadow.draw(surface, light_pos)