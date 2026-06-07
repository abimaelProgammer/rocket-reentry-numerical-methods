def eliminacao_gaussiana(n,A,b):
    try:
        for k in range(0,n-1):
            for i in range(k+1,n):
                m = -A[i][k]/A[k][k]
                A[i][k] = 0
                for j in range(k+1,n):
                    A[i][j] = A[i][j] + m*A[k][j]
                b[i] = b[i] + m*b[k]
        x = substituicao_Retroativa(n,A,b)
        return x
    except ZeroDivisionError:
        print("Erro: Divisão por zero. O sistema pode ser indeterminado ou impossível.")
        return pivotacao(n,A,b)

def substituicao_Retroativa(n,A,b):
    try:
        x = [0]*n
        x[n-1] = b[n-1]/A[n-1][n-1]
        for i in range(n-2,-1,-1):
            soma = 0
            for j in range(i+1,n):
                soma = soma + A[i][j]*x[j]
            x[i] = (b[i] - soma)/A[i][i]
        return x
    except ZeroDivisionError:
        print("Erro: Divisão por zero. O sistema pode ser indeterminado ou impossível.")
        return None
   
def substituicao_Progressiva(n,A,b):
    try:
        x = [0]*n
        x[0] = b[0]/A[0][0]
        for i in range(1,n):
            soma = 0
            for j in range(i):
                soma = soma + A[i][j]*x[j]
            x[i] = (b[i] - soma)/A[i][i]
        return x
    except ZeroDivisionError:
        print("Erro: Divisão por zero. O sistema pode ser indeterminado ou impossível.")
        return None

def pivotacao(n,A,b):
    for k in range(0,n-1):
        max_index = k
        for i in range(k+1,n):
            if abs(A[i][k]) > abs(A[max_index][k]):
                max_index = i
        if max_index != k:
            A[k], A[max_index] = A[max_index], A[k]
            b[k], b[max_index] = b[max_index], b[k]
    return eliminacao_gaussiana(n,A,b)

def LDU(n,A):
    pass

def LDP(n, A, f):
    # Presumindo que sua função LDU retorne as matrizes L, D e U corretamente
    matrizes = LDU(n, A)
    L = matrizes[0]
    D = matrizes[1]
    U = matrizes[2]
    
    # 1. Pegando a inversa de D (apenas a diagonal importa)
    D_inv = [[0]*n for _ in range(n)]
    for i in range(n):
        D_inv[i][i] = 1.0 / D[i][i]
        
    # 2. Construindo a matriz P (P = D_inv * U)
    P = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            P[i][j] = D_inv[i][i] * U[i][j]
            
    # 3. Achando y: Ly = f (Substituição Progressiva / Avanço)
    y = substituicao_Progressiva(n, L, f)
    
    # 4. Achando z: Dz = y (Divisão direta, pois D é diagonal)
    z = [0] * n
    for i in range(n):
        z[i] = y[i] / D[i][i]
        
    # 5. Achando d: Pd = z (Substituição Regressiva / Retroativa)
    # Nota: Certifique-se de passar n, P e z para a sua função de substituição para trás
    d = substituicao_Retroativa(n, P, z)
    
    return d

def main():
    A = [[3, 2, 4], [0, 1/3, 2/3], [0, 0, -8]]
    b = [1, 5/3, 0]
    n = len(A)
    x = eliminacao_gaussiana(n, A, b)
    print("Solução do sistema: ", x)

if __name__ == "__main__":
    main() 