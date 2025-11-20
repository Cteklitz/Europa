import pygame

def loadAudio(filename):
    try:
        # Try to load .ogg
        base_name = filename.replace(".wav", "").replace(".mp3", "")
        ogg_filename = f"Compressed_{base_name}.ogg"
        return pygame.mixer.Sound(ogg_filename)
    except:
        # If .ogg fails, try the original file in "Raw Audio/" directory
        try:
            return pygame.mixer.Sound(filename)
        except:
            raise

def loadMusic(filename):
    try:
        base_name = filename.replace(".wav", "").replace(".mp3", "")
        ogg_filename = f"Compressed_{base_name}.ogg"
        pygame.mixer.music.load(ogg_filename)
    except:
        try:
            pygame.mixer.music.load(filename)
        except:
            raise

valveSound = loadAudio("Audio/valve.wav")
switchSound = loadAudio("Audio/switch.wav")

heartbeat = loadAudio("Audio/heartbeat.wav")

ominousAmb = loadAudio("Audio/mainroomambience.wav")
ominousAmb.set_volume(0.075)
powerAmb = loadAudio("Audio/powerambience-1.wav")
powerAmb.set_volume(0.80)

brainwash = loadAudio("Audio/weird noises.-2.wav")
book = loadAudio("Audio/book.wav")
page = loadAudio("Audio/page.wav")

magnet1 = loadAudio("Audio/magnet1.wav")
magnet2 = loadAudio("Audio/magnet2.wav")
magnet3 = loadAudio("Audio/magnet3.wav")

glass1 = loadAudio("Audio/glass1.wav")
glass2 = loadAudio("Audio/glass2.wav")

magnets = [magnet1, magnet2, magnet3]
glass = [glass1, glass2]

for magnet in magnets:
    magnet.set_volume(0.75)

draweropen = loadAudio("Audio/draweropen.wav")
drawerclose = loadAudio("Audio/drawerclose.wav")

letter = loadAudio("Audio/opentriangle.wav")

combo = loadAudio("Audio/combo.wav")

powerOn = loadAudio("Audio/powerOnAmbStart.wav")
powerOnAmb = loadAudio("Audio/powerOnAmb.wav")

mopSound = loadAudio("Audio/mopsounds.wav")

electricityNoise = loadAudio("Audio/ElectricityNoise.wav")

pipe = loadAudio("Audio/pipe.wav")

toolbox = loadAudio("Audio/toolboxOpenClose.wav")

lockerOpen = loadAudio("Audio/locker_open.wav")
lockerClose = loadAudio("Audio/locker_close.wav")

powerDown = loadAudio("Audio/power_down.mp3")

tape = loadAudio("Audio/tape.wav")

scaryBell = loadAudio("Audio/scary_bell.wav")
slowCreepy = loadAudio("Audio/slow_creepy.wav")

pickup = loadAudio("Audio/pickup.wav")
pickup.set_volume(.8)

spark1 = loadAudio("Audio/spark1.wav")
spark2 = loadAudio("Audio/spark2.wav")
spark3 = loadAudio("Audio/spark3.wav")
spark4 = loadAudio("Audio/spark4.wav")
spark5 = loadAudio("Audio/spark5.wav")
spark1.set_volume(0.4)
spark2.set_volume(0.4)
spark3.set_volume(0.4)
spark4.set_volume(0.4)
spark5.set_volume(0.4)

radioClose = loadAudio("Audio/radio_close.wav")
radioFar = loadAudio("Audio/radio_far.wav")

curtain = loadAudio("Audio/curtain.wav")
curtain.set_volume(.5)
openClose = loadAudio("Audio/toolboxOpenClose.wav")
openClose.set_volume(.5)
sink = loadAudio("Audio/sink.wav")
sink.set_volume(.3)
sink2 = loadAudio("Audio/sink.wav")
sink2.set_volume(.3)

accessGranted = loadAudio("Audio/accessgranted.mp3")

bunsen = loadAudio("Audio/bunsen.wav")
lighter = loadAudio("Audio/lighter.wav")

unlock = loadAudio("Audio/unlock.wav")

scary = loadAudio("Audio/scary.wav")
scary.set_volume(0.5)

TrashSounds = loadAudio("Audio/TrashSounds.wav")

pour = loadAudio("Audio/pour.wav")
pour.set_volume(0.1)

explosion = loadAudio("Audio/explosion.wav")

plop = loadAudio("Audio/plop.wav")
plop.set_volume(0.1)