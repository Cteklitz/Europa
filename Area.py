from Rooms import TitleScreen, ControlRoom, MainRoom, PinkRoom, PinkLowerWing, BookcaseView, OrangeYellow, \
Safe, PinkUpperWing, TrianglePuzzle, TriangleSolution, BeakerPuzzle, MscopeTable, Microscope, \
LockedDoor, Desk, SpotDiffs, PinkPower, BlueRoom, BreakerRoom, PuddleRoom, Toolbox, BreakerPuzzle,     \
StorageCloset, ValvePuzzle, BluePower, LockerView, PuddleView, GreenRoom, Bedroom, Greenhouse, Bathroom, BedView, \
TornNotePuzzle, BedroomDeskView, GreenPower, YellowRoom, YellowHallway, SubRoom, Fishtank_puzzle, Lockbox_puzzle

# Getter functions for getting information about rooms the player isn't currently in. Use the corresponding functions in Objects.py, not these, when accessing info.
def getPipeDungeonInfo():
    return ControlRoom.level, ControlRoom.power

def getPinkWingInfo():
    return PinkRoom.upperWingPower, PinkRoom.lowerWingPower

def getBunsenOn():
    if MscopeTable.correctIngredients:
        return False
    else:
        return MscopeTable.bunsen and MscopeTable.on

def getCutscene():
    return BookcaseView.cutscene

def getTriangleSolved():
    return TrianglePuzzle.solved

def getBeakerSolved():
    # return BeakerPuzzle.solved
    return True

def getSpotDiffsSolved():
    return SpotDiffs.chestOpen

def getLockboxSolved():
    return Lockbox_puzzle.solved

def getColorsFound():
    return MscopeTable.redFound, OrangeYellow.yellowFound, Desk.blueFound

def getColorsPlaced():
    return MscopeTable.redPlaced, MscopeTable.yellowPlaced, MscopeTable.bluePlaced

def getSelected():
    return MscopeTable.selected

def getOpen():
    #return LockedDoor.solved
    return True

def getPinkPower():
    return True
    #return PinkPower.pinkPower

def getBluePower():
    return True
    return BluePower.bluePower

def getGreenPower():
    # return GreenPower.greenPower
    return True

def getLetterCount():
    return LockedDoor.letterCount

def getWaterLevelsSolved():
    return ValvePuzzle.solved

def getBreakerSolved():
    return True
    #return BreakerPuzzle.solved

def RepairWire():
    PuddleRoom.wireRepaired = True

def getWireRepaired():
    return PuddleRoom.wireRepaired

def getBedroomNumber():
    return Bedroom.BedroomNumber

def setBedroomNumber(num):
    Bedroom.BedroomNumber = num

def getBedNumber():
    return BedView.bedNumber

def setBedNumber(num):
    BedView.bedNumber = num

def getEyeLockerUnlocked():
    return True
    # return LockerView.unlocked

def getRadioOn():
    return GreenRoom.radioOn

def toggleRadio():
    GreenRoom.radioOn = not GreenRoom.radioOn

def getValvePlaced():
    return YellowHallway.valvePlaced

class Area:
    def __init__(self, roomLayout):
        self.roomLayout = roomLayout

    def getRoom(self, Room, check):
        return self.roomLayout[Room][check]

    # Passes information from main game loop to the current room's Room() loop, as well as returns results of the room's loop back to main game loop.
    def getPos(self, screen, screen_res, events, room):
        player_pos, xSpeedScale, ySpeedScale = room.Room(screen, screen_res, events)
        return player_pos, xSpeedScale, ySpeedScale


PipeDungeon = Area(
    # Map/Dictionary that is a list of all of the rooms in the Area and what rooms they are connected to.
    roomLayout = {
            TitleScreen: [MainRoom],
            ControlRoom: [MainRoom],
            MainRoom: [ControlRoom, PinkRoom, BlueRoom, GreenRoom, YellowRoom],
            PinkRoom: [MainRoom, PinkLowerWing, PinkUpperWing],
            PinkLowerWing: [PinkRoom, BookcaseView, LockedDoor, Desk, SpotDiffs, PinkPower, Fishtank_puzzle],
            BookcaseView: [PinkLowerWing, OrangeYellow, Safe, Fishtank_puzzle],
            OrangeYellow: [BookcaseView],
            Safe: [BookcaseView],
            LockedDoor: [PinkLowerWing, PinkPower],
            Desk: [PinkLowerWing],
            SpotDiffs: [PinkLowerWing, Lockbox_puzzle],
            PinkUpperWing: [PinkRoom, TrianglePuzzle, TriangleSolution, BeakerPuzzle, MscopeTable],
            TrianglePuzzle: [PinkUpperWing],
            TriangleSolution: [PinkUpperWing],
            BeakerPuzzle: [PinkUpperWing], 
            MscopeTable: [PinkUpperWing, Microscope],
            Microscope: [MscopeTable],
            PinkPower: [PinkLowerWing],
            BlueRoom: [MainRoom, BreakerRoom],
            BreakerRoom: [BlueRoom, PuddleRoom, BreakerPuzzle, Toolbox],
            PuddleRoom: [BreakerRoom, StorageCloset, ValvePuzzle, BluePower, PuddleView],
            PuddleView: [PuddleRoom],
            BreakerPuzzle: [BreakerRoom],
            StorageCloset: [PuddleRoom, LockerView],
            LockerView: [StorageCloset],
            ValvePuzzle: [PuddleRoom],
            BluePower: [PuddleRoom],
            Toolbox: [BreakerRoom],
            GreenRoom: [MainRoom, Bathroom, Bedroom, Greenhouse, GreenPower],
            Bedroom: [GreenRoom, BedView, TornNotePuzzle, BedroomDeskView],
            BedroomDeskView: [Bedroom],
            Greenhouse: [GreenRoom],
            Bathroom: [GreenRoom],
            BedView: [Bedroom],
            TornNotePuzzle: [Bedroom],
            GreenPower: [GreenRoom],
            YellowRoom: [MainRoom, YellowHallway],
            YellowHallway: [YellowRoom, SubRoom],
            SubRoom: [YellowHallway],
            Fishtank_puzzle: [PinkLowerWing, BookcaseView],
            Lockbox_puzzle: [SpotDiffs]
    }
)

