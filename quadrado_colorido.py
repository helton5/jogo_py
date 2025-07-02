import pygame
import random
import math
from quadrado import *


# Grupos de sprites
todos_sprites = pygame.sprite.Group()
grupo_cinza = pygame.sprite.Group()
grupo_colorido = pygame.sprite.Group()
grupo_verde = pygame.sprite.Group()
grupo_vermelho = pygame.sprite.Group()
grupo_amarelo = pygame.sprite.Group()


class QuadradoColorido(pygame.sprite.Sprite):
    def __init__(self, x=None, y=None, cor=None, id_personalizado=None):
        super().__init__()
        self.vermelho = (255, 0, 0)
        self.verde = (0, 255, 0)
        self.amarelo = (255, 255, 0)
        self.id = gerar_id() if id_personalizado is None else id_personalizado
        self.cor = random.choice([self.verde, self.vermelho, self.amarelo]) if cor is None else cor
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.idade = 0
        self.max_idade = 600
        self.tamanho = random.randrange(0,20)
        if self.cor == self.verde:
            pygame.draw.rect(self.image, self.cor, (0, 0, self.tamanho, self.tamanho), border_radius=12)
            
        if self.cor == self.vermelho:
             pygame.draw.rect(self.image, self.cor, (0, 0, self.tamanho, self.tamanho), border_radius=12)
        
        if self.cor == self.amarelo:
            pygame.draw.rect(self.image, self.cor, (0, 0, self.tamanho, self.tamanho), border_radius=12)

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
        with open("conf.txt", "r") as f:
            f.readline()
            linha2 = f.readline().strip()
            velocidade = int(linha2.split(":")[1].strip())
        if distancia > 0:
            dx /= distancia
            dy /= distancia

        move_x = dx * velocidade
        move_y = dy * velocidade

        repulsao_x = 0
        repulsao_y = 0
        repulsao_forca = 1.5
        distancia_minima = 15

        # Atualiza idade
        self.idade += 1
        if self.idade >= self.max_idade:
            print(f"Bola ID {self.id} morreu de velhice")

            # Remover do jogo
            grupo_colorido.remove(self)
            todos_sprites.remove(self)

            if self.cor == self.verde:
                grupo_verde.remove(self)
            elif self.cor == self.vermelho:
                grupo_vermelho.remove(self)
            elif self.cor == self.amarelo:
                grupo_amarelo.remove(self)

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
cores_balanceadas = [ (0,255,0) ] * 4 + [ (255,0,0) ] * 4 + [ (255,255,0) ] * 4
random.shuffle(cores_balanceadas)