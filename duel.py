import pygame
import assets
from fighter import Fighter
from projectile import ShurikenProjectile

class DuelFighter(Fighter):
    def __init__(self, player, x, y, flip, char_key, sword_fx, characters=None):
        character = None
        if characters and char_key in characters:
            character = characters[char_key]

        super().__init__(x, y, flip=flip, char_key=char_key, character=character)

        self.player = player
        self.sword_fx = sword_fx

        self.characters = characters or {}

        self.speed = 5
        self.velocity_y = 0
        self.gravity = 1

        self.is_attacking = False
        self.is_attack3_active = False
        self.is_throwing = False
        self.is_ultimate = False
        self.ultimate_started = False
        self.is_jumping = False

        self.direction = -1 if self.flip else 1

        self.action_cooldown = 500
        self.last_action_time = 0
        self.jump_cooldown = 700
        self.last_jump_time = 0

        self.throw_cooldown = 700
        self.last_throw_time = 0

        self.attack_damage = 10
        self.throw_damage = 10
        self.ultimate_multiplier = 1.2

        self.target = None

    @property
    def active_character(self):
        if hasattr(self.character, "current_character"):
            return self.character.current_character
        return self.character

    def check_attack_hit(self, target, damage):
        distance = abs(self.rect.centerx - target.rect.centerx)
        if distance <= 100:
            target.take_damage(damage)

    def handle_input(self, screen_width, screen_height, screen, target, round_over, keys, prev_keys):
        current_time = pygame.time.get_ticks()

        if not self.alive or round_over:
            return

        dx = 0

        if self.player == 1:
            key_map = {
                "left": pygame.K_a,
                "right": pygame.K_d,
                "jump": pygame.K_w,
                "throw": pygame.K_q,
                "attack1": pygame.K_e,
                "attack2": pygame.K_r,
                "attack3": pygame.K_t,
                "ultimate": pygame.K_f,
            }
        else:
            key_map = {
                "left": pygame.K_LEFT,
                "right": pygame.K_RIGHT,
                "jump": pygame.K_UP,
                "throw": pygame.K_KP4,
                "attack1": pygame.K_KP1,
                "attack2": pygame.K_KP2,
                "attack3": pygame.K_KP3,
                "ultimate": pygame.K_KP5,
            }

        if keys[key_map["left"]]:
            dx = -self.speed
        elif keys[key_map["right"]]:
            dx = self.speed

        self.move(dx, 0, screen_width, screen_height)

        if target.rect.centerx > self.rect.centerx:
            self.flip = False
            self.direction = 1
        else:
            self.flip = True
            self.direction = -1

        def just_pressed(key):
            return keys[key] and not prev_keys[key]

        if just_pressed(key_map["jump"]) and not self.is_jumping and not self.is_ultimate and (current_time - self.last_jump_time) > self.jump_cooldown:
            self.is_jumping = True
            self.velocity_y = -15
            if self.char_key == "samurai7":
                self.action = "IDLE"
            else:
                if "JUMP" in self.active_character.animation_list and self.active_character.animation_list["JUMP"]:
                    self.action = "JUMP"
            self.frame_index = 0
            self.last_jump_time = current_time
            self.last_action_time = current_time

        if self.is_jumping:
            self.rect.y += self.velocity_y
            self.velocity_y += self.gravity
            if self.rect.y >= 310:
                self.rect.y = 310
                self.is_jumping = False
                self.velocity_y = 0
                self.action = "IDLE"
                self.frame_index = 0

        if not (self.is_attacking or self.is_attack3_active or self.is_throwing or self.is_ultimate) and (current_time - self.last_action_time) >= self.action_cooldown:
            if just_pressed(key_map["attack1"]) and "ATTACK1" in self.active_character.animation_list and self.active_character.animation_list["ATTACK1"]:
                self.is_attacking = True
                self.action = "ATTACK1"
                self.frame_index = 0
                self.last_action_time = current_time
                self.sword_fx.play()
            elif just_pressed(key_map["attack2"]) and "ATTACK2" in self.active_character.animation_list and self.active_character.animation_list["ATTACK2"]:
                self.is_attacking = True
                self.action = "ATTACK2"
                self.frame_index = 0
                self.last_action_time = current_time
                self.sword_fx.play()
            elif just_pressed(key_map["attack3"]) and "ATTACK3" in self.active_character.animation_list and self.active_character.animation_list["ATTACK3"]:
                self.is_attack3_active = True
                self.action = "ATTACK3"
                self.frame_index = 0
                self.last_action_time = current_time
                self.sword_fx.play()

        if not self.is_jumping:
            if just_pressed(key_map["throw"]) and not self.is_throwing and (current_time - self.last_throw_time) > self.throw_cooldown and "THROW" in self.active_character.animation_list and self.active_character.animation_list["THROW"]:
                self.is_throwing = True
                self.action = "THROW"
                self.frame_index = 0
                proj_x = self.rect.centerx + (self.direction * 50)
                proj_y = self.rect.centery
                projectile = ShurikenProjectile(proj_x, proj_y, self.direction)
                self.projectiles.append(projectile)
                shuriken_fx = assets.get_sound("shuriken_fx")
                if shuriken_fx:
                    shuriken_fx.play()
                self.last_action_time = current_time
                self.last_throw_time = current_time

            if just_pressed(key_map["ultimate"]) and not self.is_ultimate:
                if self.char_key == "samurai7":
                    if hasattr(self.character, "ultimate") and callable(getattr(self.character, "ultimate")):
                        self.character.ultimate()
                        self.is_ultimate = True
                        self.ultimate_started = True
                        self.last_action_time = current_time
                        self.action = "SHOUT"
                        self.frame_index = 0
                else:
                    if "ULTIMATE" in self.active_character.animation_list and self.active_character.animation_list["ULTIMATE"]:
                        self.is_ultimate = True
                        self.ultimate_started = True
                        self.last_action_time = current_time
                        self.action = "ULTIMATE"
                        self.frame_index = 0

        if not (self.is_attacking or self.is_attack3_active or self.is_throwing or self.is_ultimate or self.is_jumping):
            if dx != 0:
                self.action = "RUN"
            else:
                self.action = "IDLE"

    def update(self):
        anim_list = self.active_character.animation_list
        frame_index = self.active_character.frame_index

        if self.char_key == "samurai7" and self.character and getattr(self.character, "transforming", False):
            shout_frames = self.character.normal.animation_list.get('SHOUT', [])
            if shout_frames and frame_index >= len(shout_frames) - 1:
                self.character.transforming = False
                self.character.mode = "flaming"
                self.character.current_character = self.character.flaming
                self.character.change_action("IDLE")
                self.is_ultimate = False
                self.action = "IDLE"
                self.frame_index = 0

        if not self.alive:
            self.active_character.change_action("DEATH")
            self.active_character.flip = self.flip
            self.active_character.update()
            death_frames = anim_list.get("DEATH", [])
            if frame_index >= len(death_frames) - 1:
                self.active_character.frame_index = len(death_frames) - 1
            return

        if not (self.char_key == "samurai7" and self.character and getattr(self.character, "transforming", False)):
            if self.action == "HURT":
                hurt_frames = anim_list.get("HURT", [])
                if frame_index >= len(hurt_frames) - 1:
                    self.action = "IDLE"
            else:
                self.active_character.change_action(self.action)

        self.active_character.flip = self.flip
        self.active_character.update()

        if self.character:
            self.character.update()

        if self.is_attacking or self.is_attack3_active:
            current_action = self.action
            frames = len(anim_list.get(current_action, []))
            if frame_index >= frames - 1:
                if self.target:
                    self.check_attack_hit(self.target, self.attack_damage)
                self.is_attacking = False
                self.is_attack3_active = False
                self.action = "IDLE"

        if self.is_throwing:
            frames = len(anim_list.get("THROW", []))
            if frame_index >= frames - 1:
                self.is_throwing = False
                self.action = "IDLE"

        if self.is_ultimate:
            frames = len(anim_list.get("ULTIMATE", []))
            if frame_index >= frames - 1:
                if self.target:
                    damage = int(self.attack_damage * self.ultimate_multiplier)
                    self.check_attack_hit(self.target, damage)
                if not (self.char_key == "samurai7" and self.character and getattr(self.character, "transforming", False)):
                    self.is_ultimate = False
                    self.action = "IDLE"

        if self.is_jumping:
            frames = len(anim_list.get("JUMP", []))
            if (frame_index >= frames - 1 if frames > 0 else True) and self.rect.y >= 310:
                self.is_jumping = False
                self.action = "IDLE"
                self.frame_index = 0

        for projectile in self.projectiles[:]:
            projectile.update()
            if projectile.active and self.target and self.target.rect.colliderect(projectile.rect):
                self.target.take_damage(self.throw_damage)
                projectile.active = False
            if not projectile.active:
                self.projectiles.remove(projectile)

    def draw(self, screen):
        super().draw(screen)
        for projectile in self.projectiles:
            projectile.draw(screen)

    def take_damage(self, amount):
        super().take_damage(amount)
        if self.alive:
            self.action = "HURT"
            if self.character:
                self.character.change_action("HURT")

