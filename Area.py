from Rooms import ControlRoom, MainRoom, PinkRoom, PinkLowerWing, BookcaseView, OrangeYellow, \
Safe, PinkUpperWing, TrianglePuzzle, TriangleSolution, BeakerPuzzle, MscopeTable, Microscope, \
LockedDoor, Desk, SpotDiffs, PinkPower, BlueRoom

# Getter functions for getting information about rooms the player isn't currently in. Use the corresponding functions in Objects.py, not these, when accessing info.
def getPipeDungeonInfo():
    return ControlRoom.level, ControlRoom.power

def getPinkWingInfo():
    return PinkRoom.upperWingPower, PinkRoom.lowerWingPower

def getCutscene():
    return BookcaseView.cutscene

def getTriangleSolved():
    return TrianglePuzzle.solved

def getBeakerSolved():
    return BeakerPuzzle.solved

def getSpotDiffsSolved():
    return SpotDiffs.chestOpen

def getColors():
    return MscopeTable.redPlaced, MscopeTable.yellowPlaced, MscopeTable.bluePlaced

def getSelected():
    return MscopeTable.selected

def getOpen():
    return LockedDoor.solved

def getPinkPower():
    return PinkPower.pinkPower

def getLetterCount():
    return LockedDoor.letterCount

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
            ControlRoom: [MainRoom],
            MainRoom: [ControlRoom, PinkRoom, BlueRoom],
            PinkRoom: [MainRoom, PinkLowerWing, PinkUpperWing],
            PinkLowerWing: [PinkRoom, BookcaseView, LockedDoor, Desk, SpotDiffs, PinkPower],
            BookcaseView: [PinkLowerWing, OrangeYellow, Safe],
            OrangeYellow: [BookcaseView],
            Safe: [BookcaseView],
            LockedDoor: [PinkLowerWing, PinkPower],
            Desk: [PinkLowerWing],
            SpotDiffs: [PinkLowerWing],
            PinkUpperWing: [PinkRoom, TrianglePuzzle, TriangleSolution, BeakerPuzzle, MscopeTable],
            TrianglePuzzle: [PinkUpperWing],
            TriangleSolution: [PinkUpperWing],
            BeakerPuzzle: [PinkUpperWing], 
            MscopeTable: [PinkUpperWing, Microscope],
            Microscope: [MscopeTable],
            PinkPower: [PinkLowerWing],
            BlueRoom: [MainRoom]
    }
)

