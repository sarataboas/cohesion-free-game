import pygame

pygame.init()

LARGURA_JANELA = 400
ALTURA_JANELA = 400
TAMANHO_CELULA = 100
LARGURA_TABULEIRO = TAMANHO_CELULA * 4
ALTURA_TABULEIRO = TAMANHO_CELULA * 4

BRANCO = (255, 255, 255)

janela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
pygame.display.set_caption("Cohesion Free Game")


while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

    janela.fill(BRANCO)

    for linha in range(4):
        for coluna in range(4):
            cor = BRANCO

            pygame.draw.rect(janela, cor, (coluna * TAMANHO_CELULA, linha * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

    pygame.display.update()
