import random
import os
import sys
import pygame

#initialize pygame
pygame.init()

# Set up clock for controlling frame rate
clock = pygame.time.Clock()

# Set up fonts
font = pygame.font.Font("assets/comic.ttf", 36)

# Get the screen resolution
screen_info = pygame.display.Info()
screen_width = 1920
screen_height = 1080

# Set up the screen in fullscreen mode
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Rock Game")

# reset values
player_move = 0
cpu_move = 0
player_points = 0
cpu_points = 0
rock_pile = None
game_start = False
cpu_first = False
human_first = False

# evaltualtion function
def evaluate(rock_pile):
    if rock_pile % 2 == 0:
        return 2
    else:
        return -2

# FOR MINIMAX
def perfect_ai_move_MM(rock_pile, cpu_first):
    is_maximizing = cpu_first
    if is_maximizing:
        best_score = float("-inf")
    else:
        best_score = float("inf")
    best_move = None
    for move in [2,3]:
        evaluation = minimax(rock_pile - move, is_maximizing, 10)
        if is_maximizing:
            if evaluation > best_score:
                best_score = evaluation
                best_move = move
        else:
            if evaluation < best_score:
                best_score = evaluation
                best_move = move
    if (rock_pile - best_move) % 2 == 0:
        return best_move
    else:
        best_move = 2
        if (rock_pile - best_move) % 2 == 0:
            return best_move
        else:
            best_move = 3
            if (rock_pile - best_move) % 2 == 0:
                return best_move

# MINIMAX ALGORITHM
def minimax(rock_pile, is_maximizing, depth):
    if is_terminal(rock_pile) or depth == 0:
        return evaluate(rock_pile)
    
    if is_maximizing:
        max_evaluation = float('-inf')
        for move in [2,3]:
            evaluation = minimax(rock_pile - move, not is_maximizing, depth - 1)
            max_evaluation = max(max_evaluation, evaluation)
        return max_evaluation
    else:
        min_evaluation = float('inf')
        for move in [2,3]:
            evaluation = minimax(rock_pile - move, not is_maximizing, depth - 1)
            min_evaluation = min(min_evaluation, evaluation)
        return min_evaluation


# FOR ALPHA-BETA
def perfect_ai_move_AB(rock_pile, cpu_first):
    is_maximizing = cpu_first
    alpha = float('-inf')
    beta = float('inf')
    best_move = None
    for move in [2,3]:
        evaluation = alpha_beta(rock_pile - move, not is_maximizing, 10, alpha, beta)
        if is_maximizing:
            if evaluation > alpha:
                alpha = evaluation
                best_move = move
        else:
            if evaluation < beta:
                beta = evaluation
                best_move = move
    best_move = move
    if (rock_pile - best_move) % 2 == 0:
        return best_move
    else:
        best_move = 2
        if (rock_pile - best_move) % 2 == 0:
            return best_move
        else:
            best_move = 3
            if (rock_pile - best_move) % 2 == 0:
                return best_move
   
