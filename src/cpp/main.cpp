// Preparacao do ambiente
#include <iostream>
#include <cmath>
#include <iomanip>
using namespace std;

// Definicao da funcao: f(x) = c*x - x*ln(x)
double funcao(double x, double c){
    /*
    Args:
        x (double): Variavel da funcao, indica deslocamento em cm
        c (double): Coeficiente constante, indica parametro de ajuste
    Returns:
        double: Resultado da funcao
    */
    if (x <= 0) return NAN;
    return c*x - x*log(x); 
}

// Definicao da derivada da funcao: f'(x) = c - ln(x) - 1
double derivada(double x, double c){
    /*
    Args:
        x (double): Variavel da funcao, indica deslocamento em cm
        c (double): Coeficiente constante, indica parametro de ajuste
    Returns:
        double: Resultado da funcao
    */
    if (x <= 0) return NAN;
    return c - log(x) - 1;
}

// Metodo da Bissecao
double bissecao(double a, double b, double tol, double c, int &iter){
    /*
    Args:
        a (double): Limite inferior do intervalo;
        b (double): Limite superior do intervalo;
        tol (double): Tolerancia;
        c (double): Constante da funcao;
        iter (ponteiro pra int): Armazena numero de iteracoes
    Returns:
        double: Raiz aproximada
    */
    double fa = funcao(a, c);
    double fb = funcao(b, c);
    double x  = (a + b) / 2;
    double fx = funcao(x, c);
    
    iter = 0;

    if (fa * fb > 0) {
        cout << "[ERRO Bissecao]: O intervalo nao isola uma raiz.\n";
        return NAN;
    }

    while (fabs(b - a) > tol && fabs(fx) > tol) {
        x = (a + b) / 2;
        fx = funcao(x, c);

        if (fx * fa > 0) {
            fa = fx;
            a = x;
        } else {
            fb = fx;
            b = x;
        }

        iter++;
    }

    return (a + b) / 2;
}

// Metodo da Posicao Falsa 
double falsa(double a, double b, double tol, double c, int &iter){
    /*
    Args:
        a (double): Limite inferior do intervalo;
        b (double): Limite superior do intervalo;
        tol (double): Tolerancia;
        c (double): Constante da funcao;
        iter (ponteiro pra int): Armazena numero de iteracoes
    Returns:
        double: Raiz aproximada
    */
    double fa = funcao(a, c);
    double fb = funcao(b, c);
    double x, fx;

    iter = 0;

    if (fa * fb > 0) {
        cout << "[ERRO Posicao Falsa]: O intervalo nao isola uma raiz.\n";
        return NAN;
    }

    do {
        x = (a*(fb) - b*(fa)) / (fb - fa);
        fx = funcao(x, c);
        if (fx * fa > 0) {
            fa = fx;
            a = x;
        } else {
            fb = fx;
            b = x;
        }
        iter++;
    } while (fabs(fx) > tol && fabs(b - a) > tol);

    return x;
}

// Metodo de Newton-Raphson
double newton(double a, double b, double tol, double c, int &iter){
    /*
    Args:
        a (double): Limite inferior do intervalo;
        b (double): Limite superior do intervalo;
        tol (double): Tolerancia;
        c (double): Constante da funcao;
        iter (ponteiro pra int): Armazena numero de iteracoes
    Returns:
        double: Raiz aproximada
    */
    double x = (a + b) / 2; // Ponto inicial: meio do intervalo
    double xant = x + 2*tol;
    double fx = funcao(x, c);
    int maxIter = 100;

    iter = 0;

    while (fabs(fx) > tol && fabs(xant - x) > tol && iter < maxIter){    
        if (fabs(derivada(x, c)) < 1e-10){
            cout << "[AVISO Newton]: Derivada proxima de zero na iteracao " << iter << ".\n";
            break;
        }

        xant = x;
        x = x - funcao(x, c) / derivada(x, c);
        fx = funcao(x, c);

        iter++;
    }

    return x;
}

// Metodo da Secante 
double secante(double a, double b, double tol, double c, int &iter){
    /*
    Args:
        a (double): Limite inferior do intervalo;
        b (double): Limite superior do intervalo;
        tol (double): Tolerancia;
        c (double): Constante da funcao;
        iter (ponteiro pra int): Armazena numero de iteracoes
    Returns:
        double: Raiz aproximada
    */
    double x = (a + b) / 2;
    double xant = x + 2*tol;

    double fx = funcao(x,c);
    double xantf = funcao(xant, c);

    iter = 0;

    while (fabs(fx) > tol && fabs(xant - x) > tol){

        if (fabs(fx - xantf) < 1e-12){
            break;
        }

        double aux = x;
        double auxf = fx;

        x = x - fx*((x - xant) / (fx - xantf));

        if (x <= 0){
            break;
        }

        xant = aux;
        xantf = auxf;

        fx = funcao(x, c);

        iter++;
    }

    return x;
}

// Imprime texto alinhado em uma coluna de largura fixa
void imprimirColuna(string texto, int largura) {
    cout << texto;

    int espacos = largura - texto.length();

    for (int i = 0; i < espacos; i++) {
        cout << " ";
    }
}

// Converte double para string com numero limitado de casas decimais
string formatarDouble(double valor, int casas) {
    if (isnan(valor)) return "---";

    string texto = to_string(valor);

    int pos = texto.find(".");

    if (pos != -1) {
        texto = texto.substr(0, pos + casas + 1);
    }

    return texto;
}

// Imprime uma linha separadora
void imprimirLinhaSeparadora() {
    cout << "------------------------------------------------------------------------------------------\n";
}

