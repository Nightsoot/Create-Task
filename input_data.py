
#initializing the data dictionary
data_dictionary = {
"kP" : 1,
"kI" : 1,
"kD" : 1,
"settle time" : 250,
"kinematics calculation" : True,
"min derv" : 10000,
"tolerance" : 1,
"mass_kg" : 8,
"rpm" : 360,
"wheel diameter" : 3.25,
"track width" : 14,
"number of motors" : 6,
"start_pose" : [640,360,0],
"target" : 0,
"input max linear speed" : 100,
"input max linear acceleration" : 50,
"input max angular speed" : 100,
"input max angular acceleration" : 50
}



'''
#allows user to select specifications of robot's drivetrain and mass
def select_robot_specs():
    selected = False
    #validates that the data can be used
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
        #error message
        except:
            print("Invalid Inputs, Try Again")
            
#allows user to select PID constants
def select_PID_constants():
    selected = False
    #validates that the data can be used
    while not selected:
        try:
            print("Select the PID constants (Must be positive numbers, negative values will be turned positive)")
            print("Extreme Values may cause performance issues")
            print("Ex: kP = 3.1, kI = .41, kD = .59")
            global kP_input ; kP_input = abs(float(input("kP = ")))
            global kI_input ; kI_input = abs(float(input("kI = ")))
            global kD_input ; kD_input = abs(float(input("kD = ")))
            selected = True
        #error message
        except:
            print("Invalid Inputs, all inputs must be positive numbers")


#allows user to select PID type, setup type, and target
def type_select():
    selected = False
    #validates that the data can be used
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
    #validates that the data can be used
    while not selected:
        try:
            out_string = ""
            if(angular):
                out_string += "Enter the degrees the robot has to turn (0 <-> 180): "
            else:
                out_string += "Enter the inches the robot has to move (max 150 in): "
            
            #limits the starting error if above max
            global start_error; start_error = abs(float(input(out_string)))
            #linear case
            if start_error > 150 and (not angular):
                start_error = 150
            #angular case
            elif start_error > 180:
                start_error = 180
           
                
            selected = True
        #error_message
        except:
            print("Invalid Inputs, must be numbers")


            
    
#allows user to specify more specific parameters to the PID loops
def advanced_select():
    selected = False
    #validates that the data can be used
    while not selected:
        try:
            print("Advanced constants selection (Must be positive numbers, negative values will be turned positive): ")
            global settle_time; settle_time = abs(float(input("Settle time (ms) = ")))
            global min_derv; min_derv = abs(float(input("Min Derivative term = ")))
            out_string = ""
            if(angular):
                out_string += "Degrees Tolerance: "
            else:
                out_string += "Inches Tolerance: "
            global tolerance; tolerance = abs(float(input(out_string)))
            selected = True
        #error message
        except:
            print("Invalid Inputs, all inputs must be positive numbers")
    

def selection():
    #setsup terminal selection and target
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
'''