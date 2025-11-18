import pygame

virtual_res = (900, 650)
virtual_screen = pygame.Surface(virtual_res)
open = False
controls = pygame.image.load("Assets/Controls.png")
running = True

def Controls(screen, screen_res, events):
    global open, running
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running  = False
            elif event.key == pygame.K_h or event.key == pygame.K_BACKSPACE:
                open = False

    virtual_screen.blit(controls, (0,0))

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return running