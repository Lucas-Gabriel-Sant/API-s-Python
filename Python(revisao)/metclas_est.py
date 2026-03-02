import datetime

class Funcionario():
    aumento = 1.04

    def __init__(self, nome, salario):
        self.nome = nome
        self.salario = salario

    def dados(self):
        return {'nome': self.nome, 'salário': self.salario}

    def aumentar_salario(self):
        self.salario *= self.aumento

    # Muda o atributo aumento da classe Funcionario
    @classmethod
    def novo_aumento(cls, novo_aumento):
        cls.aumento = novo_aumento

    @staticmethod
    def dia_util(dia):
        if dia.weekday() == 5 or dia.weekday() == 6:
            print('Descanso')
            return False
        print('Dia útil')
        return True

junior = Funcionario('Júnior', 4000)
print(junior.dados())
Funcionario.novo_aumento(1.08)
junior.aumentar_salario()
print(junior.dados())

data= datetime.date(2026, 1, 14)
Funcionario.dia_util(data)
