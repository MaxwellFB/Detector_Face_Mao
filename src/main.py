from Detector_Face_Mao.src.Atividades.menu import Menu
from Detector_Face_Mao.src.Atividades.filtros_imagem import FiltrosImagem
from Detector_Face_Mao.src.Atividades.face_mesh_background import FaceMeshBackground
from detecta_mao import DetectaMao
from detecta_face import DetectaFace
from detecta_face_mesh import DetectaFaceMesh
from detecta_corpo import DetectaCorpo
import cv2


def main():
    sistema = Sistema()
    sistema.iniciar()


class Sistema:
    def __init__(self):
        """Metodo principal"""
        # ----- CONFIGURACOES ----- #
        # self.is_desenha = False
        # ------------------------- #

        # Instancia detectores
        self.mao = DetectaMao()
        self.face = DetectaFace()
        self.face_mesh = DetectaFaceMesh()
        self.corpo = DetectaCorpo()
        # Instancia atividades
        self.menu = Menu()
        self.filtros_imagem = FiltrosImagem()
        self.face_mesh_background = FaceMeshBackground()

        # Tempo que precisa ficar solicitando comando ate ele ser executado. Evita executar comando por engano
        self.comando_atual = ''
        self.delay_selec_comando = 10
        self.contador_delay_selec_comando = 0

        """
        Atividades:
            0 = Sistema principal
            1 = Menu
            2 = Filtros imagem
            3 = Face mesh background
            4 = Corpo # desativado
        """
        self.atividades_inicia = []
        self.atividades_continua = [0]
        self.atividades_termina = []

        self.atividades_usam_mao = [0, 1, 2]
        self.atividades_usam_face = []
        self.atividades_usam_face_mesh = [3]
        self.atividades_usam_corpo = []

        self.atividades_permitidas_serem_iniciadas = []

    def iniciar(self):
        """Inicia sistema"""
        cap = cv2.VideoCapture(0)
        contador_dedo = 0
        dedos_levantados = []
        opcao_selecionada = 0

        while cap.isOpened():
            marcas_mao = None
            marcas_face = None
            marcas_face_mesh = None
            marcas_corpo = None

            success, frame = cap.read()
            # Deixa a imagem como se fosse um espelho
            frame = cv2.flip(frame, 1)
            frame_originial = frame.copy()

            comando = self.verificar_comando(dedos_levantados)
            if comando == 1:
                break

            # ----- Inicializa novas atividades ----- #
            qtd_excluida = 0
            atividades_temp = self.atividades_inicia.copy()
            for idx, atividade in enumerate(self.atividades_inicia):
                if atividade == 1:
                    self.menu.iniciar(frame_originial)
                elif atividade == 2:
                    self.filtros_imagem.iniciar(opcao_selecionada)
                elif atividade == 3:
                    self.face_mesh_background.iniciar(self.face_mesh)

                # Passa para proxima etapa
                self.atividades_continua.append(atividade)

                # Remove atividade iniciada
                del(atividades_temp[idx-qtd_excluida])
                qtd_excluida += 1

            self.atividades_inicia = atividades_temp.copy()
            # ----- Fim inicializa novas atividades ----- #

            # ----- Coleta informacoes ----- #
            # Coleta de informacoes conforme necessidade das atividades
            if any(atividade in self.atividades_usam_mao for atividade in self.atividades_continua):
                marcas_mao = self.mao.detectar(frame_originial)
                contador_dedo = 0
                if marcas_mao:
                    contador_dedo, dedos_levantados = self.mao.contar_dedo(marcas_mao)
                    frame = self.mao.desenhar(frame_originial, marcas_mao)
            if any(atividade in self.atividades_usam_face for atividade in self.atividades_continua):
                marcas_face = self.face.detectar(frame_originial)
            if any(atividade in self.atividades_usam_face_mesh for atividade in self.atividades_continua):
                marcas_face_mesh = self.face_mesh.detectar(frame_originial)
            if any(atividade in self.atividades_usam_corpo for atividade in self.atividades_continua):
                marcas_corpo, marcas_segmentacao_corpo = self.corpo.detectar(frame_originial)
            # ----- Fim coleta informacoes ----- #

            # ----- Continua atividades ja iniciadas ----- #
            qtd_excluida = 0
            atividades_temp = self.atividades_continua.copy()
            for idx, atividade in enumerate(self.atividades_continua):
                if atividade == 0:
                    cv2.putText(frame, str(contador_dedo), (frame.shape[1] - 100, 80),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
                elif atividade == 1:
                    if self.menu.continuar(contador_dedo, comando) == 1:
                        del (atividades_temp[idx - qtd_excluida])
                        qtd_excluida += 1
                        # Passa para proxima etapa
                        self.atividades_termina.append(atividade)
                elif atividade == 2:
                    frame = self.filtros_imagem.continuar(frame, contador_dedo)
                elif atividade == 3:
                    frame = self.face_mesh_background.continuar(frame_originial, marcas_face_mesh)

            self.atividades_continua = atividades_temp.copy()
            # ----- Fim continua atividades ja iniciadas ----- #

            # ----- Termina atividades ----- #
            qtd_excluida = 0
            atividades_temp = self.atividades_termina.copy()
            for idx, atividade in enumerate(self.atividades_termina):
                if atividade == 1:
                    opcao_selecionada = self.menu.terminar()
                    if 2 in self.atividades_permitidas_serem_iniciadas:
                        self.atividades_inicia.append(2)
                elif atividade == 2:
                    self.filtros_imagem.terminar()
                elif atividade == 3:
                    self.face_mesh_background.terminar()

                # Remove atividade iniciada
                del (atividades_temp[idx - qtd_excluida])
                qtd_excluida += 1

            self.atividades_termina = atividades_temp.copy()
            # ----- Fim termina atividades ----- #

            # TODO: Desativado, exige muitas alteracoes para funcionar. Nao eh prioridade
            '''
            # Se deseja desenhar as deteccoes de face
            if self.is_desenha:
                if marcas_face:
                    frame = self.face.desenhar_box(frame, marcas_face)
                if marcas_face_mesh:
                    frame = self.face_mesh.desenhar(frame, marcas_face_mesh)
                if marcas_corpo:
                    frame = self.corpo.desenhar(frame, marcas_corpo)
            '''

            cv2.imshow('Face', frame)
            if cv2.waitKey(5) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    def verificar_comando(self, dedos_levantados):
        """
        Comandos que podem ser realizado com a mao

        :return: 0 = nenhum comando executado, 1 = encerrar, 2 = comando executado/solicitado
        """
        # Levantar indicador, anelar e mindinho para encerrar
        if len(dedos_levantados) == 3 and 1 in dedos_levantados and 3 in dedos_levantados and 4 in dedos_levantados:
            if self.verificar_delay('Exit') == 1:
                return 1
            return 2
        # Levantar indicador e mindinho para acessar menu
        elif len(dedos_levantados) == 2 and 1 in dedos_levantados and 4 in dedos_levantados:
            if self.verificar_delay('Menu') == 1:
                if not any([1 in self.atividades_inicia, 1 in self.atividades_continua, 1 in self.atividades_termina]):
                    self.atividades_inicia.append(1)
                    self.mudar_atividade_principal([0, 1])
                    self.atividades_permitidas_serem_iniciadas = [2]
            return 2
        # Levantar indicador, mindinho e polegar para acessar face mesh com background
        elif len(dedos_levantados) == 3 and 1 in dedos_levantados and 4 in dedos_levantados and 5 in dedos_levantados:
            if self.verificar_delay('Mesh_background') == 1:
                if not any([3 in self.atividades_inicia, 3 in self.atividades_continua, 3 in self.atividades_termina]):
                    self.atividades_inicia.append(3)
                    self.mudar_atividade_principal([0, 3])
                    self.atividades_permitidas_serem_iniciadas = []
            return 2

        # Informa que nenhum comando foi solicitado, entao limpa temporizador
        self.verificar_delay('')
        # Nenhum comando foi acionado
        return 0

    def mudar_atividade_principal(self, atividades_permitidas):
        """Quando for iniciar uma nova atividade, outras podem nao fazerem sentido existirem, entao encerra elas"""
        qtd_excluida = 0
        atividades_temp = self.atividades_inicia.copy()
        for idx, atividade in enumerate(self.atividades_inicia):
            if atividade in atividades_permitidas:
                continue
            del (atividades_temp[idx - qtd_excluida])
            qtd_excluida += 1
        self.atividades_inicia = atividades_temp.copy()

        qtd_excluida = 0
        atividades_temp = self.atividades_continua.copy()
        for idx, atividade in enumerate(self.atividades_continua):
            if atividade in atividades_permitidas:
                continue
            del (atividades_temp[idx - qtd_excluida])
            qtd_excluida += 1
            self.atividades_termina.append(atividade)
        self.atividades_continua = atividades_temp.copy()

    def verificar_delay(self, comando):
        """Tempo que precisa ficar solicitando o comando para executa-lo. Evita solicitar comando por engano"""
        if self.comando_atual == comando and comando != '':
            if self.contador_delay_selec_comando < self.delay_selec_comando:
                self.contador_delay_selec_comando += 1
                return 0
            # Se acabou o delay, executa comando
            return 1
        self.comando_atual = comando
        self.contador_delay_selec_comando = 0
        return 0

if __name__ == '__main__':
    main()
