'''
⛶ Desafio 001.
-----------------------------------
Author:    Vitor Gabriel
Version:   1.0
Date:      2018/06/11
Email:     edvitor13@hotmail.com
'''

from functools import partial
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class Botao(Button):
	# Função responsável por mudar o texto do label
	def mudar_texto_label(self, label, *args):
		# Se o texto do botão for 'Fritar'
		if (self.text == 'Fritar'):
			# Novo Texto do Label
			label.text = 'Batata Frita'
		# Se o texto do botão for 'Assar'
		elif (self.text == 'Assar'):
			label.text = 'Batata Assada'

class Programa(App):
	def build(self):
		# Criando BoxLayout
		box = BoxLayout(orientation='vertical')

		# Criando Label e Botões
		lab = Label(text='Aperte algum botão', font_size='25dp')
		bt1 = Botao(text='Fritar', font_size='20dp')
		bt2 = Botao(text='Assar', font_size='20dp')

		# Adicionando Função ao on_release de bt1
		bt1.bind(
			# Quando o botão terminar de ser clicado, o método 'mudar_texto_label'
			# de 'Botao' será executado
			on_release = partial(bt1.mudar_texto_label, lab)
		)
		# Adicionando Função ao on_release de bt2
		bt2.bind(
			on_release = partial(bt2.mudar_texto_label, lab)
		)

		# Adicionando Label e Botões ao BoxLayout
		box.add_widget(lab)
		box.add_widget(bt1)
		box.add_widget(bt2)

		# Retornando o BoxLayout
		return box

Programa().run()
