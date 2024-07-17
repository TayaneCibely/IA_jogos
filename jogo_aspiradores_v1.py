import pygame
import random
import math

# Inicializar Pygame
pygame.init()

# Definir as dimensões da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jogo do Aspirador")

# Definir cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Definir o relógio para controlar a taxa de quadros
clock = pygame.time.Clock()

# Inicializar fonte para o relógio
pygame.font.init()
font = pygame.font.Font(None, 36)

# Definir a classe do Aspirador
class Aspirador(pygame.sprite.Sprite):
    def __init__(self, color, start_x, start_y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        self.speed = 5

    def update(self, sujeiras):
        # Encontrar a sujeira mais próxima
        if sujeiras:
            closest_sujeira = min(sujeiras, key=lambda sujeira: self.distance_to(sujeira))

            # Mover na direção da sujeira mais próxima
            if self.rect.x < closest_sujeira.rect.x:
                self.rect.x += self.speed
            elif self.rect.x > closest_sujeira.rect.x:
                self.rect.x -= self.speed

            if self.rect.y < closest_sujeira.rect.y:
                self.rect.y += self.speed
            elif self.rect.y > closest_sujeira.rect.y:
                self.rect.y -= self.speed

        # Manter o aspirador dentro da tela
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

    def distance_to(self, sprite):
        return math.hypot(self.rect.x - sprite.rect.x, self.rect.y - sprite.rect.y)

# Definir a classe da Sujeira
class Sujeira(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(0, screen_height - self.rect.height)

# Criar grupos de sprites
all_sprites = pygame.sprite.Group()
sujeiras = pygame.sprite.Group()

# Criar os aspiradores
aspirador1 = Aspirador(BLACK, screen_width // 4, screen_height // 2)
aspirador2 = Aspirador(BLUE, 3 * screen_width // 4, screen_height // 2)
all_sprites.add(aspirador1)
all_sprites.add(aspirador2)

# Criar sujeiras
for _ in range(20):
    sujeira = Sujeira()
    all_sprites.add(sujeira)
    sujeiras.add(sujeira)

# Função para calcular o tempo de limpeza
def calcular_tempo_de_limpeza():
    tempo_inicio = pygame.time.get_ticks()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        # Atualizar os sprites
        aspirador1.update(sujeiras.sprites())
        aspirador2.update(sujeiras.sprites())

        # Verificar colisões entre os aspiradores e as sujeiras
        pygame.sprite.spritecollide(aspirador1, sujeiras, True)
        pygame.sprite.spritecollide(aspirador2, sujeiras, True)

        # Limpar a tela
        screen.fill(WHITE)

        # Desenhar os sprites
        all_sprites.draw(screen)

        # Calcular o tempo atual
        tempo_atual = (pygame.time.get_ticks() - tempo_inicio) / 1000  # Converter milissegundos para segundos
        texto_tempo = font.render(f"Tempo: {tempo_atual:.2f} segundos", True, BLACK)
        
        # Desenhar o relógio na parte superior da tela
        screen.blit(texto_tempo, (10, 10))

        # Atualizar a tela
        pygame.display.flip()

        # Controlar a taxa de quadros
        clock.tick(30)

        # Verificar se todas as sujeiras foram limpas
        if len(sujeiras) == 0:
            running = False

    tempo_fim = pygame.time.get_ticks()
    tempo_total = (tempo_fim - tempo_inicio) / 1000  # Converter milissegundos para segundos
    print(f"Tempo total para limpar a tela: {tempo_total:.2f} segundos")

# Chamar a função para iniciar o jogo e calcular o tempo de limpeza
calcular_tempo_de_limpeza()

pygame.quit()

