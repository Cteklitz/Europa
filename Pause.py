import pygame
import Controls
import Sounds
import Objects
import Assets

virtual_res = (900, 650)
virtual_screen = pygame.Surface(virtual_res)
open = False
background = pygame.image.load("Assets/Pause.png")
resume = pygame.image.load("Assets/resume.png")
exit = pygame.image.load("Assets/exit.png")
controls = pygame.image.load("Assets/controlsButton.png")
resumeRect = pygame.Rect(325, 150, 250, 75)
controlsRect = pygame.Rect(325, 250, 250, 75)
exitRect = pygame.Rect(325, 350, 250, 75)
running = True

eye = Assets.eye
oneWayOut = pygame.image.load("Assets/ONEWAYOUT.png")
timer = Objects.timer(6.0, False)
clicked = False
evilAudio = Sounds.loadAudio("Audio/evil2Trimmed2.wav")

played = False

# Variables to store current music playing so that it can resume once unpaused
musicPath = None
volume = None

def loadMusic():
    global musicPath, volume
    pygame.mixer.music.load(musicPath)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)

def Pause(screen, screen_res, events):
    global open, running, clicked, timer, played
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    valvePlaced = Objects.getValvePlaced()

    if valvePlaced and not played:
        played = True
        Sounds.scaryBell.play()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h or event.key == pygame.K_BACKSPACE or pygame.K_ESCAPE:
                open = False
                # Resume in-game audio
                pygame.mixer.unpause()
                pygame.mixer.music.stop()
                if musicPath != None:
                    loadMusic()
                else:
                    pygame.mixer.music.set_volume(1)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_pos = (mouse_x/xScale, mouse_y/yScale)
                if resumeRect.collidepoint(mouse_pos):
                    open = False
                    # Resume in-game audio
                    pygame.mixer.unpause()
                    pygame.mixer.music.stop()
                    if musicPath != None:
                        loadMusic()
                    else:
                        pygame.mixer.music.set_volume(1)
                elif controlsRect.collidepoint(mouse_pos) and not clicked:
                    Controls.open = True
                elif exitRect.collidepoint(mouse_pos) and not valvePlaced:
                    running = False
                elif exitRect.collidepoint(mouse_pos) and valvePlaced and not clicked:
                    evilAudio.play()
                    timer.setInitial()
                    clicked = True


    virtual_screen.blit(background, (0,0))
    if valvePlaced:
        virtual_screen.fill((0,0,0))
    virtual_screen.blit(resume, resumeRect)
    if not clicked:
        virtual_screen.blit(controls, controlsRect)
    if not valvePlaced or not clicked:
        virtual_screen.blit(exit, exitRect)
 
    if not valvePlaced:
        font = pygame.font.Font("Assets/asusrog_regular.ttf", 76)
        text = font.render("PAUSED", False, "black")
        textRect = text.get_rect()
        textRect.center = (450, 50)
        virtual_screen.blit(text, textRect)
    elif valvePlaced and not clicked:
        font = pygame.font.Font("Assets/asusrog_regular.ttf", 60)
        text = font.render("IT IS TOO LATE TO FLEE", False, "red")
        textRect = text.get_rect()
        textRect.center = (450, 50)
        virtual_screen.blit(text, textRect)
        virtual_screen.blit(eye, (180, 300))

    if not timer.Done() and clicked:
        virtual_screen.fill((0,0,0))
        virtual_screen.blit(oneWayOut, (203, 224))

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return running