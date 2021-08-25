"""Detecta um corpo e pega diversos pontos do corpo"""

import cv2
import numpy as np
import mediapipe as mp


class DetectaCorpo:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_pose = mp.solutions.pose

        # Cor solida de fundo na segmentacao
        # self.background_segmentation = np.zeros((1000, 1000, 3), dtype=np.uint8)
        # self.background_segmentation[:] = (192, 192, 192)
        # Imagem de fundo na segmentacao
        self.background_segmentation = cv2.imread('space-wallpaper-7.jpg', cv2.COLOR_RGB2BGR)

        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=True,
            min_detection_confidence=0.5)

    def detectar(self, img):
        """Detecta corpo e retorna coordenadas corpo e segmentacao. Recebe imagem BGR"""
        results = self.pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        return results.pose_landmarks, results.segmentation_mask

    def desenhar(self, img, marcas_corpo):
        """Desenha os ligamentos do corpo"""
        # Somente detecta um corpo
        #for marca in marcas:
        self.mp_drawing.draw_landmarks(
            image=img,
            landmark_list=marcas_corpo,
            connections=self.mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style())

        return img

    def segmentar(self, img, marcas_segmentacao):
        """Pinta o fundo com uma cor uniforme, mantendo apenas a pessoa em destaque"""
        condition = np.stack((marcas_segmentacao,) * 3, axis=-1) > 0.1
        bg_image = cv2.resize(self.background_segmentation, (img.shape[1], img.shape[0]))
        img = np.where(condition, img, bg_image)
        return img
