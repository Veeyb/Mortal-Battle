import pygame
import assets

def safe_load_animation(key, frames_count, scale=3):
    sprite_sheet = assets.get_image(key)
    if sprite_sheet is None:
        print(f"Warning: Asset '{key}' not found or failed to load!")
        return []
    return split_sprite_sheet(sprite_sheet, frames_count, scale)

def split_sprite_sheet(sprite_sheet, frames_count, scale=3):
    frames = []
    frame_width = sprite_sheet.get_width() // frames_count
    frame_height = sprite_sheet.get_height()
    for i in range(frames_count):
        frame = sprite_sheet.subsurface(i * frame_width, 0, frame_width, frame_height)
        frame = pygame.transform.scale(frame, (frame_width * scale, frame_height * scale))
        frames.append(frame)
    return frames

class Character:
    def __init__(self, animation_frames, scale=3, facing_left=False, offset=(0,0)):
        self.scale = scale
        self.facing_left = facing_left
        self.offset = offset
        self.animation_list = animation_frames
        self.frame_index = 0
        self.action = "IDLE"
        self.update_time = pygame.time.get_ticks()
        self.flip = False
        self.x = 0
        self.y = 0

    def change_action(self, new_action):
        new_action = new_action.upper()
        if new_action != self.action and new_action in self.animation_list and self.animation_list[new_action]:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        elif new_action not in self.animation_list or not self.animation_list[new_action]:
            print(f"Warning: Animation '{new_action}' not found or empty for this character!")

    def update(self):
        animation_cooldown = 50
        current_time = pygame.time.get_ticks()
        frames = self.animation_list.get(self.action, [])
        if frames:
            if current_time - self.update_time > animation_cooldown:
                self.frame_index += 1
                if self.frame_index >= len(frames):
                    self.frame_index = 0
                self.update_time = current_time
        else:
            self.frame_index = 0

    def draw(self, surface, x=None, y=None):
        frames = self.animation_list.get(self.action, [])
        if frames and 0 <= self.frame_index < len(frames):
            frame = frames[self.frame_index]
            # Jangan gabungkan flip dan facing_left
            # Hanya flip kalau self.flip True, facing_left jangan dipakai karena menyebabkan bug samurai2
            if self.flip:
                frame = pygame.transform.flip(frame, True, False)
            draw_x = (x if x is not None else self.x) - self.offset[0] * self.scale
            draw_y = (y if y is not None else self.y) - self.offset[1] * self.scale
            surface.blit(frame, (draw_x, draw_y))

class TransformingCharacter:
    def __init__(self, normal_animations, flaming_animations, scale=3, facing_left=False, offset=(0,0)):
        self.normal = Character(normal_animations, scale, facing_left, offset)
        self.flaming = Character(flaming_animations, scale, facing_left, offset)
        self.mode = 'normal'
        self.transforming = False
        self.current_character = self.normal

    def ultimate(self):
        if not self.transforming and self.mode == 'normal':
            self.transforming = True
            self.current_character.change_action('SHOUT')

    def change_action(self, action):
        action = action.upper()
        self.current_character.change_action(action)

    def update(self):
        self.current_character.update()
        if self.transforming:
            shout_frames = self.current_character.animation_list.get('SHOUT', [])
            if shout_frames and self.current_character.frame_index >= len(shout_frames) - 1:
                self.transforming = False
                self.mode = 'flaming'
                self.current_character = self.flaming
                self.current_character.change_action('IDLE')

    def draw(self, surface, x=None, y=None):
        self.current_character.draw(surface, x, y)

    def reset(self):
        self.mode = 'normal'
        self.transforming = False
        self.current_character = self.normal
        self.current_character.change_action('IDLE')

    @property
    def animation_list(self):
        return self.current_character.animation_list

offsets = {
    "samurai1": (32, 32),
    "samurai2": (32, 0),
    "samurai3": (37, 27),
    "samurai4": (32, 19),
    "samurai5": (32, 6),
    "samurai6": (33, 14),
    "samurai7": (40, 46),
}

