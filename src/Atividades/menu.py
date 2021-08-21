"""Atividade para manipular quadro de opcoes (menu)"""

from .atividade import Atividade
from ..quadro import Quadro


class Menu(Atividade):
    def __init__(self):
        self.quadro = Quadro()
        self.opcao_atual = 0
        # Tempo que precisa ficar com os dedos levantados ate coletar opcao (para evitar pegar opcao errada enquanto
        # estiver levantando)
        self.contador_delay_selec_opcao = 0
        self.delay_selec_opcao = 10

    def iniciar(self, img):
        self.quadro.criar(img)
        self.quadro.escrever('Menu', (int(self.quadro.get_shape()[0] / 2), 50))
        self.quadro.escrever('1 - Blur', (10, 110))
        self.quadro.escrever('2 - GaussianBlur', (10, 170))
        self.quadro.escrever('3 - MedianBlur', (10, 240))
        self.quadro.escrever('4 - Erode', (10, 300))
        self.quadro.escrever('5 - Dilate', (10, 360))
        # TODO: Separar corpo do menu
        # self.quadro.escrever('6 - Corpo', (10, 420))
        self.quadro.mostrar()

    def continuar(self, contador_dedo, comando):
        if contador_dedo != 0 and contador_dedo == self.opcao_atual and comando == 0:
            # Permanecer tempo com dedo levantado ate adquirir opcao
            if self.contador_delay_selec_opcao < self.delay_selec_opcao:
                self.contador_delay_selec_opcao += 1
            else:
                return 1
        # Nao levantou dedo, mudou quantidade de dedos levantados ou acionou comando
        else:
            self.contador_delay_selec_opcao = 0
            self.opcao_atual = contador_dedo
        return 0

    def terminar(self):
        self.quadro.destruir()
        print('Opcao {} selecionada'.format(self.opcao_atual))
        return self.opcao_atual