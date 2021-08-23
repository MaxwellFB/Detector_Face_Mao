"""Atividade para jogos"""

from .atividade import Atividade
try:
    from ..Jogos.Skier_Game_Like_Gym.Skier import Game
except ModuleNotFoundError:
    raise ModuleNotFoundError('Jogo "Skier_Game_Like_Gym" nao encontrado, favor baixar repositorio em: "https://github.com/MaxwellFB/Skier_Game_Like_Gym" e colocar dentro da pasta "Jogos".')


class Jogos(Atividade):
    def __init__(self):
        self.jogo = None
        self.opcao_selecionada = 0

    def iniciar(self, opcao_selecionada):
        """Armazena opcao selecionada e inicializa jogo"""
        self.opcao_selecionada = opcao_selecionada
        # Sckier
        if self.opcao_selecionada == 1:
            self.jogo = Game()
            self.jogo.start(keyboard_game=False, increase_speed=1, low_speed=6, max_speed=15)

    def continuar(self, marcas_corpo):
        """Realiza acoes no jogo"""
        if self.opcao_selecionada == 1:
            if marcas_corpo:
                # Esquerda
                if marcas_corpo.landmark[11].x < marcas_corpo.landmark[23].x:
                    self.jogo.step(1)
                # Direita
                elif marcas_corpo.landmark[12].x > marcas_corpo.landmark[24].x:
                    self.jogo.step(2)
                else:
                    self.jogo.step(0)
            else:
                print('Corpo nao identificado')

    def terminar(self):
        """Encerra o jogo"""
        self.jogo.quit()
