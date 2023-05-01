import pygame
import graphics
import time
import input_data as data
from robot import Robot
from robot import settle_status
pygame.init()

running = True
mouse_position = 0


data.selection()

graphics.create_window()
play = graphics.Button("images/start_button.png",0,0, "images/start_button_pressed.png")
redo = graphics.Button("images/redo button.png", 53, 0, "images/Redo button pressed.png")



start_pose = [640,360,0]

if data.angular:
    start_pose = [676,560, data.start_error]
    settle_line = graphics.Vector(640,360, 270, 100, (0,255, 0))
    target_text = graphics.DisplayText(640,210,"Target", None, (0,255,0))
else:
    start_pose = [1100 - data.start_error * 5.9444, 360, 90]
    settle_line = graphics.Vector(1100,500, 270, 280, (0,255,0))
    target_text = graphics.DisplayText(1100, 200, "Target", None, (0,255,0))


robot = Robot(*start_pose, data.angular, data.mass_kg, data.rpm, data.track_width, data.wheel_diameter, data.num_motors)
robot.render()



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
                robot.PID(data.kP_input, data.kI_input, data.kD_input, data.settle_time, data.min_derv, data.target, data.tolerance)
            elif(redo.pressed):
                robot.reset(*start_pose)
    
        else:
            play.pressed = False
            redo.pressed = False


    # Fill the background with black
    graphics.screen.fill((0, 0, 0))

    # Draw a solid blue circle in the center
    settle_status.variable = True
    for instance in graphics.instances:
        instance.render()
    # Flip the display
    pygame.display.flip()
    
 
    
    time.sleep(.025);

# Done! Time to quit.
pygame.quit()