# 🚀 Rocket Reentry: Numerical Methods Solver

Este projeto implementa métodos numéricos de busca de raízes para calcular o deslocamento da extremidade de um foguete espacial durante a reentrada na atmosfera terrestre. O objetivo principal é simular o estresse estrutural e garantir que os parâmetros de segurança sejam estritamente atendidos.

## 📋 Sobre o Problema

O deslocamento ($d$) da extremidade do foguete (medido em cm) é modelado pela seguinte equação não linear:

$$f(d) = a \cdot d - d \cdot \ln(d)$$

Onde:
- **$a$** é um parâmetro de ajuste aerodinâmico/estrutural de cada foguete.
- **Limiar de Segurança:** Caso o deslocamento $d$ ultrapasse **2 cm**, a estrutura sofre colapso (explosão). 

O sistema resolve a equação $f(d) = 0$ para encontrar o ponto exato de deslocamento sob dadas condições de $a$, garantindo precisão em testes e simulações para evitar perdas catastróficas.

## ⚙️ Métodos Implementados

O algoritmo resolve o problema utilizando três abordagens clássicas de Cálculo Numérico:
1. **Método da Bisseção:** Abordagem de isolamento original.
2. **Método da Posição Falsa (Regula Falsi):** Interpolação linear para convergência otimizada.
3. **Método de Newton-Raphson:** Utilização da derivada da função para convergência rápida.

### Parâmetros de Teste Padrão
- Parâmetro do foguete ($a$): `1`
- Intervalo de Isolamento: `[2, 3]`
- Tolerância de Erro ($\epsilon$): `10^{-5}`

## 💻 Entradas e Saídas

**Dados de Entrada:**
- $n$: Número de foguetes a serem simulados.
- $a$: Parâmetro de ajuste individual para cada foguete.
- $\epsilon$: Precisão (tolerância de erro) desejada.

**Dados de Saída:**
- **Quadro de Respostas:** Exibe o deslocamento $d$ calculado e o erro para cada foguete testado, variando os métodos.
- **Quadro Comparativo:** Compara o desempenho dos três métodos numéricos (Bisseção, Posição Falsa e Newton-Raphson) detalhando o isolamento, as raízes encontradas e os dados de convergência.
- **Análise de Variação:** Avaliação do impacto da mudança do parâmetro $a$ no deslocamento para cada método.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python
- Estruturas de dados para formatação tabular dos quadros comparativos.

---
*Projeto desenvolvido para a disciplina de Cálculo Numérico / Métodos Numéricos.*
