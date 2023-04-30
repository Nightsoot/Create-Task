import pygame
import graphics
import time
pygame.init()

for i in range(10):
    print("\n")

kP_input = 0
kI_input = 0
kD_input = 0
settle_time = 250
min_derv = 10000
tolerance = 1
angular = False
advanced_setup = False
error_graph = False
start_error = 0


def select_PID_constants():
    selected = False
    while not selected:
        try:
            print("Select the PID constants (Must be positive numbers, negative values will be turned positive)")
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
            
            graph_option = input("Would you like a graph of the error at the end [Y/N]: ")
            
            if(graph_option.lower() == "y"):
                global error_graph; error_graph = True
            elif(graph_option.lower() == "n"):
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
                out_string += "Enter the inches the robot has to move"
            
            
            global start_error; start_error = abs(float(input(out_string)))
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
    




select_PID_constants()
type_select()
if(advanced_setup):
    advanced_select()

graphics.create_window()
play = graphics.Button("start_button.png",0,0, "start_button_pressed.png")
redo = graphics.Button("redo button.png", 53, 0, "Redo button pressed.png")

start_pose = [640,360,0]
target = 0

if angular:
    start_pose = [640,360, start_error]
else:
    start_pose = [1100 - start_error, 360, 90]
    target = 1100

robot = graphics.Robot(*start_pose, angular)
robot.render()




running = True
mouse_position = 0



while running:


    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if(event.type == pygame.MOUSEBUTTONDOWN):
            mouse_position = pygame.mouse.get_pos()
            if not robot.moving:
                play.check_press(*mouse_position)
                redo.check_press(*mouse_position)
            if(play.pressed):
                print("PID started")
                robot.PID(kP_input, kI_input, kD_input, settle_time, min_derv, target, tolerance)
            elif(redo.pressed):
                robot.reset(*start_pose)
    
        else:
            play.pressed = False
            redo.pressed = False


    # Fill the background with black
    graphics.screen.fill((0, 0, 0))

    # Draw a solid blue circle in the center
    
    for instance in graphics.instances:
        instance.render()
    # Flip the display
    pygame.display.flip()
    
 
    
    time.sleep(.025);

# Done! Time to quit.
pygame.quit()