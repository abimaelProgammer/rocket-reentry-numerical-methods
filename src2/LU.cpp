#include <iostream>
#include <cmath>
#include <vector>
using namespace std;

//A.x=b
//A= L.U
//Ux= y 
//Ly = b

//pega matriz a -> transforma em matriz triangular inferior (L) e guarda os coeficientes


void verificador (vector<vector<double>> &A, int n) {
    for (int i = 0; i < n; i++){
        int zeros = 0;
        for (int j  = 0; j < n; j++){
            if (A[i][j] != 0){
                break;
            }
            zeros++;
        }
        if(zeros == n){
            cout << "linha nula, inválido";
            return;
        }
    }
}




void pivoteamento (int k, int n, vector<double>&b, vector<vector<double>>&A){
//partindo da linha que eu to eu vejo se tem algum na mesma coluna em uma linha mai spra baixo com valor maior, 
//se tiver, troca a linha e troca no b tb 
double maior = A[k][k];
int indice = k;
for (int i = k; i < n; i++){
    if (abs(maior) < abs(A[i][k])){
        maior = A[i][k];
        indice = i;
        }
    }



if (maior != A[k][k]){
//será feito pivoteamento 
for (int j = k; j < n; j++){ //varrendo a linha 
    double aux = A[k][j];
    A[k][j] = A[indice][j];
    A[indice][j] = aux;
    }
    double auxb = b[k];
    b[k] = b[indice];
    b[indice] = auxb;

//código do coeficiente da matriz l (nao pensei aind)

    }
}



void gauss (int n, int k,  vector<double>&b, vector<vector<double>>&A, vector<vector<double>>&L){
    //apos o pivoteamento, preciso zerar todos da coluna k que estou. 
    //linha_seguinte = linha_seguinte - coef x linha_atual
    //coef = linha_seguinte/linha_atual

    for (int i = k+1; i < n; i++){
        double coef = A[i][k]/A[k][k]; 
        for (int j = k; j < n; j++){
            A[i][j] = A[i][j] - coef * A[k][j];
        }

        //b[i] = b[i] - coef * b[k];
        L[i][k] = coef;
        //no lu o b nao muda aqui
    }
}



void matriz_y(int n, vector<vector<double>>&L,vector<double>&b, vector<double>&y){
//L.y = b //b[i] = A[linha i]
    for (int i = 0; i < n; i++) {//matriz triangular inferior

        double soma = 0;

        for (int j = 0; j < i; j++) {
            soma += L[i][j] * y[j];
        }

        y[i] = (b[i] - soma) / L[i][i];
    }
}




void matriz_x(int n, vector<vector<double>>&A,vector<double>&y, vector<double>&x){
//U(no caso matriz a).x=y

    
    for (int i = n - 1; i >= 0; i--) {//matriz triangular superiro

        double soma = 0;

        for (int j = i + 1; j < n; j++) {
            soma += A[i][j] * x[j];
        }

        x[i] = (y[i] - soma) / A[i][i];
    }
}












int main (){
    int n;
    cout << "digite o numero de variáveis: ";
    cin >> n;

    //matriz A e L
    vector<vector<double>>A(n, vector<double>(n));
    vector<vector<double>>L(n, vector<double>(n));

    //vetor b 
    vector<double>b(n);
    vector<double>y(n);
    vector<double>x(n);
    
    for (int i = 0; i < n; i++ ){
        for (int j = 0; j < n; j++){
            cout << "digite o valor do coef a" << i << j<< ": ";
            double coef_a;
            cin >> coef_a;
            A[i][j]=coef_a;
        }
    }

      for (int i = 0; i < n; i++ ){
        cout << "digite o valor do coef b" << i<< ": ";
        double B;
        cin >> B;
        b[i] = B;
      }

 // verifica linhas nulas
    verificador(A, n);

    //monta diagonal da matriz dos coef
    for (int i = 0; i < n; i++) {
        L[i][i] = 1;
    }

    // Fatoracao LU
    for (int k = 0; k < n - 1; k++) {

        pivoteamento(k, n, b, A);

        gauss(n, k, b, A, L);
    }

    // resolve Ly = b
    matriz_y(n, L, b, y);

    //resolve Ux = y
    matriz_x(n, A, y, x);

    cout << "\nSolucao:\n";

    for (int i = 0; i < n; i++) {
        cout << "x" << i + 1 << " = " << x[i] << endl;
    }

    return 0;
}




