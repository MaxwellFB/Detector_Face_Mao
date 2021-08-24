"""Atividade para manipular quadro de opcoes (menu)"""

from .atividade import Atividade
from ..quadro import Quadro


class Menu(Atividade):
    """
    Tipos de Menu
        1.0 = Opcoes principais
        2.0 = Opcoes de filtros
        3.0 = Opcoes de jogos
    """

    def __init__(self):
        self.quadro = Quadro()
        self.shape_quadro = (100, 100, 3)
        self.opcao_atual = 0
        # Tempo que precisa ficar com os dedos levantados ate coletar opcao (para evitar pegar opcao errada enquanto
        # estiver levantando)
        self.contador_delay_selec_opcao = 0
        self.delay_selec_opcao = 10

        self.menu_atual = 1.0

    def iniciar(self, shape=(480, 640, 3)):
        self.shape_quadro = shape
        self._gerar_menu(1.0)
        self.menu_atual = 1.0

    def continuar(self, contador_dedo, comando):
        if contador_dedo != 0 and contador_dedo == self.opcao_atual and comando == 0:
            # Permanecer tempo com dedo levantado ate adquirir opcao
            if self.contador_delay_selec_opcao < self.delay_selec_opcao:
                self.contador_delay_selec_opcao += 1
            else:
                # Menu principal
                if self.menu_atual == 1.0 and contador_dedo in [1, 2]:
                    if contador_dedo == 1:
                        self.menu_atual = 2.0
                        self._gerar_menu(self.menu_atual)
                    else:
                        self.menu_atual = 3.0
                        self._gerar_menu(self.menu_atual)
                # Menu de filtros
                elif self.menu_atual == 2.0 and contador_dedo in [1, 2, 3, 4, 5, 6]:
                    if contador_dedo == 6:
                        self.menu_atual = 1.0
                        self._gerar_menu(self.menu_atual)
                    else:
                        return 1
                # Menu de jogos
                elif self.menu_atual == 3.0 and contador_dedo in [1, 2, 6]:
                    if contador_dedo == 6:
                        self.menu_atual = 1.0
                        self._gerar_menu(self.menu_atual)
                    else:
                        return 1

                self.contador_delay_selec_opcao = -10
                return 0
        # Nao levantou dedo, mudou quantidade de dedos levantados ou acionou comando
        else:
            self.contador_delay_selec_opcao = 0
            self.opcao_atual = contador_dedo
        return 0

    def terminar(self):
        self.quadro.destruir()
        print('Opcao {} selecionada'.format(self.opcao_atual))
        return self.menu_atual, self.opcao_atual

    def _gerar_menu(self, tipo_menu):
        self.quadro.criar(self.shape_quadro)
        if tipo_menu == 1.0:
            self.quadro.escrever('Menu - Principal', (int(self.quadro.get_shape()[0] / 9), 50))
            self.quadro.escrever('1 - Filtros', (10, 110))
            self.quadro.escrever('2 - Jogos', (10, 170))
        elif tipo_menu == 2.0:
            self.quadro.escrever('Menu - Filtros', (int(self.quadro.get_shape()[0] / 6), 50))
            self.quadro.escrever('1 - Blur', (10, 110))
            self.quadro.escrever('2 - GaussianBlur', (10, 170))
            self.quadro.escrever('3 - MedianBlur', (10, 240))
            self.quadro.escrever('4 - Erode', (10, 300))
            self.quadro.escrever('5 - Dilate', (10, 360))
            self.quadro.escrever('6 - Voltar', (10, 420))
        elif tipo_menu == 3.0:
            self.quadro.escrever('Menu - Jogos', (int(self.quadro.get_shape()[0] / 5), 50))
            self.quadro.escrever('1 - Skier', (10, 110))
            self.quadro.escrever('2 - Car Race', (10, 170))
            self.quadro.escrever('6 - Voltar', (10, 420))
        self.quadro.mostrar()
