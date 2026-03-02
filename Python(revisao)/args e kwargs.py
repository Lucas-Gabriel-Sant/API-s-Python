def soma_longa(arg1, arg2, arg3):
    return arg1 + arg2 + arg3
print(soma_longa(1, 2, 3))

def soma_lista(lista):
    return sum(lista)
print(soma_lista((2, 3, 4)))

#número indefinido de argumentos
def soma_simples(*args):
    return sum(args)
print(soma_simples(3, 4, 5))

# argumentos (lista) e argumentos com palavras chave (tupla)
#args sempre antes de kwargs
def met_kwargs(*args, **kwargs):
    print(args)
    print(kwargs)
met_kwargs(4, 'numeros aleatorios', 5, 6, nome='Josimar', peso='36 kg')