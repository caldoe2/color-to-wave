import pygame
from settings import *
from functions import *
from math import *
pygame.init()
screen = pygame.display.set_mode(resilution_int)
clock = pygame.time.Clock()
running = True
is_drawing = False
# setting up the waves
subsection_a = wave_subsection(subsection_a_width_int, subsection_a_hight_int, 1,1, sin)
subsection_b = wave_subsection(subsection_b_width_int, subsection_b_hight_int,1,1, sin)
subsection_c = wave_subsection(subsection_c_width_int, subsection_c_hight_int,1,1, cos)

combined_wave = combined_wave_subsection(resilution_int[0], resilution_int[1], [subsection_a, subsection_b, subsection_c])
drawable_subsection = DrawableSubsection(400, 800)
color_display = color_subsection(400, 50, combined_wave)



while running:
    # Event handler
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        # Quit
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the click is within the drawable subsection
            if 400 <= mouse_pos[0] <= 800 and 250 <= mouse_pos[1] <= 850:
                is_drawing = True
                rel_x, rel_y = mouse_pos[0] - 400, mouse_pos[1] - 200
                drawable_subsection.draw(rel_x, rel_y, color_display.get_color())
            else:
                for subsection, position in [(subsection_a, (0, 0)), (subsection_b, (0, 200)),
                                             (subsection_c, (0, 400))]:
                    # Adjusting mouse position relative to each subsection's position
                    relative_pos = (mouse_pos[0] - position[0], mouse_pos[1] - position[1])
                    subsection.check_button_click(relative_pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            is_drawing = False

    # Continuous drawing
    if is_drawing:
        mouse_pos = pygame.mouse.get_pos()
        if 400 <= mouse_pos[0] <= 800 and 200 <= mouse_pos[1] <= 800:
            rel_x, rel_y = mouse_pos[0] - 400, mouse_pos[1] - 200
            drawable_subsection.draw(rel_x, rel_y, color_display.get_color())
            # Check if the click is within the drawable subsection
            if 400 <= mouse_pos[0] <= 800 and 200 <= mouse_pos[1] <= 400:
                rel_x, rel_y = mouse_pos[0] - 400, mouse_pos[1] - 200
                drawable_subsection.draw(rel_x, rel_y, color_display.get_color())
            else:
                for subsection, position in [(subsection_a, (0, 0)), (subsection_b, (0, 200)),
                                             (subsection_c, (0, 400))]:
                    # Adjusting mouse position relative to each subsection's position
                    relative_pos = (mouse_pos[0] - position[0], mouse_pos[1] - position[1])
                    subsection.check_button_click(relative_pos)

    screen.fill((0, 0, 0))  # Fill the main screen with black color


    # Draw on the subsections
    subsection_a.draw()
    subsection_b.draw()
    subsection_c.draw()
    combined_wave.draw()
    color_display.draw()

    # Render the subsection onto the main screen at a specific position
    subsection_a.render(screen, (0, 0))
    subsection_b.render(screen, (0, 200))
    subsection_c.render(screen, (0, 400))
    combined_wave.render(screen, (400, 0))
    color_display.render(screen, (400, 200))
    drawable_subsection.render(screen, (400, 250))

    pygame.display.flip()
    clock.tick(fps_int)

pygame.quit()

