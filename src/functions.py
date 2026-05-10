import sympy as sp

d = sp.Symbol('d')

def funcao(a) -> sp.Function:
   return a*d - d*sp.ln(d)

def df(f) -> sp.Function:
    return sp.diff(f,d)

def teste_bolzano(f_num, Intervalo):
    a, b = Intervalo[0], Intervalo[1]
    funcao_A = f_num(a)
    funcao_B = f_num(b)

    if funcao_A * funcao_B < 0:
        return True
    else:
        return False

def Bissecao(f, I, erro) -> list:
    # Implente Aqui o Método da Bisseção! return([i,d] e tabela com i,di,f(di), |xi - xi|)
    pass

def PF(f, I, erro) -> list:
    # Implente Aqui o Método da Posição Falsa! return([i,d] e tabela com i,di,f(di), |xi - xi|)
    pass

def NR(f, df, erro, Intervalo) -> list:
    func_numerica = sp.lambdify(d, f, "numpy")
    df_numerica = sp.lambdify(d, df, "numpy")
    x_atual = (Intervalo[0] + Intervalo[1]) / 2

    achou_raiz =  False
    tabela = []
    i = 0

    while not achou_raiz and i < 100:
        fx = func_numerica(x_atual)
        dfx = df_numerica(x_atual)

        tabela.append({
            "iteração" : i,
            "d" : x_atual,
            "f(d)" : fx
        })

        if abs(fx) < erro:
            achou_raiz = True
            
        elif abs(dfx) < 1e-12 :
            print("Erro: Derivada nula. O método divergiu.")
            achou_raiz = True
        else:
            x_novo = x_atual - (fx/dfx)
            
            if abs(x_novo - x_atual) < erro:
                x_atual = x_novo
                tabela.append({
                    "iteração" : i  + 1,
                    "d" : x_atual,
                    "f(d)" : func_numerica(x_atual)
                })    
                achou_raiz = True

            x_atual = x_novo
            i += 1

        if i >= 100:
            print("Aviso: Máximo de Iterações atingido")
            achou_raiz = True

    return tabela                