import heapq
import pygame

from graph import Node, Graph
from grid import GridWorld
from utils import *
from d_star_lite import *

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY1 = (145, 145, 102)
GRAY2 = (77, 77, 51)
BLUE = (0, 0, 80)

colors = {
    0: WHITE,
    1: GREEN,
    -1: GRAY1,
    -2: GRAY2
}

# This sets the WIDTH and HEIGHT of each grid location

# This sets the margin between each cell
MARGIN = 3

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(10):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(10):
        grid[row].append(0)  # Append a cell

# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)
grid[1][5] = 1

# Initialize pygame
pygame.init()

X_DIM = 72
Y_DIM = 72
VIEWING_RANGE = 10


# Set the HEIGHT and WIDTH of the screen


# Set title of screen
pygame.display.set_caption("D* Lite Path Planning")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()


s_goals = ['x41y70','x29y70','x29y45','x41y4']  

if __name__ == "__main__":
    obstacle = []
    path = []
    for i in range(72):
        obstacle.append((i,24))
        obstacle.append((i,48))
    for i in range(4,67):
        obstacle.append((i,36))
    graph = GridWorld(X_DIM, Y_DIM)
    s_start = 'x41y4'
    s_goal = s_goals[0]
    graph.goal = s_goal
    goal_coords = stateNameToCoords(s_goal)
    graph.goal_coords = goal_coords
    graph.setStart(s_start)
    graph.setGoal(s_goal)
    k_m = 0
    s_last = s_start
    queue = []
    s_current = s_start
    pos_coords = stateNameToCoords(s_current)
    graph.pos_coords = pos_coords
    graph, queue, k_m = initDStarLite(graph, queue, s_start, s_goal, k_m)
    for item in obstacle:
        graph.cells[item[0]][item[1]] = -1
    path, s_new, k_m = moveAndRescan(
                    graph, queue, s_current, VIEWING_RANGE, k_m)
    basicfont = pygame.font.SysFont('Comic Sans MS', 12)

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # print('space bar! call next action')
                path, s_new, k_m = moveAndRescan(
                    graph, queue, s_current, VIEWING_RANGE, k_m)
                if s_new == 'goal':
                    print('Goal Reached!')
                    del s_goals[0]
                    s_goal = s_goals[0]
                    graph = GridWorld(X_DIM, Y_DIM)
                    for item in obstacle:
                        graph.cells[item[0]][item[1]] = -1
                    goal_coords = stateNameToCoords(s_goal)
                    graph.goal_coords = goal_coords
                    graph.setStart(s_current)
                    graph.setGoal(s_goal)   
                    if len(s_goals) == 0:
                        done = True
                    k_m = 0
                    queue = []
                    pos_coords = stateNameToCoords(s_current)
                    graph.pos_coords = pos_coords
                    graph, queue, k_m = initDStarLite(graph, queue, s_current, s_goal, k_m)
                else:
                    # print('setting s_current to ', s_new)
                    s_current = s_new
                    pos_coords = stateNameToCoords(s_current)
                    graph.pos_coords = pos_coords
                    # print('got pos coords: ', pos_coords)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                # Set that location to one
                if(graph.cells[row][column] in [0,2,3]):
                    obstacle.append((row,column))
                    graph.cells[row][column] = -1

        # Set the screen background
        render_all(graph)
    pygame.quit()
