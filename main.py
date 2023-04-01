import pygame

pygame.init()

largura_janela = 400
altura_janela = 400
tamanho_celula = 100
largura_tabuleiro = tamanho_celula * 4
altura_tabuleiro = tamanho_celula * 4

branco = (255, 255, 255)

janela = pygame.display.set_mode((largura_janela, altura_janela))
pygame.display.set_caption("Cohesion Free Game")


while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

    janela.fill(branco)

    for linha in range(4):
        for coluna in range(4):
            cor = branco

            pygame.draw.rect(janela, cor, (coluna * tamanho_celula, linha * tamanho_celula, tamanho_celula, tamanho_celula))

    pygame.display.update()