# ALPHA-BETA ALGORITHM
def alpha_beta(rock_pile, is_maximizing, depth, alpha, beta):
    if is_terminal(rock_pile) or depth == 0:
        return evaluate(rock_pile)
    
    if is_maximizing:
        max_evaluation = float('inf')
        for move in [2,3]:
            evaluation = alpha_beta(rock_pile - move, True, depth - 1, alpha, beta)
            max_evaluation = max(max_evaluation, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_evaluation
    else:
        min_evaluation = float('-inf')
        for move in [2,3]:
            evaluation = alpha_beta(rock_pile - move, False, depth - 1, alpha, beta)
            min_evaluation = min(min_evaluation, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_evaluation

# function for determining terminal game state
def is_terminal(rock_pile):
    return rock_pile <= 0

# button class for button functionality
class Button:
    def __init__(self, image_path, position, size):
        self.position = position
        self.image = pygame.image.load(image_path)
        self.size = size
        self.rect = self.image.get_rect(topleft=position)
        self.hovered = False
        self.clicked = False

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# scrolling texts
scrolling_text = ["click on the window in the middle of the screen to choose the rockpile starting amount!", "press R to reset the game!", "remember to choose who goes first after each restart!", "remember to pick the ai algorythm each time you restart!"]
current_text_index = 0

# Initial position of the scrolling text (off-screen to the right)
text_x = screen_width
text_y = screen_height // 1.05

# load images
image_path_1 = "assets/rockPile_1.png"
image_path_2 = "assets/rockPile_game_field.png"
image_path_3 = "assets/rockPile_2.png"
image_path_4 = "assets/rockPile_3.png"
image_path_5 = "assets/rockPile_4.png"
image_path_6 = "assets/rockPile_5.png"
image_1 = pygame.image.load(image_path_1)
image_2 = pygame.image.load(image_path_2)
image_3 = pygame.image.load(image_path_3)
image_4 = pygame.image.load(image_path_4)
image_5 = pygame.image.load(image_path_5)
image_6 = pygame.image.load(image_path_6)

# take2/take3 button image paths
button_1_normal_image_path = "assets/button_take2.png"
button_2_normal_image_path = "assets/button_take3.png"
button_1_pressed_image_path = "assets/button_take2_pressed.png"
button_2_pressed_image_path = "assets/button_take3_pressed.png"

# who goes first button image paths
button_3_normal_image_path = "assets/button_human.png"
button_4_normal_image_path = "assets/button_AI.png"
button_3_pressed_image_path = "assets/button_human_pressed.png"
button_4_pressed_image_path = "assets/button_AI_pressed.png"

# ai algorythm selection button image paths
button_9_normal_image_path = "assets/button_minimax.png"
button_10_normal_image_path = "assets/button_alpha-beta.png"
button_9_pressed_image_path = "assets/button_minimax_pressed.png"
button_10_pressed_image_path = "assets/button_alpha-beta_pressed.png"

# exit button image paths
button_13_normal_image_path = "assets/button_exit.png"
button_13_pressed_image_path = "assets/button_exit_pressed.png"

# resize rockpile
new_width_1 = screen_width // 6.4
new_height_1 = screen_height // 3.6
new_width_4 = screen_width // 6.4
new_height_4 = screen_height // 4.55
new_width_5 = screen_width // 6.4
new_height_5 = screen_height // 5.95
new_width_6 = screen_width // 6.4
new_height_6 = screen_height // 8
new_width_7 = screen_width // 10
new_height_7 = screen_height // 10

# resize game field
new_width_2 = screen_width
new_height_2 = screen_height

# resize buttons
new_width_3 = screen_width // 9.6
new_height_3 = screen_height // 5.4

# generate images
image_1 = pygame.transform.scale(image_1, (new_width_1, new_height_1))
image_2 = pygame.transform.scale(image_2, (new_width_2, new_height_2))
image_3 = pygame.transform.scale(image_3, (new_width_4, new_height_4))
image_4 = pygame.transform.scale(image_4, (new_width_5, new_height_5))
image_5 = pygame.transform.scale(image_5, (new_width_6, new_height_6))
image_6 = pygame.transform.scale(image_6, (new_width_7, new_height_7))

# rockpile image positioning
image_1_x = screen_width // 2.4
image_1_y = screen_height // 3.0857
image_3_x = screen_width // 2.4
image_3_y = screen_height // 2.615
image_4_x = screen_width // 2.4
image_4_y = screen_height // 2.294
image_5_x = screen_width // 2.4
image_5_y = screen_height // 2.085
image_6_x = screen_width // 2.2
image_6_y = screen_height // 2

# gamefield image positioning
image_2_x = 0
image_2_y = 0

# take2/take3 button image positioning
button_image_1_x = screen_width // 2.9767
button_image_1_y = screen_height // 1.3935
button_image_2_x = screen_width // 1.85866
button_image_2_y = screen_height // 1.39715

button_image_3_x = screen_width // 2.887
button_image_3_y = screen_height // 1.35
button_image_4_x = screen_width // 1.82857
button_image_4_y = screen_height // 1.375796

# who goes first selection button image positioning
button_image_5_x = screen_width // 2.887218
button_image_5_y = screen_height // 9.3913
button_image_6_x = screen_width // 1.8028
button_image_6_y = screen_height // 10.2857

button_image_7_x = screen_width // 2.84444
button_image_7_y = screen_height // 8.78
button_image_8_x = screen_width // 1.786
button_image_8_y = screen_height // 9.231

# ai algorythm selection button image positioning
button_image_9_x = screen_width // 6.7368
button_image_9_y = screen_height // 3.22
button_image_10_x = screen_width // 6.7368
button_image_10_y = screen_height // 1.9459

button_image_11_x = screen_width // 6.65
button_image_11_y = screen_height // 3.12
button_image_12_x = screen_width // 6.679
button_image_12_y = screen_height // 1.925

# exit button positioning
button_image_13_x = screen_width // 1.19
button_image_13_y = screen_height // 30
button_image_14_x = screen_width // 1.18
button_image_14_y = screen_height // 29.5

# create take2/take3 image buttons
button_1 = Button(button_1_normal_image_path, (button_image_1_x, button_image_1_y), (new_width_3, new_height_3))
button_2 = Button(button_2_normal_image_path, (button_image_2_x, button_image_2_y), (new_width_3, new_height_3))
button_3 = Button(button_1_pressed_image_path, (button_image_3_x, button_image_3_y), (new_width_3, new_height_3))
button_4 = Button(button_2_pressed_image_path, (button_image_4_x, button_image_4_y), (new_width_3, new_height_3))

# create who goes first selection image buttons
button_5 = Button(button_3_normal_image_path, (button_image_5_x, button_image_5_y), (new_width_3, new_height_3))
button_6 = Button(button_4_normal_image_path, (button_image_6_x, button_image_6_y), (new_width_3, new_height_3))
button_7 = Button(button_3_pressed_image_path, (button_image_7_x, button_image_7_y), (new_width_3, new_height_3))
button_8 = Button(button_4_pressed_image_path, (button_image_8_x, button_image_8_y), (new_width_3, new_height_3))

# create ai algorythm selection image buttons
button_9 = Button(button_9_normal_image_path, (button_image_9_x, button_image_9_y), (new_width_3, new_height_3))
button_10 = Button(button_10_normal_image_path, (button_image_10_x, button_image_10_y), (new_width_3, new_height_3))
button_11 = Button(button_9_pressed_image_path, (button_image_11_x, button_image_11_y), (new_width_3, new_height_3))
button_12 = Button(button_10_pressed_image_path, (button_image_12_x, button_image_12_y), (new_width_3, new_height_3))

# create exit button image
button_13 = Button(button_13_normal_image_path, (button_image_13_x, button_image_13_y), (new_width_3, new_height_3))
button_14 = Button(button_13_pressed_image_path, (button_image_14_x, button_image_14_y), (new_width_3, new_height_3))

# Function to display text on the screen
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# main program cycle
player_turn = False
cpu_turn = False
reset = False
pause = True
running = True
human_first = False
cpu_first = False
game_start = False
cpu_algorythm = None
button_13.clicked = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset = True

    if reset:
        # Reset game state here (initialize or set variables to initial values)
        player_move = 0
        cpu_move = 0
        player_points = 0
        cpu_points = 0
        rock_pile = None
        reset = False
        pause = True
        human_first = False
        cpu_first = False
        game_start = False
        player_turn = False
        cpu_turn = False
        cpu_algorythm = None
        button_13.clicked = False

    #mouse_pos = pygame.mouse.get_pos()

    # clear screen
    screen.fill((255, 255, 255))

    # load second image
    screen.blit(image_2, (image_2_x, image_2_y))

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            if button_13.rect.collidepoint(event.pos):
                button_13.clicked = True
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            if button_13.clicked and button_13.rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
            button_13.clicked = False

    # handle the who goes first selection button logic
    if event.type == pygame.MOUSEBUTTONDOWN and not game_start:
        if button_5.is_clicked(event.pos) and not cpu_algorythm == None:
            game_start = True
            human_first = True
            player_turn = True
            cpu_first = False
            cpu_turn = False
            pause = True
            button_5.clicked = True
        elif button_6.is_clicked(event.pos) and not cpu_algorythm == None:
            game_start = True
            cpu_first = True
            cpu_turn = True
            human_first = False
            player_turn = False
            pause = True
            button_6.clicked = True
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            button_6.clicked = False
            button_5.clicked = False

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            if button_9.is_clicked(event.pos):
                cpu_algorythm = minimax
            elif button_10.is_clicked(event.pos):
                cpu_algorythm = alpha_beta

    # draw the buttons
    if event.type == pygame.MOUSEBUTTONDOWN:
        if game_start:
            if event.button == 1: # Left mouse button
                if button_1.is_clicked(event.pos):
                    button_3.draw(screen)
                    button_2.draw(screen)
                    button_6.draw(screen)
                    button_5.draw(screen)
                    button_9.draw(screen)
                    button_10.draw(screen)
                    button_13.draw(screen)
                elif button_2.is_clicked(event.pos):
                    button_4.draw(screen)
                    button_1.draw(screen)
                    button_6.draw(screen)
                    button_5.draw(screen)
                    button_9.draw(screen)
                    button_10.draw(screen)
                    button_13.draw(screen)
                elif not button_1.is_clicked(event.pos) and not button_2.is_clicked(event.pos) and not button_5.is_clicked(event.pos) and not button_6.is_clicked(event.pos) and not button_9.is_clicked(event.pos) and not button_10.is_clicked(event.pos):
                    button_1.draw(screen)
                    button_2.draw(screen)
                    button_5.draw(screen)
                    button_6.draw(screen)
                    button_9.draw(screen)
                    button_10.draw(screen)
                    button_13.draw(screen)
                elif button_5.is_clicked(event.pos):
                    button_1.draw(screen)
                    button_2.draw(screen)
                    button_7.draw(screen)
                    button_6.draw(screen)
                    button_9.draw(screen)
                    button_10.draw(screen)
                    button_13.draw(screen)
                elif button_6.is_clicked(event.pos):
                    button_1.draw(screen)
                    button_2.draw(screen)
                    button_8.draw(screen)
                    button_5.draw(screen)
                    button_9.draw(screen)
                    button_10.draw(screen)
                    button_13.draw(screen)
                elif button_9.is_clicked(event.pos):
                    button_1.draw(screen)
                    button_2.draw(screen)
                    button_5.draw(screen)
                    button_6.draw(screen)
                    button_11.draw(screen)
                    button_10.draw(screen)
                    button_13.draw(screen)
                elif button_10.is_clicked(event.pos):
                    button_1.draw(screen)
                    button_2.draw(screen)
                    button_5.draw(screen)
                    button_6.draw(screen)
                    button_9.draw(screen)
                    button_12.draw(screen)
                    button_13.draw(screen)
                elif button_13.is_clicked(event.pos):
                    button_1.draw(screen)
                    button_2.draw(screen)
                    button_5.draw(screen)
                    button_6.draw(screen)
                    button_9.draw(screen)
                    button_10.draw(screen)
                    button_14.draw(screen)
        elif button_1.is_clicked(event.pos):
            button_3.draw(screen)
            button_2.draw(screen)
            button_5.draw(screen)
            button_6.draw(screen)
            button_9.draw(screen)
            button_10.draw(screen)
            button_13.draw(screen)
        elif button_2.is_clicked(event.pos):
            button_1.draw(screen)
            button_4.draw(screen)
            button_5.draw(screen)
            button_6.draw(screen)
            button_9.draw(screen)
            button_10.draw(screen)
            button_13.draw(screen)
        elif button_9.is_clicked(event.pos):
            button_1.draw(screen)
            button_2.draw(screen)
            button_5.draw(screen)
            button_6.draw(screen)
            button_11.draw(screen)
            button_10.draw(screen)
            button_13.draw(screen)
        elif button_10.is_clicked(event.pos):
            button_1.draw(screen)
            button_2.draw(screen)
            button_5.draw(screen)
            button_6.draw(screen)
            button_9.draw(screen)
            button_12.draw(screen)
            button_13.draw(screen)
        elif button_5.is_clicked(event.pos):
            button_1.draw(screen)
            button_2.draw(screen)
            button_7.draw(screen)
            button_6.draw(screen)
            button_9.draw(screen)
            button_10.draw(screen)
            button_13.draw(screen)
        elif button_6.is_clicked(event.pos):
            button_1.draw(screen)
            button_2.draw(screen)
            button_5.draw(screen)
            button_8.draw(screen)
            button_9.draw(screen)
            button_10.draw(screen)
            button_13.draw(screen)
        elif button_13.is_clicked(event.pos):
            button_1.draw(screen)
            button_2.draw(screen)
            button_5.draw(screen)
            button_6.draw(screen)
            button_9.draw(screen)
            button_10.draw(screen)
            button_14.draw(screen)
        else:
            button_1.draw(screen)
            button_2.draw(screen)
            button_5.draw(screen)
            button_6.draw(screen)
            button_9.draw(screen)
            button_10.draw(screen)
            button_13.draw(screen)
    elif event.type == pygame.MOUSEBUTTONUP:
        button_1.draw(screen)
        button_2.draw(screen)
        button_5.draw(screen)
        button_6.draw(screen)
        button_9.draw(screen)
        button_10.draw(screen)
        button_13.draw(screen)
        if event.button == 1:
            button_1.clicked = False
            button_2.clicked = False 
    else:
        button_1.draw(screen)
        button_2.draw(screen)
        button_5.draw(screen)
        button_6.draw(screen)
        button_9.draw(screen)
        button_10.draw(screen)
        button_13.draw(screen)

    # if human has first move
    if human_first and not cpu_first and game_start:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_1.is_clicked(event.pos):
                player_move = 2
                player_turn = False
                cpu_turn = True
                pause = True
                button_1.clicked = True
            elif button_2.is_clicked(event.pos):
                player_move = 3
                player_turn = False
                cpu_turn = True
                pause = True
                button_2.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            button_1.clicked = False
            button_2.clicked = False
            pause = False

        # calculating human points
        if not player_turn and not (button_1.clicked or button_2.clicked) and game_start and not pause:
            rock_pile -= player_move
            player_points += player_move + evaluate(rock_pile)
            #pause = True
            #cpu_turn = True
            player_turn = False
            if is_terminal(rock_pile):
                #rock_pile += player_move
                player_points += rock_pile - evaluate(rock_pile)
                rock_pile = 0
                game_start = False
        # ai move
        if cpu_turn and not pause and game_start:
            if cpu_algorythm == minimax:
                cpu_move = perfect_ai_move_MM(rock_pile, cpu_first)
                rock_pile -= cpu_move
                cpu_points += cpu_move + evaluate(rock_pile)
                cpu_turn = False
                player_turn = True
                pause = True
                if is_terminal(rock_pile):
                    #rock_pile += cpu_move
                    cpu_points += rock_pile - evaluate(rock_pile)
                    rock_pile = 0
                    game_start = False
            if cpu_algorythm == alpha_beta:
                cpu_move = perfect_ai_move_AB(rock_pile, cpu_first)
                rock_pile -= cpu_move
                cpu_points += cpu_move + evaluate(rock_pile)
                cpu_turn = False
                player_turn = True
                pause = True
                if is_terminal(rock_pile):
                    #rock_pile += cpu_move
                    cpu_points += rock_pile - evaluate(rock_pile)
                    rock_pile = 0
                    game_start = False

    # if ai has first move
    if cpu_first and not human_first and game_start:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_1.is_clicked(event.pos):
                player_move = 2
                player_turn = False
                cpu_turn = True
                pause = True
                button_1.clicked = True
            elif button_2.is_clicked(event.pos):
                player_move = 3
                player_turn = False
                cpu_turn = True
                pause = True
                button_2.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            button_1.clicked = False
            button_2.clicked = False
            pause = False

        # calculating human points
        if not player_turn and not (button_1.clicked or button_2.clicked) and game_start and not pause and not player_move == 0:
            rock_pile -= player_move
            player_points += player_move + evaluate(rock_pile)
            #pause = True
            #cpu_turn = True
            #player_turn = False
            if is_terminal(rock_pile):
                #rock_pile += player_move
                player_points += rock_pile - evaluate(rock_pile)
                rock_pile = 0
                game_start = False

        # ai move
        if cpu_turn and not pause and game_start:
            if cpu_algorythm == minimax:
                cpu_move = perfect_ai_move_MM(rock_pile, cpu_first)
                rock_pile -= cpu_move
                cpu_points += cpu_move + evaluate(rock_pile)
                cpu_turn = False
                player_turn = True
                pause = True
                if is_terminal(rock_pile):
                    #rock_pile += cpu_move
                    cpu_points += rock_pile - evaluate(rock_pile)
                    rock_pile = 0
                    game_start = False
            if cpu_algorythm == alpha_beta:
                cpu_move = perfect_ai_move_AB(rock_pile, cpu_first)
                rock_pile -= cpu_move
                cpu_points += cpu_move + evaluate(rock_pile)
                cpu_turn = False
                player_turn = True
                pause = True
                if is_terminal(rock_pile):
                    #rock_pile += cpu_move
                    cpu_points += rock_pile - evaluate(rock_pile)
                    rock_pile = 0
                    game_start = False

    # render the text
    text1 = font.render(f"Human Chose: {player_move}", True, (0, 0, 0))
    text2 = font.render(f"CPU Chose: {cpu_move}", True, (0, 0, 0))
    text3 = font.render(f"humanPoints: {player_points}", True, (0, 0, 0))
    text4 = font.render(f"cpuPoints: {cpu_points}", True, (0, 0, 0))

    # render the scrolling text
    current_text = scrolling_text[current_text_index]
    text8 = font.render(current_text, True, (0, 0, 0))

    # Update scrolling text position (slide from right to left)
    text_x -= 10
    if text_x < -1500:
        text_x = screen_width
        current_text_index = (current_text_index + 1) % len(scrolling_text)

    text1_rect = text1.get_rect()
    text2_rect = text2.get_rect()
    text3_rect = text3.get_rect()
    text4_rect = text4.get_rect()

    # position the Human Chose text on the screen
    text1_rect.topleft = (screen_width - 1600, screen_height - 220)

    # position the CPU Chose text on the screen
    text2_rect.topleft = (screen_width - 600, screen_height - 220)

    # position the humanPoints text on the screen
    text3_rect.topleft = (screen_width - 1600, screen_height - 180)

    # position the cpuPoints text on the screen
    text4_rect.topleft = (screen_width - 600, screen_height - 180)

    screen.blit(text1, text1_rect)
    screen.blit(text2, text2_rect)
    screen.blit(text3, text3_rect)
    screen.blit(text4, text4_rect)

    if not rock_pile == None and rock_pile >= 40:
        screen.blit(image_1, (image_1_x, image_1_y))
    if not rock_pile == None and rock_pile <= 40 and rock_pile > 30:
        screen.blit(image_3, (image_3_x, image_3_y))
    if not rock_pile == None and rock_pile <= 30 and rock_pile > 20:
        screen.blit(image_4, (image_4_x, image_4_y))
    if not rock_pile == None and rock_pile <= 20 and rock_pile > 10:
        screen.blit(image_5, (image_5_x, image_5_y))
    if not rock_pile == None and rock_pile <= 10 and rock_pile >= 1:
        screen.blit(image_6, (image_6_x, image_6_y))

    # Get input from the user for the initial rock pile value
    if not game_start and rock_pile == None:
        def get_input():
            input_text = ""
            input_rect = pygame.Rect(screen_width // 2 - 65, screen_height // 2, 100, 50)
            color_inactive = pygame.Color('lightskyblue3')
            color_active = pygame.Color('dodgerblue2')
            color = color_inactive
            active = False
            max_length = 3
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if input_rect.collidepoint(event.pos):
                            screen.fill((236, 200, 123), input_rect)
                            active = True
                            if active:
                                draw_text("Enter the initial rock pile value:", font, (0, 0, 0), screen_width // 2, screen_height // 1.6)
                        color = color_active if active else color_inactive
                    if event.type == pygame.KEYDOWN:
                        if active:
                            if event.key == pygame.K_RETURN:
                                input_text = int(input_text)
                                if input_text <= 50:
                                    input_text = 50
                                    return int(input_text)
                                    screen.fill((236, 200, 123), input_rect)
                                if input_text >= 70:
                                    input_text = 70
                                    return int(input_text)
                                    screen.fill((236, 200, 123), input_rect)
                                else:
                                    return int(input_text)
                                    screen.fill((236, 200, 123), input_rect)
                            if event.unicode.isdigit() and len(input_text) <= max_length:
                                input_text = input_text + event.unicode
                                screen.fill((236, 200, 123), input_rect)
                                draw_text(input_text, font, (0, 0, 0), input_rect.x + 50, input_rect.y + 25)
                            if event.key == pygame.K_BACKSPACE:
                                input_text = input_text[:-1]
                                screen.fill((236, 200, 123), input_rect)
                                draw_text(input_text, font, (0, 0, 0), input_rect.x + 50, input_rect.y + 25)
                        if event.key == pygame.K_ESCAPE:
                            screen.fill((236, 200, 123), input_rect)
                            active = False
                            color = color_inactive
                pygame.draw.rect(screen, color, input_rect, 2)
                pygame.display.flip()
                clock.tick(60)

            pygame.display.update(input_rect)
        rock_pile = get_input()

    # drawing the game over text
    if is_terminal(rock_pile):
        if player_points > cpu_points:
            screen.blit(text5, text5_rect)
            pause = True
            game_start = False
        elif cpu_points > player_points:
            screen.blit(text6, text6_rect)
            pause = True
            game_start = False
        else:
            screen.blit(text7, text7_rect)
            pause = True
            game_start = False

    # create a text surface
    text_rockpile = font.render(f"Current rock count: {rock_pile}", True, (0, 0, 0))
    text5 = font.render(f"Humanity lives on!", True, (0, 0, 0))
    text6 = font.render(f"Skynet is coming!", True, (0, 0, 0))
    text7 = font.render(f"Tie!", True, (0, 0, 0))

    # get the rectangle around the text surface
    text_rockpile_rect = text_rockpile.get_rect()
    text5_rect = text5.get_rect()
    text6_rect = text6.get_rect()
    text7_rect = text7.get_rect()

    # center the rockPile text on the screen
    text_rockpile_rect.center = (screen_width // 2, screen_height - 400)

    # position the Humanity lives on! text on the screen
    text5_rect.topleft = (screen_width - 800, screen_height - 600)

    # position the Skynet is coming! text on the screen
    text6_rect.topleft = (screen_width - 800, screen_height - 600)

    # position the Tie! text on the screen
    text7_rect.topleft = (screen_width - 800, screen_height - 600)

    # draw the scrolling text surface onto the screen
    screen.blit(text8, (text_x, text_y))

    # draw the text on the screen
    screen.blit(text_rockpile, text_rockpile_rect)

    # Cap the frame rate
    clock.tick(60)

    # update screen
    pygame.display.flip()

# end pygame
pygame.quit()
sys.exit()