kP_input = 0
kI_input = 0
kD_input = 0
settle_time = 250
min_derv = 10000
tolerance = 1
angular = False
advanced_setup = False
start_error = 0
mass_kg = 0
rpm = 0
wheel_diameter = 0
track_width = 0
num_motors = 0
start_pose = [640,360,0]
target = 0

def select_robot_specs():
    selected = False
    while not selected:
        try:
            print("Input Robot Specifications for a differential drive (Must be positive, negative values will be turned positive)")
            print("Extreme Values may cause performance issues")
            
            global num_motors; num_motors = abs(int(input("Number of 11W V5 motors (Must be multiple of 2) = ")))
            if(num_motors % 2 != 0):
                raise Exception
            
            global mass_kg; mass_kg = abs(float(input("Mass of the robot (kg) = ")))
            global rpm; rpm = abs(float(input("Rpm of drivetrain = ")))
            global wheel_diameter; wheel_diameter = abs(float(input("Diameter of driving wheels (in) = ")))
            global track_width; track_width = abs(float(input("Track width (in) = ")))
            
            selected = True
            
        except:
            print("Invalid Inputs, Try Again")
            

def select_PID_constants():
    selected = False
    while not selected:
        try:
            print("Select the PID constants (Must be positive numbers, negative values will be turned positive)")
            print("Extreme Values may cause performance issues")
            print("Ex: kP = 3.1, kI = .41, kD = .59")
            global kP_input ; kP_input = abs(float(input("kP = ")))
            global kI_input ; kI_input = abs(float(input("kI = ")))
            global kD_input ; kD_input = abs(float(input("kD = ")))
            selected = True
        except:
            print("Invalid Inputs, all inputs must be positive numbers")

def type_select():
    selected = False
    while not selected:
        try:
            print("Answer with one of the letters in the square brackets")
            
            type_PID = input("Angular or Linear? [A/L]: ")
            
            if(type_PID.lower() == "a"):
                global angular; angular = True
            elif(type_PID.lower() == "l"):
                pass
            else:
                raise Exception
    
            advanced = input("Would you like to go through advanced setup [Y/N]: ")
    
            if(advanced.lower() == "y"):
                global advanced_setup; advanced_setup = True
            elif(advanced.lower() == "n"):
                pass
            else:
                raise Exception
            
            selected = True
        except:
            print("Invalid Inputs, answer with one of the letters in the brackets")
    
    selected = False
    while not selected:
        try:
            out_string = ""
            if(angular):
                out_string += "Enter the degrees the robot has to turn (0 <-> 180): "
            else:
                out_string += "Enter the inches the robot has to move (max 150 in): "
            
            
            global start_error; start_error = abs(float(input(out_string)))
            if start_error > 150 and (not angular):
                start_error = 150
           
                
            selected = True
        except:
            print("Invalid Inputs, must be numbers")


            
    

def advanced_select():
    selected = False
    while not selected:
        try:
            print("Advanced constants selection (Must be positive numbers, negative values will be turned positive): ")
            global settle_time; settle_time = abs(float(input("Settle time (ms) = ")))
            global min_derv; min_derv = abs(float(input("Min Derivative term = ")))
            out_string = ""
            if(angular):
                out_string += "Degrees Tolerance: "
            else:
                out_string += "Inches Tolerance"
            global tolerance; tolerance = abs(float(input(out_string)))
            selected = True
        except:
            print("Invalid Inputs, all inputs must be positive numbers")
    

def selection():
    global target
    select_robot_specs()
    select_PID_constants()
    type_select()
    if(advanced_setup):
        advanced_select()
    if(angular):
        target = 0
    else:
        target = 1100
    print("Simulation can be stopped anytime by clicking anywhere on screen")
