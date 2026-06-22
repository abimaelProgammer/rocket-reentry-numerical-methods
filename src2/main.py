import functions
import LU

def resolver_LU_aux(matriz_A, vetor_f):
    n = 3
    L = [[0.0] * n for _ in range(n)]
    for i in range(n): L[i][i] = 1.0
    A_copia = [l[:] for l in matriz_A]
    f_copia = vetor_f[:]
    if LU.verificador(A_copia, n):
        for k in range(n - 1):
            if not LU.pivoteamento(k, n, f_copia, A_copia, L): return None
            LU.gauss(n, k, f_copia, A_copia, L)
        y, x = [0.0] * n, [0.0] * n
        LU.matriz_y(n, L, f_copia, y)
        LU.matriz_x(n, A_copia, y, x)
        return x
    return None

def main():
    A_original = [[3.0, -2.0, 1.0], [1.0, -3.0, 4.0], [9.0, 4.0, -5.0]]
    f_original = [8.0, 6.0, 11.0]
    
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
                print(f"| {cenario_str:<24} | {nome_metodo:<7} | {'Erro de Cálculo':^45} | {'FALHA':^11} |")
            else:
                sol_str = f"[{sol[0]:.6f}, {sol[1]:.6f}, {sol[2]:.6f}]"
                estourou = any(abs(v) > 2.0 for v in sol)
                status = "EXPLODIU" if estourou else "SEGURO"
                print(f"| {cenario_str:<24} | {nome_metodo:<7} | {sol_str:^45} | {status:^11} |")
            
            primeira_linha = False
        print("|" + "-"*26 + "|" + "-"*9 + "|" + "-"*47 + "|" + "-"*13 + "|")

    print("="*110)
    print(f"{'Critério de Segurança: Estabilidade garantida para |d| <= 2.000000 cm.':^110}")
    print("="*110)

if __name__ == "__main__":
    main()