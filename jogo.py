import random

import pygame

pygame.init()

largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo de Reciclagem")

# Cores
cor_fundo_menu = (50, 168, 82)
cor_texto = (255, 255, 255)

# Carregar fundo
fundo = pygame.image.load('imagens/fundo.jpg').convert()
fundo = pygame.transform.scale(fundo, (largura, altura))

# Lista de caminhos para imagens
imagens_reciclaveis = [
    'imagens/caixa.png', 'imagens/garrafa.png', 'imagens/garrafag.png',
    'imagens/lata.png', 'imagens/papel.png'
]

imagens_nao_reciclaveis = [
    'imagens/banana.png', 'imagens/bolo.png', 'imagens/cenoura.png',
    'imagens/maca.png', 'imagens/carne.png'
]

# Sons
som_coleta = pygame.mixer.Sound('musicas/coletaPontos.mp3')
som_erro = pygame.mixer.Sound('musicas/erro.mp3')
pygame.mixer.music.load('musicas/musicaFundo.mp3')
pygame.mixer.music.set_volume(0.5)


# Função para carregar uma imagem aleatória
def carregar_imagem_aleatoria(lista_imagens):
    caminho_imagem = random.choice(lista_imagens)
    imagem = pygame.image.load(caminho_imagem).convert_alpha()
    return imagem


# Classe para o lixo
class Lixo(pygame.sprite.Sprite):

    def _init_(self, imagem, largura, altura, velocidade_y, tipo):
        super()._init_()
        self.image = pygame.transform.scale(imagem, (largura, altura))
        self.rect = self.image.get_rect()
        self.velocidade_y = velocidade_y
        self.tipo = tipo  # Define o tipo (reciclável ou não reciclável)

    def update(self, *args, **kwargs):
        self.rect.y += self.velocidade_y


# Classe para o personagem
class Personagem(pygame.sprite.Sprite):

    def _init_(self, imagem):
        super()._init_()
        self.image = imagem  # Imagem do personagem
        self.rect = self.image.get_rect()  # Define a colisão
        self.rect.centerx = largura // 2
        self.rect.bottom = altura - 5  # Posição ajustada para não cortar o personagem
        self.velocidade = 5

    def update(self, *args, **kwargs):
        # Movimento
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidade

        # Limitar movimento
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > largura:
            self.rect.right = largura


# Função para exibir o menu
def mostrar_menu():
    menu_ativo = True
    while menu_ativo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    menu_ativo = False

        tela.fill(cor_fundo_menu)

        fonte = pygame.font.Font(None, 36)
        texto1 = fonte.render("Bem-vindo ao Jogo de Reciclagem", True,
                              cor_texto)
        texto2 = fonte.render("Pressione ESPAÇO para começar", True, cor_texto)
        texto3 = fonte.render(
            "Use as setas para a esquerda e direita para mover", True,
            cor_texto)
        texto4 = fonte.render("Colete apenas itens recicláveis", True,
                              cor_texto)
        texto5 = fonte.render("Uma produção: Bruna e Naeli", True,
                              (200, 200, 200))

        tela.blit(texto1, (100, 100))
        tela.blit(texto2, (100, 200))
        tela.blit(texto3, (100, 300))
        tela.blit(texto4, (100, 400))
        tela.blit(texto5, (100, 500))

        pygame.display.flip()


# Função principal
def main():
    mostrar_menu()

    jogo_ativo = True
    relogio = pygame.time.Clock()

    itens_reciclaveis = pygame.sprite.Group()
    todos_itens = pygame.sprite.Group()

    # Carregar o personagem
    personagem_imagem = pygame.image.load(
        'imagens/personagem.png').convert_alpha()
    largura_personagem, altura_personagem = 100, 100
    personagem_imagem = pygame.transform.scale(
        personagem_imagem, (largura_personagem, altura_personagem))
    personagem = Personagem(personagem_imagem)
    todos_itens.add(personagem)

    pontuacao = 0

    pygame.mixer.music.play(-1)

    tempo_jogo = 120
    contador_tempo = pygame.time.get_ticks() + tempo_jogo * 1000

    while jogo_ativo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogo_ativo = False

        if pygame.time.get_ticks() >= contador_tempo:
            jogo_ativo = False

        if random.randint(1, 100) == 1:
            tipo = random.choice(['reciclavel', 'nao_reciclavel'])
            if tipo == 'reciclavel':
                imagem_reciclavel = carregar_imagem_aleatoria(
                    imagens_reciclaveis)
                novo_item = Lixo(imagem_reciclavel, largura_personagem,
                                 altura_personagem, 5, 'reciclavel')
            else:
                imagem_nao_reciclavel = carregar_imagem_aleatoria(
                    imagens_nao_reciclaveis)
                novo_item = Lixo(imagem_nao_reciclavel, largura_personagem,
                                 altura_personagem, 5, 'nao_reciclavel')

            novo_item.rect.x = random.randrange(largura - largura_personagem)
            novo_item.rect.y = -altura_personagem

            itens_reciclaveis.add(novo_item)
            todos_itens.add(novo_item)

        colisoes = pygame.sprite.spritecollide(personagem, itens_reciclaveis,
                                               True)
        for item in colisoes:
            if item.tipo == 'reciclavel':
                som_coleta.play()
                pontuacao += 1
            elif item.tipo == 'nao_reciclavel':
                som_erro.play()

        todos_itens.update()

        tela.blit(fundo, (0, 0))

        todos_itens.draw(tela)

        fonte = pygame.font.Font(None, 36)
        texto_pontuacao = fonte.render(f'Pontuação: {pontuacao}', True,
                                       cor_texto)
        tela.blit(texto_pontuacao, (10, 10))

        segundos_restantes = max(
            (contador_tempo - pygame.time.get_ticks()) // 1000, 0)
        texto_tempo = fonte.render(f'Tempo restante: {segundos_restantes} s',
                                   True, cor_texto)
        tela.blit(texto_tempo, (largura - 300, 10))

        pygame.display.flip()

        relogio.tick(60)

    tela.fill(cor_fundo_menu)
    fonte_final = pygame.font.Font(None, 48)
    texto_final = fonte_final.render(f'Pontuação Final: {pontuacao}', True,
                                     cor_texto)
    tela.blit(texto_final, (largura // 2 - 200, altura // 2 - 50))
    pygame.display.flip()

    pygame.time.wait(3000)

    pygame.mixer.music.stop()
    pygame.mixer.quit()
    pygame.quit()


if _name_ == "_main_":
    main()