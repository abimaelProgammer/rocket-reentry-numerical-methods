import subprocess
import sys
PACOTES_NECESSARIOS = ['numpy']
for pacote in PACOTES_NECESSARIOS:
    try:
        __import__(pacote)
    except ImportError:
        print(f"📦 Biblioteca '{pacote}' não encontrada. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])

import functions
import numpy as np
import LU


def resolver_LU_aux(matriz_A, vetor_f):
    # CORREÇÃO: 'n' passa a ser dinâmico com base no tamanho da matriz inserida
    n = len(matriz_A)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n): L[i][i] = 1.0
    A_copia = [l[:] for l in matriz_A]
    f_copia = vetor_f[:]
    
    if LU.verificador(A_copia, n):
        for k in range(n - 1):
            if not LU.pivoteamento(k, n, f_copia, A_copia, L): 
                return None
            LU.gauss(n, k, f_copia, A_copia, L)
        
        y, x = [0.0] * n, [0.0] * n
        LU.matriz_y(n, L, f_copia, y)
        LU.matriz_x(n, A_copia, y, x)
        return x
    return None

def capturar_dados_usuario():
    print("\n--- INSERÇÃO DE DADOS PERSONALIZADOS (Matriz 3x3) ---")
    print("Digite as linhas da Matriz A separando os elementos por espaço:")
    A_user = []
    for i in range(3):
        linha = list(map(float, input(f"Linha {i+1}: ").split()))
        if len(linha) != 3:
            print("Erro: A linha precisa ter exatamente 3 elementos.")
            return None, None
        A_user.append(linha)
        
    print("\nDigite os 3 elementos do vetor f separados por espaço:")
    f_user = list(map(float, input("Vetor f: ").split()))
    if len(f_user) != 3:
        print("Erro: O vetor f precisa ter exatamente 3 elementos.")
        return None, None
        
    return A_user, f_user

def imprimir_tabela(cenarios):
    print("\n" + "="*110)
    print(f"{'QUADRO COMPARATIVO DE VARIAÇÕES - SENSIBILIDADE':^110}")
    print("="*110)
    print(f"| {'Cenário':<24} | {'Método':<7} | {'Vetor de Deslocamentos {d} em cm':^45} | {'Status':^11} |")
    print("|" + "-"*26 + "|" + "-"*9 + "|" + "-"*47 + "|" + "-"*13 + "|")

    for nome_cenario, metodos in cenarios.items():
        primeira_linha = True
        for nome_metodo, sol in metodos.items():
            cenario_str = nome_cenario if primeira_linha else ""
            
            if not sol:
                print(f"| {cenario_str:<24} | {nome_metodo:<7} | {'Erro de Cálculo (Singular/Pivô)':^45} | {'FALHA':^11} |")
            else:
                sol_str = f"[{sol[0]:.6f}, {sol[1]:.6f}, {sol[2]:.6f}]"
                estourou = any(abs(v) > 2.0 for v in sol) # Verifica limite de explosão
                status = "EXPLODIU" if estourou else "SEGURO"
                print(f"| {cenario_str:<24} | {nome_metodo:<7} | {sol_str:^45} | {status:^11} |")
            
            primeira_linha = False
        print("|" + "-"*26 + "|" + "-"*9 + "|" + "-"*47 + "|" + "-"*13 + "|")

    print("="*110)
    print(f"{'Critério de Segurança: Estabilidade garantida para |d| <= 2.000000 cm.':^110}")
    print("="*110)

def main():
    print("=" * 60)
    print("     SISTEMA DE ANÁLISE ESTRUTURAL DO FOGUETE")
    print("=" * 60)
    print("Opção 1 - Executar Quadro de Testes Padrão (Cenários 0 a 3)")
    print("Opção 2 - Inserir Variação Personalizada via Teclado")

    opcao = input("\nEscolha uma opção (1 ou 2): ").strip()

    A_original = [[3.0, -2.0, 1.0], [1.0, -3.0, 4.0], [9.0, 4.0, -5.0]]
    f_original = [8.0, 6.0, 11.0]

    if opcao == "1":
        f_c1 = [16.0, 12.0, 22.0] 
        A_c2 = [[1.0, -2.0, 1.0], [1.0, -1.0, 4.0], [9.0, 4.0, -5.0]]

        # Dicionário para guardar as soluções de todos os métodos em cada cenário
        cenarios = {
            "0. Caso Padrão": {
                "Gauss": functions.eliminacao_gaussiana(3, [l[:] for l in A_original], f_original[:]),
                "LU":    resolver_LU_aux(A_original, f_original),
                "LDP":   functions.LDP(3, [l[:] for l in A_original], f_original[:])
            },
            "1. Força Dobrada - (f)": {
                "Gauss": functions.eliminacao_gaussiana(3, [l[:] for l in A_original], f_c1[:]),
                "LU":    resolver_LU_aux(A_original, f_c1),
                "LDP":   functions.LDP(3, [l[:] for l in A_original], f_c1[:])
            },
            "2. Rigidez Menor - [A]": {
                "Gauss": functions.eliminacao_gaussiana(3, [l[:] for l in A_c2], f_original[:]),
                "LU":    resolver_LU_aux(A_c2, f_original),
                "LDP":   functions.LDP(3, [l[:] for l in A_c2], f_original[:])
            },
            "3. Caso Extremo -(f)/[A]": {
                "Gauss": functions.eliminacao_gaussiana(3, [l[:] for l in A_c2], f_c1[:]),
                "LU":    resolver_LU_aux(A_c2, f_c1),
                "LDP":   functions.LDP(3, [l[:] for l in A_c2], f_c1[:])
            }
        }
        imprimir_tabela(cenarios)

    elif opcao == "2": #entrada personalizada de [A] e (f)
        A_user, f_user = capturar_dados_usuario()
        if A_user is not None and f_user is not None:
            cenarios = {
                "Usuário: Personalizado": {
                    "Gauss": functions.eliminacao_gaussiana(3, [l[:] for l in A_user], f_user[:]),
                    "LU":    resolver_LU_aux(A_user, f_user),
                    "LDP":   functions.LDP(3, [l[:] for l in A_user], f_user[:])
                }
            }
            imprimir_tabela(cenarios)
    else:
        print("Opção Inválida! Finalizando programa...")

if __name__ == "__main__":
    main()