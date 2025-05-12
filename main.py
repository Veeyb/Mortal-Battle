import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

#create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mortal Battle")  # Updated game name

#set framerate
clock = pygame.time.Clock()
FPS = 60

# Global flag to trigger game restart
restart_game = False
paused = False  # Global paused state
selected_map = None  # Variable to store selected map

#define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

#define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# Load music and sounds
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

# Load background images
bg_image = pygame.image.load("assets/images/background/map1night.png").convert_alpha()  # Default map
mainmenu_bg = pygame.image.load("assets/images/background/mainmenu.png").convert_alpha()  # Main menu background
map1_preview = pygame.image.load("assets/images/background/map1night.png").convert_alpha()  # Map 1 preview
map2_preview = pygame.image.load("assets/images/background/map2.png").convert_alpha()  # Map 2 preview

# Load spritesheets
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

# Load victory image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

#define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

#define font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)
menu_font = pygame.font.Font("assets/fonts/turok.ttf", 40)

# Function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# Function to draw background for Main Menu
def draw_main_menu_bg():
    scaled_mainmenu_bg = pygame.transform.scale(mainmenu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_mainmenu_bg, (0, 0))

# Function for drawing fighter health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

# Main Menu
def main_menu():
    menu_running = True
    while menu_running:
        draw_main_menu_bg()  # Draw the main menu background

        draw_text("Mortal Battle", count_font, WHITE, SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 4)

        # Draw start and exit buttons
        draw_text("Start", menu_font, WHITE, SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2)
        draw_text("Exit", menu_font, WHITE, SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 60)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Start button
                if SCREEN_WIDTH // 2 - 60 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 60 and SCREEN_HEIGHT // 2 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 + 40:
                    mode_selection()
                # Exit button
                elif SCREEN_WIDTH // 2 - 60 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 60 and SCREEN_HEIGHT // 2 + 60 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 + 100:
                    pygame.quit()
                    exit()

