import pygame
import assets
from fighter import Fighter
from character import load_all_characters
from projectile import ShurikenProjectile
import random

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Story Mode")

clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

font_dialog = pygame.font.Font("assets/fonts/turok.ttf", 28)
font_big = pygame.font.Font("assets/fonts/turok.ttf", 50)
font_medium = pygame.font.Font("assets/fonts/turok.ttf", 35)

assets.load_assets()
characters = load_all_characters()
sword_fx = assets.get_sound('sword_fx')
if sword_fx:
    sword_fx.set_volume(0.5)

player_char = "samurai1"
stage_enemies = {
    1: "samurai5",
    2: "samurai4",
    3: "samurai2",
    4: "samurai7",
}

stage_dialogs_opening = {
    1: "Ini adalah awal dari pembalasan dendamku,akan ku musnahkan semua musuh yang menghalangiku!",
    2: "Majulah semua musuhku,akan ku bunuh kalian semua selayaknya kalian membunuh keluargaku!",
    3: "Kau Samurai Biadap bawa tuanmu sang Demon Samurai kesini,Akan kupenggal kepala kalian berdua!",
    4: "Kau bajingan, kau sudah mengotori martabat seorang samurai!,kau membunuh semua keluargaku hanya untuk mendapatkan kekuatan Demon yang keji itu!,akan ku musnahkan kau dari muka bumi ini!"
}

stage_dialogs_defeat = {
    1: "Tidak ini tidak mungkin terjadi!balas dendamku! aghh...",
    2: "Tidak ini tidak mungkin terjadi!balas dendamku! aghh...",
    3: "Tidak ini tidak mungkin terjadi!balas dendamku! aghh...",
    4: "Tidak ini tidak mungkin terjadi!balas dendamku! aghh...",
}

final_dialog = "Akhirnya dendamku terbalaskan...tak ada lagi artinya hidupku,disinilah perjalananku berakhir..."

paused = [False]

SPAWN_Y = 450

CHARACTER_OFFSETS = {
    "samurai1": (-50, -140),
    "samurai2": (-48, -138),
    "samurai3": (-45, -135),
    "samurai4": (-46, -137),
    "samurai5": (-50, -139),
    "samurai6": (-49, -140),
    "samurai7": (-47, -136),
}

