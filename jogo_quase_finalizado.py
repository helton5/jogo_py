import pygame
import random

# Inicializações
pygame.init()
pygame.font.init()

# Tela e relógio
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

# Grupos de sprites
todos_sprites = pygame.sprite.Group()
grupo_cinza = pygame.sprite.Group()
grupo_colorido = pygame.sprite.Group()

# Contador de ID global
contador_id = 0

def gerar_id():
    global contador_id
    contador_id += 1
    return contador_id

# Classes
class Quadrado(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.id = gerar_id()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (128, 128, 128), (0, 0, 10, 10), border_radius=12)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, 1280 - self.rect.width)
        self.rect.y = random.randrange(0, 720 - self.rect.height)

    def update(self):
        pass

class QuadradoColorido(pygame.sprite.Sprite):
    def __init__(self, x=None, y=None, cor=None, id_personalizado=None):
        super().__init__()
        self.id = gerar_id() if id_personalizado is None else id_personalizado
        self.cor = random.choice([(255, 0, 0), (0, 255, 0)]) if cor is None else cor
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.cor, (0, 0, 10, 10), border_radius=12)
        self.rect = self.image.get_rect()

        if x is not None and y is not None:
            self.rect.x = x
            self.rect.y = y
        else:
            self.rect.x = random.randrange(0, 1280 - self.rect.width)
            self.rect.y = random.randrange(0, 720 - self.rect.height)

        self.velocidadeX = random.choice([-1, 2])
        self.velocidadeY = random.choice([-1, 2])

    def update(self):
        self.rect.x += self.velocidadeX
        self.rect.y += self.velocidadeY

        # Rebater nas bordas
        if self.rect.left <= 0 or self.rect.right >= 1280:
            self.velocidadeX *= -1
        if self.rect.top <= 0 or self.rect.bottom >= 720:
            self.velocidadeY *= -1

# Criar os sprites
for _ in range(12):
    cinza = Quadrado()
    colorido = QuadradoColorido()

    grupo_cinza.add(cinza)
    grupo_colorido.add(colorido)
    todos_sprites.add(cinza, colorido)

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualiza todos os sprites
    todos_sprites.update()

    # Verificar colisões entre coloridos e cinzas
    colisoes = pygame.sprite.groupcollide(grupo_colorido, grupo_cinza, False, False)
    for colorido, cinzas_colididos in colisoes.items():
        for cinza in cinzas_colididos:
            print(f"Colisão entre ID {colorido.id} (colorido) e ID {cinza.id} (cinza)")

            # Remover o cinza e criar um novo colorido com a mesma posição e ID
            grupo_cinza.remove(cinza)
            todos_sprites.remove(cinza)

            novo_colorido = QuadradoColorido(x=cinza.rect.x, y=cinza.rect.y, cor=colorido.cor, id_personalizado=cinza.id)
            grupo_colorido.add(novo_colorido)
            todos_sprites.add(novo_colorido)

    # Desenhar
    screen.fill((0, 0, 0))
    todos_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

