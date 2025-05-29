import pygame
from pygame import mixer
import assets
from character import load_all_characters
from charselection import run_character_selection
from duel import duel_mode
from story import story_mode  # import story_mode yang baru dibuat

pygame.init()
mixer.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mortal Battle")

assets.load_assets()

clock = pygame.time.Clock()
FPS = 60

characters = load_all_characters()

pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = assets.get_sound('sword_fx')
sword_fx.set_volume(0.5)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
menu_font = pygame.font.Font("assets/fonts/turok.ttf", 40)

mainmenu_bg = assets.get_image('mainmenu_bg')
map1_preview = assets.get_image('bg_map1')
map2_preview = assets.get_image('bg_map2')

paused = [False]  # mutable pause flag

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_main_menu_bg():
    scaled_mainmenu_bg = pygame.transform.scale(mainmenu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_mainmenu_bg, (0, 0))

def pause_menu():
    global paused
    while paused[0]:
        screen.fill(BLACK)
        draw_text("PAUSED", count_font, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 4)

        btn_continue = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 40)
        btn_restart = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60, 200, 40)
        btn_back = pygame.Rect(SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 + 120, 320, 40)

        draw_text("Continue", menu_font, WHITE, btn_continue.x + 50, btn_continue.y)
        draw_text("Restart", menu_font, WHITE, btn_restart.x + 50, btn_restart.y)
        draw_text("Back to Mode Selection", menu_font, WHITE, btn_back.x + 20, btn_back.y)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if btn_continue.collidepoint(mx, my):
                    paused[0] = False
                    return False
                elif btn_restart.collidepoint(mx, my):
                    paused[0] = False
                    return True
                elif btn_back.collidepoint(mx, my):
                    paused[0] = False
                    return None

def main_menu():
    running = True
    while running:
        draw_main_menu_bg()
        draw_text("Mortal Battle", count_font, WHITE, SCREEN_WIDTH // 2 - 255, SCREEN_HEIGHT // 4)
        draw_text("Start", menu_font, WHITE, SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2)
        draw_text("Exit", menu_font, WHITE, SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 60)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if SCREEN_WIDTH // 2 - 60 <= mx <= SCREEN_WIDTH // 2 + 60:
                    if SCREEN_HEIGHT // 2 <= my <= SCREEN_HEIGHT // 2 + 40:
                        mode_selection()
                    elif SCREEN_HEIGHT // 2 + 60 <= my <= SCREEN_HEIGHT // 2 + 100:
                        pygame.quit()
                        exit()

def mode_selection():
    running = True
    while running:
        screen.fill(BLACK)
        draw_text("Select Mode", count_font, WHITE, SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 4)
        draw_text("Duel Mode", menu_font, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
        draw_text("Story Mode", menu_font, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60)
        draw_text("Main Menu", menu_font, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if SCREEN_WIDTH // 2 - 100 <= mx <= SCREEN_WIDTH // 2 + 100:
                    if SCREEN_HEIGHT // 2 <= my <= SCREEN_HEIGHT // 2 + 40:
                        map_selection()
                    elif SCREEN_HEIGHT // 2 + 60 <= my <= SCREEN_HEIGHT // 2 + 100:
                        story_mode()
                    elif SCREEN_HEIGHT // 2 + 120 <= my <= SCREEN_HEIGHT // 2 + 160:
                        main_menu()

def map_selection():
    running = True

    btn_back = pygame.Rect(20, 20, 120, 40)

    while running:
        screen.fill(BLACK)
        draw_text("Select Map", count_font, WHITE, SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 6)
        screen.blit(pygame.transform.scale(map1_preview, (300, 200)), (SCREEN_WIDTH // 4 - 100, SCREEN_HEIGHT // 2 - 100))
        draw_text("Map 1", menu_font, WHITE, SCREEN_WIDTH // 4 - 50, SCREEN_HEIGHT // 2 + 100)
        screen.blit(pygame.transform.scale(map2_preview, (300, 200)), (SCREEN_WIDTH * 3 // 4 - 100, SCREEN_HEIGHT // 2 - 100))
        draw_text("Map 2", menu_font, WHITE, SCREEN_WIDTH * 3 // 4 - 50, SCREEN_HEIGHT // 2 + 100)

        draw_text("Back", menu_font, WHITE, btn_back.x + 30, btn_back.y + 5)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if btn_back.collidepoint(mx, my):
                    running = False
                elif SCREEN_WIDTH // 4 - 100 <= mx <= SCREEN_WIDTH // 4 + 200 and SCREEN_HEIGHT // 2 - 100 <= my <= SCREEN_HEIGHT // 2 + 100:
                    selected_map = "bg_map1"
                    chars = run_character_selection(screen, characters)
                    if chars == "back":
                        continue
                    paused[0] = False
                    while True:
                        duel_mode(chars[1], chars[2], selected_map, screen, clock, sword_fx, characters, paused)
                        if paused[0]:
                            result = pause_menu()
                            if result is None:
                                running = False
                                break
                            elif result is True:
                                paused[0] = False
                                continue
                        else:
                            break
                elif SCREEN_WIDTH * 3 // 4 - 100 <= mx <= SCREEN_WIDTH * 3 // 4 + 200 and SCREEN_HEIGHT // 2 - 100 <= my <= SCREEN_HEIGHT // 2 + 100:
                    selected_map = "bg_map2"
                    chars = run_character_selection(screen, characters)
                    if chars == "back":
                        continue
                    paused[0] = False
                    while True:
                        duel_mode(chars[1], chars[2], selected_map, screen, clock, sword_fx, characters, paused)
                        if paused[0]:
                            result = pause_menu()
                            if result is None:
                                running = False
                                break
                            elif result is True:
                                paused[0] = False
                                continue
                        else:
                            break

main_menu()
