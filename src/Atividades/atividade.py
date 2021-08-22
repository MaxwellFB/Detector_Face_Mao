"""Classe abstrata para as atividades"""

from abc import ABC


class Atividade(ABC):
    def iniciar(self, *args, **kwargs):
        """O que sera feito quando a atividade for chamada pela primeira vez"""
        pass

    def continuar(self, *args, **kwargs):
        """O que sera feito enquanto estiver executando a atividade"""
        pass

    def terminar(self, *args, **kwargs):
        """O que sera feito quando deixar de ser executado a atividade"""
        pass
