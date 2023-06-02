import pygame
import graphics
import time
from input_data import data_dictionary
from robot import Robot
from robot import settle_status
from event_handler import event_handler
from widgets import Button
from widgets import TextInput
from widgets import test

pygame.init()

#initializing variables
running = True

#initalizes window and buttons
field = graphics.Image(100,100 ,"images/Over Under Field.jpg", hidden_= False)

play = Button("images/start_button.png",0,0,test, pressed_image_= "images/start_button_pressed.png", hidden_= False)
test = TextInput( 1450,400,150,40,20,(0,0,0), test, 8, "rpm",numerical_= True, hidden_= False)




#test2 = TextInput( 450,400,100,20,36,(0,0,0), test, 6, numerical_= True, hidden_= False)
#redo = Button("images/redo button.png", 53, 0, "images/Redo button pressed.png", hidden_= False)



#creates and renders the robot
robot = Robot(*data_dictionary["start_pose"])
#robot.render()



while running:

    #goes through event handler methods
    event_handler.get_events()
    event_handler.update_mouse_status(*pygame.mouse.get_pos())
    event_handler.update_keyboard_inputs()
    event_handler.update_widget()
    
    # Fill the background with white
    graphics.screen.fill((255, 255, 255))

    #renders graphics
    graphics.render_instances()
    # Flip the display
    pygame.display.flip()
    
    #time step
    time.sleep(.025);
    
    robot.sync_constants()
    #print(str(data_dictionary["rpm"]))
    #print(str(robot.rpm))

# Done! Time to quit.
pygame.quit()