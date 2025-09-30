# sand_demo_box_brush_full_clear.py
import pygame
import sys
import random
import math

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_RES = screen.get_size()
VIRTUAL_RES = screen.get_size()  # Define your virtual resolution here
exit = False  # Global exit flag
bg_img = pygame.image.load("Assets/Fishtank_puzzle.png").convert()
bg_img = pygame.transform.scale(bg_img, WINDOW_RES)
player_pos = pygame.Vector2(192, 128)
exit = False
print("Loaded background image:", bg_img.get_size())

# Pre-load squeegee image at module level to avoid loading delay
try:
    squeegee_img = pygame.image.load("Assets/squeegee_fishtank_puzzle.png").convert_alpha()
    squeegee_img = pygame.transform.scale(squeegee_img, (45, 45))
except Exception as e:
    print("Error loading squeegee image:", e)
    squeegee_img = pygame.Surface((48, 24), pygame.SRCALPHA)
    pygame.draw.rect(squeegee_img, (200, 200, 200), (0, 6, 48, 12))
    pygame.draw.rect(squeegee_img, (100, 100, 100), (0, 0, 48, 6))

def Room(screen, screen_res, events):
    global player_pos, exit
    print("Fishtank_puzzle Room started")
    pygame.mouse.set_visible(False)

    DIG_RADIUS = 7
    DIG_OFFSET_Y = -5
    # Center BOX_RECT
    box_width, box_height = 50, 500
    box_x = (VIRTUAL_RES[0] - box_width) // 2
    box_y = (VIRTUAL_RES[1] - box_height) // 2
    BOX_RECT = pygame.Rect(box_x, box_y, box_width, box_height)
    CLEAR_THRESHOLD = 1.0

    virtual = pygame.Surface(VIRTUAL_RES).convert()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 22)

    xScale = screen.get_width() / virtual.get_width()
    yScale = screen.get_height() / virtual.get_height()

    bg_closed = pygame.Surface(VIRTUAL_RES).convert()
    bg_closed.fill((58, 76, 102))
    pygame.draw.rect(bg_closed, (139, 69, 19), pygame.Rect(150, 130, 100, 60))
    pygame.draw.rect(bg_closed, (160, 82, 45), pygame.Rect(150, 110, 100, 25))
    pygame.draw.rect(bg_closed, (230, 230, 90), pygame.Rect(190, 150, 20, 30))

    bg_open = bg_closed.copy()
    pygame.draw.rect(bg_open, (200, 170, 40), pygame.Rect(150, 100, 100, 15))

    
    ALGAE_COLOR = (80, 120, 60)

    algae = pygame.Surface(WINDOW_RES, pygame.SRCALPHA)
    algae.fill((0, 0, 0, 0))  # Fully transparent

    glass_margin_x = int(WINDOW_RES[0] * 0.09)  
    glass_margin_y = int(WINDOW_RES[1] * 0.147)
    glass_width = WINDOW_RES[0] - 2 * glass_margin_x
    glass_height = WINDOW_RES[1] - 2 * glass_margin_y
    glass_x = glass_margin_x
    glass_y = glass_margin_y
    # Move algae region horizontally by a percent of the screen width
    horizontal_shift = int(WINDOW_RES[0] * .02) 
    vertical_shift = int(WINDOW_RES[1] * 0.014) 
    glass_y = glass_margin_y + vertical_shift  # Moves algae down
    
    glass_x = glass_margin_x - horizontal_shift
    GLASS_RECT = pygame.Rect(glass_x, glass_y, glass_width, glass_height)

    # Center BOX_RECT in the window
    box_width, box_height = 100, 80
    box_x = (WINDOW_RES[0] - box_width) // 2
    box_y = (WINDOW_RES[1] - box_height) // 2
    BOX_RECT = pygame.Rect(box_x, box_y, box_width, box_height)

    # Fill the entire glass area with base algae color first
    # Create a fully transparent base surface
    algae = pygame.Surface(WINDOW_RES, pygame.SRCALPHA)
    algae.fill((0, 0, 0, 0))  # Start completely transparent
    
    # Create the algae surface just for the glass area with solid color
    base_algae = pygame.Surface((GLASS_RECT.width, GLASS_RECT.height), pygame.SRCALPHA)
    base_algae.fill((*ALGAE_COLOR, 252))
    
    # Only draw algae in the glass area
    algae.blit(base_algae, (GLASS_RECT.left, GLASS_RECT.top))

    # Reduced texture dots for better performance (200 instead of 500)
    DARK_ALGAE = (60, 100, 40)  # Slightly darker green
    for _ in range(200):  # Reduced from 500 to 200
        x = GLASS_RECT.left + random.randint(0, GLASS_RECT.width - 4)
        y = GLASS_RECT.top + random.randint(0, GLASS_RECT.height - 4)
        # Draw a 4x4 pixel dark spot
        pygame.draw.rect(algae, (*DARK_ALGAE, 252), pygame.Rect(x, y, 4, 4))

    def clean_at(pos, radius=DIG_RADIUS):
        erase_circle(algae, pos, radius)
        for _ in range(8):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.uniform(radius * 0.7, radius * 1.1)
            offset_x = int(dist * math.cos(angle))
            offset_y = int(dist * math.sin(angle))
            jitter_radius = random.randint(int(radius * 0.4), int(radius * 0.7))
            erase_circle(algae, (pos[0] + offset_x, pos[1] + offset_y), jitter_radius)
        return True

    def cleared_fraction_in_box():
        sub = algae.subsurface(BOX_RECT).copy()
        sub_mask = pygame.mask.from_surface(sub)
        remaining = sub_mask.count()
        total = BOX_RECT.width * BOX_RECT.height
        return 1.0 - (remaining / total)

    particles = []

    def spawn_sand_particles(pos, count=8):
        for _ in range(count):
            dx = random.uniform(-0.5, 0.5)
            dy = random.uniform(0.5, 1.2)
            particles.append({
                "x": pos[0],
                "y": pos[1],
                "dx": dx,
                "dy": dy,
                "life": random.randint(18, 28)
            })

    floating_particles = []
    for _ in range(15):  # Reduced from 30 to 15 for better performance
        floating_particles.append({
            "x": random.randint(GLASS_RECT.left, GLASS_RECT.right),
            "y": random.randint(GLASS_RECT.top, GLASS_RECT.bottom),
            "dx": random.uniform(-0.2, 0.2),
            "dy": random.uniform(-0.1, 0.1),
            "radius": random.randint(1, 3),
            "color": (80 + random.randint(-20, 20), 120 + random.randint(-20, 20), 60 + random.randint(-20, 20))
        })

    running = True
    dragging = False
    chest_open = False
    show_box_outline = True
    prev_vmx, prev_vmy = None, None
    exit = False

    PARTICLE_SPAWN_CHANCE = 0.1
    PARTICLE_COUNT = 1

    last_angle = 0
    angle = 0  

    def squeegee_clean(pos, prev_pos, radius):
        if GLASS_RECT.collidepoint(pos):
            if prev_pos is None:
                angle = 0
            else:
                x1, y1 = prev_pos
                x2, y2 = pos
                angle = math.degrees(math.atan2(y2 - y1, x2 - x1))

            swipe_length = max(1, int(math.hypot(pos[0] - prev_pos[0], pos[1] - prev_pos[1]))) if prev_pos else radius*2
            swipe_surf = pygame.Surface((swipe_length, radius*2), pygame.SRCALPHA)
            swipe_surf.fill((0, 0, 0, 0))
            pygame.draw.rect(swipe_surf, (0, 0, 0, 0), (0, 0, swipe_length, radius*2))
            rotated_swipe = pygame.transform.rotate(swipe_surf, -angle)
            center_x = pos[0]
            center_y = pos[1]
            rect = rotated_swipe.get_rect(center=(center_x, center_y))
            algae.blit(rotated_swipe, rect.topleft, special_flags=pygame.BLEND_RGBA_MULT)

    def get_angle(x1, y1, x2, y2):
        return math.degrees(math.atan2(y2 - y1, x2 - x1))

    # Removed expensive blur operation for better performance

    while running:
        dt = clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE or e.key == pygame.K_BACKSPACE:
                    running = False
                    exit = True
                elif e.key == pygame.K_b:
                    show_box_outline = not show_box_outline
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                dragging = True
                prev_vmx, prev_vmy = None, None
            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                dragging = False
                prev_vmx, prev_vmy = None, None

        mx, my = pygame.mouse.get_pos()
        offset_x = (WINDOW_RES[0] - VIRTUAL_RES[0]) // 2
        offset_y = (WINDOW_RES[1] - VIRTUAL_RES[1]) // 2
        vmx = mx - offset_x
        vmy = my - offset_y

        BRUSH_RADIUS = int(DIG_RADIUS * 2)

        if dragging:
            if prev_vmx is not None and prev_vmy is not None:
                prev_mx = int(prev_vmx * xScale)
                prev_my = int(prev_vmy * yScale)
                dx = mx - prev_mx
                dy = my - prev_my
                if abs(dx) > 2 or abs(dy) > 2:
                    last_angle = get_angle(prev_mx, prev_my, mx, my)
                angle = last_angle
            else:
                angle = last_angle

            if prev_vmx is not None and prev_vmy is not None:
                dx = vmx - prev_vmx
                dy = vmy - prev_vmy
                dist = max(abs(dx), abs(dy))
                if dist > 0:
                    for i in range(dist + 1):
                        x = int(prev_vmx + dx * i / dist)
                        y = int(prev_vmy + dy * i / dist) + DIG_OFFSET_Y
                        if GLASS_RECT.collidepoint(x, y):
                            
                            squeegee_clean((x, y), (prev_vmx, prev_vmy + DIG_OFFSET_Y), BRUSH_RADIUS)
                            if random.random() < PARTICLE_SPAWN_CHANCE:
                                spawn_sand_particles((x, y), PARTICLE_COUNT)
                else:
                    if GLASS_RECT.collidepoint(vmx, vmy + DIG_OFFSET_Y):
                        squeegee_clean((vmx, vmy + DIG_OFFSET_Y), None, BRUSH_RADIUS)
                        # Simplified particle spawning without expensive mask comparison
                        if random.random() < PARTICLE_SPAWN_CHANCE:
                            spawn_sand_particles((vmx, vmy + DIG_OFFSET_Y), PARTICLE_COUNT)
            else:
                if GLASS_RECT.collidepoint(vmx, vmy + DIG_OFFSET_Y):
                    squeegee_clean((vmx, vmy + DIG_OFFSET_Y), None, BRUSH_RADIUS)
                    # Simplified particle spawning without expensive mask comparison
                    if random.random() < PARTICLE_SPAWN_CHANCE:
                        spawn_sand_particles((vmx, vmy + DIG_OFFSET_Y), BRUSH_RADIUS)
            prev_vmx, prev_vmy = vmx, vmy
        else:
            prev_vmx, prev_vmy = None, None
            angle = last_angle  

        cleared = cleared_fraction_in_box()
        if not chest_open and cleared >= CLEAR_THRESHOLD:
            chest_open = True

        
        virtual.fill((0, 0, 0))
        virtual.blit(bg_img, (0, 0))
        virtual.blit(algae, (0, 0))

        # Only update and draw particles when actively cleaning (dragging)
        if dragging:
            # Update particles
            for particle in particles[:]: 
                particle["x"] += particle["dx"]
                particle["y"] += particle["dy"]
                particle["dy"] += 0.1  # Gravity
                particle["life"] -= 1
                if particle["life"] <= 0:
                    particles.remove(particle)

            # Draw particles
            for particle in particles:
                alpha = min(255, particle["life"] * 20)
                color = (*ALGAE_COLOR, alpha)
                pos = (int(particle["x"]), int(particle["y"]))
                pygame.draw.circle(virtual, color, pos, 4) 

       
        scaled = pygame.transform.scale(virtual, WINDOW_RES)
        screen_width, screen_height = screen.get_size()
        surf_width, surf_height = scaled.get_size()
        center_x = (screen_width - surf_width) // 2
        center_y = (screen_height - surf_height) // 2
        screen.blit(scaled, (center_x, center_y))

        # Draw squeegee on top of everything (directly to screen)
        rotated_squeegee = pygame.transform.rotate(squeegee_img, -angle)
        rect = rotated_squeegee.get_rect(center=(mx, my))
        screen.blit(rotated_squeegee, rect.topleft)

        pygame.display.flip()

    xSpeedScale = VIRTUAL_RES[0] / WINDOW_RES[0]
    ySpeedScale = VIRTUAL_RES[1] / WINDOW_RES[1]
    return player_pos, xSpeedScale, ySpeedScale

def positionDeterminer(arg):
    pass

def erase_circle(surface, pos, radius):
    temp = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    temp.fill((0, 0, 0, 0))
    pygame.draw.circle(temp, (0, 0, 0, 0), (radius, radius), radius)
    surface.blit(temp, (pos[0] - radius, pos[1] - radius), special_flags=pygame.BLEND_RGBA_MULT)

def inBounds(x=None, y=None):
        global exit
        if 'exit' in globals() and exit:
            exit = False
            return 0
        return False