class StoryFighter(Fighter):
    def __init__(self, player, x, y, flip, char_key, characters=None):
        character = None
        if characters and char_key in characters:
            character = characters[char_key]
        super().__init__(x, y, flip=flip, char_key=char_key, character=character)

        self.player = player
        self.characters = characters or {}

        self.is_ai = (player != 1)
        self.ai_action_cooldown = 1000
        self.ai_last_action = 0
        self.ai_action = "idle"

        self.blocking = False
        self.ultimate_cooldown = 5000
        self.last_ultimate_time = -self.ultimate_cooldown

        self.throw_cooldown = 3000
        self.last_throw_time = -self.throw_cooldown

        self.damage = 10
        self.transformed = False

        self.projectiles = []

        self.offset_x, self.offset_y = CHARACTER_OFFSETS.get(char_key, (0, 0))
        self.rect.x += self.offset_x
        self.rect.y = SPAWN_Y + self.offset_y

        self.is_attacking = False
        self.is_attack2_active = False
        self.is_attack3_active = False
        self.is_throwing = False
        self.is_ultimate = False

        self.is_jumping = False
        self.velocity_y = 0
        self.gravity = 1

        self.action = "IDLE"
        self.last_dx = 0

    @property
    def active_character(self):
        if hasattr(self.character, "current_character"):
            return self.character.current_character
        return self.character

    def handle_input(self, screen_width, screen_height, screen, target, round_over):
        current_time = pygame.time.get_ticks()
        if not self.alive or round_over:
            return

        dx = 0

        if self.player == 1:
            keys = pygame.key.get_pressed()
            left = keys[pygame.K_a]
            right = keys[pygame.K_d]
            jump_key = keys[pygame.K_w]
            attack1_key = keys[pygame.K_e]
            attack2_key = keys[pygame.K_r]
            attack3_key = keys[pygame.K_t]
            throw_key = keys[pygame.K_q]
            ultimate_key = keys[pygame.K_f]
            block_key = keys[pygame.K_g]

            if left:
                dx = -self.speed
            elif right:
                dx = self.speed

            self.last_dx = dx

            self.move(dx, 0, screen_width, screen_height)

            if jump_key and not self.is_jumping and not self.is_ultimate:
                self.is_jumping = True
                self.velocity_y = -15
                self.action = "JUMP"
                self.frame_index = 0

            if self.is_jumping:
                self.rect.y += self.velocity_y
                self.velocity_y += self.gravity
                if self.rect.y >= SPAWN_Y + self.offset_y:
                    self.rect.y = SPAWN_Y + self.offset_y
                    self.is_jumping = False
                    self.velocity_y = 0
                    self.action = "IDLE"
                    self.frame_index = 0

            if block_key and not self.blocking:
                self.blocking = True
                self.action = "DEFEND"
                self.frame_index = 0
            elif not block_key and self.blocking:
                self.blocking = False
                self.action = "IDLE"

            if not (self.is_attacking or self.is_attack2_active or self.is_attack3_active or
                    self.is_throwing or self.is_ultimate or self.blocking or self.is_jumping):
                if attack1_key and "ATTACK1" in self.active_character.animation_list:
                    self.is_attacking = True
                    self.action = "ATTACK1"
                    self.frame_index = 0
                elif attack2_key and "ATTACK2" in self.active_character.animation_list:
                    self.is_attack2_active = True
                    self.action = "ATTACK2"
                    self.frame_index = 0
                elif attack3_key and "ATTACK3" in self.active_character.animation_list:
                    self.is_attack3_active = True
                    self.action = "ATTACK3"
                    self.frame_index = 0
                elif dx != 0:
                    self.action = "RUN"
                else:
                    self.action = "IDLE"

            if (throw_key and not self.is_throwing and not self.blocking and
                current_time - self.last_throw_time >= self.throw_cooldown):
                if "THROW" in self.active_character.animation_list:
                    self.is_throwing = True
                    self.action = "THROW"
                    self.frame_index = 0
                    proj_x = self.rect.centerx + (50 if not self.flip else -50)
                    proj_y = self.rect.centery
                    proj_dir = -1 if self.flip else 1
                    projectile = ShurikenProjectile(proj_x, proj_y, proj_dir)
                    self.projectiles.append(projectile)
                    shuriken_fx = assets.get_sound("shuriken_fx")
                    if shuriken_fx:
                        shuriken_fx.play()
                    self.last_throw_time = current_time

            if (ultimate_key and not self.is_ultimate and
                current_time - self.last_ultimate_time >= self.ultimate_cooldown and
                not self.blocking):
                if "ULTIMATE" in self.active_character.animation_list:
                    self.is_ultimate = True
                    self.action = "ULTIMATE"
                    self.frame_index = 0
                    self.last_ultimate_time = current_time

        else:
            if self.char_key == "samurai7" and not self.transformed and self.health <= 30:
                self.transformed = True
                self.is_ultimate = True
                self.action = "SHOUT"
                self.frame_index = 0
                self.health = 50
                self.damage *= 1.2
                self.last_ultimate_time = current_time
                return

            if current_time - self.ai_last_action > self.ai_action_cooldown:
                self.ai_last_action = current_time
                self.ai_action = self.decide_ai_action()

            dx = 0
            if self.ai_action == "left":
                dx = -self.speed
            elif self.ai_action == "right":
                dx = self.speed

            if self.ai_action == "jump" and not self.is_jumping:
                self.is_jumping = True
                self.velocity_y = -15
                self.action = "JUMP"
                self.frame_index = 0

            if self.is_jumping:
                self.rect.y += self.velocity_y
                self.velocity_y += self.gravity
                if self.rect.y >= SPAWN_Y + self.offset_y:
                    self.rect.y = SPAWN_Y + self.offset_y
                    self.is_jumping = False
                    self.velocity_y = 0
                    self.action = "IDLE"
                    self.frame_index = 0

            if self.ai_action == "attack" and not self.is_attacking:
                self.is_attacking = True
                self.action = "ATTACK1"
                self.frame_index = 0
            elif self.ai_action == "attack2" and not self.is_attack2_active:
                self.is_attack2_active = True
                self.action = "ATTACK2"
                self.frame_index = 0
            elif self.ai_action == "attack3" and not self.is_attack3_active:
                self.is_attack3_active = True
                self.action = "ATTACK3"
                self.frame_index = 0
            elif self.ai_action == "throw" and not self.is_throwing:
                current_time = pygame.time.get_ticks()
                if ("THROW" in self.active_character.animation_list and
                    current_time - self.last_throw_time >= self.throw_cooldown):
                    self.is_throwing = True
                    self.action = "THROW"
                    self.frame_index = 0
                    proj_x = self.rect.centerx + (50 if not self.flip else -50)
                    proj_y = self.rect.centery
                    proj_dir = -1 if self.flip else 1
                    projectile = ShurikenProjectile(proj_x, proj_y, proj_dir)
                    self.projectiles.append(projectile)
                    self.last_throw_time = current_time
            elif self.ai_action == "ultimate" and not self.is_ultimate:
                if "ULTIMATE" in self.active_character.animation_list:
                    self.is_ultimate = True
                    self.action = "ULTIMATE"
                    self.frame_index = 0
                    self.last_ultimate_time = current_time

            self.last_dx = dx

            if dx != 0 and not (self.is_attacking or self.is_attack2_active or self.is_attack3_active or
                               self.is_throwing or self.is_ultimate or self.is_jumping):
                self.action = "RUN"
            elif not (self.is_attacking or self.is_attack2_active or self.is_attack3_active or
                      self.is_throwing or self.is_ultimate or self.is_jumping):
                self.action = "IDLE"

            self.move(dx, 0, screen_width, screen_height)

        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

    def decide_ai_action(self):
        possible_actions = ["idle", "left", "right", "attack", "attack2", "attack3"]
        if "THROW" in self.active_character.animation_list:
            possible_actions.append("throw")
        if "ULTIMATE" in self.active_character.animation_list:
            possible_actions.append("ultimate")
        return random.choice(possible_actions)

    def check_attack_hit(self, target, damage):
        distance = abs(self.rect.centerx - target.rect.centerx)
        if distance <= 100 and not target.blocking:
            target.take_damage(damage)

    def update(self):
        anim_list = self.active_character.animation_list
        frame_index = self.active_character.frame_index

        if not self.alive:
            self.active_character.change_action("DEATH")
            self.active_character.flip = self.flip
            self.active_character.update()
            death_frames = anim_list.get("DEATH", [])
            if frame_index >= len(death_frames) - 1:
                self.active_character.frame_index = len(death_frames) - 1
            return

        super().update()

        if self.action == "HURT":
            hurt_frames = anim_list.get("HURT", [])
            if frame_index >= len(hurt_frames) - 1:
                self.action = "IDLE"
        elif self.action == "DEFEND":
            if not self.blocking:
                self.action = "IDLE"
        else:
            self.active_character.change_action(self.action)

        self.active_character.flip = self.flip
        self.active_character.update()

        if self.character:
            self.character.update()

        if self.is_attacking:
            frames = len(anim_list.get("ATTACK1", []))
            if frame_index == frames - 1:
                self.check_attack_hit(self.target, self.damage)
            if frame_index >= frames - 1:
                self.is_attacking = False
                if self.last_dx != 0 and not self.blocking and not self.is_jumping:
                    self.action = "RUN"
                else:
                    self.action = "IDLE"

        if self.is_attack2_active:
            frames = len(anim_list.get("ATTACK2", []))
            if frame_index == frames - 1:
                self.check_attack_hit(self.target, self.damage)
            if frame_index >= frames - 1:
                self.is_attack2_active = False
                if self.last_dx != 0 and not self.blocking and not self.is_jumping:
                    self.action = "RUN"
                else:
                    self.action = "IDLE"

        if self.is_attack3_active:
            frames = len(anim_list.get("ATTACK3", []))
            if frame_index == frames - 1:
                self.check_attack_hit(self.target, self.damage)
            if frame_index >= frames - 1:
                self.is_attack3_active = False
                if self.last_dx != 0 and not self.blocking and not self.is_jumping:
                    self.action = "RUN"
                else:
                    self.action = "IDLE"

        if self.is_throwing:
            frames = len(anim_list.get("THROW", []))
            if frame_index == frames - 1:
                self.check_attack_hit(self.target, self.damage)
            if frame_index >= frames - 1:
                self.is_throwing = False
                if self.last_dx != 0 and not self.blocking and not self.is_jumping:
                    self.action = "RUN"
                else:
                    self.action = "IDLE"

        if self.is_ultimate:
            frames = len(anim_list.get("ULTIMATE", []))
            if frame_index == frames - 1:
                self.check_attack_hit(self.target, int(self.damage * 1.2))
            if frame_index >= frames - 1:
                self.is_ultimate = False
                if self.last_dx != 0 and not self.blocking and not self.is_jumping:
                    self.action = "RUN"
                else:
                    self.action = "IDLE"

        if self.is_jumping:
            frames = len(anim_list.get("JUMP", []))
            if frame_index >= frames - 1 and self.rect.y >= SPAWN_Y + self.offset_y:
                self.is_jumping = False
                self.action = "IDLE"
                self.frame_index = 0

        for projectile in self.projectiles[:]:
            projectile.update()
            if projectile.active and self.target.rect.colliderect(projectile.rect):
                if not self.target.blocking:
                    self.target.take_damage(self.damage)
                projectile.active = False
            if not projectile.active:
                self.projectiles.remove(projectile)

