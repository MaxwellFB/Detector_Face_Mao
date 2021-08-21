"""Baseado no MediaPipe, disponibilizado em: https://google.github.io/mediapipe/solutions/face_mesh.html"""

import cv2
import numpy as np
import mediapipe as mp


class DetectaFaceMesh:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_face_mesh = mp.solutions.face_mesh

        self.mp_drawing_spec = self.mp_drawing.DrawingSpec(thickness=2, circle_radius=0, color=(255, 255, 255))

        self.face_mesh = self.mp_face_mesh.FaceMesh(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)

    def detectar(self, img):
        """Pega as coordenadas das marcas da malha da face"""
        results = self.face_mesh.process(img)

        return results.multi_face_landmarks

    def desenhar(self, img, marcas):
        """Desenha a malha na face"""
        # Faz copia, caso contrario altera a imagem passada como parametro, influenciando em quem chamou
        imagem = img.copy()
        for marca in marcas:
            self.mp_drawing.draw_landmarks(
                image=imagem,
                landmark_list=marca,
                connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.mp_drawing_spec)
        return imagem

    def coletar(self, img, marcas, background_preto=True):
        """Pega somente a face da pessoa colorida"""
        img_original = img.copy()
        mask = img.copy()

        img_com_mesh = self.desenhar(img, marcas)

        # Identificacao dos contornos do rosto para criar mascara
        img_gray = cv2.cvtColor(img_com_mesh, cv2.COLOR_BGR2GRAY)
        _, img_threshold = cv2.threshold(img_gray, 254, 255, cv2.THRESH_BINARY)
        res = cv2.findContours(img_threshold.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours = res[-2]

        # Retira qualquer ponto 255 para nao misturar com a mascara (caso contrario podem aparecer falhas)
        mask[mask == 255] = 254
        # Desenha a mascara de branco
        cv2.fillPoly(mask, pts=contours, color=(255, 255, 255))
        # Tudo que nao for a mascara vira preto
        mask[mask < 255] = 0

        resultado = cv2.bitwise_and(img_original, mask)

        grayscale = cv2.cvtColor(resultado, cv2.COLOR_BGR2GRAY)

        # Box da face
        bbox = cv2.boundingRect(grayscale)

        x, y, w, h = bbox
        if background_preto:
            return resultado[y:y+h, x:x+w]
        else:
            return img_original[y:y+h, x:x+w]

    def colocar_face_mesh_background(self, face_mesh, background, pos_x_inicial=0, pos_y_inicial=0):
        """Coloca face dentro de um background, recebe e retorna imagens em formato BGR"""
        if face_mesh.shape[0] > background.shape[0] or face_mesh.shape[1] > background.shape[1]:
            raise Exception('Imagem da face maior que background')

        # Pega fundo preto da face e transforma em transparente (alpha)
        tmp = cv2.cvtColor(face_mesh, cv2.COLOR_BGR2GRAY)
        _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
        b, g, r = cv2.split(face_mesh)
        rgba = [b, g, r, alpha]
        dst = cv2.merge(rgba, 4)
        alpha_s = dst[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        # Posicao que a face ira aparecer no background
        x1, x2 = pos_x_inicial, pos_x_inicial + dst.shape[1]
        y1, y2 = pos_y_inicial, pos_y_inicial + dst.shape[0]

        # Transforma background em alpha e coloca face dentro da imagem
        background = cv2.cvtColor(background, cv2.COLOR_BGR2BGRA)
        for c in range(0, 3):
            background[y1:y2, x1:x2, c] = (alpha_s * dst[:, :, c] + alpha_l * background[y1:y2, x1:x2, c])

        return cv2.cvtColor(background, cv2.COLOR_BGRA2BGR)
