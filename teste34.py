import pygame
import random
import math

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
grupo_verde = pygame.sprite.Group()
grupo_vermelho = pygame.sprite.Group()


# Contador de ID global
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

class QuadradoColorido(pygame.sprite.Sprite):
    def __init__(self, x=None, y=None, cor=None, id_personalizado=None):
        super().__init__()
        self.verde = (255, 0, 0)
        self.vermelho = (0, 255, 0)
        self.id = gerar_id() if id_personalizado is None else id_personalizado
        self.cor = random.choice([self.verde, self.vermelho]) if cor is None else cor
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        if self.cor == self.verde:
            pygame.draw.rect(self.image, self.cor, (0, 0, 10, 10), border_radius=12)
        if self.cor == self.vermelho:
             pygame.draw.rect(self.image, self.cor, (0, 0, 20, 20), border_radius=12)

        if x is not None and y is not None:
            self.rect.x = x
            self.rect.y = y
        else:
            self.rect.x = random.randrange(0, 1280 - self.rect.width)
            self.rect.y = random.randrange(0, 720 - self.rect.height)

    def update(self):
        global grupo_cinza, grupo_colorido
        if not grupo_cinza:
            return

        alvo_mais_proximo = min(grupo_cinza, key=lambda alvo: self.distancia_para(alvo))
        dx = alvo_mais_proximo.rect.centerx - self.rect.centerx
        dy = alvo_mais_proximo.rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)
        if distancia > 0:
            dx /= distancia
            dy /= distancia
        if self.cor == self.verde:
            velocidade = 2.5
        if self.cor == self.vermelho:
            velocidade = 2

        move_x = dx * velocidade
        move_y = dy * velocidade

        repulsao_x = 0
        repulsao_y = 0
        repulsao_forca = 1.5
        distancia_minima = 15

        for outro in grupo_colorido:
            if outro == self:
                continue
            dx_o = self.rect.centerx - outro.rect.centerx
            dy_o = self.rect.centery - outro.rect.centery
            dist_o = math.hypot(dx_o, dy_o)
            if dist_o < distancia_minima and dist_o > 0:
                repulsao_x += (dx_o / dist_o) * (distancia_minima - dist_o) * repulsao_forca
                repulsao_y += (dy_o / dist_o) * (distancia_minima - dist_o) * repulsao_forca

        self.rect.x += int(move_x + repulsao_x)
        self.rect.y += int(move_y + repulsao_y)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1280:
            self.rect.right = 1280
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 720:
            self.rect.bottom = 720

    def distancia_para(self, outro):
        dx = outro.rect.centerx - self.rect.centerx
        dy = outro.rect.centery - self.rect.centery
        return math.hypot(dx, dy)

# Criar os sprites iniciais
for _ in range(12):
     cinza = Quadrado()
     colorido = QuadradoColorido()

     grupo_cinza.add(cinza)
     grupo_colorido.add(colorido)
     todos_sprites.add(cinza, colorido)

    # Adicionar o colorido ao grupo correspondente
     if colorido.cor == colorido.verde:
        grupo_verde.add(colorido)
     elif colorido.cor == colorido.vermelho:
        grupo_vermelho.add(colorido)
     todos_sprites.add(cinza, colorido)

# Função para gerar 3 bolas cinzas aleatórias na tela
def gerar_cinco_cinzas_aleatorias():
    for _ in range(5):
        x = random.randint(0, 1280 - 10)
        y = random.randint(0, 720 - 10)
        nova_cinza = Quadrado(x, y)
        grupo_cinza.add(nova_cinza)
        todos_sprites.add(nova_cinza)

# Variável para controlar intervalo de geração
frames_para_proxima_geracao = 0
intervalo_geracao = 60 # gera 3 bolas cinzas a cada 120 frames (~2 segundos a 60fps)

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualiza todos os sprites
    todos_sprites.update()

    # Gera as bolas cinzas aleatórias a cada intervalo
    if frames_para_proxima_geracao <= 0:
        gerar_cinco_cinzas_aleatorias()
        frames_para_proxima_geracao = intervalo_geracao
    else:
        frames_para_proxima_geracao -= 1

    # Verificar colisões entre coloridos e cinzas (continua a lógica original)
    colisao_cinza = pygame.sprite.groupcollide(grupo_colorido, grupo_cinza, False, False)
    colisoes_verde_vermelho = pygame.sprite.groupcollide(grupo_verde, grupo_vermelho, False, True)
    for colorido, cinzas_colididos in colisao_cinza.items():
        for cinza in cinzas_colididos:
            print(f"Colisão entre ID {colorido.id} (colorido) e ID {cinza.id} (cinza)")

            grupo_cinza.remove(cinza)
            todos_sprites.remove(cinza)

            novo_colorido = QuadradoColorido(x=cinza.rect.x, y=cinza.rect.y, cor=colorido.cor, id_personalizado=cinza.id)
            grupo_colorido.add(novo_colorido)
            todos_sprites.add(novo_colorido)
    for verde, vermelhos_comidos in colisoes_verde_vermelho.items():
     for vermelho in vermelhos_comidos:
        print(f"Verde ID {verde.id} comeu vermelho ID {vermelho.id}")
        todos_sprites.remove(vermelho)
        grupo_colorido.remove(vermelho)

    # Desenhar
    screen.fill((0, 0, 0))
    todos_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()