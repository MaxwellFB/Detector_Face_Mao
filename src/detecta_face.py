"""Baseado no MediaPipe, disponibilizado em: https://google.github.io/mediapipe/solutions/face_detection.html"""

import cv2
import mediapipe as mp


class DetectaFace:
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils

        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=0.5)

    def detectar_face(self, img):
        """Detecta face e retorna coordenadas dos boxes. Recebe imagem BGR"""
        results = self.face_detection.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # Retorna coordenadas normalizadas, com pontos em algumas regioes
        # return results.detections

        h, w, c = img.shape
        boxes = []

        if results.detections:
            for idx, detection in enumerate(results.detections):
                xmin = int(detection.location_data.relative_bounding_box.xmin * w)
                ymin = int(detection.location_data.relative_bounding_box.ymin * h)
                width = int(detection.location_data.relative_bounding_box.width * w)
                height = int(detection.location_data.relative_bounding_box.height * h)
                boxes.append([idx, xmin, ymin, width, height])

        # Retorna coordenadas reais somente dos boxes
        return boxes

    def desenhar_box(self, img, boxes):
        """Desenha box da face na imagem"""
        # Desenha box e alguns pontos utilizando coordenadas normalizadas
        #for box in boxes:
        #    self.mp_drawing.draw_detection(img, box)

        # Desenha somente box utilizando coordenadas reais
        for idx, x, y, w, h in boxes:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return img
