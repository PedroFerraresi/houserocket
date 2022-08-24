# Projeto de Insights

O Objetivo de um projeto de Insights é recomendar soluções para a empresa ou negócio através de ***Insights*** gerados por uma Análise de Dados. Por tanto, vamos dentro do *roadmap* de resolução de problemas em Data Science, cobrimos somente os 5 primeiros passos:
* Recebimento da Questão de Negócio
* Definição de Escopo e entendimento do Problema de Negócio
* Coleta de Dados
* Limpeza dos Dados
* Exploração dos dados

Cumprindo esses primeiros 5 passos e obtendo ***isights***, conseguiremos sugerir soluções sem termos que implementar algoritmos de ***Machine Learning*** mais complexos, dando assim agilidade na entrega de resultados para a empresa.

Todo o contexto de negócio deste projeto é fictício e foi criado pela [Comunidade DS](https://www.comunidadedatascience.com/).

# 1. Problema de Negócio - A Empresa *House Rocket*
## Contexto do Problema

A **House Rocket** é uma plataforma digital que tem como modelo de negócio, a compra e a venda de imóveis usando tecnologia. O CEO da House Rocket gostaria de maximizar a receita da empresa encontrando boas oportunidades de negócio.

Sua principal estratégia é comprar boas casas em ótimas localizações com preços baixos e depois revendê-las posteriormente à preços mais altos. Quanto maior a diferença entre a compra e a venda, maior o lucro da empresa e portanto maior sua receita.

Entretanto, as casas possuem muitos atributos que as tornam mais ou menos atrativas aos compradores e vendedores e a localização e o período do ano também podem influenciar os preços.

Dessa forma, o objetivo desse projeto é responder as seguintes perguntas utilizando Análise Exploratória de Dados:

1. Quais casas o CEO da House Rocket deveria comprar e por qual preço de compra?
2. Uma vez a casa em posse da empresa, qual o melhor momento para vendê-las e qual seria o preço da venda?

# 2. Premissas de Negócio
## 2.1. Os dados

A base de dados utilizada na construção desse projeto pode ser encontrada dentro da plataforma [Kaggle](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction).

As colunas da base de dados são:

| Nome da Coluna | Descrição da Coluna |
| :------------- | :------------------ |
| id | ID único de cada imóvel na base de dados |
| date | Data da venda do imóvel |
| price | Preço de venda do imóvel |
| bedrooms | Número de quartos |
| bedrooms | Número de banheiros. Onde 0.5 representa um quarto com vaso sanitário, mas sem chuveiro; 0.75 representa um banheiro que contém uma pia, uma privada, um chuveiro ou uma banheira. Um banheiro completo tradicionalmente possui uma pia, uma privada, um chuveiro e uma banheira, dessa forma, 0.75 representa que o banheiro tem ou um chuveiro ou uma banheira |
| sqft_living | Metragem quadrada (em pés) do espaço interior do imóvel |
| sqft_lot | Metragem quadrada (em pés) do espaço terrestre do imóvel |
| floors | Número de andares do imóvel |
| waterfront | Coluna que representa se o imóvel possui vista para o mar/lago ou não. 0 representa sem vista para a água e 1 representa vista para a água |
| view | Índice de 0 a 4 de quão boa é a vista do imóvel. 0 é a pior vista e 4 é a melhor vista |
| condition | Índice de 1 a 5 sobre a condição (usado) do imóvel. 1 é a pior condição e 5 é a melhor |
| grade	| Índice de 1 a 13 sobre a condição da construção e design do imóvel. 1 é a pior nota e 13 é a melhor nota |
| sqft_above | Metragem quadrada (em pés) do espaço interno do imóvel que está acima do nível do solo |
| sqft_basement | Metragem quadrada (em pés) do espaço interno do imóvel que está abaixo do nível do solo (porão) |
| yr_built | Ano em que o imóvel foi construído |
| yr_renovated | Ano da última reforma do imóvel |
| zipcode | Código postal do imóvel |
| lat | Ponto de latitude do imóvel |
| long | Ponto de longitude do imóvel |
| sqft_living15 | Metragem quadrada (em pés) do espaço habitacional interior para os 15 vizinhos mais próximos |
| sqft_lot15 | A metragem quadrada (em pés) dos terrenos (lotes vazios) dos 15 vizinhos mais próximos |

## 2.2. Estratégia de Resolução
01. **Entender o problema de Negócio:** O objetivo desta etapa é compreender corretamente o que é pedido, ajustar as expectativas e demonstrar exemplos de como serão os resultados.
02. **Descrição dos Dados:** O objetivo é utilizar ferramentas estatísticas de localização e dispersão para possuir um entendimento melhor dos dados.
03. **Filtragem dos Dados:** O objetivo desta etapa é remover as linhas que possam conter dados incorretos ou dados que possam prejudicar a análise de alguma forma.
04. **Análise Exploratória dos Dados:** O objetivo desta etapa é realizar uma exploração dos dados validando hipóteses de negócio, para melhor entender o comportamento das variáveis na base de dados.
05. **Responder as perguntas de Negócio:**  O objetivo desta etapa é utilizar todo o conhecimento adquirido nas etapas anteriores e criar estratégias para responder as perguntas realizadas.

## 2.3. Ferramentas e Métodos Utilizados
- Python 3.8.13
- Jupyter Notebook
- CRISP-DS
- Git
- Framework Streamlit

## 2.3. Premissas
* ID duplicados serão removidos da base de dados.
* Casas que não possuiam quartos ou banheiros serão removidos da base de dados
* Para definição da compra dos imóvel foram utilizadas duas condições:
    * O imóvel deve está em boa condição de compra. O indicador é representado pela coluna condição, sendo considerado as condições boas como 3 a 5.
    * O valor de compra do imóvel deve ser menor do que o valor mediano da região (Código Postal)
* Para definição da venda dos imóveis selecionados anteriormente foram utilizadas três condições:
    * Caso o imóvel tenha sido adquirido em uma estação diferente do Inverno, o preço de venda sugerido será 30% em cima do valor de compra.
    * Caso o imóvel tenha sido adquirido no Inverno, o preço de venda sugerido será 10% em cima do valor de compra
    * Conforme foi verificado, o preço médio de venda dos imóveis é sempre maior no inverno, dessa forma, a sugestão é que todas os imóveis sejam preferencialmente vendidos no período do inverno.

# 3. Resultado de Negócio
## 3.1. Hipóteses de Negócio
| Hipótese | Validação |
| -------- | --------- |
| H1: Imóveis que possuem vista para água, são 30% mais caros, na média. | **VERDADEIRA:** Os imóveis com vista para a água são 212.36% mais caros que os imóveis sem vista para a água | 
| H2: Imóveis com data de construção menor que 1955, são 50% mais baratos, na média. | **FALSA:** Os imóveis construídos antes de 1955 são 0.43% mais baratos | 
| H3: Imóveis sem porão são 50% maiores, na média, do que os imóveis com porão. | **FALSA:** Os imóveis com porão são 18.5% maiores que os imóveis sem porão | 
| H4: O crescimento do preço médio dos imóveis YoY ( Year over Year ) é de 10% | **FALSA:** O crescimento YoY é de 0.73% | 
| H5: Imóveis com 3 banheiros tem um crescimento MoM ( Month over Month ) de 15% | **FALSA:** O percentual de crescimento MoM máximo foi de 12.31 | 
| H6: Imóveis com porão são mais caros, em média, do que imóveis sem porão | **VERDADEIRA:** Os imóveis com porão são 21.69% mais caros que os imóveis sem porão | 
| H7: Imóveis reformados a partir do ano 2000 são, em média, 30% mais caros | **VERDADEIRA:** Os imóveis renovados a partir do ano 200 são 34.6% mais caros | 
| H8: Pelo menos 80% dos imóveis com vista para água possuem nível de construção 10 ou mais. | **FALSA:** Os imóveis que possuem nível de construção 10 ou mais representam 36.2% dentre os imóveis com vista para a água | 
| H9: Pelo menos 80% dos imóveis com condição 4 e 5 tem níveis de construção 7 ou mais. | **VERDADEIRA:** Os imóveis que possuem nível de construção 7 ou mais representam 85.67% dentre os imóveis com condição de uso entre 4 e 5 | 
| H10: Imóveis no vendidos no inverno são, em média, 20% mais baratos do que no resto do ano. | **FALSA:** Os imóveis vendidos no inverno são 3.37% mais caros do que no resto do ano |

## 3.2. Perguntas de Negócio
### 3.2.1. Quais são os imóveis que a House Rocket deveria comprar e por qual preço ?
Foi realizado o agrupamento dos imóveis por código postal e calculado o valor mediano do preço de venda de cada código postal. A partir disso, foram selecionados os imóveis que possuiam o valor de venda menor que o valor mediano e que estavam em boa condições, gerando assim uma lista com **21.419** imóveis elegíveis para compra.

### 3.2.2. Uma vez a casa comprada, qual o melhor momento para vendê-las e por qual preço ?
A partir dos imóveis selecionados anteriormente, foi verificado a estação do ano em que cada imóvel foi vendido. Novamente, agrupando os dados por código postal e por estação do ano, foi calculado o valor mediano de venda do imóvel. Com o valor mediano calculado, foi selecionado o menor valor mediano de cada estação como base e realizado o cálculo do valor sugerido de venda para os 21.419 imóveis a partir das regras colocadas anteriormente.

Caso a sugestão de valores de venda seja acatada, o lucro previsto com a venda dos imóveis será de **$ 1.460.518.541,70**

### 3.2.3. Exibição das Análises
Foi criado uma aplicação web utilizando o framework web Streamlit para facilitar o consumo das análises feitas pelo CEO.

Link para acesso à aplicação: [Análises](https://houserokectanalytics.herokuapp.com/)

# 4. Lições Aprendidas
Foi constatado que poderíamos verificar e selecionar oportunidades de negócio para o CEO da empresa House Rocket somente utilizando técnicas de manipulação de dados e ferramentas estatísticas, podendo entregar resultados sem a necessidade de utilizar técnicas e ferramentas mais complexas.

# 5. Próximos Passos
* Realizar mais análises a fim de melhorar o entendimento dos dados da base de dados.
* Utilizar algoritmos de Machine Learning para melhorar a precificação dos imóvies, conseguindo assim melhorar os lucros previstos.
* Melhorar a estrutura da aplicação Web, utilizando seções para a exibição das análises
* Adicionar testes automatizados deixar o código mais robusto