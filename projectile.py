import pygame
from assets import get_image

class ShurikenProjectile:
    def __init__(self, x, y, direction, speed=15):
        self.image = get_image('shuriken')
        self.x = x
        self.y = y
        self.direction = direction  # 1 atau -1
        self.speed = speed
        self.rect = self.image.get_rect(center=(x, y))
        self.active = True

    def update(self):
        self.x += self.speed * self.direction
        self.rect.x = int(self.x)
        # Nonaktifkan projectile jika keluar layar (misal 0 sampai 1000 width)
        if self.x < 0 or self.x > 1000:
            self.active = False

    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.direction < 0, False)
        surface.blit(flipped_image, self.rect)
