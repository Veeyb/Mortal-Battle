import pygame
from entity import Entity

class Fighter(Entity):
    def __init__(self, x, y, width=80, height=180, health=100, flip=False, char_key=None, character=None):
        super().__init__(x, y, width, height, health)
        self.flip = flip
        self.char_key = char_key
        self.character = character  # objek Character atau TransformingCharacter

        self.speed = 5
        self.velocity_y = 0
        self.gravity = 1

        self.action = "IDLE"
        self.frame_index = 0

        self.is_jumping = False
        self.alive = True

        # Status serangan dasar, tapi logic spesifik duel dipindah ke DuelFighter
        self.is_attacking = False
        self.is_throwing = False
        self.is_ultimate = False

        self.target = None  # target opponent, dipakai di duel

        self.projectiles = []

        self.direction = -1 if self.flip else 1

        self.last_action_time = 0

    def move(self, dx, dy, screen_width=None, screen_height=None):
        if not self.alive:
            return

        self.rect.x += dx
        self.rect.y += dy

        # Batasi di layar jika ada
        if screen_width is not None:
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > screen_width:
                self.rect.right = screen_width
        if screen_height is not None:
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > screen_height:
                self.rect.bottom = screen_height

    def take_damage(self, amount):
        if not self.alive:
            return

        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.on_death()
        else:
            self.on_hurt()

    def on_death(self):
        pass  # bisa di-override

    def on_hurt(self):
        pass  # bisa di-override

    def update(self):
        # Update animasi karakter jika ada
        if self.character:
            self.character.update()

    def draw(self, screen):
        if self.character:
            self.character.draw(screen, self.rect.x, self.rect.y)
