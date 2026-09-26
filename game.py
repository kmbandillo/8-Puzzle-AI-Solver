import pygame
import pygame.gfxdraw
import os
from button import Button
from dropdown import DropDown
from node import Node
import time

# pygame setup
pygame.init()
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eight Puzzle")
font = os.path.join("pixel.ttf")
initial_state = [[0,0,0],[0,0,0],[0,0,0]]
goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# read the values from puzzle.in
with open("puzzle.in", "r") as file:
    lines = file.readlines()

# assign the values to the grid
for i in range(3):
    num = lines[i].split()
    for j in range(3):
        initial_state[i][j] = int(num[j])

current_state = initial_state

# function for drawing white background for the game board
def draw_background(color):
    pygame.draw.rect(screen, color, [0, 0, WIDTH, HEIGHT], 0, 0)

# function for counting the number of inversion
    # according to (How to Check If an Instance of 8 Puzzle Is Solvable, 2014)s an 
    # 8-puzzle with an even number of inversion in its input state is solvable

def inversion_counter(s):
    # Convert 2D array into a 1D array omitting 0 values
    array_values = [tile for row in s for tile in row if tile != 0]
    inversions = 0

    for i in range(len(array_values)):
        for j in range(i + 1, len(array_values)):
            if array_values[i] > array_values[j]:
                inversions += 1

    return inversions

# function for finding the tiles with 0 value
def blank_position(s):
    blank_row, blank_col = None, None
    for row in range(3):
        for col in range(3):
            if s[row][col] == 0:
                blank_row, blank_col = row, col
                break
        if blank_row is not None:
            break
    return blank_row, blank_col

# function that checks if the puzzle is solvable
def is_solvable(puzzle):
    inversions_count = inversion_counter(puzzle)

    # if the inversion count is even, the puzzle is solvable
    if inversions_count % 2 == 0: 
        return True
    return False

