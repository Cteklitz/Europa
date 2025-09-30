"""
Debug System for Europa Game
Provides debug panel and cheat functions for development and testing
"""

import pygame


class DebugSystem:
    """Debug system for Europa game - handles debug panel and cheat functions"""
    
    def __init__(self):
        self.panel_open = False
        self.font_large = None
        self.font_medium = None
        self.current_tab = "cheats"  
        self.teleport_target = None  # Room to teleport to
    
    def initialize_fonts(self):
        """Initialize fonts when pygame is ready"""
        if self.font_large is None:
            self.font_large = pygame.font.Font(None, 36)
            self.font_medium = pygame.font.Font(None, 24)
    
    def toggle_panel(self):
        """Toggle the debug panel open/closed"""
        self.panel_open = not self.panel_open
    
    def close_panel(self):
        """Close the debug panel"""
        self.panel_open = False
    
    def complete_control_room(self):
        """Debug function to autocomplete the ControlRoom puzzle"""
        import Rooms.ControlRoom as ControlRoom
        
        # Set the pipePuzzle to the correct solution
        for (row, col), correct_value in ControlRoom.solution.items():
            ControlRoom.pipePuzzle[row][col] = correct_value
        
        # Trigger the solution check which will set solved=True, power=True, and activeSquares
        ControlRoom.checkSolution(ControlRoom.pipePuzzle, ControlRoom.solution)
        
        print("DEBUG: ControlRoom autocompleted!")
    
    def enable_pink_power(self):
        """Debug function to enable pink power by completing the full sequence"""
        import Rooms.ControlRoom as ControlRoom
        
        # Step 1: Complete ControlRoom puzzle (if not already done)
        if not ControlRoom.solved:
            # Set the pipePuzzle to the correct solution
            for (row, col), correct_value in ControlRoom.solution.items():
                ControlRoom.pipePuzzle[row][col] = correct_value
            
            # Trigger the solution check
            ControlRoom.checkSolution(ControlRoom.pipePuzzle, ControlRoom.solution)
        
        # Step 2: Set pink switch active (level = 1) and ensure power is on
        ControlRoom.level = 1
        ControlRoom.power = True
        
        # Step 3: Set active squares to pink pattern
        ControlRoom.activeSquares = [
            [0,0,1,0,0],
            [1,1,1,0,0],
            [1,1,1,1,1],
            [1,1,1,1,1],
            [1,1,1,0,0]
        ]
        
        # Step 4: Activate the pink switch in the switches
        if hasattr(ControlRoom, 'switches') and 1 in ControlRoom.switches:
            ControlRoom.switches[1].image = ControlRoom.switches[1].tileset[1]  # Set to active state
        
        print("DEBUG: Pink Power sequence completed! (ControlRoom solved + Pink switch activated + Power on)")
    
    def teleport_to_room(self, room_name):
        """Debug function to teleport to a specific room"""
        self.teleport_target = room_name
        print(f"DEBUG: Teleporting to {room_name}!")
    
    def draw_panel(self, screen, screen_res, events):
        """Draw the debug panel with tabs and clickable buttons"""
        if not self.panel_open:
            return
        
        self.initialize_fonts()
        
        # Create semi-transparent overlay
        overlay = pygame.Surface(screen_res, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        screen.blit(overlay, (0, 0))
        
        # Panel dimensions
        panel_width = 450
        panel_height = 400
        panel_x = (screen_res[0] - panel_width) // 2
        panel_y = (screen_res[1] - panel_height) // 2
        
        # Draw panel background
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(screen, (50, 50, 70), panel_rect)
        pygame.draw.rect(screen, (100, 100, 120), panel_rect, 3)
        
        # Draw tabs
        tab_width = panel_width // 2
        tab_height = 35
        
        # Cheats tab
        cheats_tab_rect = pygame.Rect(panel_x, panel_y, tab_width, tab_height)
        cheats_active = self.current_tab == "cheats"
        cheats_color = (70, 70, 90) if cheats_active else (40, 40, 60)
        pygame.draw.rect(screen, cheats_color, cheats_tab_rect)
        pygame.draw.rect(screen, (100, 100, 120), cheats_tab_rect, 2)
        
        cheats_text = self.font_medium.render("Cheats", True, (255, 255, 255))
        cheats_text_rect = cheats_text.get_rect(center=cheats_tab_rect.center)
        screen.blit(cheats_text, cheats_text_rect)
        
        # Teleport tab
        teleport_tab_rect = pygame.Rect(panel_x + tab_width, panel_y, tab_width, tab_height)
        teleport_active = self.current_tab == "teleport"
        teleport_color = (70, 70, 90) if teleport_active else (40, 40, 60)
        pygame.draw.rect(screen, teleport_color, teleport_tab_rect)
        pygame.draw.rect(screen, (100, 100, 120), teleport_tab_rect, 2)
        
        teleport_text = self.font_medium.render("Teleport", True, (255, 255, 255))
        teleport_text_rect = teleport_text.get_rect(center=teleport_tab_rect.center)
        screen.blit(teleport_text, teleport_text_rect)
        
        # Close button (X) - positioned below tabs
        close_button_size = 25
        close_button_x = panel_x + panel_width - close_button_size - 8
        close_button_y = panel_y + tab_height + 5
        close_button_rect = pygame.Rect(close_button_x, close_button_y, close_button_size, close_button_size)
        
        mouse_pos = pygame.mouse.get_pos()
        close_hovering = close_button_rect.collidepoint(mouse_pos)
        close_color = (150, 50, 50) if close_hovering else (120, 40, 40)
        pygame.draw.rect(screen, close_color, close_button_rect)
        pygame.draw.rect(screen, (200, 80, 80), close_button_rect, 2)
        
        # X text
        x_text = self.font_medium.render("X", True, (255, 255, 255))
        x_text_rect = x_text.get_rect(center=close_button_rect.center)
        screen.blit(x_text, x_text_rect)
        
        # Content area
        content_y = panel_y + tab_height + 10
        content_height = panel_height - tab_height - 60
        
        button_rects = []
        
        if self.current_tab == "cheats":
            button_rects = self.draw_cheats_tab(screen, panel_x, content_y, panel_width, content_height, mouse_pos)
        elif self.current_tab == "teleport":
            button_rects = self.draw_teleport_tab(screen, panel_x, content_y, panel_width, content_height, mouse_pos)
        
        # Instructions
        instruction_text = self.font_medium.render("Press H again or ESC to close", True, (200, 200, 200))
        instruction_rect = instruction_text.get_rect(center=(panel_x + panel_width // 2, panel_y + panel_height - 20))
        screen.blit(instruction_text, instruction_rect)
        
        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h or event.key == pygame.K_ESCAPE:
                    self.close_panel()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Check close button first (highest priority)
                    if close_button_rect.collidepoint(event.pos):
                        self.close_panel()
                    # Then check tabs
                    elif cheats_tab_rect.collidepoint(event.pos):
                        self.current_tab = "cheats"
                    elif teleport_tab_rect.collidepoint(event.pos):
                        self.current_tab = "teleport"
                    # Then check if click is outside panel
                    elif not panel_rect.collidepoint(event.pos):
                        self.close_panel()  # Close if clicked outside panel
                    else:
                        # Finally check content button clicks
                        self.handle_button_clicks(event.pos, button_rects)
    
    def draw_cheats_tab(self, screen, panel_x, content_y, panel_width, content_height, mouse_pos):
        """Draw the cheats tab content"""
        button_width = 350
        button_height = 50
        button_x = panel_x + (panel_width - button_width) // 2
        
        # Button 1: Autocomplete ControlRoom
        button1_y = content_y + 20
        button1_rect = pygame.Rect(button_x, button1_y, button_width, button_height)
        
        # Button 2: Complete Pink Power Sequence
        button2_y = content_y + 80
        button2_rect = pygame.Rect(button_x, button2_y, button_width, button_height)
        
        hovering1 = button1_rect.collidepoint(mouse_pos)
        hovering2 = button2_rect.collidepoint(mouse_pos)
        
        # Draw Button 1 (ControlRoom)
        button1_color = (80, 120, 80) if hovering1 else (60, 100, 60)
        pygame.draw.rect(screen, button1_color, button1_rect)
        pygame.draw.rect(screen, (120, 160, 120), button1_rect, 2)
        
        button1_text = self.font_medium.render("Autocomplete ControlRoom", True, (255, 255, 255))
        button1_text_rect = button1_text.get_rect(center=button1_rect.center)
        screen.blit(button1_text, button1_text_rect)
        
        # Draw Button 2 (Pink Power)
        button2_color = (120, 80, 120) if hovering2 else (100, 60, 100)
        pygame.draw.rect(screen, button2_color, button2_rect)
        pygame.draw.rect(screen, (160, 120, 160), button2_rect, 2)
        
        button2_text = self.font_medium.render("Complete Pink Power Sequence", True, (255, 255, 255))
        button2_text_rect = button2_text.get_rect(center=button2_rect.center)
        screen.blit(button2_text, button2_text_rect)
        
        return [("complete_control_room", button1_rect), ("enable_pink_power", button2_rect)]
    
    def draw_teleport_tab(self, screen, panel_x, content_y, panel_width, content_height, mouse_pos):
        """Draw the teleport tab content"""
        button_width = 350
        button_height = 45
        button_x = panel_x + (panel_width - button_width) // 2
        
        rooms = [
            ("ControlRoom", "Control Room"),
            ("PinkLowerWing", "Pink Lower Wing"), 
            ("PinkUpperWing", "Pink Upper Wing")
        ]
        
        button_rects = []
        
        for i, (room_id, room_name) in enumerate(rooms):
            button_y = content_y + 20 + (i * 55)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            
            hovering = button_rect.collidepoint(mouse_pos)
            button_color = (80, 80, 120) if hovering else (60, 60, 100)
            
            pygame.draw.rect(screen, button_color, button_rect)
            pygame.draw.rect(screen, (120, 120, 160), button_rect, 2)
            
            button_text = self.font_medium.render(f"Teleport to {room_name}", True, (255, 255, 255))
            button_text_rect = button_text.get_rect(center=button_rect.center)
            screen.blit(button_text, button_text_rect)
            
            button_rects.append((f"teleport_{room_id}", button_rect))
        
        return button_rects
    
    def handle_button_clicks(self, click_pos, button_rects):
        """Handle button clicks based on the button rectangles"""
        for action, rect in button_rects:
            if rect.collidepoint(click_pos):
                if action == "complete_control_room":
                    self.complete_control_room()
                    self.close_panel()
                elif action == "enable_pink_power":
                    self.enable_pink_power()
                    self.close_panel()
                elif action.startswith("teleport_"):
                    room_name = action.replace("teleport_", "")
                    self.teleport_to_room(room_name)
                    self.close_panel()
                break


# Global debug system instance
debug_system = DebugSystem()