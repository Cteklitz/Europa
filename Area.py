from Rooms import ControlRoom, MainRoom, PinkRoom, PinkLowerWing, BookcaseView, OrangeYellow, \
Safe, PinkUpperWing, TrianglePuzzle, TriangleSolution, BeakerPuzzle, MscopeTable, Microscope, \
LockedDoor, Desk, Lockbox_puzzle, PinkPower, BlueRoom, Fishtank_puzzle, SpotDiffs

import pygame

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

def getLockboxSolved():
    return Lockbox_puzzle.chestOpen

def getColors():
    return MscopeTable.redFound, OrangeYellow.yellowFound, Desk.blueFound

def getSelected():
    return MscopeTable.selected

def getOpen():
    return LockedDoor.solved

def getPinkPower():
    return PinkPower.pinkPower

def getLetterCount():
    count = 0
    if TrianglePuzzle.collected:
        count += 1
    if BeakerPuzzle.collected:
        count += 1
    if Safe.collected:
        count += 1
    if Lockbox_puzzle.collected:
        count += 1
    return count

class Area:
    def __init__(self, roomLayout):
        self.roomLayout = roomLayout

    def getRoom(self, Room, check):
        return self.roomLayout[Room][check]

    def getPos(self, screen, screen_res, events, room):
        # Always show cursor
        pygame.mouse.set_visible(True)
            
        result = room.Room(screen, screen_res, events)
        if len(result) == 4:  # Some rooms return a transition value
            player_pos, xSpeedScale, ySpeedScale, transition = result
            if transition != 0:  # If transitioning
                next_room = self.roomLayout[room][transition]  # Get the next room
                return self.getPos(screen, screen_res, events, next_room)  # Go to next room
        else:  # Normal case with 3 values
            player_pos, xSpeedScale, ySpeedScale = result
        
        # Get the virtual resolution from the room
        virtual_res = getattr(room, 'virtual_res', (400, 400))  # Default if not found
        
        # Only draw player sprite if not in a puzzle room or zoomed view, and not viewing whiteboard
        if (room not in [TrianglePuzzle, TriangleSolution, BeakerPuzzle, Lockbox_puzzle, Fishtank_puzzle, MscopeTable, Microscope, BookcaseView, OrangeYellow, Safe, SpotDiffs, Desk, LockedDoor,] 
            and not (room == PinkUpperWing and PinkUpperWing.whiteboard)):
            # Get the current sprite
            import Player  # Import here to avoid circular import
            current_sprite = Player.get_current_sprite()
            if current_sprite:
                # Use consistent sprite size regardless of room
                BASE_SPRITE_SIZE = 100  # Fixed base sprite size
                
                # Scale sprite size based on screen resolution, not virtual resolution
                sprite_size = int(BASE_SPRITE_SIZE * (screen_res[1] / 1080))  # Scale based on screen height
                scaled_sprite = pygame.transform.scale(current_sprite, (sprite_size, sprite_size))
                
                # Calculate scaled position
                screen_x = player_pos.x * screen_res[0] / virtual_res[0]
                screen_y = player_pos.y * screen_res[1] / virtual_res[1]
                
                # Position the sprite
                sprite_rect = scaled_sprite.get_rect(center=(screen_x, screen_y))
                screen.blit(scaled_sprite, sprite_rect)
            
        return player_pos, xSpeedScale, ySpeedScale
    
PipeDungeon = Area(
    roomLayout = {
            ControlRoom: [MainRoom],
            MainRoom: [ControlRoom, PinkRoom, BlueRoom],
            PinkRoom: [MainRoom, PinkLowerWing, PinkUpperWing],
            PinkLowerWing: [PinkRoom, BookcaseView, LockedDoor, Desk, SpotDiffs, PinkPower, Fishtank_puzzle],
            BookcaseView: [PinkLowerWing, OrangeYellow, Safe],
            OrangeYellow: [BookcaseView],
            Safe: [BookcaseView],
            LockedDoor: [PinkLowerWing, PinkPower],
            Desk: [PinkLowerWing],
            Lockbox_puzzle: [PinkLowerWing],
            PinkUpperWing: [PinkRoom, TrianglePuzzle, TriangleSolution, BeakerPuzzle, MscopeTable],
            TrianglePuzzle: [PinkUpperWing],
            TriangleSolution: [PinkUpperWing],
            BeakerPuzzle: [PinkUpperWing], 
            MscopeTable: [PinkUpperWing, Microscope],
            Microscope: [MscopeTable],
            PinkPower: [PinkLowerWing],
            BlueRoom: [MainRoom],
            Fishtank_puzzle: [PinkLowerWing],
            SpotDiffs: [PinkLowerWing, Lockbox_puzzle],
            Lockbox_puzzle: [SpotDiffs]
    }
)

