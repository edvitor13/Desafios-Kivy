'''
Desafio 004. Editor de Imagens.
------------------------------------
Author:    Vitor Gabriel
Version:   1.0
Date:      2018/07/08
Email:     edvitor13@hotmail.com
'''

# Geral #
from PIL import Image as ImagePIL, ImageEnhance
import os
import io

# Kivy Classes Externas #
from kivyplugin.hoverbehavior import HoverBehavior

# Kivy #
import kivy
kivy.require('1.10.0')
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.config import Config

from kivy.core.image import Image as CoreImage
from kivy.properties import ObjectProperty

from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition, SlideTransition
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup


#############################
# 0. Configurações Iniciais #
#############################

# Alterando tamanho da janela
Window.size = (550, 650)

# Registrando Classe Externa
Factory.register('HoverBehavior', HoverBehavior)

# Mundando Cor de Fundo da Janela para Cinza
Window.clearcolor = (.92, .92, .92, 1)

# Carregando arquivo do código kvlang
Builder.load_file('kvlang.kv')


#####################
# 1. Classes Gerais #
#####################

class Geral():
  def transicao(self, nome_tela, direcao='left', tipo='Slide', *args):
    self.manager.transition = eval(tipo + 'Transition()')
    self.manager.transition.direction = direcao
    self.manager.current = nome_tela

class Editor():
	img = None
	img_formato = None
	img_pasta_base = None
	img_nome_base = None

	def __init__(self):
		pass

	def resetar(self):
		self.img = None
		self.img_formato = None
		self.img_pasta_base = None
		self.img_nome_base = None

	def carregar_imagem(self, local, callback=None):
		if (self.img is None):
			try:
				# Carregando imagem fia PIL
				self.img = ImagePIL.open(local)

				# Armazenando formato da imagem
				self.img_formato = self.img.format.lower()

				if (self.img.mode == 'P'):
					self.img = self.img.convert(mode='RGBA')

				# Armazenando pasta base da imagem
				self.img_pasta_base = os.path.dirname(os.path.realpath(local))
				# Armazenando nome base da imagem
				nome_base, extensao = os.path.splitext(os.path.basename(local))
				self.img_nome_base = (nome_base + '_editado')

				if (callback is not None):
					callback('[b]Imagem Carregada![/b]')
				return True

			except Exception as e:
				if (callback is not None):
					callback('[b]Imagem inválida[/b] tente novamente')
				print(e)
				return False

	def girar_imagem(self, graus=90, sentido='horario'):
		if (sentido == 'antihorario'):
			self.img = self.img.rotate(graus, expand=True)
		else:
			self.img = self.img.rotate(graus * -1, expand=True)

	def remover_cores(self):
		converter = ImageEnhance.Color(self.img)
		self.img = converter.enhance(0)

	def salvar(self, pasta, arquivo_nome):
		try:
			self.img.save(pasta + '/' + arquivo_nome + '.' + self.img_formato, self.img_formato.upper())
			self.resetar()
			return True
		except:
			return False

ed = Editor()


###################
# 2. Classes Kivy #
###################

class TelaInicial(Screen, Geral):
	def __init__(self, **kargs):
		super(TelaInicial, self).__init__(**kargs)
		#Window.bind(on_cursor_enter=self._on_cursor_enter)
		
		Window.bind(on_dropfile=self._on_dropfile)

	def resetar(self):
		self.alterar_mensagem('[b]Procure uma imagem[/b] e arraste ela aqui')

	def alterar_mensagem(self, texto):
		lab = self.ids.mensagem
		lab.text = texto

	def _on_dropfile(self, window, file_path):
		if (ed.img is None):
			self.alterar_mensagem('Carregando...')

		if (ed.carregar_imagem(file_path.decode('utf8'), self.alterar_mensagem) == True):
			tela_edicao = self.manager.get_screen('tela_edicao')
			tela_edicao.gerar_tela()


class TelaEdicao(Screen, Geral):
	def __init__(self, **kargs):
		super(TelaEdicao, self).__init__(**kargs)

	def gerar_tela(self):
		self.exibir_imagem()
		self.transicao('tela_edicao')

	def exibir_imagem(self):
		ce = self.ids.conteudo_edicao
		ce.clear_widgets()

		#############################
		# Obtendo Textura da Imagem #
		#############################

		# Criando Buffer
		image_bytes = io.BytesIO()

		# Salvando Imagem de PIL no Buffer
		ed.img.save(image_bytes, format=ed.img_formato)

		# Defininto ponto inicial 0
		image_bytes.seek(0)

		# Carregando imagem no CoreImage -> Ex: (Buffer, ext='png')
		im = CoreImage(image_bytes, ext=ed.img_formato)

		# Coletando textura da Imagem de CoreImage
		tex = im.texture

		# Encerrando Buffer
		image_bytes.close()

		# ----------------------- #

		# Criando Widget de Imagem
		img = Image(nocache=True)
		# Passando a textura gerada no CoreImage para ele
		img.texture = tex

		ce.add_widget(img)

	def girar_antihorario(self):
		ed.girar_imagem(90, 'antihorario')
		self.exibir_imagem()

	def girar_horario(self):
		ed.girar_imagem(90, 'horario')
		self.exibir_imagem()

	def preto_e_branco(self):
		ed.remover_cores()
		self.exibir_imagem()

	def dismiss_popup(self):
		self._popup.dismiss()

	def show_save(self):
		content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
		content.configurando_filechooser()
		self._popup = Popup(title="Salvar Imagem", content=content, size_hint=(1, 1))
		self._popup.open()

	def save(self, path, filename):
		if (ed.salvar(path, filename) == True):
			self.transicao('tela_inicial', 'left', 'No')
			self.manager.get_screen('tela_inicial').resetar()
			self.dismiss_popup()
		else:
			pass

class SaveDialog(FloatLayout):
	save = ObjectProperty(None)
	text_input = ObjectProperty(None)
	cancel = ObjectProperty(None)

	def configurando_filechooser(self):
		self.ids.filechooser.path = ed.img_pasta_base
		self.ids.text_input.text = ed.img_nome_base

sm = ScreenManager()
sm.add_widget(TelaInicial(name='tela_inicial'))
sm.add_widget(TelaEdicao(name='tela_edicao'))

class ProgramaApp(App):
	title = 'Editor de Imagem'

	def build(self):
		return sm

if __name__ == '__main__':
	ProgramaApp().run()