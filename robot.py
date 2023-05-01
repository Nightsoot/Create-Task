import graphics
import pygame
import time
#Degrees to Radians conversion snd vice versa and aprox. for Pi
M_PI = 3.1415926
DEGREES = M_PI/180
RADIANS = 180/M_PI
IN_TO_M = .0254
PIXELS_TO_IN = 1/5.944

settle_status = graphics.DisplayVariable(200,100,"Settled: ", True, (255,255,0))
error_status = graphics.DisplayVariable(600,100, "Error = ", "Hit play to start error", (255,0,255))
time_status = graphics.DisplayVariable(1000, 100, "Time (s)= ", 0, (255,255,255))

#returns the sign for numbers
# -1 = -, 1 = + (0 is considered positive)
def sign(a):
    if(a < 0):
        return -1
    else:
        return 1
    
def truncate_to_hundreth(number):
    number = str(number)
    output_number = ""
    for character in range(len(number)):
        if number[character] == ".":
            try:
                output_number += number[character] + number[character + 1] + number[character + 2]
            except:
                output_number = number
            break
        else:
            output_number += number[character]
    
    return output_number
            
        

#if the velocity difference is greater than possible than it will change velocity by maximum amount
#finally it will check that the new velocity doesn't exceed the max
def limit_velocity(prev_velocity, current_velocity,max_velocity, max_accel):
    #checks that prev_velocity is not equal to 0 so that errors aren't made at the start of movements
    if abs((prev_velocity - current_velocity)) > max_accel and prev_velocity != 0:
        if(sign(current_velocity) != sign(prev_velocity)):
            current_velocity = prev_velocity + sign(current_velocity) * max_accel
        elif (abs(current_velocity) > abs(prev_velocity)):
            current_velocity = prev_velocity + sign(current_velocity) * max_accel
        elif (abs(current_velocity) < abs(prev_velocity)):
            current_velocity = prev_velocity - sign(current_velocity) * max_accel
        
        
    if abs(current_velocity) > max_velocity:
        current_velocity = sign(current_velocity) * max_velocity
     

    return current_velocity