def load_all_characters():
    samurai1_animations = {
        "IDLE": safe_load_animation('samurai1_idle', 10),
        "RUN": safe_load_animation('samurai1_RUN', 16),
        "ATTACK1": safe_load_animation('samurai1_ATTACK1', 7),
        "ATTACK2": safe_load_animation('samurai1_ATTACK2', 7),
        "ATTACK3": safe_load_animation('samurai1_ATTACK3', 6),
        "DEATH": safe_load_animation('samurai1_DEATH', 9),
        "DEFEND": safe_load_animation('samurai1_DEFEND', 6),
        "HEALING": safe_load_animation('samurai1_HEALING', 15),
        "HURT": safe_load_animation('samurai1_HURT', 4),
        "JUMP": safe_load_animation('samurai1_JUMP', 3),
        "JUMPFALL": safe_load_animation('samurai1_jumpfall', 3),
        "THROW": safe_load_animation('samurai1_THROW', 7),
        "ULTIMATE": safe_load_animation('samurai1_ultimate', 14),
    }
    samurai1 = Character(samurai1_animations, scale=3, offset=offsets["samurai1"])

    samurai2_animations = {
        "IDLE": safe_load_animation('samurai2_IDLE', 5),
        "RUN": safe_load_animation('samurai2_RUN', 7),
        "ATTACK1": safe_load_animation('samurai2_ATTACK1', 5),
        "ATTACK2": safe_load_animation('samurai2_ATTACK2', 5),
        "ATTACK3": safe_load_animation('samurai2_ATTACK3', 10),
        "DEATH": safe_load_animation('samurai2_DEATH', 10),
        "DEFEND": safe_load_animation('samurai2_defend', 6),
        "DUSTEFFECT": safe_load_animation('samurai2_DUSTEFFECT', 4),
        "HURT": safe_load_animation('samurai2_HURT', 3),
        "JUMP": safe_load_animation('samurai2_JUMP', 3),
        "THROW": safe_load_animation('samurai2_THROW', 7),
        "ULTIMATE": safe_load_animation('samurai2_ultimate', 11),
    }
    # Perbaikan bug facing kiri: facing_left=False
    samurai2 = Character(samurai2_animations, scale=3, facing_left=False, offset=offsets["samurai2"])

    samurai3_animations = {
        "IDLE": safe_load_animation('samurai3_IDLE', 14),
        "RUN": safe_load_animation('samurai3_RUN', 8),
        "ATTACK1": safe_load_animation('samurai3_ATTACK1', 5),
        "ATTACK2": safe_load_animation('samurai3_ATTACK2', 5),
        "ATTACK3": safe_load_animation('samurai3_ATTACK3', 5),
        "DEATH": safe_load_animation('samurai3_DEATH', 10),
        "THROW": safe_load_animation('samurai3_THROW', 7),
        "HURT": safe_load_animation('samurai3_HURT', 4),
        "ULTIMATE": safe_load_animation('samurai3_ultimate', 11),
        "JUMP": safe_load_animation('samurai3_JUMP', 3),
    }
    samurai3 = Character(samurai3_animations, scale=3, offset=offsets["samurai3"])

    samurai4_animations = {
        "IDLE": safe_load_animation('samurai4_IDLE', 5),
        "RUN": safe_load_animation('samurai4_RUN', 8),
        "ATTACK1": safe_load_animation('samurai4_ATTACK1', 6),
        "ATTACK2": safe_load_animation('samurai4_ATTACK2', 5),
        "ATTACK3": safe_load_animation('samurai4_ATTACK3', 5),
        "DEATH": safe_load_animation('samurai4_DEATH', 10),
        "HURT": safe_load_animation('samurai4_HURT', 4),
        "JUMP": safe_load_animation('samurai4_JUMP', 3),
        "THROW": safe_load_animation('samurai4_THROW', 7),
    }
    samurai4 = Character(samurai4_animations, scale=3, offset=offsets["samurai4"])

    samurai5_animations = {
        "IDLE": safe_load_animation('samurai5_IDLE', 5),
        "RUN": safe_load_animation('samurai5_RUN', 8),
        "ATTACK1": safe_load_animation('samurai5_ATTACK1', 6),
        "ATTACK2": safe_load_animation('samurai5_ATTACK2', 5),
        "ATTACK3": safe_load_animation('samurai5_ATTACK3', 7),
        "DEATH": safe_load_animation('samurai5_DEATH', 10),
        "HURT": safe_load_animation('samurai5_HURT', 4),
        "JUMP": safe_load_animation('samurai5_JUMP', 3),
    }
    samurai5 = Character(samurai5_animations, scale=3, offset=offsets["samurai5"])

    samurai6_animations = {
        "IDLE": safe_load_animation('samurai6_IDLE', 5),
        "RUN": safe_load_animation('samurai6_RUN', 8),
        "ATTACK1": safe_load_animation('samurai6_ATTACK1', 5),
        "ATTACK2": safe_load_animation('samurai6_ATTACK2', 5),
        "ATTACK3": safe_load_animation('samurai6_ATTACK3', 7),
        "DEATH": safe_load_animation('samurai6_DEATH', 9),
        "HURT": safe_load_animation('samurai6_HURT', 4),
        "JUMP": safe_load_animation('samurai6_JUMP', 3),
    }
    samurai6 = Character(samurai6_animations, scale=3, offset=offsets["samurai6"])

    samurai7_normal = {
        "IDLE": safe_load_animation('samurai7_IDLE', 6),
        "RUN": safe_load_animation('samurai7_RUN', 8),
        "ATTACK1": safe_load_animation('samurai7_ATTACK1', 7),
        "ATTACK2": safe_load_animation('samurai7_ATTACK2', 5),
        "ATTACK3": safe_load_animation('samurai7_ATTACK3', 7),
        "DEATH": safe_load_animation('samurai7_DEATH', 26),
        "HURT": safe_load_animation('samurai7_HURT', 4),
        "JUMP_ATTACK": safe_load_animation('samurai7_JUMP_ATTACK', 12),
        "SHOUT": safe_load_animation('samurai7_SHOUT', 17),
    }

    samurai7_flaming = {
        "IDLE": safe_load_animation('samurai7_idleflaming', 6),
        "RUN": safe_load_animation('samurai7_runflaming', 8),
        "ATTACK1": safe_load_animation('samurai7_attack1flaming', 7),
        "ATTACK2": safe_load_animation('samurai7_attack2flaming', 6),
        "ATTACK3": safe_load_animation('samurai7_attack3flaming', 7),
        "DEATH": safe_load_animation('samurai7_DEATH_flaming', 26),
        "HURT": safe_load_animation('samurai7_hurtflaming', 4),
        "JUMP_ATTACK": safe_load_animation('samurai7_jumpattackflamming', 11),
    }

    samurai7 = TransformingCharacter(samurai7_normal, samurai7_flaming, scale=3, offset=offsets["samurai7"])

    return {
        "samurai1": samurai1,
        "samurai2": samurai2,
        "samurai3": samurai3,
        "samurai4": samurai4,
        "samurai5": samurai5,
        "samurai6": samurai6,
        "samurai7": samurai7,
    }
