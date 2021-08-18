from detecta_mao import DetectaMao
from detecta_face import DetectaFace
from detecta_face_mesh import DetectaFaceMesh
import cv2


# ----- CONFIGURACOES ----- #
com_background = False

if com_background:
    background = cv2.imread('space-wallpaper-7.jpg', cv2.COLOR_RGB2BGR)
    background = cv2.resize(background, (1000, 500))
# ------------------------- #

mao = DetectaMao()
face = DetectaFace()
face_mesh = DetectaFaceMesh()

cap = cv2.VideoCapture(0)

contador_dedo = 0
while cap.isOpened():
    success, image = cap.read()
    # Deixa a imagem como se fosse um espelho
    image = cv2.flip(image, 1)

    marcas_mao = mao.detectar_mao(image)
    marcas_face = face.detectar_face(image)
    marcas_face_mesh = face_mesh.detectar_face_mesh(image)

    if com_background:
        if marcas_face_mesh:
            image = face_mesh.coletar_face_mesh(image, marcas_face_mesh)
            image = face_mesh.colocar_face_mesh_background(image, background, 110, 80)
    else:
        cv2.putText(image, str(contador_dedo), (image.shape[1] - 100, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
        if marcas_mao:
            image = mao.desenhar_mao(image, marcas_mao)
            contador_dedo = mao.contar_dedo(marcas_mao)
        else:
            contador_dedo = 0
        if marcas_face:
            image = face.desenhar_box(image, marcas_face)
        if marcas_face_mesh:
            image = face_mesh.desenhar_face_mesh(image, marcas_face_mesh)

    cv2.imshow('Face', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
