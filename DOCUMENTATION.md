# 🗎👣 Guia do Usuário e Documentação Técnica do Dashboard da Fórmula Mágica

Este documento serve como um guia abrangente para usuários finais e desenvolvedores interessados em entender, utilizar, replicar ou aprimorar o dashboard interativo da "Fórmula Mágica de Joel Greenblatt".

---

## 🎯 1. Sobre o Projeto

O "Dashboard Interativo: Fórmula Mágica de Joel Greenblatt com Alocação Inteligente" é uma ferramenta desenvolvida em Python com a biblioteca Dash para auxiliar investidores na aplicação de uma das estratégias de investimento bastante conhecida. Além de ranquear empresas, o dashboard simula a alocação de capital, tornando o processo de decisão mais prático e visual.

### 1.1. O que é a Fórmula Mágica?

A Fórmula Mágica, popularizada por Joel Greenblatt em seu livro "O Pequeno Livro Que Vence o Mercado", é uma estratégia de investimento que busca combinar duas características essenciais em empresas:
1.  **Boas Empresas (Empresas de Qualidade):** Medido pelo ROIC (Return on Invested Capital).
2.  **Boas Barganhas (Empresas Baratas):** Medido pelo Earnings Yield (Lucro por Ação / Preço por Ação, ou o inverso do P/L).

A estratégia ranqueia empresas com base nesses dois fatores e sugere investir nas empresas com o melhor ranqueamento combinado.

---

## 💡 2. Funcionalidades Detalhadas

### 2.1. Configurações do Ranking (Sidebar Esquerda)

A barra lateral permite que você ajuste os parâmetros para a seleção e ranqueamento das empresas:

*   **Número de empresas a exibir e pré-selecionar:** Use o slider para definir quantas empresas com melhor ranqueamento pela Fórmula Mágica serão exibidas na tabela principal. Este número também pré-seleciona as empresas para o cálculo de alocação.
*   **Volume Médio Negociado (últimos 2 meses) Mínimo (R$):** Filtra as empresas com base na liquidez. Insira um valor mínimo para o volume médio diário de negociação nos últimos 2 meses. Empresas com volume abaixo desse limite não serão consideradas, evitando ações com baixa liquidez que poderiam dificultar a compra/venda.

### 2.2. Configurações de Investimento (Barra Lateral Esquerda)

*   **Valor a Investir (R$):** Digite o valor total que você pretende alocar nesta estratégia. O dashboard utilizará este valor para calcular a quantidade de ações e o peso na carteira para as empresas selecionadas.
*   **Tipo de Lote de Compra:**
    *   **Fracionário (1+ ações):** Permite a compra de qualquer quantidade de ações, incluindo frações (simulado aqui como compra de 1, 2, 3... ações).
    *   **Padrão (100+ ações):** Restringe a compra a múltiplos de 100 ações.

### 2.3. Colunas a Exibir (Barra Lateral Esquerda)

*   **Selecione as colunas para exibir:** Use o dropdown para escolher quais informações das empresas você deseja visualizar na tabela principal. A ordem em que você seleciona as colunas definirá a ordem delas na tabela.

### 2.4. Tabela Principal (Magic Formula Table)

Apresenta as empresas ranqueadas e suas métricas.

*   **Seleção de Linhas:** As caixas de seleção na primeira coluna permitem incluir ou excluir empresas do cálculo de alocação. Por padrão, as empresas são pré-selecionadas com base no slider "Número de empresas a exibir".
*   **Dados e Formatação:** A tabela exibe os dados das empresas com formatação numérica amigável para o padrão brasileiro (e.g., "R$ 1.234,56", "1.234.567", "12,34%").
*   **Colunas de Cálculo Dinâmico:** As colunas "Qtd. Ações", "Valor Alocado (R$)" e "% na Carteira" são atualizadas em tempo real com base nas suas seleções e configurações de investimento.

### 2.5. Resumo da Alocação de Investimento

Localizado abaixo da tabela, este resumo oferece uma visão consolidada dos resultados da sua alocação:

