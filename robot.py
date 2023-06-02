import graphics
import pygame
import time
from input_data import data_dictionary



#Unit Conversions
M_PI = 3.1415926
DEGREES = M_PI/180
RADIANS = 180/M_PI
IN_TO_M = .0254
PIXELS_TO_IN = 1/5.944

#error list
error_data = []

#variable displays
settle_status = graphics.DisplayVariable(200,100,"Settled: ", True, (255,255,0))
error_status = graphics.DisplayVariable(600,100, "Error = ", "Hit play to start error", (255,0,255))
time_status = graphics.DisplayVariable(1000, 100, "Time (s)= ", 0, (255,255,255))

#returns the sign for numbers
# -1 = -, 1 = + (0 is considered positive)
def sign(number):
    if(number < 0):
        return -1
    else:
        return 1

#truncates a float for easier printing    
def truncate_to_hundreth(number):
    number = str(number)
    output_number = ""
    #loops through characters in the input number
    for character in range(len(number)):
        #detects if the decimal point has been found
        if number[character] == ".":
            #tries to append the decimal and next 2 digits 
            try:
                output_number += number[character] + number[character + 1] + number[character + 2]
            #if the number has less than 2 decimal digits returns the number as normal
            except:
                output_number = number
            #stops looping through number
            break
        #adds character to output number otherwise
        else:
            output_number += number[character]
    
    #returns the new number
    return output_number
            
        

#if the velocity difference is greater than possible than it will change velocity by maximum amount
#finally it will check that the new velocity doesn't exceed the max
def limit_velocity(prev_velocity, current_velocity,max_velocity, max_accel):
    #checks that prev_velocity is not equal to 0 so that errors aren't made at the start of movements
    if abs((prev_velocity - current_velocity)) > max_accel and prev_velocity != 0:
        #case that velocity changes signs
        if(sign(current_velocity) != sign(prev_velocity)):
            current_velocity = prev_velocity + sign(current_velocity) * max_accel
        #case that robot is accelerating
        elif (abs(current_velocity) > abs(prev_velocity)):
            current_velocity = prev_velocity + sign(current_velocity) * max_accel
        #case that the robot is deaccelerating
        elif (abs(current_velocity) < abs(prev_velocity)):
            current_velocity = prev_velocity - sign(current_velocity) * max_accel
        
    #limits velocity to max
    if abs(current_velocity) > max_velocity:
        current_velocity = sign(current_velocity) * max_velocity
     
    #returns new velocity
    return current_velocity

