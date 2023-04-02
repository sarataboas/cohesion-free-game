import pygame

# Define as cores utilizadas no jogo
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Inicializa o pygame
pygame.init()

# Define as dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Define o título da janela
pygame.display.set_caption("Meu jogo")

# Define a fonte utilizada no menu
font = pygame.font.SysFont("Arial", 32)

# Define as opções do menu
menu_options = [
    "Jogar",
    "Opções",
    "Créditos",
    "Sair"
]

# Define a posição inicial do menu
menu_x = SCREEN_WIDTH // 2 - 100
menu_y = SCREEN_HEIGHT // 2 - 50

# Loop principal do jogo
running = True
while running:
    # Eventos do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Desenha o menu na tela
    screen.fill(WHITE)
    for i, option in enumerate(menu_options):
        text = font.render(option, True, BLACK)
        text_rect = text.get_rect()
        text_rect.centerx = menu_x
        text_rect.centery = menu_y + i * 50
        screen.blit(text, text_rect)

    # Atualiza a tela
    pygame.display.flip()

# Finaliza o pygame
pygame.quit()
