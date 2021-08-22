"""Tela do OpenCV para escrever mensagem e mostrar para o usuario"""

import cv2
import numpy as np


class Quadro:
    def __init__(self):
        # Cor fundo quadro
        self.background_color = (0, 0, 0)

        # Configuracoes das letras
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.fontScale = 2
        self.color = (255, 255, 255)
        self.thickness = 2

        self.quadro = np.array([])
        self.criar()

    def criar(self, tamanho=(100, 100, 3)):
        """Cria quadro com tamanho informado"""
        self.quadro = np.full_like(np.zeros(tamanho), self.background_color).astype(np.uint8)

    def escrever(self, texto, pos):
        """Escreve texto no quadro"""
        self.quadro = cv2.putText(self.quadro, texto, pos, self.font, self.fontScale, self.color, self.thickness)

    def mostrar(self):
        """Mostra quadro"""
        cv2.imshow('Quadro', self.quadro)

    def destruir(self):
        """Destroi quadro"""
        if cv2.getWindowProperty('Quadro', cv2.WND_PROP_VISIBLE):
            cv2.destroyWindow('Quadro')

    def get_shape(self):
        """Pega shape do quadro que esta na memoria"""
        return self.quadro.shape