def render_multiline_text(text, font, color, x, y, max_width, line_height):
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] > max_width:
            lines.append(current_line)
            current_line = word + ' '
        else:
            current_line = test_line
    lines.append(current_line)
    for i, line in enumerate(lines):
        txt_surf = font.render(line.strip(), True, color)
        screen.blit(txt_surf, (x, y + i * line_height))

def wait_for_space():
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def countdown():
    count = 3
    count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
    last_count_time = pygame.time.get_ticks()

    while count > 0:
        screen.fill(BLACK)
        render_multiline_text(f"{count}", count_font, RED, SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 40, 100, count_font.get_height())
        pygame.display.update()

        while True:
            now = pygame.time.get_ticks()
            if now - last_count_time >= 1000:
                last_count_time = now
                count -= 1
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            clock.tick(FPS)

def pause_menu():
    font = pygame.font.Font("assets/fonts/turok.ttf", 40)
    btn_continue = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 70, 200, 50)
    btn_restart = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
    btn_back = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 50)

    while True:
        screen.fill((20, 20, 20))

        title_surf = font.render("PAUSED", True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 130))
        screen.blit(title_surf, title_rect)


        cont_surf = font.render("Continue", True, WHITE)
        rest_surf = font.render("Restart Duel", True, WHITE)
        back_surf = font.render("Back to Mode Selection", True, WHITE)

        screen.blit(cont_surf, cont_surf.get_rect(center=btn_continue.center))
        screen.blit(rest_surf, rest_surf.get_rect(center=btn_restart.center))
        screen.blit(back_surf, back_surf.get_rect(center=btn_back.center))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if btn_continue.collidepoint(mx, my):
                    return "continue"
                elif btn_restart.collidepoint(mx, my):
                    return "restart"
                elif btn_back.collidepoint(mx, my):
                    return "back"

