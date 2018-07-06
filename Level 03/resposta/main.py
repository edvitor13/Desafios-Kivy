'''
Desafio 003. Jogo da Memória.
------------------------------------
Author:    Vitor Gabriel
Version:   1.0
Date:      2018/06/20
Email:     edvitor13@hotmail.com
'''


# Geral #
from functools import partial
import threading
import time
import random

# Kivy #
import kivy
# Versão mínima requerida
kivy.require('1.10.0')
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image


#############################
# 0. Configurações Iniciais #
#############################

# Mundando Cor de Fundo da Janela para Cinza
Window.clearcolor = (.85, .85, .85, 1)

# Carregando arquivo do código kvlang
Builder.load_file('kvlang.kv')


#####################
# 1. Classes Gerais #
#####################

# Classe responsável por gerenciar a estrutura do jogo
class JogoDaMemoria:
    # Imagens que serão utilizadas
    imagens = ['IMG/bola.png', 'IMG/bandeira-brasil.png', 'IMG/bandeira-suica.png', 'IMG/falta.png', 'IMG/estadio.png', 'IMG/jogador.png']
    # Responsável pela ordem das imagens no jogo e seus respectivos pares
    memoria = []
    # Quantidade de Colunas que o "GridMemoria" terá
    colunas = None

    def __init__(self):
        self.gerar_memoria()

    # Gera o conteúdo de self.memoria
    def gerar_memoria(self):

        # Resetando a lista de self.memoria
        self.memoria = []

        # O INDEX de cada imagem será armazenado duas vezes
        # em self.memoria, representando a imagem e seu par 
        for i in range(len(self.imagens)):
            self.memoria.append(i)
            self.memoria.append(i)

        # Executando o método para embaralhar os índices 
        # das imagens em self.memoria
        self.embaralhar()
        self.identificar_colunas()

    # Identifica e gera a quantidade de colunas que
    # "GridMemoria" terá, com base na quantidade de imagens
    def identificar_colunas(self):
        lm = len(self.imagens)
        if (lm == 2):
            self.colunas = 2
        else:
            self.colunas = round(lm/2)

    # Embaralha os itens da lista de self.memoria
    def embaralhar(self):
        random.shuffle(self.memoria)


###################
# 2. Classes Kivy #
###################

class BotaoMemoria(BoxLayout):
    pass

class TelaDeEspera(BoxLayout):
    pass

class GridMemoria(GridLayout):
    pass

# Botão responsável por ocultar as imagens e interagir
class BotaoSecreto(Button):
    # Armazena o index da imagem que está oculta na mesma posição
    id_img = None
    # Identifica se o botão está ativo ou não
    ativo = True

    # Função para quando o botão for clicado
    # "tela" = Widget "TelaJogo"
    def clicado(self, tela, *args):

        # Se o Botão estiver ativo
        if (self.ativo == True):

            # Remove seu texto
            self.text = ''
            # Deixa seu background transparente
            self.background_color = 0, 0, 0, 0

            # Se este botão não estiver armazenado na lista
            # "tela.bt_clicado" e ela for menor que 2
            if (self not in tela.bt_clicado and len(tela.bt_clicado) < 2):
                # Adiciona este botão pra lista "tela.bt_clicado"
                tela.bt_clicado.append(self)

            # Se "tela.bt_clicado" tiver dois botões
            if (len(tela.bt_clicado) == 2):
                # Executa o método "resolver" de "tela" (TelaJogo)
                tela.resolver()

    # Restaura o texto e a cor de fundo do BotaoSecreto
    def resetar(self, *args):
        if (self.ativo == True):
            self.background_color = .4, .4, .4, 1
            self.text = '?'

