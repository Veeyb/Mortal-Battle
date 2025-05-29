import pygame

class Entity:
    def __init__(self, x, y, width, height, health=100):
        self.rect = pygame.Rect(x, y, width, height)
        self.health = health
        self.alive = True
        self.speed = 5

        self.action = "IDLE"
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def move(self, dx, dy, screen_width=None, screen_height=None):
        if not self.alive:
            return

        self.rect.x += dx
        self.rect.y += dy

        # Jika batas layar diberikan, batasi posisi entity agar tidak keluar layar
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

    def attack(self, target):
        # Default attack method, override di subclass
        pass

    def on_death(self):
        # Hook method, override di subclass untuk aksi saat mati
        pass

    def on_hurt(self):
        # Hook method, override di subclass untuk aksi saat kena damage
        pass

    def update(self):
        # Update umum (misal animasi), override di subclass
        pass

    def draw(self, surface):
        # Draw umum (misal debug hitbox), override di subclass
        pass
