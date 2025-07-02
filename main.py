import pygame
import random
import time
from quadrado import *
from quadrado_colorido import *


# Inicializações
pygame.init()
pygame.font.init()

# Tela e relógio
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()




def carregar_configuracoes():
    with open("conf.txt", "r") as f:
        linha1 = f.readline().strip()
        quantidade = int(linha1.split(":")[1].strip())

        return quantidade

for cor in cores_balanceadas:
    velocidade_def = carregar_configuracoes()
    cinza = Quadrado()
    colorido = QuadradoColorido(cor=cor)

    grupo_cinza.add(cinza)
    grupo_colorido.add(colorido)
    todos_sprites.add(cinza, colorido)

    if cor == (0, 255, 0):
        grupo_verde.add(colorido)
    elif cor == (255, 0, 0):
        grupo_vermelho.add(colorido)
    elif cor == (255, 255, 0):
        grupo_amarelo.add(colorido)



# Função para gerar 3 bolas cinzas aleatórias na tela
def gerar_cinzas_aleatorias():
    with open("conf.txt", "r") as f:
               linha = f.readline().strip()
               linha2 = f.readline().strip()
               velocidade_def = int(linha2.split(":")[1].strip())
               quantidade = int(linha.split(":")[1].strip())
    for _ in range(quantidade):
        x = random.randint(0, 1280 - 10)
        y = random.randint(0, 720 - 10)
        nova_cinza = Quadrado(x, y)
        grupo_cinza.add(nova_cinza)
        todos_sprites.add(nova_cinza)

def todos_no_grupo():
        if len(grupo_colorido) == len(grupo_verde):
            tempo = time.time() 
            with open("controle.txt", "a") as arquivo:
                arquivo.write(f"Verde ganhou em um tempo de: {tempo:.2f} segundos\n")
                pygame.quit

        elif len(grupo_colorido) == len(grupo_vermelho):
            tempo = time.time() 
            with open("controle.txt", "a") as arquivo:
                arquivo.write(f"Vermelho ganhou em um tempo de: {tempo:.2f} segundos\n")
                pygame.quit

        
        elif len(grupo_colorido) == len(grupo_amarelo):
            tempo = time.time() 
            with open("controle.txt", "a") as arquivo:
                arquivo.write(f"Amarelo ganhou em um tempo de: {tempo:.2f} segundos\n")
                pygame.quit

# Variável para controlar intervalo de geração
with open("conf.txt", "r") as f:
    f.readline()
    f.readline()
    linha3 = f.readline().strip()
