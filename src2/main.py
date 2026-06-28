import functions
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


def modo_interativo():
    print("\n--- ENTRADA DE DADOS (Tema 1) ---")
    try:
        n = int(input("Introduza o número de deslocamentos (n): "))
        if n <= 0:
            print("Número inválido.")
            return

        A = []
        print("Introduza os valores da matriz de propriedades [A]:")
        for i in range(n):
            linha = []
            for j in range(n):
                val = float(input(f"A[{i+1}][{j+1}]: "))
                linha.append(val)
            A.append(linha)

        f = []
        print("Introduza os valores do vetor de forças {f}:")
        for i in range(n):
            val = float(input(f"f[{i+1}]: "))
            f.append(val)

        print("\n--- RESULTADOS ---")
        
        # Alínea a) Método LU Normal
        d_lu = resolver_LU_aux(A, f)
        print("Método LU Normal:")
        if d_lu:
            print(f"Vetor {{d}} = {[round(val, 6) for val in d_lu]}")
        else:
            print("Falha na resolução (matriz singular).")

        # Alínea b) Método LDP
        print("\nMétodo Fatoração LDP:")
        try:
            d_ldp = functions.LDP(n, [l[:] for l in A], f[:])
            print(f"Vetor {{d}} = {[round(val, 6) for val in d_ldp]}")
        except Exception as e:
            print(f"Falha na resolução LDP: {e}")
            d_ldp = None

        # Alínea e) Análise do Foguetão (Limite de 2cm em módulo)
        print("\n--- ANÁLISE DO FOGUETÃO ---")
        d_final = d_lu if d_lu else d_ldp
        if d_final:
            estourou = False
            for i, deslocamento in enumerate(d_final):
                if abs(deslocamento) > 2.0:
                    estourou = True
                    print(f"ALERTA: Deslocamento d{i+1} = {abs(deslocamento):.4f} cm excede o limite de 2 cm!")
            
            if estourou:
                print("ESTADO: EXPLODIU! Ocorreram danos gigantescos.")
            else:
                print("ESTADO: SEGURO! Todos os deslocamentos estão dentro do limite tolerável.")

    except ValueError:
        print("Erro: Introduziu um valor inválido.")


def modo_calibracao():
    # Alínea c) Calibração com os valores padrão
    A_original = [[3.0, -2.0, 1.0], [1.0, -3.0, 4.0], [9.0, 4.0, -5.0]]
    f_original = [8.0, 6.0, 11.0]
    
    # Alínea d) Variação dos valores de [A] e {f} para o quadro resposta
    f_c1 = [16.0, 12.0, 22.0] 
    A_c2 = [[1.0, -2.0, 1.0], [1.0, -1.0, 4.0], [9.0, 4.0, -5.0]]

    cenarios = {
        "0. Caso Padrão (Alínea C)": {
            "LU":    resolver_LU_aux(A_original, f_original),
            "LDP":   functions.LDP(3, [l[:] for l in A_original], f_original[:])
        },
        "1. Força Dobrada {f}": {
            "LU":    resolver_LU_aux(A_original, f_c1),
            "LDP":   functions.LDP(3, [l[:] for l in A_original], f_c1[:])
        },
        "2. Rigidez Menor [A]": {
            "LU":    resolver_LU_aux(A_c2, f_original),
            "LDP":   functions.LDP(3, [l[:] for l in A_c2], f_original[:])
        },
        "3. Caso Extremo": {
            "LU":    resolver_LU_aux(A_c2, f_c1),
            "LDP":   functions.LDP(3, [l[:] for l in A_c2], f_c1[:])
        }
    }

    print("\n" + "="*105)
    print(f"{'QUADRO RESPOSTA - VARIAÇÕES DE [A] E {f} (Tema 1 - Alínea D e E)':^105}")
    print("="*105)
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

    print("="*105)
    print(f"{'Critério de Segurança: Estabilidade garantida para |d| <= 2.000000 cm.':^105}")
    print("="*105)


def main():
    while True:
        print("\n=== MENU PRINCIPAL - TEMA 1 (Reentrada do Foguetão) ===")
        print("1. Introduzir dados dinâmicos do sistema (Alíneas A, B e Entrada de Dados)")
        print("2. Executar calibração e quadro resposta (Alíneas C, D, E)")
        print("0. Sair")
        
        escolha = input("Selecione uma opção: ")
        
        if escolha == '1':
            modo_interativo()
        elif escolha == '2':
            modo_calibracao()
        elif escolha == '0':
            print("A encerrar o programa...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()