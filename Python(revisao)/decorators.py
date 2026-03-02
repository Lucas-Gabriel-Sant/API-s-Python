import functools

#altera o comportamento da função abaixo

def decorador(funcao):
    @functools.wraps(funcao)
    def func_roda_funcao():
        print('!!!!! Embrulhando função !!!!!')
        funcao()
        print('!!!!! Fechando embrulho !!!!!')
    return func_roda_funcao

@decorador
def uma_funcao():
    print('Está é uma função.')
uma_funcao()