import random
import pygame


contador_id = 0

def gerar_id():
    global contador_id
    contador_id += 1
    return contador_id


class Quadrado(pygame.sprite.Sprite):
    def __init__(self, x=None, y=None):
        super().__init__()
        self.id = gerar_id()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (128, 128, 128), (0, 0, 10, 10), border_radius=12)
        self.rect = self.image.get_rect()
        if x is not None and y is not None:
            self.rect.x = x
            self.rect.y = y
        else:
            self.rect.x = random.randrange(0, 1280 - self.rect.width)
            self.rect.y = random.randrange(0, 720 - self.rect.height)

    def update(self):
        pass
