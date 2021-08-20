from detecta_mao import DetectaMao
from detecta_face import DetectaFace
from detecta_face_mesh import DetectaFaceMesh
from detecta_corpo import DetectaCorpo
from quadro import Quadro
import cv2
import numpy as np


def main():
    """Funcao principal"""
    # ----- CONFIGURACOES ----- #
    background = cv2.imread('space-wallpaper-7.jpg', cv2.COLOR_RGB2BGR)
    background = cv2.resize(background, (1000, 500))

    is_desenha = True
    # ------------------------- #

    mao = DetectaMao()
    face = DetectaFace()
    face_mesh = DetectaFaceMesh()
    corpo = DetectaCorpo()

    cap = cv2.VideoCapture(0)

    contador_dedo = 0
    dedos_levantados = []
    opcao_selecionada = 1
    atividade = 0

    # Tempo que precisa ficar com os dedos levantados ate coletar opcao (para evitar pegar opcao errada enquanto estiver
    # levantando)
    delay_selec_opcao = 10
    opcao_temporaria = 0
    contador_delay_selec_opcao = 0

    # Cria quadro para escrita
    quadro = Quadro()

    while cap.isOpened():
        success, image = cap.read()
        # Deixa a imagem como se fosse um espelho
        image = cv2.flip(image, 1)

        marcas_mao = mao.detectar_mao(image)
        marcas_face = face.detectar_face(image)
        marcas_face_mesh = face_mesh.detectar_face_mesh(image)
        marcas_corpo, marcas_segmentacao_corpo = corpo.detectar(image)

        cv2.putText(image, str(contador_dedo), (image.shape[1] - 100, 80), cv2.FONT_HERSHEY_SIMPLEX, 2,
                    (0, 0, 255), 2)
        if marcas_mao:
            image = mao.desenhar_mao(image, marcas_mao)
            contador_dedo, dedos_levantados = mao.contar_dedo(marcas_mao)
        else:
            contador_dedo = 0

        # Se deseja desenhar as deteccoes de face
        if is_desenha:
            if marcas_face:
                image = face.desenhar_box(image, marcas_face)
            if marcas_face_mesh:
                image = face_mesh.desenhar_face_mesh(image, marcas_face_mesh)
            if marcas_corpo:
                image = corpo.desenhar(image, marcas_corpo)

        comando = verificar_comando(dedos_levantados)
        # TODO: Pensar em fazer essa selecao diferente, ficou grande e repetitivo (logo em seguida faz praticamente a
        #  mesma checagem)
        # Encerra
        if comando == 1:
            break
        # Menu
        elif comando == 2:
            atividade = 2
            quadro.criar(image)
            quadro.escrever('Menu', (int(quadro.get_shape()[0] / 2), 50))
            quadro.escrever('1 - Blur', (10, 110))
            quadro.escrever('2 - GaussianBlur', (10, 170))
            quadro.escrever('3 - MedianBlur', (10, 240))
            quadro.escrever('4 - Erode', (10, 300))
            quadro.escrever('5 - Dilate', (10, 360))
            # TODO: Separar corpo do menu
            quadro.escrever('6 - Corpo', (10, 420))
            quadro.mostrar()
        # Face com background
        elif comando == 3:
            # TODO: Achar uma forma melhor para destruir o quadro (caso tenha sido aberto por outro comando)
            quadro.destruir()
            atividade = 3

        # Menu de opcoes
        if atividade == 2:
            if contador_dedo != 0 and contador_dedo == opcao_temporaria and comando == 0:
                # Permanecer tempo com dedo levantado ate adquirir opcao
                if contador_delay_selec_opcao < delay_selec_opcao:
                    contador_delay_selec_opcao += 1
                else:
                    # Opcao selecionada
                    quadro.destruir()
                    opcao_selecionada = contador_dedo
                    atividade = 0
                    print('Opcao {} selecionada'.format(contador_dedo))
            # Nao levantou dedo, mudou quantidade de dedos levantados ou acionou comando
            else:
                contador_delay_selec_opcao = 0
                opcao_temporaria = contador_dedo
        # Mostra face com background
        elif atividade == 3:
            if marcas_face_mesh:
                image = face_mesh.coletar_face_mesh(image, marcas_face_mesh)
                image = face_mesh.colocar_face_mesh_background(image, background, 110, 80)
        # Realiza atividades da opcao selecionada
        else:
            # Blur
            if opcao_selecionada == 1:
                if contador_dedo != 0:
                    image = cv2.blur(image, (contador_dedo, contador_dedo))
            # GaussianBlur
            elif opcao_selecionada == 2:
                if contador_dedo != 0:
                    # Obs: ksize precisa ser impar
                    image = cv2.GaussianBlur(image, (contador_dedo*2-1, contador_dedo*2-1), 0)
            # MedianBlur
            elif opcao_selecionada == 3:
                if contador_dedo != 0:
                    # Obs: ksize precisa ser impar
                    image = cv2.medianBlur(image, contador_dedo*2-1)
            # Erode
            elif opcao_selecionada == 4:
                if contador_dedo != 0:
                    image = cv2.erode(image, np.ones((contador_dedo, contador_dedo), np.uint8))
            # Dilate
            elif opcao_selecionada == 5:
                if contador_dedo != 0:
                    image = cv2.dilate(image, np.ones((contador_dedo, contador_dedo), np.uint8))
            # TODO: Tirar corpo deste local
            elif opcao_selecionada == 6:
                image = corpo.segmentar(image, marcas_segmentacao_corpo)


        cv2.imshow('Face', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


def verificar_comando(dedos_levantados):
    """Comando que podem ser realizado com a mao"""
    # Levantar indicador, anelar e mindinho para encerrar
    if len(dedos_levantados) == 3 and 1 in dedos_levantados and 3 in dedos_levantados and 4 in dedos_levantados:
        return 1
    # Levantar indicador e mindinho para acessar menu
    elif len(dedos_levantados) == 2 and 1 in dedos_levantados and 4 in dedos_levantados:
        return 2
    # Levantar indicador, mindinho e polegar para acessar face com background
    elif len(dedos_levantados) == 3 and 1 in dedos_levantados and 4 in dedos_levantados and 5 in dedos_levantados:
        return 3
    # Nenhum comando foi acionado
    else:
        return 0


if __name__ == '__main__':
    main()