class Robot:
    
    
    moving = False
    
    #intializes the robot with given parameters
    def __init__(self, x_, y_, theta_, PID_type, mass_kg, rpm, track_width_in_, wheel_diameter, num_motors):
        self.image = pygame.image.load("images/robot.png").convert()
        self.x = x_ - 36
        self.y = y_  - 53.5
        self.theta = theta_
        self.render()
        self.moving = False
        self.type = PID_type
        #calculates max_speed from rpm and wheel diamter in m/s

        self.max_speed_linear = ((rpm/60) * M_PI * wheel_diameter)/39.37
        #in meters 
        self.track_width_m = track_width_in_ * IN_TO_M
        #Sovles for force based on torque and wheel radius
        #Uses the force and mass of robot to solve for acceleration
        #limits max theoretical acceleration to 50% to avoid overheating
        self.max_acceleration_linear = .5 * ((2.1 * num_motors) / (wheel_diameter * IN_TO_M * .5))/mass_kg
        #solves for angular speed by calculating the distance of a full rotation
        #the robot can travel in one second and multpilies that fraction by 360
        #so angular speed is in degrees/second
        self.max_speed_angular = self.max_speed_linear/(self.track_width_m * M_PI) * 360  
        #uses the tangential speed and curvature equation to solve for angular acceleration converted to degrees/second^2
        self.max_acceleration_angular = self.max_speed_linear/(self.track_width_m / 2) * RADIANS

        graphics.instances.append(self)
    
    #renders itself on screen
    def render(self):
        width, height = self.image.get_size()
        graphics.Center_Rotate(graphics.screen, self.image, (self.x,self.y), (width/2, height/2), self.theta )


        
    def angular_PID(self, kP, kI, kD, settle_time, min_derv, target, tolerance):
        done = False
        self.moving = True
        integral_power = 0
        settle_count = 0
        prev_error = error = target - self.theta
        same_sign_integral_count = 1
        graphics.error_data.clear()
        prev_velocity = 0
        tick = 0
        while not done:
            self.theta %= 360
            error = target - self.theta
            graphics.error_data.append(error)
            if(len(graphics.error_data) > 10):
                graphics.error_data.pop(0)
            

            
            if(error > 180):
                error -= 360
            elif(error < -180):
                error += 360
                
            prop_power = kP * error
            derv_power = kD * (error - prev_error)
            
        
            
            if(sign(prev_error) != sign(error)):
                integral_power = 0
                same_sign_integral_count = 1
            else:
                integral_power = -kI * sum(graphics.error_data[len(graphics.error_data) - same_sign_integral_count - 1 : len(graphics.error_data) -1 ])
                if not same_sign_integral_count > 10:
                    same_sign_integral_count += 1
            
            output_velocity = (prop_power + integral_power + derv_power) 
            #print("Unlimited: " + str(output_velocity))
            output_velocity = limit_velocity(prev_velocity, output_velocity, self.max_speed_angular, self.max_acceleration_angular * .025)
            #print("Limited: " + str(output_velocity))
            prev_velocity  = output_velocity
            
            self.theta += output_velocity * .025
            
            
            if abs(error) < tolerance and derv_power < min_derv:
                settle_count += 1
            
            if settle_count == int(settle_time/25):
                done = True
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    done = True    
            
            time_status.variable = truncate_to_hundreth(.025 * tick)
            settle_status.variable = False
            error_status.variable = truncate_to_hundreth(error)
            graphics.screen.fill((0, 0, 0))
            for instance in graphics.instances:
                instance.render()
            pygame.display.flip()
            
            prev_error = error
        
            time.sleep(.025)
            
            tick += 1
        
        self.moving = False
            

       
    def linear_PID(self, kP, kI, kD, settle_time, min_derv, target, tolerance):
        done = False
        self.moving = True
        integral_power = 0
        settle_count = 0
        prev_error = error = (target - self.x) * PIXELS_TO_IN * IN_TO_M 
        same_sign_integral_count = 1
        graphics.error_data.clear()
        prev_velocity = 0
        tick = 0
        while not done:
            error = (target - self.x) * PIXELS_TO_IN * IN_TO_M 
            graphics.error_data.append(error)
            if(len(graphics.error_data) > 10):
                graphics.error_data.pop(0)
                
            prop_power = kP * error
            derv_power = kD * (error - prev_error)
            
            if(sign(prev_error) != sign(error)):
                integral_power = 0
                same_sign_integral_count = 1
            else:
                integral_power = -kI * sum(graphics.error_data[len(graphics.error_data) - same_sign_integral_count - 1 : len(graphics.error_data) -1 ])
                if not same_sign_integral_count > 10:
                    same_sign_integral_count += 1
            
            output_velocity = (prop_power + integral_power + derv_power) 
            #print("Unlimited: " + str(output_velocity))
            output_velocity = limit_velocity(prev_velocity, output_velocity, self.max_speed_linear, self.max_acceleration_linear * .025)
            #print("Limited: " + str(output_velocity))
            prev_velocity  = output_velocity
            
            self.x += (output_velocity * .025)/IN_TO_M/PIXELS_TO_IN
            
            if abs(error/IN_TO_M) < tolerance and derv_power < min_derv:
                settle_count += 1
            
            if settle_count == int(settle_time/25):
                done = True
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    done = True    
            
            time_status.variable = truncate_to_hundreth(.025 * tick)
            settle_status.variable = False
            error_status.variable = truncate_to_hundreth(error / IN_TO_M)
            graphics.screen.fill((0, 0, 0))
            for instance in graphics.instances:
                instance.render()
            pygame.display.flip()
            
            prev_error = error
    
            time.sleep(.025)
            
            tick += 1
        
        self.moving = False
    
    def PID(self, kP, kI, kD, settle_time, min_derv, target, tolerance):
        if self.type:
            self.angular_PID(kP, kI, kD, settle_time, min_derv, target, tolerance)
        else:
            self.linear_PID(kP, kI, kD, settle_time, min_derv, target, tolerance)
            
    def reset(self, x_, y_, theta_):
        self.x  = x_ - 36
        self.y = y_ - 53.5
        self.theta = theta_
