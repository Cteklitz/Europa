import pygame
class LightFalloff(pygame.sprite.Sprite):
    def __init__(self, screen_size, radius = 300, darkness = 180):
        super().__init__()
        self.radius = radius
        self.darkness = darkness
        self.screen_size = screen_size
        self.overlay = self.create_overlay(self.screen_size)
        self.gradient = self.create_gradient()

    def update_darkness(self, _darkness):
        self.darkness = _darkness
    
    # Creates transparent surface size of the screen to hold the gradient
    def create_overlay(self, screen_size):
        overlay = pygame.Surface(screen_size, pygame.SRCALPHA)  
        return overlay
    
    # Creates radial falloff gradient darkening outwards from the center
    def create_gradient(self):
        surface_size = max(self.screen_size) * 2
        gradient = pygame.Surface((surface_size, surface_size ), pygame.SRCALPHA)

        center = surface_size/2

        for y in range(surface_size):
            for x in range(surface_size):
                dx = x - center
                dy = y - center
                dist = (dx**2 + dy**2) ** 0.5
                if dist < self.radius:
                    alpha = int(self.darkness * (dist / self.radius))
                    gradient.set_at((x, y), (0, 0, 0, alpha))
                else:
                    gradient.set_at((x, y), (0, 0, 0, self.darkness))
        return gradient

    # Draws falloff gradient on surface at light position
    def draw(self, surface, light_pos):
        self.overlay.fill((0, 0, 0, 0)) # Clears previous drawing of gradient
        self.overlay.blit(self.gradient, (light_pos[0] - max(self.screen_size), light_pos[1] - max(self.screen_size)), special_flags=pygame.BLEND_RGBA_ADD)
        surface.blit(self.overlay, (0, 0)) # Blit overlay onto screen