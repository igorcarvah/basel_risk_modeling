# 🏦 Credit Scorecard Engine: Do Laboratório (V1) à Esteira de Produção (V2)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Status](https://img.shields.io/badge/Status-V2.0%20Homologado-success)
![Methodology](https://img.shields.io/badge/Methodology-Basileia%20%7C%20FGV-darkblue)
![Domain](https://img.shields.io/badge/Finance-Credit%20Risk%20%26%20P%26L-orange)
![License](https://img.shields.io/badge/License-MIT-green)

> **"Modelos estatísticos de 'Caixa Preta' não sobrevivem a auditorias do Banco Central. Lucro real se protege com governança, higiene de dados e respeito à macroeconomia."**

Este repositório documenta a construção ponta a ponta de um **Scorecard de Crédito Multivariável** (*White-box Model*). O projeto ilustra a evolução de um modelo experimental (V1) para uma **Esteira de Governança de Risco (V2)**, detalhando o tratamento de dados brutos, a matemática do Weight of Evidence (WoE) e a simulação de impacto no balanço patrimonial sob estresse da Taxa Selic.

---

## 🎯 1. O Problema de Negócio (A Batalha de Modelos)

Modelos de risco puramente estatísticos quebram em produção por ingerirem "Lixo Operacional". Ao cruzar a base tratada com as predições na matriz de teste cega (*Out-of-Time*), comparamos o modelo *baseline* (V1) com a nossa esteira de alta governança (V2).

A introdução das réguas da FGV e o tratamento estrito de DTI no V2 eliminaram o *Overfitting* e recalibraram os pesos da Regressão Logística. 

**O Prêmio da Governança:** O V2 gerou um aumento de **R$ 33,69 milhões** adicionais na proteção de capital em relação ao V1.

| Métrica / Auditoria | V1 (Baseline / Caixa Cinza) | V2 (Champion / Auditável) | Impacto no Balanço |
| :--- | :--- | :--- | :--- |
| **GINI (Capacidade de Separação)** | 31.00% (AUC: 0.6550) | **32.93% (AUC: 0.6647)** | Maior precisão na distinção de risco. |
| **Caloteiros Reais Barrados** | 22.083 CPFs | **25.452 CPFs** | **+ 3.369** fraudes/calotes evitados. |
| **Estimativa de Loss Evitado** | R$ 220.830.000,00 | **R$ 254.520.000,00** | **+ R$ 33.690.000,00** salvos. |

---

## 🚀 2. Funcionalidades do Pipeline (A Anatomia dos Dados)

O sistema opera em uma arquitetura modularizada, separando a limpeza de dados da estatística e da tesouraria:

### A. Higiene de Dados & ETL
* **O Gabarito (Target):** Para evitar *Data Leakage*, a variável original `loan_status` foi ejetada após a criação da bússola binária `good_bad_loan` (1 = Lucro/Bom Pagador, 0 = Loss/Caloteiro).
* **Expurgo de Ativos Tóxicos (Regra dos 50%):** Variáveis com mais de 50% de dados nulos (NaN) foram sumariamente excluídas. Imputar esses vazios configuraria fraude estatística.
* **Filtro de Sobrevivência (Zero Data Loss):** Rendas anuais declaradas abaixo de R$ 3.600 não indicam pobreza, mas **erro de digitação na captação**. Em vez de deletar esses clientes (gerando *crash* na API em produção), o algoritmo recalibra essas distorções internamente.
* **Abrasileiramento (Padrão FGV):** A renda bruta não linearizada destrói a Regressão Logística. A base foi submetida ao enquadramento oficial da Fundação Getúlio Vargas (FGV), transformando valores contínuos em "gavetas" socioeconômicas auditáveis.

### B. Motor Estatístico (WoE & IV)
Para cumprir o Acordo de Basileia, algoritmos *Black-box* foram descartados. A matriz foi convertida em pesos de risco utilizando o **Weight of Evidence (WoE)**, que lineariza o risco calculando o logaritmo natural da proporção entre clientes adimplentes e inadimplentes:

$$WoE = \ln \left( \frac{\text{Proporção de Bons}}{\text{Proporção de Maus}} \right)$$

* **Auditoria de Monotonicidade:** Variáveis chave foram forçadas a apresentar progressão lógica. Ex: Hipotecas representam risco mitigado (WoE positivo), enquanto Locatários geram risco acentuado (WoE negativo).
* **Information Value (IV):** Variáveis com $IV < 0.02$ foram classificadas como "ruído inútil" e isoladas do motor preditivo.

### C. Laudo de Tesouraria: Teste de Estresse Macroeconômico (Copom)
Modelos estáticos falham quando o custo de captação do banco aumenta. O V2 possui uma **Política de Crédito Dinâmica** baseada no Valor Esperado (EV), reagindo em tempo real à Taxa Selic:

| Cenário Econômico | Selic (a.a.) | Taxa de Aprovação | CPFs Reprovados | Lucro Líquido Final |
| :--- | :--- | :--- | :--- | :--- |
| **Otimista (Dinheiro Barato)** | 7.0% | 91.0% | 8.414 | R$ 94.328.100,00 |
| **Base (Operação Normal)** | 10.5% | 84.7% | 14.300 | R$ 68.260.750,00 |
| **Estresse (Crise / Dinheiro Caro)** | 14.0% | 74.3% | 24.000 | R$ 45.317.600,00 |

---
## 🛡️ 3. Decisões Arquiteturais e Impacto de Negócio

Este projeto não é apenas um classificador estatístico; é um motor de proteção de balanço. As decisões de modelagem foram tomadas com base no rigor de auditoria interna e na realidade da Diretoria Comercial:

### A. Mitigação de Risco e o Poder do *Collateral* (Garantias)
Quando a Selic sobe para 14%, a simulação mostra a aprovação caindo para 74.3%. Isso não é uma "falha comercial", é a trava de segurança contra o **Esmagamento de Margem (*Margin Squeeze*)**. Com o custo de captação alto, a margem de lucro não cobre o risco de clientes *Subprime*. 
* **A Estratégia:** Para manter o *Market Share* sem gerar *Loss*, o modelo aponta para a exigência de **Garantias Reais (Veículos ou Imóveis)**. Ao atrelar um bem à dívida, a Probabilidade de Default (PD) e a Severidade da Perda (LGD) despencam. A própria auditoria matemática do WoE comprova isso: clientes na categoria *Mortgage* (Bens Alienados) mitigam o risco a ponto de viabilizar a aprovação mesmo em cenários de juros altos.

### B. Auditabilidade Bacen (White-Box vs. Black-Box)
Modelos preditivos complexos como *Random Forest* e *XGBoost* operam como "Caixas Pretas". Embora tenham alta acurácia, eles falham em auditorias do Banco Central porque a instituição precisa justificar legalmente o motivo de uma recusa de crédito. 
* A escolha pela **Regressão Logística com WoE** lineariza o risco, lida naturalmente com *missing values* sem imputações artificiais e gera um Scorecard onde cada ponto ganho ou perdido pelo cliente é 100% explicável e rastreável. 

### C. Tolerância Zero para Lixo Operacional (*Data Leakage*)
A infraestrutura do pipeline segue protocolos rígidos para garantir que o modelo não "engasgue" em produção:
* **Prevenção de Vazamento:** A variável *Target* original (`loan_status`) foi expurgada no momento zero para evitar *Data Leakage*.
* **Higiene de Dados:** Variáveis com mais de 50% de nulidade foram descartadas. Valores anômalos (rendas irracionais) não deletam a linha do cliente (o que causaria perda de dados na API), mas são isoladas e penalizadas matematicamente. O código segue a máxima corporativa: é modular, performático e não faz "SELECT *" em bases de produção.

---

## 📸 4. Evidências Visuais (O Dossiê de Auditoria)

### 1. Calibração de Renda (Padrão FGV)
*Para garantir alinhamento com a Diretoria Comercial, a base foi segmentada utilizando a documentação oficial da FGV (Salário Mínimo base R$ 1.380).*
![Divisão Salarial por Classe Social FGV](imagem/fgv.png)

### 2. Auditoria de Risco Visual (Monotonicidade WoE)
*A "escadinha" perfeita de risco: clientes com financiamento imobiliário (Mortgage) apresentam menor propensão ao default, enquanto locatários (Rent) geram WoE negativo.*
![Auditoria de Risco - Status de Moradia](imagem/woe.png)

---

## 🛠️ 5. Arquitetura Técnica

O projeto segue princípios de **Clean Code** e **Governança de Dados**, isolando as etapas críticas de transformação para garantir reprodutibilidade.

```text
BASEL_RISK_MODELING/
├── data/                    # Data Lake (Bases de Crédito Bruta e Teste)
├── img/                     # Evidências Visuais e Documentação de Regras
├── src/                     # Motores de Processamento (Lógica Estrita)
│   ├── data_ingestion.py    # ETL e Higienização Inicial
│   ├── feature_engineering.py # Regras de Negócio (FGV e DTI)
│   ├── woe_iv.py            # Motor Estatístico (Weight of Evidence)
│   ├── scorecard_scaler.py  # P&L, Escalonamento e Estresse Selic
│   └── plots_woe.py         # Geração de Laudos Visuais
├── 01_Challenger_V1.ipynb   # Laboratório Experimental (Baseline)
├── 02_Champion_V2.ipynb     # Esteira de Produção e Teste Macroeconômico (Homologado)
├── README.md                # Documentação Executiva
└── requirements.txt         # Dependências do Projeto


# Clone o repositório
git clone [https://github.com/igorcarvah/lab_risco_quant.git](https://github.com/igorcarvah/lab_risco_quant.git)