*   **Valor a Investir:** O valor total que você informou.
*   **Número de Empresas Selecionadas para Alocação:** Quantas empresas estão ativas no cálculo.
*   **Valor Alocado por Empresa (Ideal):** O investimento dividido igualmente entre as empresas selecionadas.
*   **Valor Total Alocado (Real):** O valor efetivamente alocado, considerando a cotação e a quantidade de ações compradas/arredondadas.
*   **Diferença (Não Alocado):** A diferença entre o valor a investir e o valor realmente alocado (pode ocorrer devido ao arredondamento da quantidade de ações).

### 2.6. Entendendo as Métricas

Uma seção detalhada para cada métrica presente no dashboard, explicando seu significado e importância para a análise de investimento.

### 2.7. Seção de Contato

No final do dashboard, há uma seção com meus links de LinkedIn e GitHub, para que interessados no trabalho possam entrar em contato.

---

## 🛠️ 3. Para Desenvolvedores e Replicadores

Esta seção é dedicada a quem deseja entender o código, replicar o ambiente ou contribuir para o projeto.

### 3.1. Estrutura do Projeto

O projeto é organizado da seguinte forma:

├── assets/ # Diretório para arquivos estáticos (CSS, JavaScript).\n
│ ├── style.css # Estilos CSS personalizados para o dashboard.

│ └── clientside.js # Funções JavaScript para callbacks clientside (formatação de inputs).

├── app.py # Script principal do Dash app.

├── fundamentus_data.csv # Arquivo CSV com os dados das empresas (fonte externa, não gerado por este app).

├── requirements.txt # Lista de dependências Python.

├── Procfile # Configurações do gunicorn. Necessário para deploy no Hugging Face.

├── Dockerfile # Configurações do container docker.

├── README.md # Este arquivo.

└── DOCUMENTATION.md # Documentação técnica do dashboard


### 3.2. Configuração do Ambiente

1.  **Clone o repositório:**
    ```bash
    git clone [LINK DO SEU REPOSITÓRIO GITHUB AQUI]
    cd [NOME DO SEU REPOSITÓRIO]
    ```
2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    (Certifique-se de que seu `requirements.txt` contém `dash`, `pandas`, `gunicorn` e `dash-bootstrap-components` se estiver usando). Um `requirements.txt` básico seria:
    ```
    dash
    pandas
    gunicorn # Necessário para deploy em ambientes como Hugging Face Spaces
    ```
4.  **Obtenha os dados:**
    O dashboard espera um arquivo `fundamentus_data.csv` na raiz do projeto. Este arquivo *não* é gerado por este aplicativo, ele foi obtido de uma fonte externa¹. Certifique-se de que as colunas no CSV correspondem às esperadas no `ALL_COLUMNS_MAP` do `app.py`.