def run_battle(player_char, enemy_char):
    fighter_1 = StoryFighter(1, 200, SPAWN_Y, False, player_char, characters=characters)
    fighter_2 = StoryFighter(2, 700, SPAWN_Y, True, enemy_char, characters=characters)

    fighter_1.target = fighter_2
    fighter_2.target = fighter_1

    countdown()

    running = True
    round_over = False
    round_over_time = 0
    winner = None

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused[0] = True
                    result = pause_menu()
                    paused[0] = False
                    if result == "continue":
                        pass
                    elif result == "restart":
                        return "restart"
                    elif result == "back":
                        return "back"

        screen.fill(BLACK)
        screen.blit(pygame.transform.scale(assets.get_image("bg_map2"), (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

        fighter_1.handle_input(screen.get_width(), screen.get_height(), screen, fighter_2, round_over)
        fighter_2.handle_input(screen.get_width(), screen.get_height(), screen, fighter_1, round_over)

        fighter_1.update()
        fighter_2.update()

        fighter_1.draw(screen)
        fighter_2.draw(screen)
        for projectile in fighter_1.projectiles:
            projectile.draw(screen)
        for projectile in fighter_2.projectiles:
            projectile.draw(screen)

        def draw_health_bar(health, x, y):
            ratio = health / 100
            pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
            pygame.draw.rect(screen, RED, (x, y, 400, 30))
            pygame.draw.rect(screen, (255, 255, 0), (x, y, 400 * ratio, 30))

        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)

        if not round_over:
            if not fighter_1.alive:
                round_over = True
                round_over_time = pygame.time.get_ticks()
                winner = 2
            elif not fighter_2.alive:
                round_over = True
                round_over_time = pygame.time.get_ticks()
                winner = 1
        else:
            if winner == 1:
                text = font_big.render("Victory!", True, WHITE)
            else:
                text = font_big.render("Defeat!", True, RED)
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, rect)

            if pygame.time.get_ticks() - round_over_time > 3000:
                return winner

        pygame.display.update()

def story_mode():
    current_stage = 1
    running = True

    while running and current_stage <= 4:
        screen.fill(BLACK)
        render_multiline_text(stage_dialogs_opening[current_stage], font_dialog, WHITE, 40, SCREEN_HEIGHT // 2 - 50, SCREEN_WIDTH - 80, font_dialog.get_height() + 5)
        pygame.display.update()
        wait_for_space()

        winner = run_battle(player_char, stage_enemies[current_stage])

        if winner == "restart":
            current_stage = 1
            continue
        elif winner == "back":
            return
        elif winner is None:
            return

        if winner == 1:
            screen.fill(BLACK)
            render_multiline_text("Victory!", font_big, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 300, font_big.get_height())
            pygame.display.update()
            wait_for_space()
            current_stage += 1
        else:
            screen.fill(BLACK)
            render_multiline_text(stage_dialogs_defeat[current_stage], font_dialog, RED, 40, SCREEN_HEIGHT // 2 - 50, SCREEN_WIDTH - 80, font_dialog.get_height() + 5)
            pygame.display.update()
            wait_for_space()

    if current_stage > 4:
        screen.fill(BLACK)
        render_multiline_text(final_dialog, font_dialog, WHITE, 40, SCREEN_HEIGHT // 2 - 50, SCREEN_WIDTH - 80, font_dialog.get_height() + 5)
        pygame.display.update()
        wait_for_space()
