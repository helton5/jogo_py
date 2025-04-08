# https://www.pygame.org/docs/tut/newbieguide.html

import pygame

import random

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((1280,720))

clock = pygame.time.Clock()

raio = 12
qtda_bolas = 0

class Bola:
    def __init__(self,screen):
        self.x = random.randrange(0,1280)
        self.y = random.randrange(0,720)
        self.screen = screen
        self.raio = 12
        self.color = (128,128,128)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.raio)

class Bola_Colorida(Bola):
    def __init__(self, screen):
        super().__init__(screen)
        self.velocidadeX = 2
        self.velocidadeY = 2
        self.color = random.choice([(255, 0, 0), (0, 255, 0)])

    def move(self):
        self.x += self.velocidadeX
        self.y += self.velocidadeY
    



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        
    while qtda_bolas <= raio:
        qtda_bolas += 1
        o1 = Bola_Colorida(screen)
        o = Bola(screen)
        o.draw()
        o1.draw()
        break
    o1.move()




    # Render the graphics here.
    # ...

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPSww