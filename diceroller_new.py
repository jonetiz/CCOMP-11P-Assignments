#  _ _ _ _
# |\       \
# | \_ _ _ _\
# |  |  * *  |
#  \ |  * *  |
#   \| _*_*_ |
# Dice Roller
# Written by Jon Etiz
# Created on 03SEP2022
# This program will roll one of six-shaped dice. Effectively remade my Processing dice roller from Intro to Programming.

# Used to generate a random integers
from random import randint
# Used for display
import pygame

# Define static color variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Triangle drawing function used for tetrahedral, octahedral, and icosahedral faces
def triangle():
    pygame.draw.polygon(dice_display, RED, [(0, 373), (200, 27), (400, 373)])
    drawText(dice_display, str(output), 200, 227, WHITE, 72)


# Square drawing function used for cubical faces
def square():
    pygame.draw.rect(dice_display, BLACK, pygame.Rect(0, 0, 400, 400), 4, 16)
    # Draw number of pips based on the output
    if output == 1:
        pygame.draw.circle(dice_display, BLACK, (200, 200), 32)
    elif output == 2:
        pygame.draw.circle(dice_display, BLACK, (75, 325), 32)
        pygame.draw.circle(dice_display, BLACK, (325, 75), 32)
    elif output == 3:
        pygame.draw.circle(dice_display, BLACK, (75, 325), 32)
        pygame.draw.circle(dice_display, BLACK, (200, 200), 32)
        pygame.draw.circle(dice_display, BLACK, (325, 75), 32)
    elif output == 4:
        pygame.draw.circle(dice_display, BLACK, (75, 75), 32)
        pygame.draw.circle(dice_display, BLACK, (75, 325), 32)
        pygame.draw.circle(dice_display, BLACK, (325, 75), 32)
        pygame.draw.circle(dice_display, BLACK, (325, 325), 32)
    elif output == 5:
        pygame.draw.circle(dice_display, BLACK, (75, 75), 32)
        pygame.draw.circle(dice_display, BLACK, (75, 325), 32)
        pygame.draw.circle(dice_display, BLACK, (200, 200), 32)
        pygame.draw.circle(dice_display, BLACK, (325, 75), 32)
        pygame.draw.circle(dice_display, BLACK, (325, 325), 32)
    elif output == 6:
        pygame.draw.circle(dice_display, BLACK, (75, 75), 32)
        pygame.draw.circle(dice_display, BLACK, (75, 325), 32)
        pygame.draw.circle(dice_display, BLACK, (75, 200), 32)
        pygame.draw.circle(dice_display, BLACK, (325, 200), 32)
        pygame.draw.circle(dice_display, BLACK, (325, 75), 32)
        pygame.draw.circle(dice_display, BLACK, (325, 325), 32)


# Kite drawing function used for trapezohedral faces
def kite():
    pygame.draw.polygon(
        dice_display, BLUE, [(00, 269), (200, 00), (400, 269), (200, 400)])
    drawText(dice_display, str(output), 200, 200, WHITE, 72)


# Pentagon drawing function used for dodecahedral faces
def pentagon():
    pygame.draw.polygon(
        dice_display, GREEN, [(200, 19), (10, 157), (82, 381), (318, 381), (390, 157)])
    drawText(dice_display, str(output), 200, 200, BLACK, 72)


# Dictionary with all of the dice information.
# idx: ("Name", num_faces, draw_function)
DICE = {
    0: ("Tetrahedron", 4, triangle),
    1: ("Cube", 6, square),
    2: ("Octahedron", 8, triangle),
    3: ("Pentagonal Trapezohedron", 10, kite),
    4: ("Dodecahedron", 12, pentagon),
    5: ("Icosahedron", 20, triangle)
}

# The currently selected die
selected_die = 1
# The currently displayed die
current_die = 1
# The currently displayed number
output = randint(1, 6)
# Used to stop inputs when die is rolling
die_rolling = False

# Initializes pygame
pygame.init()

# Establishes window height/width
display = (800, 800)

# Initializes surface for drawing and window based on above height/width
screen = pygame.display.set_mode(display)
# Initializes surface for die display - separate so we can transform (rotation and scale, specifically)
dice_display = pygame.Surface((400, 400))

# Sets window title to "Dice Roller"
pygame.display.set_caption("Dice Roller")


