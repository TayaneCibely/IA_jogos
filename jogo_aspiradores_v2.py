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

# Definir a grade para rastrear as posições visitadas
grid_size = 10
cols = screen_width // grid_size
rows = screen_height // grid_size
visit_count = [[0 for _ in range(cols)] for _ in range(rows)]

# Definir a classe do Aspirador Baseado em Objetivos (Preto)
class AspiradorObjetivo(pygame.sprite.Sprite):
    def __init__(self, color, start_x, start_y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        self.speed = 5

    def update(self, sujeiras, outros_aspiradores):
        # Mover em direção à sujeira mais próxima
        if sujeiras:
            closest_sujeira = min(sujeiras, key=lambda sujeira: self.distance_to(sujeira))
            self.move_towards(closest_sujeira)

        # Manter o aspirador dentro da tela
        self.keep_within_bounds()

    def move_towards(self, target):
        if self.rect.x < target.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > target.rect.x:
            self.rect.x -= self.speed

        if self.rect.y < target.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > target.rect.y:
            self.rect.y -= self.speed

    def keep_within_bounds(self):
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

# Definir a classe do Aspirador Reativo Baseado em Modelos (Azul)
class AspiradorReativo(pygame.sprite.Sprite):
    def __init__(self, color, start_x, start_y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        self.speed = 5
        self.direction = random.choice(["up", "down", "left", "right"])

    def update(self, sujeiras, outros_aspiradores):
        # Mover em direção aleatória
        self.move_randomly()

        # Manter o aspirador dentro da tela
        self.keep_within_bounds()

        # Evitar colisão com outros aspiradores
        self.avoid_collision(outros_aspiradores)

        # Atualizar a grade de visitas
        self.update_visit_count()

    def move_randomly(self):
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

        # Mudar direção aleatoriamente para evitar posições frequentemente visitadas
        if random.random() < 0.05 or self.should_change_direction():
            self.direction = self.choose_new_direction()

    def keep_within_bounds(self):
        if self.rect.right > screen_width:
            self.rect.right = screen_width
            self.direction = random.choice(["up", "down", "left"])
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction = random.choice(["up", "down", "right"])
        if self.rect.top < 0:
            self.rect.top = 0
            self.direction = random.choice(["down", "left", "right"])
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.direction = random.choice(["up", "left", "right"])

    def distance_to(self, sprite):
        return math.hypot(self.rect.x - sprite.rect.x, self.rect.y - sprite.rect.y)

    def avoid_collision(self, outros_aspiradores):
        for outro in outros_aspiradores:
            if self != outro and self.distance_to(outro) < 60:  # Verifica se a distância é menor que 60
                # Resolver a colisão movendo o aspirador para uma direção alternativa
                self.direction = random.choice(["up", "down", "left", "right"])

    def update_visit_count(self):
        col = self.rect.x // grid_size
        row = self.rect.y // grid_size
        visit_count[row][col] += 1

    def should_change_direction(self):
        col = self.rect.x // grid_size
        row = self.rect.y // grid_size
        return visit_count[row][col] > 5  # Mudar de direção se a posição foi visitada mais de 5 vezes

    def choose_new_direction(self):
        current_col = self.rect.x // grid_size
        current_row = self.rect.y // grid_size
        directions = ["up", "down", "left", "right"]
        best_direction = self.direction
        min_visits = visit_count[current_row][current_col]

        for direction in directions:
            new_col = current_col
            new_row = current_row
            if direction == "up" and current_row > 0:
                new_row -= 1
            elif direction == "down" and current_row < rows - 1:
                new_row += 1
            elif direction == "left" and current_col > 0:
                new_col -= 1
            elif direction == "right" and current_col < cols - 1:
                new_col += 1

            if visit_count[new_row][new_col] < min_visits:
                min_visits = visit_count[new_row][new_col]
                best_direction = direction

        return best_direction

# Definir a classe da Sujeira
class Sujeira(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(0, screen_height - self.rect.height)

def criar_aspiradores():
    aspirador1 = AspiradorObjetivo(BLACK, screen_width // 4, screen_height // 2)
    while True:
        aspirador2 = AspiradorReativo(BLUE, random.randint(0, screen_width - 50), random.randint(0, screen_height - 50))
        if not pygame.sprite.collide_rect(aspirador1, aspirador2):
            break
    return aspirador1, aspirador2

# Criar grupos de sprites
all_sprites = pygame.sprite.Group()
sujeiras = pygame.sprite.Group()

# Criar os aspiradores
aspirador1, aspirador2 = criar_aspiradores()
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
        aspirador1.update(sujeiras.sprites(), [aspirador2])
        aspirador2.update(sujeiras.sprites(), [aspirador1])

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
