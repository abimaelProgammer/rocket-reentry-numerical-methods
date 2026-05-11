import sympy as sp
import numpy as np

d = sp.Symbol('d')

def funcao(a_param) -> sp.Function:
    # f(d) = a*d - d*ln(d)
    return a_param*d - d*sp.ln(d)

def df(f) -> sp.Function:
    return sp.diff(f, d)

def teste_bolzano(f_num, Intervalo):
    a, b = Intervalo[0], Intervalo[1]
    if f_num(a) * f_num(b) < 0:
        return True
    return False

def Bissecao(f, I, erro) -> list:
    f_num = sp.lambdify(d, f, "numpy")
    a, b = I[0], I[1]
    tabela = []
    i = 0
    
    while abs(b - a) > erro:
        x = (a + b) / 2
        fx = f_num(x)
        tabela.append({"i": i, "d": x, "f(d)": fx, "erro": abs(b - a)})
        
        if abs(fx) < erro: break
        if f_num(a) * fx < 0:
            b = x
        else:
            a = x
        i += 1
        if i > 100: break
    return tabela

def PF(f, I, erro) -> list:
    """Implementação do Método da Posição Falsa"""
    f_num = sp.lambdify(d, f, "numpy")
    a, b = I[0], I[1]
    tabela = []
    i = 0
    x = a # valor inicial
    
    while True:
        fa, fb = f_num(a), f_num(b)
        # Fórmula da Posição Falsa
        x_novo = (a * fb - b * fa) / (fb - fa)
        fx_novo = f_num(x_novo)
        
        erro_at = abs(x_novo - x) if i > 0 else abs(b - a)
        tabela.append({"i": i, "d": x_novo, "f(d)": fx_novo, "erro": erro_at})
        
        if abs(fx_novo) < erro or i > 100:
            break
            
        if fa * fx_novo < 0:
            b = x_novo
        else:
            a = x_novo
        x = x_novo
        i += 1
    return tabela

def NR(f, df_f, erro, I) -> list:
    f_num = sp.lambdify(d, f, "numpy")
    df_num = sp.lambdify(d, df_f, "numpy")
    x = (I[0] + I[1]) / 2 # Chute inicial no meio do intervalo
    tabela = []
    
    for i in range(100):
        fx = f_num(x)
        dfx = df_num(x)
        tabela.append({"i": i, "d": x, "f(d)": fx, "erro": fx}) # Simplificado
        
        if abs(fx) < erro: break
        if abs(dfx) < 1e-12: break
        
        x_prox = x - (fx / dfx)
        if abs(x_prox - x) < erro:
            x = x_prox
            break
        x = x_prox
    return tabela

def encontrar_intervalo(f, d_sir, chute_inicial=0.5, passo=0.5):
    """
    Procura automaticamente um intervalo [a, b] onde f(a) * f(b) < 0.
    Útil quando o parâmetro 'a' muda e a raiz se desloca.
    """
    f_num = sp.lambdify(d, f, "numpy")
    a = chute_inicial
    
    for _ in range(50): # Tenta 50 vezes expandir a busca
        b = a + passo
        try:
            if f_num(a) * f_num(b) < 0:
                return [a, b]
        except:
            pass # Evita erros com ln(d) para d <= 0
        a = b
    return None