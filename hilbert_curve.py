import pygame
import numpy as np
import colorsys

# order of the Hilbert curve
order = 6

# drawing speed
draw_speed = 60  # the higher this value the faster it draws

# number of points
N = 2 ** order
total = N ** 2


# Return the coordinates of the points, given the order
def hilbert(i):
    points = np.array([[0, 0],  # point 1
                       [0, 1],  # point 2
                       [1, 1],  # point 3
                       [1, 0]])  # point 4

    v = points[i & 3]

    for j in range(1, order):
        i = i >> 2  # Shifts the bits of the number by 2
        index = i & 3
        len_seg = 2 ** j
        if index == 0:
            v[0], v[1] = v[1], v[0]
        elif index == 1:
            v[1] += len_seg
        elif index == 2:
            v[0] += len_seg
            v[1] += len_seg
        elif index == 3:
            temp = - 1 - v[0] + len_seg
            v[0] = - 1 - v[1] + (2 * len_seg)
            v[1] = temp
    return v


# define a main function
def main():
    # initialize the pygame module
    pygame.init()

    # initialize clock object
    clock = pygame.time.Clock()

    # the width and height must be powers of 2
    size = width, height = 512, 512
    col_back = 0, 0, 0  # 255, 255, 255

    len_line = width / N

    path = np.empty((0, 2))
    for i in range(0, total):
        h = (hilbert(i) * len_line) + (len_line / 2)
        path = np.round(np.vstack((path, h)))
        # print(f"countdown: {total - i}")
        if ((total - i) % 1000) == 0:
            print(f"countdown: {total - i}")


    # create a surface on screen
    screen = pygame.display.set_mode(size)

    # define a variable to control the main loop
    running = True
    c1 = 1

    # main loop
    while running:

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

        # clock.tick(60)  # drawing speed
        clock.tick(draw_speed)  # drawing speed

        if c1 <= total:
            for i in range(1, c1):
                h = i / total
                # Line color
                col_line = tuple(round(i * 255)/1 for i in colorsys.hsv_to_rgb(h, 1, 1))
                add_points = False
                if add_points:
                    pygame.draw.circle(screen, col_line, (path[i - 1, 0], path[i - 1, 1]), 2)
                    pygame.draw.circle(screen, col_line, (path[i, 0], path[i, 1]), 2)
                pygame.draw.lines(screen,
                                  col_line,
                                  False,
                                  [(path[i - 1, 0], path[i - 1, 1]), (path[i, 0], path[i, 1])],
                                  1)
            c1 += 1
        elif c1 > total:
            c1 = 1

        pygame.display.update()
        screen.fill(col_back)


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