¹ Verifique os repositórios abaixo para para gerar seu próprio arquivo `fundamentus_data.csv` caso tenha interesse:
[https://github.com/f-avila-84/Fundamentus_ETL_local] ETL rodando sob demanda na máquina local.
[https://github.com/f-avila-84/Fundamentus_ETL_Airflow] ETL rodando de forma agendada na máquina local em conteiner Docker (possibilidade de colocar para rodar na nuvem).


5.  **Execute o aplicativo:**
    ```bash
    python app.py
    ```
    O dashboard estará acessível em `http://127.0.0.1:8050/` (ou outra porta, se indicado no console).

### 3.3. Deploy no Hugging Face Spaces

Para fazer o deploy deste dashboard no Hugging Face Spaces:

1.  Crie um novo Space no Hugging Face.
2.  Escolha `Gradio SDK` (sim, Dash apps podem rodar nele) ou `Docker` se precisar de mais controle. Para `Gradio SDK`, o Hugging Face detectará automaticamente seu `app.py`.
3.  **Certifique-se de que todos os arquivos necessários estão no repositório:**
    *   `app.py`
    *   `requirements.txt`
    *   `assets/` (com `style.css` e `clientside.js`)
    *   `fundamentus_data.csv`
4.  O Hugging Face irá instalar as dependências de `requirements.txt` e executar `app.py`.

### 3.4. Personalização e Extensão

*   **Estilização (CSS):**
    *   O arquivo `assets/style.css` contém todas as regras de estilo. Você pode modificar cores, fontes, espaçamentos e layouts. As variáveis CSS (`:root` no início do arquivo) são um bom ponto de partida para mudanças rápidas de tema.
    *   **Responsividade:** A seção `@media (max-width: 768px)` em `style.css` contém os ajustes para telas menores.
*   **Lógica do Dashboard (Python):**
    *   **`app.py`:** Este é o coração da aplicação.
        *   `ALL_COLUMNS_MAP`: Adicione ou remova colunas que você deseja que o dashboard reconheça e exiba.
        *   `FORMATTING_RULES`: Defina como cada coluna numérica deve ser formatada para exibição (e.g., moeda, porcentagem).
        *   `calculate_allocation_for_df`: Modifique a lógica de alocação de acordo com outras estratégias (e.g., alocação por valor, por setor).
        *   **Callbacks:** Entenda como os `Input`, `Output` e `State` conectam a interface do usuário à lógica Python.
*   **Dados:**
    *   Para atualizar os dados, basta substituir o arquivo `fundamentus_data.csv` por uma versão mais recente, mantendo a estrutura de colunas.

### 3.5. Solução de Problemas Comuns

*   **`SyntaxError: invalid syntax`:** Geralmente ocorre por um erro de digitação, uma vírgula fora do lugar, ou um caractere invisível. Verifique a linha indicada no erro no `app.py` com atenção redobrada. Garanta que o arquivo salvo está exatamente como o código fornecido, sem caracteres extras.
*   **"Cálculos Zerados" ou Tabela Vazia:**
    *   Verifique se o `fundamentus_data.csv` está presente na raiz do projeto e se não está vazio.
    *   Confirme se as colunas no CSV correspondem aos nomes esperados no `app.py`.
    *   Verifique os `Input`s dos callbacks `update_filtered_data_and_table` e `update_allocation_and_summary` para garantir que os valores dos filtros estão sendo passados corretamente.
    *   Certifique-se de que a lista de `dash_table_columns_ids` em `update_table_with_calculated_data` contenha apenas *strings* (os IDs das colunas) e não dicionários ou outros objetos.
*   **CSS não Aplicado/Design Quebrado:**
    *   Verifique se o arquivo `style.css` está em `assets/style.css`.
    *   Limpe o cache do seu navegador (Ctrl+Shift+R ou Cmd+Shift+R).
    *   No `app.py`, confirme que `external_stylesheets=[ '/assets/style.css', ...]` está correto.

---

## 🤝 4. Contribuindo

Este é um projeto desenvolvido para fins de estudo e portfólio. No momento, não estou buscando contribuições externas. No entanto, sinta-se à vontade para fazer um fork, explorar e adaptar o código para suas necessidades!

---

## 📧 5. Contato

**Felipe Avila**

[<i class="fab fa-linkedin"></i> LinkedIn](https://www.linkedin.com/in/avilafelipe/) | [<i class="fab fa-github"></i> GitHub](https://github.com/f-avila-84)

---

## ⚠️ 6. Aviso Legal e Disclaimer de Investimento

Este código foi desenvolvido para fins **educacionais e informativos** como parte de um projeto de estudo pessoal. Ele tem como objetivo demonstrar a coleta e organização de dados fundamentalistas.

É fundamental entender que as informações obtidas através deste script **NÃO constituem aconselhamento financeiro, recomendação de investimento ou endosso de qualquer tipo de estratégia de investimento.** O mercado financeiro é complexo e investimentos envolvem riscos, incluindo a **possibilidade de perda de capital.**

*   **Não se baseie unicamente** nos dados gerados por este código para tomar decisões de investimento.
*   **Retornos passados não são garantia** de retornos futuros.
*   Qualquer decisão de investimento é de sua **inteira responsabilidade**.

Recomenda-se **sempre consultar um profissional financeiro qualificado** antes de tomar qualquer decisão de investimento. O desenvolvedor deste código não se responsabiliza por quaisquer perdas ou prejuízos decorrentes do uso ou interpretação das informações aqui contidas.


## 📜 7. Licença
Este projeto está licenciado sob a licença MIT. 
Veja o arquivo LICENSE para mais detalhes.
[opensource.org](https://opensource.org/license/mit)

Este código é um projeto de estudo pessoal, portanto não se baseie unicamente nele para tomada de decisões de investimentos. Retornos passados não são garantia de retornos futuros. 

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. 

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.