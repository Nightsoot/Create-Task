import pygame
import math

#display specs
screen = 0
screen_width = 1280
screen_height = 720


#initializes text font
pygame.font.init()
font = pygame.font.SysFont('freesanbold.ttf', 50)

#creates the window so the window can be referenced but not created on startup
def create_window():
    global screen; screen = pygame.display.set_mode([1280,720])

#instances list
instances = []

#unit conversions
M_PI = 3.1415926
DEGREES = M_PI/180

#Object to easily display text with changing variable
class DisplayVariable:
    #takes in coordinates, text, variable, and color
    def __init__(self, x_, y_, text_, variable_, color_):
        self.x = x_
        self.y = y_
        self.text = text_
        self.variable = variable_
        self.color = color_
        instances.append(self)
    
    #renders itself
    def render(self):
        output_text = font.render(self.text + str(self.variable), True, self.color )
        output_text_rect = output_text.get_rect()
        output_text_rect.center = (self.x, self.y)
        screen.blit(output_text, output_text_rect)

#Object to easily display text. Inherits from DisplayVariable but has no variable part
class DisplayText(DisplayVariable):
    def render(self):
        output_text = font.render(self.text, True, self.color )
        output_text_rect = output_text.get_rect()
        output_text_rect.center = (self.x, self.y)
        screen.blit(output_text, output_text_rect)


#Object to easily add buttons to screen
class Button:
    
    pressed = False
    
    #initializes a button with a on/off image and coordinates
    def __init__(self, image_, x_, y_, pressed_image_ = None):
        self.x = x_
        self.y = y_
        self.image = pygame.image.load(image_).convert()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        instances.append(self)
        
        if(pressed_image_ != None):
            self.pressed_image = pygame.image.load(pressed_image_).convert()
        else:
            self.pressed_image = None
    
    #renders the button to current state
    def render(self):
       if self.pressed and self.pressed_image != None:
           screen.blit(self.pressed_image, (self.x, self.y))
       else:
           screen.blit(self.image, (self.x, self.y))
    
    #checks to see if the mouse coordinates are over the button
    def check_press(self, mouse_x, mouse_y):
        #updates pressed status accordingly
        if self.x + self.width > mouse_x and self.x < mouse_x and self.y + self.height > mouse_y and self.y < mouse_y:
            self.pressed = True
        else:
            self.pressed = False           
        
#Object to easily display vector/line segment to screen
class Vector:
    
    #initializes with starting coordinates, angle, magnitude, and color
    def __init__(self, x_, y_, theta_, magnitude_, color_):
        self.x = x_
        self.y = y_
        self.theta = theta_
        self.magnitude = magnitude_
        self.color = color_
        instances.append(self)
    
    #renders itself by converting polar coordinates to cartesian coordinates to find the endpoints    
    def render(self):
        pygame.draw.line(screen, self.color, (self.x,self.y), (self.x + self.magnitude * math.cos(self.theta * DEGREES), (self.y + self.magnitude * math.sin(self.theta * DEGREES))))
    

#allows images to be rotated around center  
def Center_Rotate(surf, image, pos, originPos, angle):
    
    # offset from pivot to center
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    
    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

    # rotate and blit the image
    surf.blit(rotated_image, rotated_image_rect)