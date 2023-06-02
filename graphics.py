import pygame
import math

#display specs
screen = pygame.display.set_mode([1960,1080])
screen_width = 1280
screen_height = 720


#initializes text font
pygame.font.init()
font = pygame.font.SysFont('freesanbold.ttf', 50)



#instances list
instances = []


def render_instances():
    #loops through graphics instances
    for instance in instances:
        if not instance.hidden:
            instance.render()
        else:
            #if an instance has an active atrribute sets it off
            try:
                instance.active = False
            except:
                pass
            

#unit conversions
M_PI = 3.1415926
DEGREES = M_PI/180

#Object to easily display text with changing variable
class DisplayVariable:
    #takes in coordinates, text, variable, and color
    def __init__(self, x_, y_, text_, variable_, color_, hidden_ = True):
        self.x = x_
        self.y = y_
        self.text = text_
        self.variable = variable_
        self.color = color_
        self.hidden = hidden_
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


class Image:
    def __init__(self, x_, y_, image, hidden_ = True):
        self.x = x_
        self.y = y_
        self.image = pygame.image.load(image).convert()
        self.hidden = hidden_
        instances.append(self)
        
    #renders the button to current state
    def render(self):
       if not self.hidden:
            screen.blit(self.image, (self.x, self.y))



        
#Object to easily display vector/line segment to screen
class Vector:
    
    #initializes with starting coordinates, angle, magnitude, and color
    def __init__(self, x_, y_, theta_, magnitude_, color_, thickness_, hidden_ = True):
        self.x = x_
        self.y = y_
        self.theta = theta_
        self.magnitude = magnitude_
        self.color = color_
        self.thickness = thickness_
        self.hidden = hidden_
        instances.append(self)
    
    #renders itself by converting polar coordinates to cartesian coordinates to find the endpoints    
    def render(self):
        pygame.draw.line(screen, self.color, (self.x,self.y), (self.x + self.magnitude * math.cos(self.theta * DEGREES), (self.y + self.magnitude * math.sin(self.theta * DEGREES))), width=self.thickness)
    

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
    
    
