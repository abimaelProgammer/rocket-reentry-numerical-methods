import sys
import subprocess
import sympy as sp
from functions import *
#pacotes nessários para o projeto, caso não estejam instalados, o programa irá instalar automaticamente.

def baixar_pacotes():
    PACOTES_NECESSARIOS = ['sympy']
    for pacote in PACOTES_NECESSARIOS:
        try:
            __import__(pacote)
        except ImportError:
            print(f"📦 Biblioteca '{pacote}' não encontrada. Instalando...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])

def exibir_quadro(titulo, dados):
    print(f"\n{'='*30} {titulo} {'='*30}")
    print(f"{'Método':<18} | {'Raiz (d)':<12} | {'Erro':<12} | {'Iterações':<10} | {'Status'}")
    print("-" * 80)
    for d_linha in dados:
        status = "EXPLODE" if d_linha['d'] > 2.0 else "SEGURO"
        print(f"{d_linha['metodo']:<18} | {d_linha['d']:<12.6f} | {d_linha['erro']:<12.2e} | {d_linha['i']:<10} | {status}")

def main():
    baixar_pacotes()
    print("SISTEMA DE ANÁLISE DE REENTRADA - TEMA 1")
    
    try:
        n = int(input("Número de foguetes a testar: "))
        precisao = float(input("Precisão (ex: 0.00001): "))
        
        for k in range(n):
            a_val = float(input(f"\nValor de 'a' para o foguete {k+1}: "))
            intervalo = [2.0, 3.0]
            
            f_exp = funcao(a_val)
            df_exp = df(f_exp)
            f_num = sp.lambdify(sp.Symbol('d'), f_exp, "numpy")
            
            if not teste_bolzano(f_num, intervalo):
                print(f"⚠️ Raiz não está em [2, 3] para a={a_val}. Buscando novo intervalo...")
                intervalo = encontrar_intervalo(f_exp, sp.Symbol('d'))

            # Execução dos métodos
            res_bi = Bissecao(f_exp, intervalo, precisao)
            res_pf = PF(f_exp, intervalo, precisao)
            res_nr = NR(f_exp, df_exp, precisao, intervalo)

            # Preparação dos dados para os quadros
            dados_foguete = [
                {"metodo": "Bisseção", "d": res_bi[-1]['d'], "erro": res_bi[-1]['f(d)'], "i": res_bi[-1]['i']},
                {"metodo": "Posição Falsa", "d": res_pf[-1]['d'], "erro": res_pf[-1]['f(d)'], "i": res_pf[-1]['i']},
                {"metodo": "Newton-Raphson", "d": res_nr[-1]['d'], "erro": res_nr[-1]['f(d)'], "i": res_nr[-1]['i']}
            ]

            exibir_quadro(f"FOGUETE {k+1} (a={a_val})", dados_foguete)
            
    except Exception as e:
        print(f"Erro na execução: {e}")

if __name__ == "__main__":
    main()