# Mode Selection
def mode_selection():
    global paused
    selecting_mode = True
    while selecting_mode:
        screen.fill(BLACK)  # Clear screen
        draw_text("Select Mode", count_font, WHITE, SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 4)

        # Draw Duel Mode and Story Mode buttons
        draw_text("Duel Mode", menu_font, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
        draw_text("Story Mode (coming soon)", menu_font, WHITE, SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 + 60)
        draw_text("Main Menu", menu_font, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Duel Mode button
                if SCREEN_WIDTH // 2 - 100 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 100 and SCREEN_HEIGHT // 2 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 + 40:
                    map_selection()  # Go to map selection
                # Story Mode button (not implemented)
                elif SCREEN_WIDTH // 2 - 160 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 160 and SCREEN_HEIGHT // 2 + 60 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 + 100:
                    pass
                # Main Menu button
                elif SCREEN_WIDTH // 2 - 100 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 100 and SCREEN_HEIGHT // 2 + 120 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 + 160:
                    main_menu()

# Map Selection
def map_selection():
    global selected_map
    selecting_map = True
    while selecting_map:
        screen.fill(BLACK)  # Clear screen
        draw_text("Select Map", count_font, WHITE, SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 6)

        # Draw map previews and selection buttons
        screen.blit(pygame.transform.scale(map1_preview, (300, 200)), (SCREEN_WIDTH // 4 - 100, SCREEN_HEIGHT // 2 - 100))
        draw_text("Map 1", menu_font, WHITE, SCREEN_WIDTH // 4 - 50, SCREEN_HEIGHT // 2 + 100)

        screen.blit(pygame.transform.scale(map2_preview, (300, 200)), (SCREEN_WIDTH * 3 // 4 - 100, SCREEN_HEIGHT // 2 - 100))
        draw_text("Map 2", menu_font, WHITE, SCREEN_WIDTH * 3 // 4 - 50, SCREEN_HEIGHT // 2 + 100)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Map 1 button
                if SCREEN_WIDTH // 4 - 100 <= mouse_pos[0] <= SCREEN_WIDTH // 4 + 200 and SCREEN_HEIGHT // 2 - 100 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 + 100:
                    selected_map = "map1night.png"  # Map 1 selected
                    start_duel()  # Start duel with selected map
                # Map 2 button
                elif SCREEN_WIDTH * 3 // 4 - 100 <= mouse_pos[0] <= SCREEN_WIDTH * 3 // 4 + 200 and SCREEN_HEIGHT // 2 - 100 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 + 100:
                    selected_map = "map2.png"  # Map 2 selected
                    start_duel()  # Start duel with selected map

# Start Duel with selected map
def start_duel():
    global bg_image
    if selected_map == "map1night.png":
        bg_image = pygame.image.load("assets/images/background/map1night.png").convert_alpha()
    elif selected_map == "map2.png":
        bg_image = pygame.image.load("assets/images/background/map2.png").convert_alpha()

    duel_mode()  # Start the duel mode with the selected map

# Duel Mode
def duel_mode():
    global restart_game, paused
    # Variables setup for duel mode
    fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
    fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
    intro_count = 3
    last_count_update = pygame.time.get_ticks()
    score = [0, 0]  # player scores. [P1, P2]
    round_over = False
    ROUND_OVER_COOLDOWN = 2000

    # Resetting pause state here to ensure it starts fresh
    paused = False

    run = True
    while run:
        clock.tick(FPS)

        if paused:
            pause_menu()  # Display pause menu
            continue

        if restart_game:
            # Resetting the game state before restarting
            fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
            fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
            score = [0, 0]  # Reset score
            intro_count = 3  # Reset intro count
            round_over = False  # Reset round-over flag
            restart_game = False  # Reset the restart flag
            continue  # Restart the game loop

        # Draw background
        draw_bg()

        # Show player stats
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)
        draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
        draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

        # Update countdown
        if intro_count <= 0:
            # Move fighters
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
        else:
            # Display count timer
            draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
            # Update count timer
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        # Update fighters
        fighter_1.update()
        fighter_2.update()

        # Draw fighters
        fighter_1.draw(screen)
        fighter_2.draw(screen)

        # Check for player defeat
        if round_over == False:
            if fighter_1.alive == False:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif fighter_2.alive == False:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            # Display victory image
            screen.blit(victory_img, (360, 150))
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                round_over = False
                intro_count = 3
                fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = True  # Pause the game

        # Update display
        pygame.display.update()

    # Exit pygame
    pygame.quit()


# Pause Menu
def pause_menu():
    global paused, score, intro_count, round_over, fighter_1, fighter_2, restart_game
    while paused:
        screen.fill(BLACK)  # Clear screen
        draw_text("PAUSED", count_font, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 4)

        # Draw continue, restart, and back to mode selection buttons
        draw_text("Continue", menu_font, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
        draw_text("Restart", menu_font, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60)
        draw_text("Back to Mode Selection", menu_font, WHITE, SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 + 120)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Continue button (Resume the game)
                if SCREEN_WIDTH // 2 - 100 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 100 and SCREEN_HEIGHT // 2 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 + 40:
                    paused = False  # Resume game

                # Restart button (Restart the duel)
                elif SCREEN_WIDTH // 2 - 100 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 100 and SCREEN_HEIGHT // 2 + 60 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 + 100:
                    # Set restart flag to true and exit pause menu
                    score[0] = score[1] = 0
                    intro_count = 3
                    round_over = False
                    fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                    fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
                    paused = False  # Exit pause menu
                    restart_game = True  # Set flag to restart the game

                # Back to Mode Selection button
                elif SCREEN_WIDTH // 2 - 160 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 160 and SCREEN_HEIGHT // 2 + 120 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 + 160:
                    mode_selection()  # Go back to mode selection
                    paused = False  # Exit pause


# Start main menu
main_menu()
