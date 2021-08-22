"""Atividade para coletar rosto e colocar em imagem de background"""


from .atividade import Atividade
import cv2

class FaceMeshBackground(Atividade):
    def __init__(self):
        self.background = cv2.imread('./space-wallpaper-7.jpg', cv2.COLOR_RGB2BGR)
        self.background = cv2.resize(self.background, (1000, 500))
        self.face_mesh = None

    def iniciar(self, face_mesh):
        """Recebe instancia para classe do face mesh"""
        self.face_mesh = face_mesh

    def continuar(self, imagem, marcas_face_mesh):
        """Adiciona face dentro do background"""
        if marcas_face_mesh:
            mesh = self.face_mesh.coletar(imagem, marcas_face_mesh)
            imagem = self.face_mesh.colocar_face_mesh_background(mesh, self.background, 110, 80)
            return imagem
        return self.background