// Imprime o cabecalho da tabela
void imprimirCabecalhoTabela() {
    cout << "\n-- Tabela de Resultados ------------------------------------------------------------------\n";

    imprimirColuna("a", 12);
    imprimirColuna("Metodo", 22);
    imprimirColuna("Raiz", 18);
    imprimirColuna("Erro", 18);
    imprimirColuna("Iteracoes", 12);
    imprimirColuna("Status", 12);

    cout << endl;
    imprimirLinhaSeparadora();
}

// Imprime uma linha da tabela
void imprimirLinhaTabela(
    double a,
    string metodo,
    double raiz,
    double erro,
    int iteracoes,
    string status
) {
    imprimirColuna(formatarDouble(a, 5), 12);
    imprimirColuna(metodo, 22);
    imprimirColuna(formatarDouble(raiz, 8), 18);
    imprimirColuna(formatarDouble(erro, 8), 18);
    imprimirColuna(to_string(iteracoes), 12);
    imprimirColuna(status, 12);

    cout << endl;
}

string verificarStatus(double raiz) {
    if (isnan(raiz)) {
        return "Erro: sem raiz";
    }

    if (isinf(raiz)) {
        return "Erro: infinito";
    }

    if (raiz <= 0) {
        return "Erro: d invalido";
    }

    if (raiz > 2.0) {
        return "Explode";
    }

    return "Seguro";
}

int main(){

    cout << "\n-- Aproximador de Raizes ------------------------------------------------------------------\n";
    cout << "Funcao a ser aproximada: f(d) = a*d - d*ln(d)\n";
    cout << "Limite de seguranca do deslocamento: 2 cm\n";
    cout << "Digite os parametros solicitados:\n";

    double a, b;
    cout << "- Extremidades do isolamento [a, b]: ";
    cin >> a >> b;

    if (a <= 0 || b <= 0){
        cout << "[ERRO] O intervalo escolhido nao e valido." << endl;
        return 0;
    }

    int n;
    cout << "- Numero de foguetes (n): ";
    cin >> n;

    double tol;
    cout << "- Valor da precisao (tol): ";
    cin >> tol;

    // Arrays para guardar resultados
    double coefs[n], R1[n], R2[n], R3[n], R4[n];
    double E1[n], E2[n], E3[n], E4[n];
    int IT1[n], IT2[n], IT3[n], IT4[n];
    cout << fixed << setprecision(6);

    for (int i = 0; i < n; i++) {
        cout << "Digite coeficiente a do foguete " << i + 1 << ": ";
        cin >> coefs[i];
 
        double y = coefs[i];

        if (funcao(a, y) * funcao(b, y) > 0) {
            cout << "[ERRO]: O intervalo nao isola uma raiz." << endl;

            R1[i] = R2[i] = R3[i] = R4[i] = NAN;
            E1[i] = E2[i] = E3[i] = E4[i] = NAN;
            IT1[i] = IT2[i] = IT3[i] = IT4[i] = 0;

            continue;
        }

        double real = exp(y); // Solucao exata

        R1[i] = bissecao(a, b, tol, y, IT1[i]);
        R2[i] = falsa(a, b, tol, y, IT2[i]);
        R3[i] = newton(a, b, tol, y, IT3[i]);
        R4[i] = secante(a, b, tol, y, IT4[i]);

        E1[i] = isnan(R1[i]) ? NAN : fabs(R1[i] - real);
        E2[i] = isnan(R2[i]) ? NAN : fabs(R2[i] - real);
        E3[i] = isnan(R3[i]) ? NAN : fabs(R3[i] - real);
        E4[i] = isnan(R4[i]) ? NAN : fabs(R4[i] - real);

        cout << "\n  Foguete " << i+1 << " | a = " << y
             << " | d* = " << formatarDouble(real, 8) << "\n";
 
        imprimirCabecalhoTabela();
        imprimirLinhaTabela(y, "Bissecao", R1[i], E1[i], IT1[i], verificarStatus(R1[i]));
        imprimirLinhaTabela(y, "Posicao Falsa", R2[i], E2[i], IT2[i], verificarStatus(R2[i]));
        imprimirLinhaTabela(y, "Newton-Raphson", R3[i], E3[i], IT3[i], verificarStatus(R3[i]));
        imprimirLinhaTabela(y, "Secante", R4[i], E4[i], IT4[i], verificarStatus(R4[i]));
        imprimirLinhaSeparadora();
    }

     cout << "\n-- Quadro Comparativo --------------------------------------------------------------------\n";
    imprimirColuna("a",         12);
    imprimirColuna("Metodo",    22);
    imprimirColuna("Raiz",      18);
    imprimirColuna("Erro",      18);
    imprimirColuna("Iteracoes", 12);
    imprimirColuna("Status",    12);
    cout << endl;
    imprimirLinhaSeparadora();
 
    for (int i = 0; i < n; i++) {
 
        double y = coefs[i];
        imprimirLinhaTabela(y, "Bissecao",       R1[i], E1[i], IT1[i], verificarStatus(R1[i]));
        imprimirLinhaTabela(y, "Posicao Falsa",  R2[i], E2[i], IT2[i], verificarStatus(R2[i]));
        imprimirLinhaTabela(y, "Newton-Raphson", R3[i], E3[i], IT3[i], verificarStatus(R3[i]));
        imprimirLinhaTabela(y, "Secante",        R4[i], E4[i], IT4[i], verificarStatus(R4[i]));
        imprimirLinhaSeparadora();
    }
 
    cout << "\n  Observacao: 'Explode' = d > 2 cm (foguete em risco).\n";
    cout << "              'Seguro'  = d <= 2 cm.\n\n";

    return 0;
}