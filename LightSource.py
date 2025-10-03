import pygame
import math
class LightSource(pygame.sprite.Sprite):
    def __init__(self, x, y, radius = 120, color = (255, 200, 150), strength = 200, shape = "circle", angle = 90, spread = 90):
        super().__init__()
        
        self.x = x
        self.y = y
        self.radius = radius
        self.strength = strength
        self.color = color
        self.shape = shape # "circle", "oval", "cone"
        self.angle = angle      # for cones
        self.spread = spread    # for cones
        self.light_surface = self.create_light_surface()

    # Returns light surface
    def create_light_surface(self):
        light_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        r, g, b = self.color
        if self.shape == "circle":
            # Draws cocentric circles with decreasing alpha values to represent fading light
            for rad in range(self.radius, 0, -1):
                falloff = (rad / self.radius) ** 1.8
                alpha = int(self.strength * (1 - falloff))
                alpha = max(0, min(alpha, 255))
                if alpha <= 0:
                    continue
                pygame.draw.circle(light_surface, (r, g, b, alpha), (self.radius, self.radius), rad)
        #if self.shape == "oval":
         #   scaled_x = self.radius * 2
          #  scaled_y = int(self.radius * 1.5) # vertical stretch
           # light_surface = pygame.transform.smoothscale(light_surface, (scaled_x, scaled_y))
        elif self.shape == "cone":
            for rad in range(self.radius, 0, -2):
                falloff = (rad / self.radius) ** 2.5
                alpha = int(min(self.strength * (1 - falloff), 180))
                
                # make cone polygon
                cx, cy = self.radius, self.radius
                angle_rad = math.radians(self.angle)
                spread_rad = math.radians(self.spread / 2)

                left = (
                    cx + rad * math.cos(angle_rad - spread_rad),
                    cy + rad * math.sin(angle_rad - spread_rad)
                )
                right = (
                    cx + rad * math.cos(angle_rad + spread_rad),
                    cy + rad * math.sin(angle_rad + spread_rad)
                )

                pygame.draw.polygon(light_surface, (r, g, b, alpha), [(cx, cy), left, right])

            # Smooth edges
            fade_mask = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            for rad in range(self.radius, 0, -1):
                mask_alpha = int(50 * (rad / self.radius) ** 2)  # smooth fade
                pygame.draw.circle(fade_mask, (255, 255, 255, mask_alpha), (self.radius, self.radius), rad)
            light_surface.blit(fade_mask, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        return light_surface

    # Draws light onto screen by substracting from dark surface and light showing throuhg
    def draw(self, surface):
        rect = self.light_surface.get_rect(center = (self.x, self.y))
        surface.blit(self.light_surface, rect, special_flags = pygame.BLEND_RGBA_SUB)