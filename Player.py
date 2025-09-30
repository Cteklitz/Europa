import pygame
import Items
import os

health = 100
inventory = []
MaxInventorySize = 7

# Sprite animation handling
sprites = {
    'idle': None,
    'walk_right': [],
    'walk_left': [],
    'walk_up': [],
    'walk_down': []
}

current_frame = 0
animation_timer = 0
ANIMATION_DELAY = 100  # milliseconds between frames
facing = 'right'
is_moving = False

def load_sprites():
    global sprites
    sprite_dir = os.path.join('Assets', 'player')
    
    # Load all walking animations
    # You'll need to place your scuba diver images in the Assets/player folder
    for i in range(1, 21):  # Assuming you have 20 frames
        try:
            img = pygame.image.load(os.path.join(sprite_dir, f'scuba_walk_{i}.png')).convert_alpha()
            # Add the sprite to the appropriate direction list
            frame_index = (i - 1) // 5  # Assuming 5 frames per direction
            if frame_index == 0:
                sprites['walk_right'].append(img)
            elif frame_index == 1:
                sprites['walk_left'].append(pygame.transform.flip(img, True, False))
            elif frame_index == 2:
                sprites['walk_up'].append(img)
            elif frame_index == 3:
                sprites['walk_down'].append(img)
        except pygame.error as e:
            print(f"Couldn't load sprite frame {i}: {e}")
    
    # Set idle sprite as the first frame of walk_right if no specific idle sprite
    if sprites['walk_right']:
        sprites['idle'] = sprites['walk_right'][0]

def get_current_sprite():
    global current_frame, animation_timer
    
    if not is_moving:
        return sprites['idle']
    
    # Update animation frame
    current_time = pygame.time.get_ticks()
    if current_time - animation_timer > ANIMATION_DELAY:
        animation_timer = current_time
        current_frame = (current_frame + 1) % len(sprites[f'walk_{facing}'])
    
    return sprites[f'walk_{facing}'][current_frame]

def update_movement(dx, dy):
    global facing, is_moving
    
    is_moving = dx != 0 or dy != 0
    
    if dx > 0:
        facing = 'right'
    elif dx < 0:
        facing = 'left'
    elif dy > 0:
        facing = 'down'
    elif dy < 0:
        facing = 'up'

def load_sprites():
    global sprites
    sprite_dir = os.path.join('Assets', 'player')
    
    # Load right walking animations (2 frames)
    for i in range(1, 3):
        try:
            img = pygame.image.load(os.path.join(sprite_dir, f'walk_right_{i}.png')).convert_alpha()
            sprites['walk_right'].append(img)
        except pygame.error as e:
            print(f"Couldn't load right walk frame {i}: {e}")
    
    # Load left walking animations (2 frames)
    for i in range(1, 3):
        try:
            img = pygame.image.load(os.path.join(sprite_dir, f'walk_left_{i}.png')).convert_alpha()
            sprites['walk_left'].append(img)
        except pygame.error as e:
            print(f"Couldn't load left walk frame {i}: {e}")

def get_current_sprite():
    global current_frame, animation_timer
    
    if not is_moving:
        # When not moving, show frame 0 of current facing direction
        return sprites[f'walk_{facing}'][0]
    
    # Update animation frame
    current_time = pygame.time.get_ticks()
    if current_time - animation_timer > ANIMATION_DELAY:
        animation_timer = current_time
        current_frame = (current_frame + 1) % len(sprites[f'walk_{facing}'])
    
    # Return current animation frame for the facing direction
    return sprites[f'walk_{facing}'][current_frame]

def update_movement(dx, dy):
    global facing, is_moving
    
    is_moving = dx != 0 or dy != 0
    
    # Only update facing direction for horizontal movement
    if dx > 0:
        facing = 'right'
    elif dx < 0:
        facing = 'left'
    # For vertical movement (dx == 0), keep the last facing direction

