import sys
import subprocess
PACOTES_NECESSARIOS = ['sympy']

for pacote in PACOTES_NECESSARIOS:
    try:
        __import__(pacote)
    except ImportError:
        print(f"📦 Biblioteca '{pacote}' não encontrada. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])
from functions import*

def main():
    print("Testando método da Bisseção original")
    fx = f(1)
    dfx = df(fx)
    print("f(d) = ",fx)
    print("\t",Bissecao(fx,[2,3],10**(-5))[1])
    print("Testando método da Posição Falsa")
    print("\t",PF(fx,[2,3],10**(-5))[1])
    print("Testando método de Newton-Raphson")
    print("\t",NR(fx,dfx,10**(-5))[1])
    print("Agora é sua vez!")
    while True:
        try:
            n = int(input("Digite o número de foguetes: "))
            F = []
            for _ in range(n):
                a = float(input("Digite o valor de a: "))
                fx = f(a)
                dfx = df(fx)
                I = [float(input("Digite o valor de I1: ")), float(input("Digite o valor de I2: "))]
                e = float(input("Digite o valor do erro: "))
                F.append((fx, dfx,I,e))
            for i, (fx, dfx, I, e) in enumerate(F):
                print(f"Foguete {i+1}:")
                print("f(d) = ",fx)
                print("\tBisseção:", Bissecao(fx, I, e)[0])
                print("\tPosição Falsa:", PF(fx, I, e)[0])
                print("\tNewton-Raphson:", NR(fx, dfx, e)[0])
        except ValueError:
            print("Valor inválido. Por favor, digite um número.")

if __name__ == "__main__":
    main()