'''
⛶ Desafio 001.
-----------------------------------
Author:    Vitor Gabriel
Version:   1.0
Date:      2018/06/11
Email:     edvitor13@hotmail.com
'''

from kivy.app import App
from kivy.lang.builder import Builder

kvcode = Builder.load_string('''
BoxLayout:
	orientation: 'vertical'
	Label:
		id: saida
		text: 'Aperte algum botão'
		font_size: '25dp'
	Button:
		text: 'Fritar'
		font_size: '20dp'
		on_release:
			# Acessando Label através do ID e modificando seu texto
			root.ids.saida.text = 'Batata Frita'
	Button:
		text: 'Assar'
		font_size: '20dp'
		on_release:
			# Acessando Label através do ID e modificando seu texto
			root.ids.saida.text = 'Batata Assada'
''')

class Programa(App):
	def build(self):
		# Retornando o código KvLang
		return kvcode

Programa().run()
