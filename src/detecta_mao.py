"""Baseado no MediaPipe, disponibilizado em: https://google.github.io/mediapipe/solutions/hands.html"""

import mediapipe as mp
import cv2


class DetectaMao:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self. drawing_styles = mp.solutions.drawing_styles

        self.hands = self.mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)

    def detectar_mao(self, img):
        """Detecta mao e retorna coordenadas dedos. Recebe imagem BGR"""
        results = self.hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        return results.multi_hand_landmarks

    def desenhar_mao(self, img, marcas):
        """Desenha os ligamentos da mao"""
        for marca in marcas:
            self.mp_drawing.draw_landmarks(
                image=img,
                landmark_list=marca,
                connections=self.mp_hands.HAND_CONNECTIONS,
                landmark_drawing_spec=self.drawing_styles.get_default_hand_landmark_style(),
                connection_drawing_spec=self.drawing_styles.get_default_hand_connection_style())

        return img

    def contar_dedo(self, marcas):
        """Retorna quantidade de dedos levantados"""
        contador_dedo = 0
        for marca in marcas:
            # Dedo index
            if marca.landmark[5].y > marca.landmark[8].y and marca.landmark[7].y > \
                    marca.landmark[8].y:
                contador_dedo += 1
            # Dedo middle
            if marca.landmark[9].y > marca.landmark[12].y and marca.landmark[11].y > marca.landmark[12].y:
                contador_dedo += 1
            # Dedo ring
            if marca.landmark[13].y > marca.landmark[16].y and marca.landmark[15].y > marca.landmark[16].y:
                contador_dedo += 1
            # Dedo pinky
            if marca.landmark[17].y > marca.landmark[20].y and marca.landmark[19].y > marca.landmark[20].y:
                contador_dedo += 1
            # Dedo thumb para esquerda
            if marca.landmark[2].x > marca.landmark[0].x and marca.landmark[4].x > marca.landmark[2].x and \
                    marca.landmark[4].x > marca.landmark[3].x:
                contador_dedo += 1
            # Dedo thumb para direita
            if marca.landmark[2].x < marca.landmark[0].x and marca.landmark[4].x < marca.landmark[2].x and \
                    marca.landmark[4].x < marca.landmark[3].x:
                contador_dedo += 1

        return contador_dedo
