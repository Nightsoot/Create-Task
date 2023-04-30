import pygame
import math
import time

#display specs
screen = 0
screen_width = 1280
screen_height = 720
error_data = []

#creates the window so the window can be referenced but not created on startup
def create_window():
    global screen; screen = pygame.display.set_mode([1280,720])


#Conversion ratio from degrees to radians for ease of calculation
DEGREES = 3.14159/180

instances = []

def sign(a):
    if(a < 0):
        return 0
    else:
        return 1
    

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
        if self.x + self.width > mouse_x and self.x < mouse_x and self.y + self.height > mouse_y and self.y < mouse_y:
            self.pressed = True
            print("pressed")
        else:
            self.pressed = False           
        
    

class Robot:
    
    moving = False
    
    def __init__(self, x_, y_, theta_, PID_type, weight_kg_, max_speed_, track_width_in_, wheel_diameter):
        self.image = pygame.image.load("robot.png").convert()
        self.x = x_ - 36
        self.y = y_  - 53.5
        self.theta = theta_
        self.render()
        self.moving = False
        self.type = PID_type
        self.weight_kg = weight_kg_
        self.max_speed = max_speed_
        self.track_width_m = track_width_in_/39.37
        self.max_accel_linear = 6.3/1
        instances.append(self)
        
    def render(self):
        width, height = self.image.get_size()
        Center_Rotate(screen, self.image, (self.x,self.y), (width/2, height/2), self.theta )


        
    def angular_PID(self, kP, kI, kD, settle_time, min_derv, target, tolerance):
        done = False
        self.moving = True
        integral_power = 0
        settle_count = 0
        prev_error = error = target - self.theta
        same_sign_integral_count = 1
        error_data.clear()
        initial_time = time.process_time()
        while not done:
            self.theta %= 360
            error = target - self.theta
            error_data.append(error)
            
            if(error > 180):
                error -= 360
            elif(error < -180):
                error += 360
                
            prop_power = kP * error
            integral_power = kI * sum(error_data[len(error_data) -10 : len(error_data) -1 ])
            derv_power = kD * (error - prev_error)
            
        
            
            if(sign(prev_error) != sign(error)):
                integral_power = 0
                same_sign_integral_count = 1
            else:
                integral_power = kI * sum(error_data[len(error_data) - same_sign_integral_count - 1 : len(error_data) -1 ])
                if not same_sign_integral_count > 10:
                    same_sign_integral_count += 1
            
            output_velocity = prop_power + integral_power + derv_power
            self.theta += output_velocity * .025
            
            if abs(error) < tolerance and derv_power < min_derv:
                settle_count += 1
            
            if settle_count == int(settle_time/25) or time.process_time() - initial_time > 10:
                done = True
                
            self.render()
            pygame.display.flip()
            
            prev_error = error
            
            print("integral power = " + str(integral_power))
            print("count = " + str(same_sign_integral_count))

            
            time.sleep(.025)
        
        self.moving = False
            

       
    def linear_PID(self, kP, kI, kD, settle_time, min_derv, target, tolerance):
        done = False
        self.moving = True
        integral_power = 0
        settle_count = 0
        prev_error = error = target - self.x
        while not done:
            error = target - self.x
                
            prop_power = kP * error
            integral_power += kI * error
            derv_power = kD * (error - prev_error)
            
            if(sign(prev_error) != sign(error)):
                integral_power = 0
            
            output_velocity = prop_power + integral_power + derv_power
            self.x += output_velocity * .025
            
            if abs(error) < tolerance and derv_power < min_derv:
                settle_count += 1
            
            if settle_count == int(settle_time/25):
                done = True
                
            self.render()
            
            time.sleep(.025)
        
        self.moving = False
    
    def PID(self, kP, kI, kD, settle_time, min_derv, target, tolerance):
        if self.type:
            self.angular_PID(kP, kI, kD, settle_time, min_derv, target, tolerance)
        else:
            self.linear_PID(kP, kI, kD, settle_time, min_derv, target, tolerance)
            
    def reset(self, x_, y_, theta_):
        self.x  = x_
        self.y = y_
        self.theta = theta_
            
        
        
class Vector:
    
    def __init__(self, x_, y_, theta_, magnitude_, color_):
        self.x = x_
        self.y = y_
        self.theta = theta_
        self.magnitude = magnitude_
        self.color = color_
        instances.append(self)
        
    def render(self):
        pygame.draw.line(screen, self.color, (self.x,self.y), (self.x + self.magnitude * math.cos(self.theta * DEGREES), (self.y + self.magnitude * math.sin(self.theta * DEGREES))))
    

    
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
  
    # draw rectangle around the image
    #pygame.draw.rect(surf, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()),2)