# General purpose function to draw text
def drawText(surface: pygame.Surface, text: str, x: int, y: int, color=BLACK, size: int = 16, align: str = "CENTER"):
    # Select the font
    f = pygame.font.SysFont("timesnewroman", size)
    # Generate the text pixels in cache
    t = f.render(text, True, color)
    # Get the dimensions and position of the text's bounding box
    r = t.get_rect()
    # Set the text alignment and position
    if align is "CENTER":
        r.center = (x, y)
    elif align is "RIGHT":
        r.midright = (x, y)
    elif align is "LEFT":
        r.midleft = (x, y)
    # Draw the text onto the surface
    surface.blit(t, r)


# General purpose function to draw everything.
def draw():
    # Grab die_rolling from global
    global die_rolling
    # Fill the screen with white
    screen.fill(WHITE)
    # Draw some helpful text
    drawText(screen, "Press space to re-roll!", 300, 15, BLACK, 16, "LEFT")
    drawText(screen, "Modify number of faces using left and right arrows.",
             300, 40, BLACK, 16, "LEFT")
    drawText(
        screen, f"Number of Faces: {DICE[selected_die][1]}", 10, 15, BLACK, 32, "LEFT")
    drawText(screen, f"({DICE[selected_die][0]})", 10, 40, BLACK, 16, "LEFT")

    # Draw the dice_display

    # Fill dice_display with white background
    dice_display.fill(WHITE)
    # Switch not implemented into python until 3.10; below is a rudimentary workaround that selects from the
    # DICE dictionary based on current_die and runs the function in the second index. PS: I use Python 3.10
    # so I really only did this for backwards compatibility so Joe could test it.
    DICE[current_die][2]()
    # Draw dice_display onto the screen
    screen.blit(dice_display, (200, 200))
    # Draw the "You rolled a x!" text only if die is not rolling. This way the "surprise" is intact.
    if not die_rolling:
        drawText(screen, f"You rolled a {output}!",
                 400, 700, BLACK, 48, "CENTER")

    # Update display with everything that has been done
    pygame.display.update()


# Function to roll the new die
def roll_die():
    # Grab die_rolling from global
    global die_rolling
    # Run draw to refresh
    draw()
    # Fill dice_display with white to hide old
    dice_display.fill(WHITE)
    # Update dice_display with the white fill
    screen.blit(dice_display, (200, 200))
    pygame.display.update()

    # Rolling die animation for 720 ticks
    for a in range(720):
        dice_display.fill(WHITE)
        # Same switch workaround as above
        DICE[current_die][2]()
        # Apply rotation of `angle` to dice_display and save the resulting surface as rot_dd; this rotates one degree every tick
        rot_dd = pygame.transform.rotate(dice_display, a+1)
        # Use `angle` to scale rot_dd from 0, save resulting surface as rot_dd.
        rot_dd = pygame.transform.scale(
            rot_dd, (400*((a+1)/720), 400*((a+1)/720)))
        # Get new bounding box of rot_dd to ensure we can keep it centered
        rect = rot_dd.get_rect(
            center=dice_display.get_rect(topleft=(200, 200)).center)
        # Put rot_dd on screen
        screen.blit(rot_dd, rect.topleft)
        # Update display
        pygame.display.update()
    else:
        # Switch die_rolling when for loop completes
        die_rolling = False

    # Draw text ***after*** die fully completes animation
    drawText(screen, f"You rolled a {output}!", 400, 700, BLACK, 48, "CENTER")
    # Update display with text
    pygame.display.update()


# Run draw
draw()

# Event loop
while True:
    # Hook event handlers
    for event in pygame.event.get():
        # Closes pygame window and quits python process
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        # Keybinds
        if event.type == pygame.KEYDOWN:
            # Cycle selected_die
            if event.key == pygame.K_LEFT and not die_rolling:
                selected_die = selected_die - 1 if selected_die > 0 else 5
                draw()
            if event.key == pygame.K_RIGHT and not die_rolling:
                selected_die = selected_die + 1 if selected_die < 5 else 0
                draw()
            # Roll die
            if event.key == pygame.K_SPACE and not die_rolling:
                die_rolling = True
                current_die = selected_die
                output = randint(1, DICE[current_die][1])
                roll_die()
