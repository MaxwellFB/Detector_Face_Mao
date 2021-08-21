"""Atividade para aplicar filtros em imagem, conforme intensidade informada"""

from .atividade import Atividade
import cv2
import numpy as np


class FiltrosImagem(Atividade):
    def __init__(self):
        self.opcao_selecionada = 0

    def iniciar(self, opcao_selecionada):
        """Armazena opcao selecionada"""
        self.opcao_selecionada = opcao_selecionada

    def continuar(self, imagem, intensidade):
        """Aplica filtro na imagem"""
        # Blur
        if self.opcao_selecionada == 1:
            if intensidade != 0:
                imagem = cv2.blur(imagem, (intensidade, intensidade))
        # GaussianBlur
        elif self.opcao_selecionada == 2:
            if intensidade != 0:
                # Obs: ksize precisa ser impar
                imagem = cv2.GaussianBlur(imagem, (intensidade * 2 - 1, intensidade * 2 - 1), 0)
        # MedianBlur
        elif self.opcao_selecionada == 3:
            if intensidade != 0:
                # Obs: ksize precisa ser impar
                imagem = cv2.medianBlur(imagem, intensidade * 2 - 1)
        # Erode
        elif self.opcao_selecionada == 4:
            if intensidade != 0:
                imagem = cv2.erode(imagem, np.ones((intensidade, intensidade), np.uint8))
        # Dilate
        elif self.opcao_selecionada == 5:
            if intensidade != 0:
                imagem = cv2.dilate(imagem, np.ones((intensidade, intensidade), np.uint8))
        # TODO: Tirar corpo deste local
        # elif opcao_selecionada == 6:
        #    imagem = self.corpo.segmentar(imagem, marcas_segmentacao_corpo)

        return imagem