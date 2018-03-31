"""
Wormy (a Nibbles clone)
By Al Sweigart al@inventwithpython.com
http://inventwithpython.com/pygame
Released under a "Simplified BSD" license
Modifications by Valdemar Svabensky valdemar@mail.muni.cz
"""

import sys, random, pygame
from pygame.locals import *

FPS = 10
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, 'Window width must be a multiple of cell size.'
assert WINDOWHEIGHT % CELLSIZE == 0, 'Window height must be a multiple of cell size.'
NUM_CELLS_X = WINDOWWIDTH/CELLSIZE
NUM_CELLS_Y = WINDOWHEIGHT/CELLSIZE

BGCOLOR = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)

# No other constants go here!
# Testing github

def main():
    pygame.init()

    global BASICFONT, DISPLAYSURF, FPSCLOCK
    
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)

    show_start_screen()
    while True:
        if was_key_pressed():
            print("play the game")
            run_game()
    
    
def terminate():
    pygame.quit()
    sys.exit()


def was_key_pressed():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYUP:
            print("play")
            return True
        return False


def wait_for_key_pressed():
    """Wait for a player to press any key."""
    msg_surface = BASICFONT.render('Press a key to play.', True, GRAY)
    msg_rect = msg_surface.get_rect()
    msg_rect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(msg_surface, msg_rect)
    pygame.display.update()


def show_start_screen():
    """Show a welcome screen at the first start of the game. (Do not modify.)"""
    title_font = pygame.font.Font('freesansbold.ttf', 100)
    title_surface = title_font.render('Snake!', True, WHITE)
    title_rect = title_surface.get_rect()
    title_rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(title_surface, title_rect)
    wait_for_key_pressed()


def show_game_over_screen():
    """Show a game over screen when the player loses. (Do not modify.)"""
    game_over_font = pygame.font.Font('freesansbold.ttf', 150)
    game_surface = game_over_font.render('Game', True, WHITE)
    over_surface = game_over_font.render('Over', True, WHITE)
    game_rect = game_surface.get_rect()
    over_rect = over_surface.get_rect()
    game_rect.midtop = (WINDOWWIDTH / 2, 10)
    over_rect.midtop = (WINDOWWIDTH / 2, game_rect.height + 10 + 25)

    DISPLAYSURF.blit(game_surface, game_rect)
    DISPLAYSURF.blit(over_surface, over_rect)
    wait_for_key_pressed()


def get_new_snake():
    """Set a random start point for a new snake and return its coordinates."""
    x = random.randint(5,NUM_CELLS_X-5)
    y = random.randint(3,NUM_CELLS_Y-3)
    snake = [(x-2,y),(x-1,y),(x,y)]
    return(snake,"right")


def get_random_location():
    """Return a random cell on the game plan."""
    x = random.randint(0,NUM_CELLS_X-1)
    y = random.randint(0,NUM_CELLS_Y-1)
    return(x,y)


def run_game():
    """Main game logic. Return on game over."""
    snake,direction = get_new_snake()
    apple = get_random_location()
    a,b = snake[len(snake)-1]
    while a>-1 and a<32 and b>-1 and b<24:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    if direction!="down":
                        direction = "up"
                        new_head = (a,b-1)
                        snake.append(new_head)
                        if new_head!=apple:
                            snake.pop(0)
                        else:
                            apple = get_random_location()
                if event.key == pygame.K_DOWN:
                    if direction!="up":
                        direction = "down"
                        new_head = (a,b+1)
                        snake.append(new_head)
                        if new_head!=apple:
                            snake.pop(0)
                        else:
                            apple = get_random_location()
                if event.key == pygame.K_LEFT:
                    if direction!="right":
                        direction = "left"
                        new_head = (a-1,b)
                        snake.append(new_head)
                        if new_head!=apple:
                            snake.pop(0)
                        else:
                            apple = get_random_location()
                if event.key == pygame.K_RIGHT:
                    if direction!="left":
                        direction = "right"
                        new_head = (a+1,b)
                        snake.append(new_head)
                        if new_head!=apple:
                            snake.pop(0)
                        else:
                            apple = get_random_location()
            elif event.type == pygame.QUIT:
                terminate()

            a,b = snake[len(snake)-1]
            #print(direction,snake)
            if (a>-1 and a<32 and b>-1 and b<24) and (len(snake) == len(set(snake))):
                draw_game_state(snake, apple)
                pygame.display.update()
            else:
                show_game_over_screen(snake)
                return True

def show_game_over_screen(snake):
    text_surf=BASICFONT.render("Konec, skóre:"+str(len(snake)),True,RED,BGCOLOR)
    text_rect=text_surf.get_rect()
    text_rect.topleft = (200,200)
    DISPLAYSURF.blit(text_surf,text_rect)

def draw_game_state(snake, apple):
    """Draw the contents on the screen. (Do not modify.)"""

    # Draw grid
    DISPLAYSURF.fill(BGCOLOR)
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # Draw vertical lines
        pygame.draw.line(DISPLAYSURF, GRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # Draw horizontal lines
        pygame.draw.line(DISPLAYSURF, GRAY, (0, y), (WINDOWWIDTH, y))

    # Draw snake
    for body_part in snake:
        x = body_part[0] * CELLSIZE
        y = body_part[1] * CELLSIZE
        outer_part_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        inner_part_rect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, outer_part_rect)
        pygame.draw.rect(DISPLAYSURF, GREEN, inner_part_rect)

    # Draw apple
    x = apple[0] * CELLSIZE
    y = apple[1] * CELLSIZE
    apple_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, apple_rect)

    # Draw score
    score_surface = BASICFONT.render('Score: ' + str(len(snake) - 3), True, WHITE)
    score_rect = score_surface.get_rect()
    score_rect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(score_surface, score_rect)


if __name__ == '__main__':
    main()