class Robot:
    
    
    moving = False
    
    #intializes the robot with given parameters
    def __init__(self, x_, y_, theta_, hidden_ = False):
        self.image = pygame.image.load("images/robot.png").convert()
        self.x = x_ - 36
        self.y = y_  - 53.5
        self.theta = theta_
        self.hidden = hidden_
        self.render()
        self.moving = False
        self.sync_constants()
        

        graphics.instances.append(self)
    
    #renders itself on screen
    def render(self):
        width, height = self.image.get_size()
        graphics.Center_Rotate(graphics.screen, self.image, (self.x,self.y), (width/2, height/2), self.theta )
        
    def sync_constants(self):
        #syncs the constants given by the widgets to the robot
        self.kP = data_dictionary["kP"]
        self.kI = data_dictionary["kI"]
        self.kD = data_dictionary["kD"]
        self.settle_time = data_dictionary["settle time"]
        self.min_derv = data_dictionary["min derv"]
        self.tolerance = data_dictionary["tolerance"]
        self.calculate_kinematics = data_dictionary["kinematics calculation"]
        
        
        #if using the calculate kinematics constraints
        #the function will sync the required constants and calculate the constraints
        if(self.calculate_kinematics):
            self.rpm = data_dictionary["rpm"]
            self.mass_kg = data_dictionary["mass_kg"]
            self.wheel_diameter = data_dictionary["wheel diameter"]
            self.track_width_m = data_dictionary["track width"] * IN_TO_M
            self.num_motors = data_dictionary["number of motors"]
            self.calculate_constraints()
        #otherwise, it'll use the input constraints
        else:
            self.max_speed_linear = data_dictionary["input max linear speed"]
            self.max_speed_angular = data_dictionary["input max angular speed"]
            self.max_acceleration_linear = data_dictionary["input max linear acceleration"]
            self.max_acceleration_angular = data_dictionary["input max angular acceleration"]
        

    def calculate_constraints(self):
        #calculates max_speed from rpm and wheel diamter in m/s
        self.max_speed_linear = ((self.rpm/60) * M_PI * self.wheel_diameter)/39.37
        #Sovles for force based on torque and wheel radius
        #Uses the force and mass of robot to solve for acceleration
        self.max_acceleration_linear = ((2.1 * self.num_motors) / (self.wheel_diameter * IN_TO_M * .5))/self.mass_kg
        #solves for angular speed by calculating the distance of a full rotation
        #the robot can travel in one second and multpilies that fraction by 360
        #so angular speed is in degrees/second
        self.max_speed_angular = self.max_speed_linear/(self.track_width_m * M_PI) * 360  
        #uses the tangential speed and curvature equation to solve for angular acceleration converted to degrees/second^2
        self.max_acceleration_angular = self.max_speed_linear/(self.track_width_m / 2) * RADIANS
        
    def angular_PID(self, kP, kI, kD, settle_time, min_derv, target, tolerance):
        #initalizes variables
        done = False
        self.moving = True
        integral_power = 0
        settle_count = 0
        prev_error = error = target - self.theta
        same_sign_integral_count = 1
        error_data.clear()
        prev_velocity = 0
        tick = 0
        #main loop
        while not done:
            #finds error and appends it to the error list
            self.theta %= 360
            error = target - self.theta
            error_data.append(error)
            #prevents error list from taking up too much memory
            if(len(error_data) > 10):
                error_data.pop(0)
            

            #finds the smallest error
            if(error > 180):
                error -= 360
            elif(error < -180):
                error += 360
            
            #calculates proportional and derivative powers    
            prop_power = kP * error
            derv_power = kD * (error - prev_error)
            
        
            
            #zeros out integral power if robot passes target
            if(sign(prev_error) != sign(error)):
                integral_power = 0
                same_sign_integral_count = 1
            #calculates the integral power since last error sign change, up to 250 ms
            else:
                integral_power = -kI * sum(error_data[len(error_data) - same_sign_integral_count - 1 : len(error_data) -1 ])
                if not same_sign_integral_count > 10:
                    same_sign_integral_count += 1
            
            #sums up powers to get the output velocity
            output_velocity = (prop_power + integral_power + derv_power) 
            #limits output_velocity based on the kinematic constraints of the robot (acceleration multiplied by time step)
            output_velocity = limit_velocity(prev_velocity, output_velocity, self.max_speed_angular, self.max_acceleration_angular * .025)
            #updates previous velocity
            prev_velocity  = output_velocity
            
            #translates velocity to angle change
            self.theta += output_velocity * .025
            
            
            #checks for settling
            if abs(error) < tolerance and derv_power < min_derv:
                settle_count += 1
            
            #checks if settled long enough
            if settle_count >= int(settle_time/25):
                done = True
            
            #stops movement if screen is clicked
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    done = True    
            
            #updates display variables
            time_status.variable = truncate_to_hundreth(.025 * tick)
            settle_status.variable = False
            error_status.variable = truncate_to_hundreth(error)
            
            #renders instances to screen
            graphics.screen.fill((0, 0, 0))
            for instance in graphics.instances:
                instance.render()
            pygame.display.flip()
            
            #updates previous error
            prev_error = error

            #time step
            time.sleep(.025)
            tick += 1
        
        #sets robot to not moving
        self.moving = False
            

       
    def linear_PID(self, kP, kI, kD, settle_time, min_derv, target, tolerance):
        #initializing variables
        done = False
        self.moving = True
        integral_power = 0
        settle_count = 0
        prev_error = error = (target - self.x) * PIXELS_TO_IN * IN_TO_M 
        same_sign_integral_count = 1
        error_data.clear()
        prev_velocity = 0
        tick = 0
        while not done:
            #finds error and appends it to the error list (converts from pixels to meters)
            error = (target - self.x) * PIXELS_TO_IN * IN_TO_M 
            error_data.append(error)
            #prevents error list from taking up too much memory
            if(len(error_data) > 10):
                error_data.pop(0)
            
            #calculates proportional and derivative powers  
            prop_power = kP * error
            derv_power = kD * (error - prev_error)
            
            #zeros out integral power if robot passes target
            if(sign(prev_error) != sign(error)):
                integral_power = 0
                same_sign_integral_count = 1
            #calculates the integral power since last error sign change, up to 250 ms
            else:
                integral_power = -kI * sum(error_data[len(error_data) - same_sign_integral_count - 1 : len(error_data) -1 ])
                if not same_sign_integral_count > 10:
                    same_sign_integral_count += 1
            
            #sums up powers to get the output velocity
            output_velocity = (prop_power + integral_power + derv_power) 
            #limits output_velocity based on the kinematic constraints of the robot (acceleration multiplied by time step)
            output_velocity = limit_velocity(prev_velocity, output_velocity, self.max_speed_linear, self.max_acceleration_linear * .025)
            #updates previous velocity
            prev_velocity  = output_velocity
            
            #updates x position of robot (converts meters to pixels)
            self.x += (output_velocity * .025)/IN_TO_M/PIXELS_TO_IN
            
            #checks for settling
            if abs(error) < tolerance and derv_power < min_derv:
                settle_count += 1
            
            #checks if settled long enough
            if settle_count >= int(settle_time/25):
                done = True
            
            #stops movement if screen is clicked
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    done = True    
            
            #updates display variables
            time_status.variable = truncate_to_hundreth(.025 * tick)
            settle_status.variable = False
            error_status.variable = truncate_to_hundreth(error)
            
            #renders instances to screen
            graphics.screen.fill((0, 0, 0))
            for instance in graphics.instances:
                instance.render()
            pygame.display.flip()
            
            #updates previous error
            prev_error = error
        
            #time step
            time.sleep(.025)
            tick += 1
        
        #sets robot to not moving
        self.moving = False
    
    #Selects PID type based on internal attribute (True = Angular)
    def PID(self, kP, kI, kD, settle_time, min_derv, target, tolerance):
        if self.type:
            self.angular_PID(kP, kI, kD, settle_time, min_derv, target, tolerance)
        else:
            self.linear_PID(kP, kI, kD, settle_time, min_derv, target, tolerance)
    
    #resets robot position
    def reset(self, x_, y_, theta_):
        self.x  = x_ - 36
        self.y = y_ - 53.5
        self.theta = theta_
