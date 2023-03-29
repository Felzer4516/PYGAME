import math
import random 
import pygame
from pygame import mixer


pygame.init()

# Cria a janela 
screen = pygame.display.set_mode((800,600))

# Fundo
background = pygame.image.load('background.png')

# Musica
mixer.music.load("background.wav")
mixer.music.play(-1)

# Definir as constantes
WIDTH = 400
HEIGHT = 300
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT_SIZE = 50
TEXT_MARGIN = 10

# Definir as variáveis de tempo
start_ticks = 0
elapsed_time = 0

pontucao = 0 
clock = pygame.time.Clock()
# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480  #altura do player
playerX_change = 0

# inimigo
inimigoImg = []
inimigoX = []
inimigoY = []
inimigoX_change = []
inimigoY_change = []
num_of_inimigos = 6 

#Loop do numero de inimigos 
for i in range(num_of_inimigos):
    inimigoImg.append(pygame.image.load('inimigo.png'))
    inimigoX.append(random.randint(0, 736))
    inimigoY.append(random.randint(50, 150))
    inimigoX_change.append(4) #adiciona elementos 
    inimigoY_change.append(40)

# bala

# Ready - Você não pode ver a bala no ecra
# Fogo- A bala está se mexendo 

balaImg = pygame.image.load('bala.png')
balaX = 0
balaY = 480
balaX_change = 0
balaY_change = 10
bala_estado = "ready"

# Score

score_valor = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10



def format_time(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    return "{:02d}:{:02d}.{:03d}".format(minutes, seconds, milliseconds)
    

def show_score(x, y): #(x e y) exibe a pontuação na tela.
    score = font.render("Score : " + str(score_valor), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y): #mostra o player na tela em uma determinada posicao
    screen.blit(playerImg, (x, y))


def inimigo(x, y, i): #mostra o inimigo na tela em uma determinada posicao
    screen.blit(inimigoImg[i], (x, y))


def fire_bala(x, y):
    global bala_estado 
    bala_estado = "fire" # variavel global "bala_estado" é definida como "fire" a dizer que esta em movimento 
    screen.blit(balaImg, (x + 16, y + 10))


def isCollision(inimigoX, inimigoY, balaX, balaY): #Ve se há uma colisão entre um inimigo e uma bala
    distance = math.sqrt(math.pow(inimigoX - balaX, 2) + (math.pow(inimigoY - balaY, 2))) #A função usa a fórmula da distance entre dois pontos em um plano cartesiano para calcular a distância entre o inimigo e a bala. O resultado é armazenado na variável "distance".
    if distance < 27: #Se a distância calculada for menor que 27
        return True # a função retorna "True" para indicar que houve uma colisão.
    else:
        return False #Caso contrario da false


# Game Loop
running = True #A correr e igual a verdadeiro
while running: #Enquanto corre

    if start_ticks == 0:
        start_ticks = pygame.time.get_ticks()
    else:
        elapsed_time = pygame.time.get_ticks() - start_ticks

    # RGB = Vermelho, Verde, Azul
    screen.fill((0, 0, 0))
    # Imagem de Fundo
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # se o pressionamento de tecla for pressionado, verifica se está à direita ou à esquerda
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bala_estado is "ready":
                    # Obtem a coordenada x atual onde se dispara
                    balaX = playerX
                    fire_bala(balaX, balaY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
        
    font = pygame.font.Font('freesansbold.ttf', 32)
    time_text = font.render(format_time(elapsed_time), True, (255, 255, 255))
    text_x = WIDTH - time_text.get_width() - TEXT_MARGIN #"WIDTH" armazena a largura da tela e "TEXT_MARGIN" é uma constante que representa a margem que será aplicada nas bordas do texto.
    text_y = TEXT_MARGIN
    screen.blit(time_text, (text_x, text_y))
    
    
   

    playerX += playerX_change #A variavel player x guarda a posicao atual do jogador no eixo horizontal e que a variável "playerX_change" armazena a quantidade de mudança de posição horizontal a ser aplicada ao jogador.
    if playerX <= 0: #Se a posição horizontal do jogador for menor ou igual a 0, ela é definida como 0 para que o jogador não se mova para fora da borda esquerda da tela.
        playerX = 0
    elif playerX >= 736: #Se a posição horizontal do jogador for maior ou igual a 736, ela será definida como 736 para que o jogador não se mova para fora da borda direita da tela.
        playerX = 736

    # inimigo em movimento
    for i in range(num_of_inimigos):

        # Game Over
        if inimigoY[i] > 440: # Se o inimigo 
            for j in range(num_of_inimigos):
                inimigoY[j] = 2000
                pygame.quit()
 #Move os inimigos no ecra fazendo com que eles se mexam e alterem a posicao y quando chegar ao fim do ecra
        inimigoX[i] += inimigoX_change[i]
        if inimigoX[i] <= 0:
            inimigoX_change[i] = 4
            inimigoY[i] += inimigoY_change[i]
        elif inimigoX[i] >= 736: #esta vendo se e maior ou igual que 736 pixeis se for a cordenada x tiver ele atualiza a coordenada y
            inimigoX_change[i] = -4
            inimigoY[i] += inimigoY_change[i]

        # Colisoes
        #verifica se houve uma colisão entre uma bala e um inimigo 
        collision = isCollision(inimigoX[i], inimigoY[i], balaX, balaY) 
        if collision:
            balaY = 480 #Faz com que a bala sai da tela porque 480 e uma area fora dos limite
            bala_estado = "ready"
            score_valor += 1 #Se bater conta mais 1 
            inimigoX[i] = random.randint(0, 736) #da spawn em posicoes aleatorias
            inimigoY[i] = random.randint(50, 150)

        inimigo(inimigoX[i], inimigoY[i], i)

    # bala em movimento 
    if balaY <= 0:
        balaY = 480
        bala_estado = "ready"

    if bala_estado is "fire":
        fire_bala(balaX, balaY)
        balaY -= balaY_change #velocidade  na vertical da bala

    player(playerX, playerY)
    show_score(textX, testY)
    
    pygame.display.update()

    print ("pontuacao =",score_valor)
    print ("Tempo =",elapsed_time)
    


