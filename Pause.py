import pygame
import Sounds

virtual_res = (900, 650)
virtual_screen = pygame.Surface(virtual_res)
open = False
background = pygame.image.load("Assets/Pause.png")
resume = pygame.image.load("Assets/resume.png")
exit = pygame.image.load("Assets/exit.png")
resumeRect = pygame.Rect(325, 150, 250, 75)
exitRect = pygame.Rect(325, 250, 250, 75)
running = True

def Pause(screen, screen_res, events):
    global open, running
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h or event.key == pygame.K_BACKSPACE or pygame.K_ESCAPE:
                open = False
                Sounds.pauseMusic.stop()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_pos = (mouse_x/xScale, mouse_y/yScale)
                if resumeRect.collidepoint(mouse_pos):
                    open = False
                    Sounds.pauseMusic.stop()
                elif exitRect.collidepoint(mouse_pos):
                    running = False


    virtual_screen.blit(background, (0,0))
    virtual_screen.blit(resume, resumeRect)
    virtual_screen.blit(exit, exitRect)

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return running