# function that draws the tiles to the screen
def draw_tiles(grid):
    for i in range(3):
        for j in range(3):
            value = grid[i][j]
            tile_color = "white" if value == 0 else "pink" 
            
            # draw the tile
            pygame.draw.rect(screen, tile_color, [j * 100 + 50, i * 100 + 50 + 40, 90, 90], 0)
            
            # gives color to the tile if its value is not 0
            if value > 0:
                font = pygame.font.Font(None, 70)
                text = font.render(str(value), True, 'white')
                text_rect = text.get_rect()
                
                # center the text on the tile
                text_rect.center = (j * 100 + 50 + 90 // 2, i * 100 + 50 + 40 + 90 // 2)
                screen.blit(text, text_rect)

# prints in the terminal if the puzzle is solvable or not
solvable_font = pygame.font.Font(font, 15)
solvable_text = solvable_font.render("SOLVABLE. You can do this!", True, "gray35")
solvable_rect = solvable_text.get_rect(center = (WIDTH // 2, solvable_text.get_height() + 90 // 2))
unsolvable_text1 = solvable_font.render("NOT SOLVABLE.", True, "gray38")
unsolvable_rect1 = unsolvable_text1.get_rect(center = (WIDTH // 2, (solvable_text.get_height() + 40  // 2)))
unsolvable_text2 = solvable_font.render("You can now exit the game.", True, "gray38")
unsolvable_rect2 = unsolvable_text2.get_rect(center = (WIDTH // 2, (solvable_text.get_height() + 80 // 2)))

# shows if the puzzle is solvable or not
def is_solvable_display(button):
    if is_solvable(initial_state) == True: 
        screen.blit(solvable_text, solvable_rect)
        
    else:
        screen.blit(unsolvable_text1, unsolvable_rect1)
        screen.blit(unsolvable_text2, unsolvable_rect2)
        button.draw(screen)
        button.handle_event(event)

# returns the how many moves it takes before reaching the goal state
def PathCost(path):   
    if path is not None:
        cost = len(path)
        return cost
    return None
    
# returns all the possible actions
def Actions(s):
    row, col = blank_position(s)

    adjacent_tiles = [
        (row - 1, col),  # up
        (row, col + 1),  # right
        (row + 1, col),  # down
        (row, col - 1),  # left
    ]
    possible_actions = [t for t in adjacent_tiles if all((value >= 0 and value < 3) for value in t)]

    for t in adjacent_tiles:
        if all((value >= 0 and value < 3) for value in t):
            # converts the coordinates to letters
            if t == (row - 1, col):
                possible_actions.append("U")  # up
            elif t == (row + 1, col):
                possible_actions.append("D")  # down
            elif t == (row, col + 1):
                possible_actions.append("R")  # right
            elif t == (row, col - 1):
                possible_actions.append("L")  # left

    return possible_actions

# determines if it reaches the goal state
def GoalTest(s):
    if s == goal_state:
        return True
    else:
        return False

# BFS algorithm 
def BFSearch(initial_state):
    frontier = []
    frontier.append(initial_state) #stores initial state to frontier
    visited = set()
    parent = {}  #stores parent node
    action_queue = {}  # queue of actions
    explored_states = 0

    while frontier:
        current_state = frontier.pop(0)

        if GoalTest(current_state):
            # Reconstruct the actions from the goal state to the initial state
            actions = []
            while current_state is not None:
                if tuple(map(tuple, current_state)) in action_queue:
                    actions.append(action_queue[tuple(map(tuple, current_state))])
                current_state = parent.get(tuple(map(tuple, current_state)))
            actions.reverse()
            return actions, explored_states
        explored_states += 1

        visited.add(tuple(map(tuple, current_state)))  # Convert to tuple for hashing
        
        for action in Actions(current_state):
            new_state = Result(current_state, action)

            # check whether the new state is not in visited before adding it to the frontier
            if tuple(map(tuple, new_state)) not in visited:
                frontier.append(new_state)
                # Store the parent and child nodes and enqueue action
                parent[tuple(map(tuple, new_state))] = current_state
                action_queue[tuple(map(tuple, new_state))] = action

    return None
# return None if there is no solution

# DFS Algorithm to search for the shortest pathcost. It behaves like a 
def DFSearch(initial_state, depth_limit=200):
    frontier = []
    frontier.append((initial_state, []))
    visited = set()
    explored_states = 0

    while frontier:
        current_state, actions = frontier.pop()  # pops the top of the stack
        explored_states += 1 


        if GoalTest(current_state):
            return actions, explored_states  # return the actions to reach the goal state
        
        # convert to tuple for hashing
        visited.add(tuple(map(tuple, current_state)))  
        
        # limit the depth to avoid infinite loops
        if len(actions) < depth_limit:  
            for action in Actions(current_state):
                new_state = Result(current_state, action)
                
                # check if the new state is not in visited before adding it to the frontier stack
                if tuple(map(tuple, new_state)) not in visited:
                    frontier.append((new_state, actions + [action]))  # append new actions

    return None, explored_states  # return None if no solution is found within the depth limit

# computes the Manhattan distance to get heuristic estimated cost from node n to the goal node
def getH(s):
    distance = [[0,0,0],[0,0,0],[0,0,0]]

    for i in range(len(s)):
        for j in range(len(s[0])):
            for x, row in enumerate(goal_state):
                for y, elem in enumerate(row):
                    # check if the current element matches s[i][j] and is not 0
                    if elem == s[i][j] and elem != 0:
                        d = abs(x - i) + abs(y - j) #distance formula
                        distance[i][j] = d
    h = sum([elem for row in distance for elem in row if elem != 0])
    return h

# gets the node with min f
def getMinF(openList):
    if not openList:
        return None
    # initializes the min_node
    min_node = openList[0]
    min_f = min_node.g + getH(min_node.state) 

    # compares the next node from the openlist
    for node in openList[1:]:
        f = node.g + getH(node.state)
        if f < min_f:
            min_node = node
            min_f = f
    # returns the min_node
    return min_node 

def AStar(initial_state):
    openList = [Node(initial_state)]
    closedList = []
    explored_states = 0
    while openList:
        bestNode = getMinF(openList)
        openList.remove(bestNode)
        closedList.append(bestNode)
        explored_states += 1 
        if GoalTest(bestNode.state):  # Implement GoalTest for your specific problem
            # Build and return the sequence of actions from the initial state to the goal state
            actions = []
            while bestNode.parent is not None:
                actions.insert(0, bestNode.action)
                bestNode = bestNode.parent
            return actions, explored_states
        
        for action in Actions(bestNode.state):  # Implement Actions for your specific problem
            child_state = Result(bestNode.state, action)  # Implement Result for your specific problem
            child_g = bestNode.g + 1

            child_node = Node(child_state, child_g, bestNode, action)
            
            
            if (not any(node.state == child_state for node in closedList) and
                not any(node.state == child_state for node in openList) or
                any(node.state == child_state and node.g > child_g for node in openList)):
                openList.append(child_node)
                
   
    return None, explored_states

                
def Result(current_state, action):
    # create a copy of the current state to avoid modifying it directly
    new_state = [row[:] for row in current_state]

    # find the coordinates of the blank tile (0)
    blank_row, blank_col = blank_position(current_state)

    # initialize new_row and new_col with current position
    new_row, new_col = blank_row, blank_col

    # determine the new position
    if action == 'U':
        new_row -= 1
    elif action == 'D':
        new_row += 1
    elif action == 'L':
        new_col -= 1
    elif action == 'R':
        new_col += 1

    # swap the blank tile with the adjacent tile
    new_state[blank_row][blank_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[blank_row][blank_col]

    return new_state

def exit_game():
    pygame.quit()
    quit()

def output(actions): 
    with open("puzzle.out", 'w') as file:
        for action in actions:
            file.write(f"{action} ")

def move_step(action, current_state):
    new_state = Result(current_state, action)  #apply the action to the current state
    draw_tiles(new_state)  # replace 'draw_grid' with your grid rendering function
    pygame.display.update()
    return new_state


# Solution info tracking
solution_info = {
    "has_run": False,
    "has_solution": False,
    "path_cost": None,
    "explored_states": None,
    "solution_str": "",
    "scroll_y": 0,
    "max_scroll": 0
}

solution_font = pygame.font.Font(font, 11)

def wrap_text(text, font_obj, max_width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        if font_obj.size(test_line)[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def draw_solution(screen):
    if not solution_info["has_run"]:
        return

    box_x = 20
    box_y = 508
    box_w = 360
    box_h = 84

    # Draw themed container matching the buttons/tiles
    pygame.draw.rect(screen, "mistyrose1", [box_x, box_y, box_w, box_h], border_radius=6)
    pygame.draw.rect(screen, "lightpink3", [box_x, box_y, box_w, box_h], width=1, border_radius=6)

    inner_pad_top = 7
    inner_pad_left = 12
    inner_pad_right = 16
    line_height = 15

    if solution_info["has_solution"]:
        cost_str = str(solution_info["path_cost"]) if solution_info["path_cost"] is not None else "-"
        states_str = str(solution_info["explored_states"]) if solution_info["explored_states"] is not None else "-"
        lines = [
            f"Path cost: {cost_str}",
            f"Explored states: {states_str}",
        ]
        wrap_w = box_w - inner_pad_left - inner_pad_right
        sol_lines = wrap_text(f"SOLUTION: {solution_info['solution_str']}", solution_font, wrap_w)
        lines.extend(sol_lines)
    else:
        lines = []
        if solution_info.get("explored_states") is not None:
            lines.append(f"Explored states: {solution_info['explored_states']}")
        lines.append("No Solution!")

    visible_h = box_h - inner_pad_top * 2
    total_content_h = len(lines) * line_height
    max_scroll = max(0, total_content_h - visible_h)
    solution_info["max_scroll"] = max_scroll

    # Clamp scroll_y
    solution_info["scroll_y"] = max(0, min(max_scroll, solution_info["scroll_y"]))

    content_clip_rect = pygame.Rect(box_x + 2, box_y + 4, box_w - 4, box_h - 8)
    screen.set_clip(content_clip_rect)

    for idx, line in enumerate(lines):
        rendered = solution_font.render(line, True, "gray25")
        screen.blit(rendered, (box_x + inner_pad_left, box_y + inner_pad_top - solution_info["scroll_y"] + idx * line_height))

    screen.set_clip(None)

    # Scrollbar indicator if content exceeds visible area
    if max_scroll > 0:
        bar_x = box_x + box_w - 9
        bar_y = box_y + 7
        bar_h = box_h - 14
        thumb_h = max(14, int(bar_h * (visible_h / total_content_h)))
        thumb_y = bar_y + int((bar_h - thumb_h) * (solution_info["scroll_y"] / max_scroll))
        pygame.draw.rect(screen, "mistyrose2", [bar_x, bar_y, 4, bar_h], border_radius=2)
        pygame.draw.rect(screen, "lightpink3", [bar_x, thumb_y, 4, thumb_h], border_radius=2)

# check if the file exists
actions_str = [] 
STEP_DELAY = 1.0 # delays the movement of a tile
# Function to handle the "Next" button click
next_button_clicked = False
def next_button():
    if b_clicked or d_clicked or a_clicked:
        global current_state
        global actions_str
        global next_button_clicked
        global solution_info
        if not next_button_clicked:
            if os.path.exists("puzzle.out"):
                with open("puzzle.out", "r") as file: #reads the output file
                    actions_str = file.read().strip().split()
            next_button_clicked = True
            if not solution_info["has_run"] and actions_str:
                solution_info["has_run"] = True
                solution_info["has_solution"] = True
                solution_info["solution_str"] = " ".join(actions_str)
                solution_info["path_cost"] = len(actions_str)
                solution_info["explored_states"] = "-"

        if actions_str:
            action = actions_str.pop(0)
            if action is not None:
                current_state = Result(current_state, action)
                draw_game_elements()
                pygame.display.update()  # update the display after each step
                time.sleep(STEP_DELAY)  # add a delay between steps

def show_solution(i):
    global soln
    global a_clicked
    global b_clicked
    global d_clicked
    global next_button_clicked
    global actions_str
    global solution_info
    soln = True
    next_button_clicked = False
    actions_str = []
    path = None
    explored_states = 0
    if b_clicked:
        path, explored_states = BFSearch(i)
    elif d_clicked: 
        path, explored_states = DFSearch(i)
    elif a_clicked:
        path, explored_states = AStar(i)
    if b_clicked or d_clicked or a_clicked:
        solution_info["has_run"] = True
        solution_info["scroll_y"] = 0
        if path is not None:
            output(path)
            solution_info["has_solution"] = True
            solution_info["path_cost"] = PathCost(path)
            solution_info["explored_states"] = explored_states
            solution_info["solution_str"] = " ".join(path)
        else:
            solution_info["has_solution"] = False
            solution_info["path_cost"] = None
            solution_info["explored_states"] = explored_states
            solution_info["solution_str"] = ""


running = True  # initial state
exit_enabled = False
win_flag = False 
soln = False
b_clicked = False
d_clicked = False
a_clicked = False

file_msg = Button(200, 40, 0, 40, WIDTH, HEIGHT, "File Saved")
exit_button = Button(100, 40, 0, 40, WIDTH, HEIGHT, "Exit", action=exit_game)
solution = Button(150, 40, -60, 165, WIDTH, HEIGHT, "Solution", action=lambda: show_solution(initial_state))
next = Button(150, 40, -60, 100, WIDTH, HEIGHT, "Next", action=next_button)
choices = DropDown(110, 40, 100, 165, WIDTH, HEIGHT, None, "CHOOSE", ["BFS", "DFS","A*"],["lightpink3","gray" ],["lightgray", "pink"])

def draw_game_elements():
    draw_background("white")
    draw_tiles(current_state)
    is_solvable_display(exit_button)
    solution.draw(screen)
    next.draw(screen)
    draw_solution(screen)
    choices.draw(screen)

is_dragging_scroll = False
last_drag_y = 0

while running:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEWHEEL:
            solution_info["scroll_y"] = max(0, min(solution_info.get("max_scroll", 0), solution_info["scroll_y"] - event.y * 15))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                solution_info["scroll_y"] = max(0, min(solution_info.get("max_scroll", 0), solution_info["scroll_y"] - 15))
            elif event.button == 5:
                solution_info["scroll_y"] = max(0, min(solution_info.get("max_scroll", 0), solution_info["scroll_y"] + 15))
            elif event.button == 1:
                box_rect = pygame.Rect(20, 508, 360, 84)
                if box_rect.collidepoint(event.pos):
                    is_dragging_scroll = True
                    last_drag_y = event.pos[1]
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                is_dragging_scroll = False
        elif event.type == pygame.MOUSEMOTION:
            if is_dragging_scroll:
                delta = event.pos[1] - last_drag_y
                last_drag_y = event.pos[1]
                solution_info["scroll_y"] = max(0, min(solution_info.get("max_scroll", 0), solution_info["scroll_y"] - delta))
        if exit_enabled:
            exit_button.draw(screen)
            exit_button.handle_event(event)

    # check if the win condition is met
    if GoalTest(current_state):
        win_flag = True

    # handle mouse click events and swap tiles if necessary
    if pygame.mouse.get_pressed()[0]:
        # get the mouse position and calculate the clicked tile index
        mouse_x, mouse_y = pygame.mouse.get_pos()
        clicked_col = (mouse_x - 50) // 100
        clicked_row = (mouse_y - 50) // 100

        row, col = blank_position(current_state)
 
        if (clicked_row, clicked_col) in Actions(current_state):
            # swap values between the clicked tile and the blank tile
            current_state[row][col], current_state[clicked_row][clicked_col] = current_state[clicked_row][clicked_col], current_state[row][col]

    # dropdown menu for choosing algorithm
    if is_solvable(current_state):
         # list the option of the dropdown menu
        selected_option = choices.update(event_list)
        if selected_option >= 0:
            choices.main = choices.options[selected_option]

         # allows the other button to be clicked or chosen again 
        if choices.main == "BFS" and not b_clicked:
            b_clicked = True  
            d_clicked = False
            a_clicked = False
        elif choices.main == "DFS" and not d_clicked:
            d_clicked = True
            b_clicked = False
            a_clicked = False
        elif choices.main == "A*" and not a_clicked:
            a_clicked = True
            d_clicked = False
            b_clicked = False
        
        draw_game_elements()
        solution.handle_event(event)
        next.handle_event(event) 
    else:
        draw_background("white")
        draw_tiles(current_state)
        is_solvable_display(exit_button)

    # if the goal state is met, player wins
    if win_flag:
        # draws the background of YOU WIN!!! text
        draw_background("mistyrose1")
        
        pygame.draw.rect(screen, "white", [0, 0, WIDTH, HEIGHT], 20, 0)
        pygame.draw.rect(screen, (204, 204, 255), [0, 0, WIDTH, HEIGHT], 15, 0)

        win_font = pygame.font.Font(font, 45)

        shadow_text1 = win_font.render("YOU WIN!!!", True, "black")
        shadow_rect1 = shadow_text1.get_rect(center=(WIDTH // 2+2, HEIGHT // 2+2))

        win_text = win_font.render("YOU WIN!!!", True, (204, 204, 255))
        win_text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        screen.blit(shadow_text1, shadow_rect1)
        screen.blit(win_text, win_text_rect)
        exit_button.rect.center = (WIDTH // 2, HEIGHT - 60)
        exit_button.draw(screen)
        exit_button.handle_event(event)
        
    
    pygame.display.update() # updates the display while the user is making a move
    
# this will execute if the player wins
pygame.quit()