frames_para_proxima_geracao = 0
intervalo_geracao = int(linha3.split(":")[1].strip()) # gera 3 bolas cinzas a cada 120 frames (~2 segundos a 60fps)

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualiza todos os sprites
    todos_sprites.update()


    todos_no_grupo()
    # Gera as bolas cinzas aleatórias a cada intervalo
    if frames_para_proxima_geracao <= 0:
        gerar_cinzas_aleatorias()
        frames_para_proxima_geracao = intervalo_geracao
    else:
        frames_para_proxima_geracao -= 1

    # Verificar colisões entre coloridos e cinzas (continua a lógica original)
    colisao_cinza = pygame.sprite.groupcollide(grupo_colorido, grupo_cinza, False, False)

    for colorido, cinzas_colididos in colisao_cinza.items():
        for cinza in cinzas_colididos:
            print(f"Colisão entre ID {colorido.id} (colorido) e ID {cinza.id} (cinza)")

            grupo_cinza.remove(cinza)
            todos_sprites.remove(cinza)

            novo_colorido = QuadradoColorido(x=cinza.rect.x, y=cinza.rect.y, cor=colorido.cor, id_personalizado=cinza.id)
            grupo_colorido.add(novo_colorido)
            todos_sprites.add(novo_colorido)

            if colorido.cor == colorido.verde:
                grupo_verde.add(novo_colorido)
            elif colorido.cor == colorido.vermelho:
                grupo_vermelho.add(novo_colorido)
            elif colorido.cor == colorido.amarelo:
                grupo_amarelo.add(novo_colorido)

       # Verde come Vermelho
    colisao_verde_vermelho = pygame.sprite.groupcollide(grupo_verde, grupo_vermelho, False, False)
    for verde, vermelhos_colididos in colisao_verde_vermelho.items():
        for vermelho in vermelhos_colididos:
            print(f"Verde ID {verde.id} comeu vermelho ID {vermelho.id}")
            grupo_vermelho.remove(vermelho)
            grupo_colorido.remove(vermelho)
            todos_sprites.remove(vermelho)

            novo_verde = QuadradoColorido(x=vermelho.rect.x, y=vermelho.rect.y, cor=verde.cor, id_personalizado=vermelho.id)
            grupo_verde.add(novo_verde)
            grupo_colorido.add(novo_verde)
            todos_sprites.add(novo_verde)

    # Vermelho come Amarelo
    colisao_vermelho_amarelo = pygame.sprite.groupcollide(grupo_vermelho, grupo_amarelo, False, False)
    for vermelho, amarelos_colididos in colisao_vermelho_amarelo.items():
        for amarelo in amarelos_colididos:
            print(f"Vermelho ID {vermelho.id} comeu Amarelo ID {amarelo.id}")
            grupo_amarelo.remove(amarelo)
            grupo_colorido.remove(amarelo)
            todos_sprites.remove(amarelo)

            novo_vermelho = QuadradoColorido(x=amarelo.rect.x, y=amarelo.rect.y, cor=vermelho.cor, id_personalizado=amarelo.id)
            grupo_vermelho.add(novo_vermelho)
            grupo_colorido.add(novo_vermelho)
            todos_sprites.add(novo_vermelho)

    # Amarelo come Verde
    colisao_amarelo_verde = pygame.sprite.groupcollide(grupo_amarelo, grupo_verde, False, False)
    for amarelo, verdes_colididos in colisao_amarelo_verde.items():
        for verde in verdes_colididos:
            print(f"Amarelo ID {amarelo.id} comeu Verde ID {verde.id}")
            grupo_verde.remove(verde)
            grupo_colorido.remove(verde)
            todos_sprites.remove(verde)

            novo_amarelo = QuadradoColorido(x=verde.rect.x, y=verde.rect.y, cor=amarelo.cor, id_personalizado=verde.id)
            grupo_amarelo.add(novo_amarelo)
            grupo_colorido.add(novo_amarelo)
            todos_sprites.add(novo_amarelo)
            
    def todos_no_grupo():
        if len(grupo_colorido) == len(grupo_verde):
            tempo_em_milisegundos = pygame.time.get_ticks()
            tempo_em_segundos = tempo_em_milisegundos / 1000
            with open("controle.txt", "a") as arquivo:
                arquivo.write(f"Verde ganhou em um tempo de: {tempo_em_segundos:.2f} segundos\n")
                pygame.quit()

        elif len(grupo_colorido) == len(grupo_vermelho):
            tempo_em_milisegundos = pygame.time.get_ticks()
            tempo_em_segundos = tempo_em_milisegundos / 1000
            with open("controle.txt", "a") as arquivo:
                arquivo.write(f"Vermelho ganhou em um tempo de: {tempo_em_segundos:.2f} segundos\n")
                pygame.quit()

        
        elif len(grupo_colorido) == len(grupo_amarelo):
            tempo_em_milisegundos = pygame.time.get_ticks()
            tempo_em_segundos = tempo_em_milisegundos / 1000
            with open("controle.txt", "a") as arquivo:
                arquivo.write(f"Amarelo ganhou em um tempo de: {tempo_em_segundos:.2f} segundos\n")
                pygame.quit()







    # Desenhar
    screen.fill((0, 0, 0))
    todos_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()