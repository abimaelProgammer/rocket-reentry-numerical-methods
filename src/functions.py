import sympy as sp

d = sp.Symbol('d')

def f(a) -> sp.Function:
   return a*d - d*sp.ln(d)

def df(f) -> sp.Function:
    return sp.diff(f,d)

def Bissecao(f,I,erro) -> list:
    # Implente Aqui o Método da Bisseção! return([i,d] e tabela com i,di,f(di), |xi - xi|)
    pass

def PF(f,I,erro) -> list:
    # Implente Aqui o Método da Posição Falsa! return([i,d] e tabela com i,di,f(di), |xi - xi|)
    pass

def NR(f,df,erro) -> list:
    # Implente Aqui o Método da Posição Falsa! return([i,d] e tabela com i,di,f(di), |xi - xi|)
    pass