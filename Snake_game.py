import pygame
from pygame.locals import *
import random

# Define o tamanho da tela para o jogo e o tamanho do Pixel da cobrinha
tamanho_janela = (600, 600)  # Largura e altura da tela do jogo em pixels
tamanho_pixel = 10          # Tamanho de cada "pixel" da cobrinha e da maçã

# Função para criar colisão no corpo da cobrinha
def collision(pos1, pos2):
    # Verifica se duas posições são iguais
    return pos1 == pos2

# Função para limitar o movimento da cobrinha à tela do jogo
def off_limits(pos):
    # Verifica se a posição está fora dos limites da tela
    return pos[0] < 0 or pos[0] >= tamanho_janela[0] or pos[1] < 0 or pos[1] >= tamanho_janela[1]

# Função para posicionar a maçã de maneira aleatória, mas garantir que ela esteja alinhada com o tamanho do pixel
def random_on_grid():
    # Gera uma posição aleatória alinhada com a grade de pixels
    x = random.randint(0, (tamanho_janela[0] // tamanho_pixel) - 1) * tamanho_pixel
    y = random.randint(0, (tamanho_janela[1] // tamanho_pixel) - 1) * tamanho_pixel
    return x, y

# Cria e inicia o programa para abrir o jogo
pygame.init()  # Inicializa o Pygame
screen = pygame.display.set_mode(tamanho_janela)  # Define o tamanho da tela do jogo
pygame.display.set_caption('Snake Game')  # Define o título da janela

# Elemento que cria a 'cobrinha' do jogo e posiciona ela
snake_pos = [(250, 50), (260, 50), (270, 50)]  # Lista de posições da cobrinha
snake_surface = pygame.Surface((tamanho_pixel, tamanho_pixel))  # Cria a superfície para a cobrinha
snake_surface.fill((255, 255, 255))  # Define a cor da cobrinha (branco)
snake_direction = K_LEFT  # Direção inicial da cobrinha

# Elemento que cria a 'maçã' do jogo e posiciona ela
apple_surface = pygame.Surface((tamanho_pixel, tamanho_pixel))  # Cria a superfície para a maçã
apple_surface.fill((255, 0, 0))  # Define a cor da maçã (vermelho)
apple_pos = random_on_grid()  # Define a posição inicial da maçã

def restart_game():
    global snake_pos, apple_pos, snake_direction
    # Reseta o jogo para o estado inicial
    snake_pos = [(250, 50), (260, 50), (270, 50)]  # Posições iniciais da cobrinha
    snake_direction = K_LEFT  # Direção inicial
    apple_pos = random_on_grid()  # Nova posição da maçã

def is_opposite_direction(direction1, direction2):
    # Verifica se duas direções são opostas
    return (direction1 == K_UP and direction2 == K_DOWN) or \
           (direction1 == K_DOWN and direction2 == K_UP) or \
           (direction1 == K_LEFT and direction2 == K_RIGHT) or \
           (direction1 == K_RIGHT and direction2 == K_LEFT)

while True:
    pygame.time.Clock().tick(10)  # Controla a taxa de quadros por segundo (FPS)
    screen.fill((0, 0, 0))  # Limpa a tela com a cor preta
    
    for event in pygame.event.get():  # Processa eventos
        if event.type == QUIT:  # Se o evento for fechar a janela
            pygame.quit()  # Fecha o Pygame
            quit()  # Encerra o programa
        elif event.type == KEYDOWN:  # Se uma tecla for pressionada
            if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                # Atualiza a direção da cobrinha se a nova direção não for oposta à atual
                if not is_opposite_direction(snake_direction, event.key):
                    snake_direction = event.key
    
    # Desenha a maçã e a cobrinha na tela
    screen.blit(apple_surface, apple_pos)  # Desenha a maçã
    for pos in snake_pos:  # Desenha a cobrinha
        screen.blit(snake_surface, pos)
    
    # Verifica se a cobrinha colidiu com a maçã
    if collision(apple_pos, snake_pos[0]):
        # Adiciona um novo segmento à cobrinha (temporariamente fora da tela)
        snake_pos.append(snake_pos[-1])  # Adiciona um novo segmento na posição do último segmento
        apple_pos = random_on_grid()  # Define uma nova posição para a maçã
    
    # Move a cobrinha
    for i in range(len(snake_pos) - 1, 0, -1):
        # Move cada segmento da cobrinha para a posição do segmento anterior
        snake_pos[i] = snake_pos[i - 1]
    
    # Atualiza a posição da cabeça da cobrinha com base na direção
    if snake_direction == K_UP:
        snake_pos[0] = (snake_pos[0][0], snake_pos[0][1] - tamanho_pixel)
    elif snake_direction == K_DOWN:
        snake_pos[0] = (snake_pos[0][0], snake_pos[0][1] + tamanho_pixel)
    elif snake_direction == K_LEFT:
        snake_pos[0] = (snake_pos[0][0] - tamanho_pixel, snake_pos[0][1])
    elif snake_direction == K_RIGHT:
        snake_pos[0] = (snake_pos[0][0] + tamanho_pixel, snake_pos[0][1])
    
    # Checa se a cobrinha saiu dos limites
    if off_limits(snake_pos[0]):
        restart_game()  # Reinicia o jogo se a cobrinha sair dos limites
    
    # Verifica se a cobrinha colidiu com seu próprio corpo
    if snake_pos[0] in snake_pos[1:]:
        restart_game()  # Reinicia o jogo se a cabeça da cobrinha colidir com seu corpo
    
    pygame.display.update()  # Atualiza a tela com as novas posições