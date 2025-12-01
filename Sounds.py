import pygame

globalVolume = 1.0

def loadAudio(filename):
    try:
        # Try to load .ogg
        base_name = filename.replace(".wav", "").replace(".mp3", "")
        ogg_filename = f"Compressed_{base_name}.ogg"
        sound = pygame.mixer.Sound(ogg_filename)
        sound.set_volume(globalVolume ** 2)
        return sound
    except:
        # If .ogg fails, try the original file in "Raw Audio/" directory
        try:
            sound = pygame.mixer.Sound(filename)
            sound.set_volume(globalVolume ** 2)
            return sound
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

def setVolume(self, volume):
    volume = volume ** 2 # use exponential scaling for volume
    volume = volume * (globalVolume ** 2) # adjust by global volume
    self.set_volume(volume)

valveSound = loadAudio("Audio/valve.wav")
switchSound = loadAudio("Audio/switch.wav")

heartbeat = loadAudio("Audio/heartbeat.wav")

ominousAmb = loadAudio("Audio/mainroomambience.wav")
setVolume(ominousAmb, 0.274)
powerAmb = loadAudio("Audio/powerambience-1.wav")
setVolume(powerAmb, 0.89)

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
    setVolume(magnet, 0.867)

draweropen = loadAudio("Audio/draweropen.wav")
drawerclose = loadAudio("Audio/drawerclose.wav")

letter = loadAudio("Audio/opentriangle.wav")

combo = loadAudio("Audio/combo.wav")

powerOn = loadAudio("Audio/powerOnAmbStart.wav")
powerOnAmb = loadAudio("Audio/powerOnAmb.wav")

mopSound = loadAudio("Audio/mopsounds.wav")

electricityNoise = loadAudio("Audio/ElectricityNoise.wav")

pipe = loadAudio("Audio/pipe.wav")

toolbox = pygame.mixer.Sound("Audio/toolboxOpenClose.wav")

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
setVolume(spark1, 0.3)
setVolume(spark2, 0.3)
setVolume(spark3, 0.3)
setVolume(spark4, 0.3)
setVolume(spark5, 0.3)
sparks = [spark1, spark2, spark3, spark4, spark5]

drain = loadAudio("Audio/drain.wav")
setVolume(drain, 0.3)

radioClose = loadAudio("Audio/radio_close.wav")
radioFar = loadAudio("Audio/radio_far.wav")

curtain = loadAudio("Audio/curtain.wav")
setVolume(curtain, 0.71)
openClose = pygame.mixer.Sound("Audio/toolboxOpenClose.wav")
openClose.set_volume(0.71)
sink = loadAudio("Audio/sink.wav")
setVolume(sink, 0.55)
sink2 = loadAudio("Audio/sink.wav")
setVolume(sink2, 0.55)

accessGranted = loadAudio("Audio/accessgranted.mp3")

bunsen = loadAudio("Audio/bunsen.wav")
lighter = loadAudio("Audio/lighter.wav")

unlock = loadAudio("Audio/unlock.wav")

scary = loadAudio("Audio/scary.wav")
setVolume(scary, 0.71)

TrashSounds = loadAudio("Audio/TrashSounds.wav")

pour = loadAudio("Audio/pour.wav")
setVolume(pour, 0.316)

explosion = loadAudio("Audio/explosion.wav")
explosion2 = loadAudio("Audio/explosion2.wav")

plop = loadAudio("Audio/plop.wav")
setVolume(plop, 0.316)

blink = loadAudio("Audio/blink.wav")
setVolume(blink, 0.20)

whispers = loadAudio("Audio/whispers.wav")
setVolume(whispers, 0.20)

## MUSIC

pauseMusic = loadAudio("Audio/wading_into_the_unknown.wav")
setVolume(pauseMusic, 0.4)

whatAwaits = loadAudio("Audio/what_awaits.wav")
setVolume(whatAwaits, 0.6)

electrician = loadAudio("Audio/Electrician.wav")
setVolume(electrician, 0.6)

valveSong = loadAudio("Audio/Glass.wav")
setVolume(valveSong, 0.4)