from graphics import instances, screen, Vector
from input_data import data_dictionary
import pygame

#mouse actions
IDLE = 0
CLICKED = 1
HELD = 2
RELEASED = 3

#widgets list
widget_instances = []
text_input_instances = []



def test(mouse_state):
    if mouse_state == CLICKED:
        #print("HELLO")
        pass


#Object to easily add buttons to screen
class Button:
    
    takes_text = False
    pressed = False
    
    #initializes a button with a on/off image and coordinates
    def __init__(self, image_, x_, y_, function_reaction_, pressed_image_ = None, hidden_ = True ):
        self.x = x_
        self.y = y_
        self.image = pygame.image.load(image_).convert()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hidden = hidden_
        self.function_reaction = function_reaction_
        instances.append(self)
        widget_instances.append(self)
        
        if(pressed_image_ != None):
            self.pressed_image = pygame.image.load(pressed_image_).convert()
        else:
            self.pressed_image = None
    
    #renders the button to current state
    def render(self):
       if not self.hidden:
        if self.pressed and self.pressed_image != None:
            screen.blit(self.pressed_image, (self.x, self.y))
        else:
            screen.blit(self.image, (self.x, self.y))
    
    def mouse_reaction(self, mouse_state):
        if mouse_state == CLICKED:
            self.pressed = True
        else:
            self.pressed = False
        
        self.function_reaction(mouse_state)
        
        
class TextInput:
    
    active = False
    takes_text = True
    
    
    def __init__(self, x_, y_, width_, height_, font_size_, color_, function_reaction_, max_characters_, variable_id_, numerical_ = True, hidden_ = True ):
        
        self.x = x_
        self.y = y_
        self.width = width_
        self.height = height_
        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))
        self.hidden = hidden_
        self.numerical = numerical_
        self.function_reaction = function_reaction_
        self.font_size = font_size_
        self.font = pygame.font.SysFont("RobotoMono-Regular.ttf", font_size_)
        self.color = color_
        self.max_characters = max_characters_
        self.variable_id = variable_id_
        self.text = str(data_dictionary[variable_id_])
        instances.append(self)
        widget_instances.append(self)
        text_input_instances.append(self)
        self.cursor = Vector(self.x + self.width/2, self.y + self.height/2 - font_size_* .25, 90, font_size_ *.5, self.color, 2)
        
    def render(self):
        if(not self.active):
            self.cursor.hidden = True
        else:
            self.cursor.hidden = False
            
        output_text = self.font.render(self.text, True, self.color )
        output_text_rect = output_text.get_rect()
        output_text_rect.center = (self.x + self.width/2, self.y + self.height/2)
        pygame.draw.rect(screen, self.color, self.rect, 1)
        screen.blit(output_text, output_text_rect)
        
        
    def mouse_reaction(self, mouse_action):
        
        active_text_input = None
        
        #finds any active text box
        for text_input in text_input_instances:
            if text_input.active and text_input != self:
                active_text_input = text_input
        
        #if clicked the text box will be set active and the previous one will be turned off
        if(mouse_action == CLICKED):
            self.active = True
            
            if active_text_input != None:
                active_text_input.active = False
                active_text_input.cursor.hidden = True
    
    
    #limits text to a predeterimed amount of characters
    def limit_text(self):
        while len(self.text) > self.max_characters:
            self.text = self.text[:-1]
    
    
    def text_reaction(self, in_text):
        
        #cuts the reaction short if the text box isn't active
        if not self.active:
            return 1
        
        for character in in_text:
            #if entered the text box will be set to inactive
            if character == "`":
                self.active = False
                break
            #removes a character if the backspace is pressed
            if character == "~" and len(self.text):
                self.text = self.text[:-1]
                break
            
            #if the text box is numerical, a number will be accepted
            #or if a decimal point is inputed and there isn't already another one
            #or if a negative sign is inputed
            if self.numerical and (character.isnumeric()
                                   or (character == "." and "." not in self.text)
                                   or (character == "-" and "-" not in self.text and len(self.text) == 0)):
                self.text += character
            elif self.numerical:
                pass
            #if not numerical just adds the character on
            else:
                self.text += character
                
            self.limit_text()
        
        #moves the cursor relative to the font size and text length
        self.cursor.x = self.x + self.width/2 + len(self.text) * self.font_size * 3/14
        
        #changes the variable in the dictionary to be equal to the text
        if self.numerical:
            try:
                data_dictionary[self.variable_id] = float(self.text)
            except:
                data_dictionary[self.variable_id] = 0
        else:
            data_dictionary[self.variable_id] = self.text
        
        