def handle_movement(keys, dt, player_pos, y_speed_scale, x_speed_scale, room, area, update_room_func):
    """
    Handle player movement input and room transitions
    Returns: (dx, dy) for animation purposes
    """
    dx = dy = 0
    
    if keys[pygame.K_w]:
        y = player_pos.y - 325 * dt / y_speed_scale
        #Checks if the movement upwards results in room change. If so, update the room to new room and set the initial position with positionDeterminer
        check = room.inBounds(player_pos.x, y)
        if type(check) == int:
            came_from = room
            update_room_func(area.getRoom(room, check))
            room = update_room_func.__globals__.get('Room')  # Get updated room reference
            if room:
                room.positionDeterminer(came_from.__name__)
        elif check:
            player_pos.y = y
            dy = -1
    
    if keys[pygame.K_s]:
        y = player_pos.y + 325 * dt / y_speed_scale
        #Checks if the movement downwards results in room change. If so, update the room to new room and set the initial position with positionDeterminer
        check = room.inBounds(player_pos.x, y)
        if type(check) == int:
            came_from = room
            update_room_func(area.getRoom(room, check))
            room = update_room_func.__globals__.get('Room')  # Get updated room reference
            if room:
                room.positionDeterminer(came_from.__name__)
        elif check:
            player_pos.y = y
            dy = 1
    
    if keys[pygame.K_a]:
        x = player_pos.x - 325 * dt / x_speed_scale
        #Checks if the movement to the left results in room change. If so, update the room to new room and set the initial position with positionDeterminer
        check = room.inBounds(x, player_pos.y)
        if type(check) == int:
            came_from = room
            update_room_func(area.getRoom(room, check))
            room = update_room_func.__globals__.get('Room')  # Get updated room reference
            if room:
                room.positionDeterminer(came_from.__name__)
        elif check:
            player_pos.x = x
            dx = -1
    
    if keys[pygame.K_d]:
        x = player_pos.x + 325 * dt / x_speed_scale
        #Checks if the movement to the right results in room change. If so, update the room to new room and set the initial position with positionDeterminer
        check = room.inBounds(x, player_pos.y)
        if type(check) == int:
            came_from = room
            update_room_func(area.getRoom(room, check))
            room = update_room_func.__globals__.get('Room')  # Get updated room reference  
            if room:
                room.positionDeterminer(came_from.__name__)
        elif check:
            player_pos.x = x
            dx = 1

    #Checks if any other input (mouse click, backspace, etc.) results in room change. If so, update the room to new room and set the initial position with positionDeterminer
    check = room.inBounds(player_pos.x, player_pos.y)
    if type(check) == int:
        came_from = room
        update_room_func(area.getRoom(room, check))
        room = update_room_func.__globals__.get('Room')  # Get updated room reference
        if room:
            room.positionDeterminer(came_from.__name__)
    
    # Update animation state
    update_movement(dx, dy)
    
    return dx, dy

# adds an item to iventory
def addItem(item):
    if (len(inventory) < MaxInventorySize):
        inventory.append(item)
        return True
    else:
        return False
    
# checks if an item is in the inventory (can check based on item object or id); Probably try to use id mostly?
def checkItem(_item):
    if (type(_item) is Items.Item):
        for item in inventory:
            if _item.id == item.id:
                return True
        return False # return false if item not found
    elif (type(_item) is str):
        for item in inventory:
                if _item == item.id:
                    return True
        return False # return false if item not found
    else:
        print("ERROR: Item type not valid")
        return False

# removes an item from the inventory, takes either id or item object
# this is for removing items that dont have a global effect, like placing a quest item or dropping an item
# use consumeItem for consumable items that should do something
def removeItem(_item):
    if (type(_item) is Items.Item):
        for i in range(len(inventory)): # int itertor bc we need the index the item is found at to pop it
            if _item.id == inventory[i].id:
                inventory.pop(i)
                return True
        return False # return false if item not found
    elif (type(_item) is str):
        for i in range(len(inventory)):
                if _item == inventory[i].id:
                    inventory.pop(i)
                    return True
        return False # return false if item not found
    else:
        print("ERROR: Item type not valid")
        return False
        
# Consumes the item at the input index in the player inventory. Will activate any global effects here
def consumeItem(index):
    if index in range(len(inventory)):
        item = inventory[index]

        match item:
            case Items.bandage:
                health += 15
                if health >= 100:
                    health = 100
                inventory.pop(index)
                return True
            case _:
                print(item.name + " cannot be consumed")
                return False
    else:
        print(str(index) + " is not a valid inventory value")
        return False