# Tela Principal
class TelaJogo(Screen):
    # Pontos Atuais do Jogo
    pontos = 0
    # Tempo de espera exibindo as imagens
    # Esse tempo de espera é multiplicado
    # com base na quantidade de imagens
    espera = .6
    # Botões que já foram clicados
    bt_clicado = []
    # Quantidade de imagens (e seus pares) encontradas
    encontrados = 0

    def __init__(self, **kwargs):
        super(TelaJogo, self).__init__(**kwargs)
        # Inicia a classe de gerenciamento em self.jome
        self.jome = JogoDaMemoria()

    # Calcula e retorna o tempo de espera
    # com base na quantidade de imagens
    def calcular_espera(self):
        espera = self.espera * (len(self.jome.imagens))
        return round(espera)

    # Altera o Texto na Tela
    def saida(self, texto):
        ls = self.ids.ls
        ls.text = texto

    # Soma/Subtrai e Exibe a Pontuação Atual
    def pontuador(self, somar_subtrair=0):
        self.pontos += somar_subtrair
        self.saida('Pontos: {}'.format(self.pontos))

    # Tempo de Espera/Contagem Regressiva
    def temporizador(self, tempo, saida=True):

        for i in range(tempo):
            # Exibe o tempo atual
            if (saida == True):
                self.saida(str(tempo - i))
            # Aguarda 1 segundo
            time.sleep(1)

        # Exibe a pontuação
        self.pontuador()

    # Verifica se todas as imagens foram encontradas
    # e recomeça o jogo
    def verificar_termino(self):

        # Se a quantidade de imagens encontradas for igual
        # a quantidade de itens em self.jome.memoria
        if (self.encontrados == len(self.jome.memoria)):
            # Reseta quantidade de imagens encontradas
            self.encontrados = 0
            # Embaralha o jogo
            self.jome.embaralhar()
            # Recomeça o jogo com a tela de espera
            self.iniciar('tela_espera')

    # Resolve a situação do jogo quando o
    # usuário clicar em duas imagens diferentes
    def resolver(self, *args):

        # Se dois botões (BotaoScreto) diferentes já foram clicados
        if (len(self.bt_clicado) == 2):
            btc0 = self.bt_clicado[0]
            btc1 = self.bt_clicado[1]

            # Se o id (index) de imagem armazenado no "btc0"
            # for igual ao do "btc1" 
            if (btc0.id_img == btc1.id_img):

                # Desativa os botões para que não possam
                # ser clicados novamente
                btc0.ativo = False
                btc1.ativo = False
                # Soma +2 na quantidade de imagens encontradas
                self.encontrados += 2
                # Reseta a lista de botões que foram clicados
                self.bt_clicado = []
                # Soma +1 ponto através do método "pontuador"
                self.pontuador(1)
                # Verifica se o jogo terminou
                self.verificar_termino()

            else:

                # Reseta os botões para seu estado inicial
                btc0.resetar()
                btc1.resetar()
                # Reseta a lista de botões que foram clicados
                self.bt_clicado = []
                # Subtrai -1 ponto através do método "pontuador"
                self.pontuador(-1)

    # Inicia o Jogo
    def iniciar(self, tipo='blocos', *args):

        # Limpando área responsável pelos blocos
        self.ids.blocos_memoria.clear_widgets()

        # Se "tipo" for "blocos", irá iniciar o jogo em si
        if (tipo == 'blocos'):

            ######################### INFO #########################
            # Para evitar problemas no "Thread" para carregar e    #
            # exibir as Imagens, elas e os Botões (BotaoSecreto)   #
            # são criados anteriormente para depois serem passados #
            # como argumento no método "gerar_blocos"              #
            ########################################################

            # Lista para armazenar os Widgets criados
            imagens = []
            botoes = []

            # Para cada item em jome.memoria
            for i in range(len(self.jome.memoria)):
                # Criando Widget de Imagem
                img = Image()
                # Passando Imagem que será utilizada com base no
                # index armazenado em jome.memoria[i]
                img.source = self.jome.imagens[self.jome.memoria[i]]
                # Adicionando à lista
                imagens.append(img)

                # Gerando Botão (BotaoSecreto)
                bts = BotaoSecreto()
                # Armazenando o id (index) da Imagem que ele representa
                bts.id_img = self.jome.memoria[i]
                # Adicionando função que será executada quando ele terminar
                # de ser clicado, e passando a tela atual (TelaJogo) como
                # argumento através do "self"
                bts.bind(on_release=partial(bts.clicado, self))
                # Adicionando à lista
                botoes.append(bts)

            # Iniciando Thread do método "gerar_blocos"
            threading.Thread(
                target = self.gerar_blocos,
                args   = (imagens, botoes)
            ).start()

        # Se "tipo" for "tela_espera", irá exibir a tela de espera antes de iniciar
        elif (tipo == 'tela_espera'):

            # Iniciando Thread do método "gerar_tela_espera"
            threading.Thread(
                target = self.gerar_tela_espera
            ).start()

    # Gera os Blocos de Memória (Imagem e BotaoSecreto)
    def gerar_blocos(self, imagens, botoes):

        # Acessando FloatLayout responsável por conter
        # os Widgets de Imagem e BotaoSecreto
        bm = self.ids.blocos_memoria
        
        # F.L. que conterá o "GridMemoria"
        fl = FloatLayout()
        # G.M. que conterá os "BotaoMemoria"
        # número de colunas definido pelo "jome.colunas"
        gm = GridMemoria(cols=self.jome.colunas)

        # Para cada Widget de Imagem gera um Bloco
        for i in range(len(imagens)):
            # B.M. que conterá a Imagem
            btm = BotaoMemoria()
            
            img = imagens[i]

            # Adicionando Imagem ao B.M.
            btm.add_widget(img)
            # B.M. ao G.M.
            gm.add_widget(btm)

        # Adicionando G.M. ao F.L.
        fl.add_widget(gm)
        # Adicionando F.L. ao "ids.blocos_memoria"
        bm.add_widget(fl)

        # Tempo de Espera para Começar
        self.temporizador(self.calcular_espera())

        # F.L. - G.M.
        fl = FloatLayout()
        gm = GridMemoria(cols=self.jome.colunas)

        # Para cada Widget de BotaoSecreto gera um Bloco
        for i in range(len(botoes)):
            bts = botoes[i]

            # Adicionando bloco ao G.M.
            gm.add_widget(bts)

        # Adicionando G.M. ao F.L.
        fl.add_widget(gm)
        # Adicionando F.L. ao "ids.blocos_memoria"
        bm.add_widget(fl)

    # Gera a tela de intervalo entre uma partida e outra
    def gerar_tela_espera(self):
        # Acessando área responsável pelos blocos
        bm = self.ids.blocos_memoria

        # Tela de Espera
        te = TelaDeEspera()

        # Adicionando tela de espera ao "ids.blocos_memoria"
        bm.add_widget(te)

        # Depois de 2 segundos
        self.temporizador(2, False)

        # Inicia o jogo novamente
        self.iniciar()

# Gerenciador de Telas
sm = ScreenManager()
sm.add_widget(TelaJogo(name='tela_jogo'))

# Classe do Programa
class ProgramaApp(App):
    # Título da Janela
    title = 'Jogo da Memória'

    def build(self):
    	# Retornando Screen Manager
        return sm

# Iniciando o Programa
if __name__ == '__main__':
    ProgramaApp().run()
