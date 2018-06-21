'''
⛶ Desafio 002. Utilizando Imagens.
------------------------------------
Author:    Vitor Gabriel
Version:   1.0
Date:      2018/06/15
Email:     edvitor13@hotmail.com
'''

from kivy.app import App
from kivy.core.window import Window
from kivy.lang.builder import Builder

# Mundando Cor de Fundo da Janela para Branco
Window.clearcolor = (1, 1, 1, 1)

kvcode = """
# Botão Principal
<Botao@Button>:
    background_normal: ''
    background_down: ''
    color: 1, 1, 1, 1
    font_size: '35dp'
    background_color: 0.2, .8, 0.2, 1
    on_press: self.background_color = 0.2, 1, 0.2, 1
    on_release: self.background_color = 0.2, 0.8, 0.2, 1

# Divisória p/ Borda, Verde - Botões    
<DivVerde@Label>:
    canvas.before:
        Color: 
            rgba: .2, .6, .2, 1
        Rectangle:
            pos: self.pos
            size: self.size

# Divisória p/ Borda, Azul - Informações
<DivAzul@Label>:
    canvas.before:
        Color: 
            rgba: .7, .87, .90, 1
        Rectangle:
            pos: self.pos
            size: self.size

# Box Principal
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        orientation: 'horizontal'
        # Imagem Base
        Image:
            id: image
            source: 'IMG/batata.png'
            
        # Borda    
        DivAzul:
            size_hint: None, 1
            width: '5dp'
            
        # Box de Informações
        BoxLayout:
            orientation: 'vertical'
            # Borda 
            DivAzul:
                size_hint: 1, None
                height: '5dp'
            
            # Box Informações Batatas Assadas
            BoxLayout:
                orientation: 'vertical'
                # Título
                Label:
                    size_hint: 1, None
                    height: '50dp' 
                    text: 'Assadas'
                    font_size: '20dp'
                    bold: True
                    color: 0, 0, 0, 1
                # Contador
                Label:
                    id: contador_assadas
                    text: '0'
                    font_size: '50dp'
                    color: .5, .5, .5, 1
            
            # Borda
            DivAzul:
                size_hint: 1, None
                height: '5dp'
            
            # Box Informações Batatas Fritas
            BoxLayout:
                orientation: 'vertical'
                # Título
                Label:
                    size_hint: 1, None
                    height: '50dp'
                    text: 'Fritas'
                    font_size: '20dp'
                    bold: True
                    color: 0, 0, 0, 1
                # Contador
                Label:
                    id: contador_fritas
                    text: '0'
                    font_size: '50dp'
                    color: .5, .5, .5, 1
    # Borda
    DivVerde:
        size_hint: 1, None
        height: '5dp'
    
    # Box dos Botões
    BoxLayout:
        orientation: 'horizontal'
        # Botão Assar
        Botao:
            text: 'Assar'
            on_release: 
                image.source='IMG/batata-assada.png'
                contador_assadas.text = str(int(contador_assadas.text) + 1)
                contador_fritas.color = .5, .5, .5, 1
                contador_assadas.color = 1, 0, 0, 1
        
        # Borda
        DivVerde:
            size_hint: None, 1
            width: '5dp'
        
        # Botão Fritar
        Botao:
            text: 'Fritar'
            on_release: 
                image.source='IMG/batata-frita.png'
                contador_fritas.text = str(int(contador_fritas.text) + 1)
                contador_fritas.color = 1, 0, 0, 1
                contador_assadas.color = .5, .5, .5, 1
"""

# Carregando código kvlang
bu = Builder.load_string(kvcode)

class ProgramaApp(App):

    def build(self):
        # Retornando código kvlang em build
        return bu

# Iniciando o programa
ProgramaApp().run()
