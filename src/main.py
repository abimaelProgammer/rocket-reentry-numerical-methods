import sys
import subprocess
import sympy as sp 
from functions import * 
d = sp.Symbol('d')


PACOTES_NECESSARIOS = ['sympy']

#pacotes nessários para o projeto, caso não estejam instalados, o programa irá instalar automaticamente.
for pacote in PACOTES_NECESSARIOS:
    try:
        __import__(pacote)
    except ImportError:
        print(f"📦 Biblioteca '{pacote}' não encontrada. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])
from functions import*

def main():
    print("Testando método da Bisseção original")
    fx = funcao(1) # função para a = 1
    dfx = df(fx)   # derivada da função para a = 1  
    
    Bi = Bissecao(fx,[2,3],10**(-5))[-1] # resultado final do método da bisseção para a = 1, intervalo [2,3] e erro de 10^(-5)
    
    print(f"Método da Bisseção: f(d) = {fx}")
    print(f"\t i | a       | f(a)    | b       | f(b)      | d        |   f(d)    | |b-a|")
    print(f"\t{Bi['i']} |{Bi['a']:.6f} |{Bi['fa']:.2e} |{Bi['b']:.6f} | {Bi['fb']:.2e} | {Bi['d']:.6f} | {Bi['fx']:.2e} | {Bi['|b-a|']:.2e}\n")

    print(f"Testando método da Posição Falsa: f(d) = {fx}")
    PF_result = PF(fx,[2,3],10**(-5))[-1] # resultado final do método da posição falsa para a = 1, intervalo [2,3] e erro de 10^(-5)
    
    print(f"\t i | a       | f(a)    | b       | f(b)      | d        |   f(d)    | |b-a|")
    print(f"\t{PF_result['i']} |{PF_result['a']:.6f} |{PF_result['fa']:.2e} |{PF_result['b']:.6f} | {PF_result['fb']:.2e} | {PF_result['d']:.6f} | {PF_result['fx']:.2e} | {PF_result['|b-a|']:.2e}\n")

    print(f"Testando método de Newton-Raphson: f(d) = {fx}")
    NR_result = NR(fx,dfx,10**(-5),[2,3])[-1] # resultado final do método de Newton-Raphson para a = 1 e erro de 10^(-5)

    print(f"\t i | d       | f(d)")
    print(f"\t{NR_result['iteração']} |{NR_result['d']:.6f} |{NR_result['f(d)']:.2e}\n")
   
    print("Agora é sua vez!")
    while True:
        try:
            n = int(input("Digite o número de foguetes: "))
            F = []

            for _ in range(n):
                a = float(input("Digite o valor de a: "))
                fx = funcao(a)
                dfx = df(fx)
                int_inf = float(input("Digite o início do intervalo: "))
                int_sup = float(input("Digite o fim do intervalo: "))
                I = [int_inf, int_sup]
                e = float(input("Digite o valor do erro: "))
                F.append((fx, dfx,I,e))

            for i, (fx, dfx, I, e) in enumerate(F):
                print(f"\n Foguete {i+1}: | f(d) = {fx} | Intervalo: {I} | Erro: {e}")
                
                f_num = sp.lambdify(d, fx, "numpy")

                #teste da raiz
                if teste_bolzano(f_num, I):
                    Bi = Bissecao(fx, I, e)[-1]
                    Pf = PF(fx, I, e)[-1]
                    NRr = NR(fx, dfx, e, I)[-1] 

                    print(f"\tMétodo da Bisseção: d = {Bi['d']:.6f}, f(d) = {Bi['fx']:.2e}")
                    print(f"\tPosição Falsa:      d = {Pf['d']:.6f}, f(d) = {Pf['fx']:.2e}")
                    print(f"\tNewton-Raphson:     d = {NRr['d']:.6f}, f(d) = {NRr['f(d)']:.2e}")
                else:
                    print(f"\t ERRO: O intervalo {I} não é válido (f(a) e f(b) têm o mesmo sinal).")

        except ValueError:
            print(" Erro: Por favor, digite apenas números válidos.")
if __name__ == "__main__":
    main()