import pygame
import sys
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
import Player
import Items

pygame.init()

VIRTUAL_RES = (400, 250)
WINDOW_RES = (800, 500)
screen = pygame.display.set_mode(WINDOW_RES)
pygame.display.set_caption("Lockbox Combination")

player_pos = pygame.Vector2(192, 128)

# Load images
lockbox_img = pygame.image.load("Assets/Lockbox_puzzle.png").convert_alpha()
lockbox_img = pygame.transform.scale(lockbox_img, VIRTUAL_RES)
lockbox_img_open = pygame.image.load("Assets/Lockbox_puzzle_open.png").convert_alpha()
lockbox_img_open = pygame.transform.scale(lockbox_img_open, VIRTUAL_RES)
numbers_img = pygame.image.load("Assets/Lockbox_numbers.png").convert_alpha()

font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 28)

# Digit regions: (left, top, right, bottom) for each digit 0-9

# Image is 2 rows x 6 columns, each cell is 166x292 pixels
cell_w, cell_h = 166, 292
# Mapping: 0 is at (col=3, row=1), 1 is (col=0, row=0), ..., 9 is (col=2, row=1)
digit_map = [
    (3, 1), # 0
    (0, 0), # 1
    (1, 0), # 2
    (2, 0), # 3
    (3, 0), # 4
    (4, 0), # 5
    (5, 0), # 6
    (0, 1), # 7
    (1, 1), # 8
    (2, 1), # 9
]
digit_regions = []
for col, row in digit_map:
    left = col * cell_w
    top = row * cell_h
    right = left + cell_w
    bottom = top + cell_h
    digit_regions.append((left, top, right, bottom))

digit_positions = [
    [105, 113], [155, 113], [207, 113], [255, 113],
]
digit_size = [45, 41]  # width, height for all digits

CORRECT_CODE = [1, 2, 3, 4]
digits = [0, 0, 0, 0]
selected = 0
unlocked = False
chestOpen = False
exit = False
collected = False

# Replace the for-loop in draw_interface with this:
def draw_interface():
    # Draw lockbox background
    virtual = pygame.Surface(VIRTUAL_RES)
    if unlocked:
        virtual.blit(lockbox_img_open, (0, 0))
    else:
        virtual.blit(lockbox_img, (0, 0))

    # Only show keypad if not unlocked
    if not unlocked:
        arrow_w, arrow_h = 30, 18  # size of clickable arrow region
        arrow_offset_y = 22        # vertical offset above/below digit

        for i in range(4):
            x, y = digit_positions[i]
            scale_w, scale_h = digit_size
            left, top, right, bottom = digit_regions[digits[i] % 10]
            src_rect = pygame.Rect(left, top, right - left, bottom - top)
            digit_sprite = numbers_img.subsurface(src_rect)
            digit_sprite = pygame.transform.smoothscale(digit_sprite, (scale_w, scale_h))
            virtual.blit(digit_sprite, (x, y))
            rect = pygame.Rect(x, y, scale_w, scale_h)
            if i == selected:
                pygame.draw.rect(virtual, (255, 220, 80), rect, 3, border_radius=8)
            

    scaled = pygame.transform.scale(virtual, WINDOW_RES)
    # Center the scaled surface on the screen
    screen_width, screen_height = screen.get_size()
    surf_width, surf_height = scaled.get_size()
    center_x = (screen_width - surf_width) // 2
    center_y = (screen_height - surf_height) // 2
    screen.blit(scaled, (center_x, center_y))
    pygame.display.flip()

def inBounds(x=None, y=None):
    global exit
    if exit:
        exit = False
        return 0
    return False

def Room(screen, screen_res, events):
    global digits, selected, unlocked, chestOpen, exit, player_pos, collected
    running = True
    while running:
        draw_interface()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not unlocked:
                mx, my = pygame.mouse.get_pos()
                vmx = int(mx * VIRTUAL_RES[0] / WINDOW_RES[0])
                vmy = int(my * VIRTUAL_RES[1] / WINDOW_RES[1])
                arrow_w, arrow_h = 30, 18
                arrow_offset_y = 22
                for i in range(4):
                    x, y = digit_positions[i]
                    scale_w, scale_h = digit_size
                    up_rect = pygame.Rect(x + (scale_w - arrow_w)//2, y - arrow_offset_y, arrow_w, arrow_h)
                    down_rect = pygame.Rect(x + (scale_w - arrow_w)//2, y + scale_h + arrow_offset_y - arrow_h, arrow_w, arrow_h)
                    if up_rect.collidepoint(vmx, vmy):
                        digits[i] += 1
                        if digits[i] > 9:
                            digits[i] = 0
                    if down_rect.collidepoint(vmx, vmy):
                        digits[i] -= 1
                        if digits[i] < 0:
                            digits[i] = 9
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    exit = True
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    selected = (selected + 1) % 4
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    selected = (selected - 1) % 4
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    digits[selected] += 1
                    if digits[selected] > 9:
                        digits[selected] = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    digits[selected] -= 1
                    if digits[selected] < 0:
                        digits[selected] = 9
                elif event.key == pygame.K_BACKSPACE:
                    running = False
                    exit = True

        # Check for correct code
        if digits == CORRECT_CODE:
            unlocked = True
            chestOpen = True
            collected = True  # <-- Set collected to True when lockbox is opened

    xScale = VIRTUAL_RES[0] / WINDOW_RES[0]
    yScale = VIRTUAL_RES[1] / WINDOW_RES[1]
    return player_pos, xScale, yScale

def positionDeterminer(arg):
    # Your logic here
    pass

