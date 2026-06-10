EPS = 1e-12

# A.x = b
# A = L.U
# Ux = y
# Ly = b


def verificador(A, n):
    for i in range(n):
        if all(abs(A[i][j]) < EPS for j in range(n)):
            return False
    return True


def pivoteamento(k, n, b, A, L):
    maior = A[k][k]
    indice = k

    for i in range(k + 1, n):
        if abs(maior) < abs(A[i][k]):
            maior = A[i][k]
            indice = i

    # matriz singular detectada já no pivoteamento
    if abs(A[indice][k]) < EPS:
        return False

    if indice != k:
        # troca linhas em A
        for j in range(n):
            A[k][j], A[indice][j] = A[indice][j], A[k][j]

        # troca b
        b[k], b[indice] = b[indice], b[k]

        # troca as colunas já preenchidas de L (0 até k-1)
        for j in range(k):
            L[k][j], L[indice][j] = L[indice][j], L[k][j]

    return True


def gauss(n, k, b, A, L):
    for i in range(k + 1, n):
        coef = A[i][k] / A[k][k]
        for j in range(k, n):
            A[i][j] = A[i][j] - coef * A[k][j]

        # no LU o b não muda aqui
        L[i][k] = coef


def matriz_y(n, L, b, y):
    # L.y = b
    for i in range(n):
        soma = 0
        for j in range(i):
            soma += L[i][j] * y[j]
        y[i] = (b[i] - soma) / L[i][i]


def matriz_x(n, A, y, x):
    # U.x = y
    for i in range(n - 1, -1, -1):
        soma = 0
        for j in range(i + 1, n):
            soma += A[i][j] * x[j]
        x[i] = (y[i] - soma) / A[i][i]


def main():
    try:
        n = int(input("digite o numero de variáveis: "))
    except ValueError:
        print("Entrada inválida.")
        return

    if n <= 0:
        print("Número de variáveis inválido.")
        return

    A = [[0.0] * n for _ in range(n)]
    L = [[0.0] * n for _ in range(n)]

    b = [0.0] * n
    y = [0.0] * n
    x = [0.0] * n

    for i in range(n):
        for j in range(n):
            try:
                coef_a = float(input(f"digite o valor do coef a{i}{j}: "))
            except ValueError:
                print("Entrada inválida.")
                return
            A[i][j] = coef_a

    for i in range(n):
        try:
            B = float(input(f"digite o valor do coef b{i}: "))
        except ValueError:
            print("Entrada inválida.")
            return
        b[i] = B

    # verifica linhas nulas
    if not verificador(A, n):
        print("Linha nula detectada. Sistema inválido.")
        return

    # monta diagonal da matriz L
    for i in range(n):
        L[i][i] = 1

    # Fatoração LU com pivoteamento parcial
    for k in range(n - 1):
        if not pivoteamento(k, n, b, A, L):
            print("Matriz singular. Sistema não tem solução única.")
            return
        if abs(A[k][k]) < EPS:
            print("Matriz singular. Sistema não tem solução única.")
            return
        gauss(n, k, b, A, L)

    # verifica último pivô
    if abs(A[n-1][n-1]) < EPS:
        print("Matriz singular. Sistema não tem solução única.")
        return

    # resolve Ly = b
    matriz_y(n, L, b, y)

    # resolve Ux = y
    matriz_x(n, A, y, x)

    print("\nSolucao:")
    for i in range(n):
        print(f"x{i + 1} = {x[i]}")


if __name__ == "__main__":
    main()