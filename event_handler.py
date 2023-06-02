from widgets import widget_instances, text_input_instances
import pygame

#mouse actions
IDLE = 0
CLICKED = 1
HELD = 2
RELEASED = 3



class Event_Handler:
    
    #False for not clicked, True for clicked
    previous_mouse_state = False
    current_mouse_state = False

    #initializes the mouse button state variables
    mouse_action = IDLE
    
    #initializes widget status
    previous_widget = None
    current_widget = None
    
    #keyboard input
    keyboard_input = ""
    
    def __init__(self):
        pass
        
    def check_boundaries(self, mouse_x, mouse_y):
        
        #updates the previous widget
        self.previous_widget = self.current_widget
        
        for widget in widget_instances:
            #updates the current hovered widget based on the boundaries and wether the widget is hidden
            if widget.x + widget.width > mouse_x and widget.x < mouse_x and widget.y + widget.height > mouse_y and widget.y < mouse_y and not widget.hidden:
                self.current_widget = widget
                break
        #if no widget is found the current widget will be set to none
        else:
            self.current_widget = None
            
  

    def get_events(self):
        self.events = pygame.event.get()

            
    def update_mouse_status(self, mouse_x, mouse_y):
        #loops through events to see if the mouse state changed
        for event in self.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.current_mouse_state = True
                break
            elif event.type == pygame.MOUSEBUTTONUP:
                self.current_mouse_state = False
                break
        else:
            self.current_mouse_state = self.previous_mouse_state
        
        #checks boundaries with widgets for checing mouse actions        
        self.check_boundaries(mouse_x=mouse_x, mouse_y=mouse_y)
        
        #based on the current and previous mouse states, updates the mouse state to IDLE, CLICKED, HELD, or RELEASED
        if(self.current_widget != self.previous_widget):
            self.mouse_action = IDLE
        elif(self.current_mouse_state and self.previous_mouse_state and (self.mouse_action == CLICKED or self.mouse_action == HELD)):
            self.mouse_action = HELD
        elif(self.current_mouse_state and not self.previous_mouse_state):
            self.mouse_action = CLICKED
        elif(not self.current_mouse_state and self.previous_mouse_state) and (self.mouse_action == HELD or self.mouse_action == CLICKED):
            self.mouse_action = RELEASED
        else:
            self.mouse_action = IDLE
        
        print(self.mouse_action)    

        self.previous_mouse_state = self.current_mouse_state
        
    #used for text inputs   
    def update_keyboard_inputs(self):
        
        #resets the keyboard input
        self.keyboard_input = ""
        
        for event in self.events:
            
            if event.type == pygame.KEYDOWN:
                #uses the ` for enter
                if event.key == pygame.K_RETURN:
                    self.keyboard_input += "`"
                #uses the ~ for backspace
                elif event.key == pygame.K_BACKSPACE:
                    self.keyboard_input += "~"
                #otherwise adds the unicode like normal
                else:
                    self.keyboard_input += event.unicode
                    
            
                
                
    def update_widget(self):
        
        #if the widget exsists, then will run through the widget's reactions
        if self.current_widget != None:
            
            self.current_widget.mouse_reaction(self.mouse_action) 
            if self.current_widget.takes_text:
                self.current_widget.text_reaction(self.keyboard_input)
        
        #updates the text input boxes        
        for text_input in text_input_instances:
            if text_input != self.current_widget:
                text_input.active = False
                text_input.cursor.hidden = True
       
  

event_handler = Event_Handler()