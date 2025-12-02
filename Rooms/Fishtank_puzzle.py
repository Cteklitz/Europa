import pygame
import sys
import random
import math
import Player
import Items
import Inventory

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_RES = screen.get_size()
VIRTUAL_RES = screen.get_size()
exit = False
bg_img = pygame.image.load("Assets/Fishtank_puzzle.png").convert()
bg_img = pygame.transform.scale(bg_img, WINDOW_RES)
player_pos = pygame.Vector2(192, 128)
exit = False

clearedFraction = 0.0

algae = None

# Pre-load squeegee image
try:
    squeegee_img = pygame.image.load("Assets/squeegee_fishtank_puzzle.png").convert_alpha()
    squeegee_img = pygame.transform.scale(squeegee_img, (135, 135))
    squeegee_img = pygame.transform.rotate(squeegee_img, 90)
except Exception as e:
    print("Error loading squeegee image:", e)
    squeegee_img = pygame.Surface((144, 72), pygame.SRCALPHA)
    pygame.draw.rect(squeegee_img, (200, 200, 200), (0, 18, 144, 36))
    pygame.draw.rect(squeegee_img, (100, 100, 100), (0, 0, 144, 18))

def Room(screen, screen_res, events):
    global player_pos, exit, algae, clearedFraction
    pygame.mouse.set_visible(False)

    DIG_RADIUS = 21
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

    glass_margin_x = int(WINDOW_RES[0] * 0.09)  
    glass_margin_y = int(WINDOW_RES[1] * 0.147)
    glass_width = WINDOW_RES[0] - 2 * glass_margin_x
    glass_height = WINDOW_RES[1] - 2 * glass_margin_y
    glass_x = glass_margin_x
    glass_y = glass_margin_y
    
    horizontal_shift = int(WINDOW_RES[0] * .02) 
    vertical_shift = int(WINDOW_RES[1] * 0.014) 
    glass_y = glass_margin_y + vertical_shift
    
    glass_x = glass_margin_x - horizontal_shift
    GLASS_RECT = pygame.Rect(glass_x, glass_y, glass_width, glass_height)

    
    box_width, box_height = 100, 80
    box_x = (WINDOW_RES[0] - box_width) // 2
    box_y = (WINDOW_RES[1] - box_height) // 2
    BOX_RECT = pygame.Rect(box_x, box_y, box_width, box_height)

    # algae persistent across room entries
    if algae is None:
        algae = pygame.Surface(WINDOW_RES, pygame.SRCALPHA)
        algae.fill((0, 0, 0, 0))
        
        # Use final algae position and size
        algae_rect = pygame.Rect(172, 233, 2119, 1018)
        base_algae = pygame.Surface((algae_rect.width, algae_rect.height), pygame.SRCALPHA)
        base_algae.fill((*ALGAE_COLOR, 252))
        
        algae.blit(base_algae, (algae_rect.left, algae_rect.top))

        DARK_ALGAE = (60, 100, 40)
        for _ in range(200):
            x = algae_rect.left + random.randint(0, algae_rect.width - 4)
            y = algae_rect.top + random.randint(0, algae_rect.height - 4)
        
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
        global clearedFraction
        if algae is None:
            return 0.0
        sub = algae.subsurface(BOX_RECT).copy()
        sub_mask = pygame.mask.from_surface(sub)
        remaining = sub_mask.count()
        total = BOX_RECT.width * BOX_RECT.height
        clearedFraction = 1.0 - (remaining / total)
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
    for _ in range(15):
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
    target_angle = 0

    def smooth_angle_transition(current_angle, target_angle, smoothness=0.5):
        
        def normalize_angle(a):
            while a > 180:
                a -= 360
            while a < -180:
                a += 360
            return a
        
        current_angle = normalize_angle(current_angle)
        target_angle = normalize_angle(target_angle)
        
        
        diff = normalize_angle(target_angle - current_angle)
        
        
        return normalize_angle(current_angle + diff * smoothness)

    def squeegee_clean(pos, prev_pos, radius):
        if GLASS_RECT.collidepoint(pos):
            if prev_pos is None:
                angle = 0
            else:
                x1, y1 = prev_pos
                x2, y2 = pos
                angle = math.degrees(math.atan2(y2 - y1, x2 - x1))

        
            clean_width = radius + 10
            clean_height = radius // 3
            
            
            offset_distance = 50
            
            
            if prev_pos is not None:
                
                dx = pos[0] - prev_pos[0]
                dy = pos[1] - prev_pos[1]
                distance = math.sqrt(dx*dx + dy*dy)
                steps = min(int(distance // 3), 10)
                
               
                if distance > 0:
                    offset_x = int((-dx / distance) * offset_distance)
                    offset_y = int((-dy / distance) * offset_distance)
                    
                    
                    clean_x = pos[0] + offset_x
                    clean_y = pos[1] + offset_y
                    
                    # Create and rotate the cleaning rectangle
                    clean_surf = pygame.Surface((clean_width, clean_height), pygame.SRCALPHA)
                    clean_surf.fill((0, 0, 0, 0))
                    rotated_clean = pygame.transform.rotate(clean_surf, -angle + 90)
                    rect = rotated_clean.get_rect(center=(clean_x, clean_y))
                    algae.blit(rotated_clean, rect.topleft, special_flags=pygame.BLEND_RGBA_MULT)
            else:
                
                clean_surf = pygame.Surface((clean_width, clean_height), pygame.SRCALPHA)
                clean_surf.fill((0, 0, 0, 0))
                rotated_clean = pygame.transform.rotate(clean_surf, -angle + 90)
                rect = rotated_clean.get_rect(center=pos)
                algae.blit(rotated_clean, rect.topleft, special_flags=pygame.BLEND_RGBA_MULT)

    def get_angle(x1, y1, x2, y2):
        return math.degrees(math.atan2(y2 - y1, x2 - x1))

    

    while running:
        dt = clock.tick(60)
        events = pygame.event.get()
        
        if Inventory.open:
            pygame.mouse.set_visible(True)
            if not Inventory.Inventory(screen, screen.get_size(), events):
                running = False
            pygame.display.flip()
            continue
        
        pygame.mouse.set_visible(False)
            
        for e in events:
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE or e.key == pygame.K_BACKSPACE:
                    running = False
                    exit = True
                elif e.key == pygame.K_TAB:
                    Inventory.open = True
                elif e.key == pygame.K_b:
                    show_box_outline = not show_box_outline
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                dragging = True
                prev_vmx, prev_vmy = None, None
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
                running = False
                exit = True
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
            # Only allow cleaning if squeegee is equipped
            if Player.equipped is not None and Player.equipped.id == "squeegee":
                if prev_vmx is not None and prev_vmy is not None:
                    prev_mx = int(prev_vmx * xScale)
                    prev_my = int(prev_vmy * yScale)
                    dx = mx - prev_mx
                    dy = my - prev_my
                    if abs(dx) > 2 or abs(dy) > 2:
                        target_angle = get_angle(prev_mx, prev_my, mx, my)
                        angle = smooth_angle_transition(angle, target_angle)
                        last_angle = angle
                else:
                    # 
                    angle = smooth_angle_transition(angle, last_angle)

                if prev_vmx is not None and prev_vmy is not None:
                    dx = vmx - prev_vmx
                    dy = vmy - prev_vmy
                    dist = max(abs(dx), abs(dy))
                    if dist > 0:
                        for i in range(dist + 1):
                            x = int(prev_vmx + dx * i / dist)
                            y = int(prev_vmy + dy * i / dist) + DIG_OFFSET_Y
                            if GLASS_RECT.collidepoint(x, y):
                                # 
                                squeegee_clean((x, y), (prev_vmx, prev_vmy + DIG_OFFSET_Y), BRUSH_RADIUS)
                                if random.random() < PARTICLE_SPAWN_CHANCE:
                                    spawn_sand_particles((x, y), PARTICLE_COUNT)
                    else:
                        if GLASS_RECT.collidepoint(vmx, vmy + DIG_OFFSET_Y):
                            squeegee_clean((vmx, vmy + DIG_OFFSET_Y), None, BRUSH_RADIUS)
                            
                            if random.random() < PARTICLE_SPAWN_CHANCE:
                                spawn_sand_particles((vmx, vmy + DIG_OFFSET_Y), PARTICLE_COUNT)
                else:
                    if GLASS_RECT.collidepoint(vmx, vmy + DIG_OFFSET_Y):
                        squeegee_clean((vmx, vmy + DIG_OFFSET_Y), None, BRUSH_RADIUS)
                        
                        if random.random() < PARTICLE_SPAWN_CHANCE:
                            spawn_sand_particles((vmx, vmy + DIG_OFFSET_Y), BRUSH_RADIUS)
                prev_vmx, prev_vmy = vmx, vmy
        else:
            prev_vmx, prev_vmy = None, None
            
            angle = smooth_angle_transition(angle, last_angle)  

        cleared = cleared_fraction_in_box()
        if not chest_open and cleared >= CLEAR_THRESHOLD:
            chest_open = True

        
        virtual.fill((0, 0, 0))
        virtual.blit(bg_img, (0, 0))
        if algae is not None:
            virtual.blit(algae, (0, 0))

        
        if dragging:
            
            for particle in particles[:]: 
                particle["x"] += particle["dx"]
                particle["y"] += particle["dy"]
                particle["dy"] += 0.1
                particle["life"] -= 1
                if particle["life"] <= 0:
                    particles.remove(particle)

            
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

        # Only show squeegee if it's equipped
        if Player.equipped is not None and Player.equipped.id == "squeegee":
            rotated_squeegee = pygame.transform.rotate(squeegee_img, -angle)
            rect = rotated_squeegee.get_rect(center=(mx, my))
            screen.blit(rotated_squeegee, rect.topleft)

        pygame.display.flip()

    
    pygame.mouse.set_visible(True)
    
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
            return 1
        return False