def duel_mode(p1_char, p2_char, map_key, screen, clock, sword_fx, characters, paused_flag, resume_state=None):
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    if resume_state:
        (fighter_1, fighter_2, score, round_over, round_over_time, intro_count, last_count_update, prev_keys) = resume_state
    else:
        fighter_1 = None
        fighter_2 = None
        score = [0, 0]
        round_over = False
        round_over_time = 0
        intro_count = 3
        last_count_update = pygame.time.get_ticks()
        prev_keys = pygame.key.get_pressed()

        def reset_round():
            nonlocal fighter_1, fighter_2, round_over, round_over_time, intro_count
            fighter_1 = DuelFighter(1, 200, 310, False, p1_char, sword_fx, characters=characters)
            fighter_2 = DuelFighter(2, 700, 310, True, p2_char, sword_fx, characters=characters)
            fighter_1.target = fighter_2
            fighter_2.target = fighter_1

            fighter_1.health = 100
            fighter_1.alive = True
            fighter_1.action = "IDLE"
            fighter_1.frame_index = 0

            fighter_2.health = 100
            fighter_2.alive = True
            fighter_2.action = "IDLE"
            fighter_2.frame_index = 0

            if p1_char == "samurai7":
                fighter_1.character.reset()
            if p2_char == "samurai7":
                fighter_2.character.reset()

            intro_count = 3
            round_over = False
            round_over_time = 0

        reset_round()

    bg_image_local = assets.get_image(map_key)

    while True:
        clock.tick(60)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused_flag[0] = True
                    return (fighter_1, fighter_2, score, round_over, round_over_time, intro_count, last_count_update, keys)

        screen.fill(BLACK)
        scaled_bg = pygame.transform.scale(bg_image_local, (screen.get_width(), screen.get_height()))
        screen.blit(scaled_bg, (0, 0))

        def draw_text(text, font, color, x, y):
            img = font.render(text, True, color)
            screen.blit(img, (x, y))

        def draw_health_bar(health, x, y):
            ratio = health / 100
            pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
            pygame.draw.rect(screen, RED, (x, y, 400, 30))
            pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

        count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
        score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)
        draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
        draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

        if intro_count <= 0:
            fighter_1.handle_input(screen.get_width(), screen.get_height(), screen, fighter_2, round_over, keys, prev_keys)
            fighter_2.handle_input(screen.get_width(), screen.get_height(), screen, fighter_1, round_over, keys, prev_keys)
        else:
            draw_text(str(intro_count), count_font, RED, screen.get_width() // 2, screen.get_height() // 3)
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        fighter_1.update()
        fighter_2.update()

        fighter_1.draw(screen)
        fighter_2.draw(screen)

        if not round_over:
            if not fighter_1.alive:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif not fighter_2.alive:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            victory_img = assets.get_image('victory')
            screen.blit(victory_img, (360, 150))

            if pygame.time.get_ticks() - round_over_time > 2000:
                def reset_round():
                    nonlocal fighter_1, fighter_2, round_over, round_over_time, intro_count
                    fighter_1 = DuelFighter(1, 200, 310, False, p1_char, sword_fx, characters=characters)
                    fighter_2 = DuelFighter(2, 700, 310, True, p2_char, sword_fx, characters=characters)
                    fighter_1.target = fighter_2
                    fighter_2.target = fighter_1

                    fighter_1.health = 100
                    fighter_1.alive = True
                    fighter_1.action = "IDLE"
                    fighter_1.frame_index = 0

                    fighter_2.health = 100
                    fighter_2.alive = True
                    fighter_2.action = "IDLE"
                    fighter_2.frame_index = 0

                    if p1_char == "samurai7":
                        fighter_1.character.reset()
                    if p2_char == "samurai7":
                        fighter_2.character.reset()

                    intro_count = 3
                    round_over = False
                    round_over_time = 0

                reset_round()

        pygame.display.update()
        prev_keys = keys
