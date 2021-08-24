"""Atividade para jogos"""

from .atividade import Atividade
import numpy as np
try:
    from ..Jogos.Skier_Game_Like_Gym.Skier import Game
except ModuleNotFoundError:
    raise ModuleNotFoundError('Jogo "Skier_Game_Like_Gym" nao encontrado, favor baixar repositorio em: "https://github.com/MaxwellFB/Skier_Game_Like_Gym" e colocar dentro da pasta "Jogos".')
try:
    from ..Jogos.Car_Race_Game_Like_Gym.car_race import CarRacing
except ModuleNotFoundError:
    raise ModuleNotFoundError('Jogo "Car_Race_Game_Like_Gym" nao encontrado, favor baixar repositorio em: "https://github.com/MaxwellFB/Car_Race_Game_Like_Gym" e colocar dentro da pasta "Jogos".')


class Jogos(Atividade):
    def __init__(self):
        self.jogo = None
        self.opcao_selecionada = 0
        self.shape_image = 0

    def iniciar(self, opcao_selecionada, shape_image):
        """Prepara e inicializa jogo"""
        self.opcao_selecionada = opcao_selecionada
        self.shape_image = shape_image
        # Sckier
        if self.opcao_selecionada == 1:
            self.jogo = Game()
            self.jogo.start(keyboard_game=False, increase_speed=1, low_speed=6, max_speed=15)
        # Car Race
        elif self.opcao_selecionada == 2:
            self.divisoria1 = int(self.shape_image[1] / 3) / self.shape_image[1]
            self.divisoria2 = self.divisoria1 * 2

            self.jogo = CarRacing(keyboard_game=False, increase_speed=1, low_enemy_car_speed=31, max_enemy_car_speed=38) #5 11
            self.jogo.start()

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
        elif self.opcao_selecionada == 2:
            if marcas_corpo:
                contador_divisorias = [0, 0, 0]
                # Esquerda
                for marca in marcas_corpo.landmark:
                    # Esquerda
                    print(marca.x)
                    if marca.x < self.divisoria1:
                        contador_divisorias[0] += 1
                    # Meio
                    elif marca.x >= self.divisoria1 and marca.x < self.divisoria2:
                        contador_divisorias[1] += 1
                    # Direita
                    elif marca.x >= self.divisoria2:
                        contador_divisorias[2] += 1
                # Realiza acao onde maior parte do corpo estiver
                self.jogo.step(np.argmax(contador_divisorias))
            else:
                print('Corpo nao identificado')

    def terminar(self):
        """Encerra o jogo"""
        self.jogo.quit()
