import numpy as np
import pandas as pd

def calcular_score_final(probabilidades, score_referencia=600, pdo=20):
    """Transforma probabilidades de calote num Score de 0 a 1000."""
    odds = (1 - probabilidades) / (probabilidades + 1e-10)
    fator = pdo / np.log(2)
    offset = score_referencia - (fator * np.log(1)) 
    score = offset + (fator * np.log(odds))
    score = np.clip(score, 0, 1000)
    return score.astype(int)

# ===================================================================
# MOTOR 1: REGRA ORIGINAL (COMPRIMIDA)
# ===================================================================
def definir_rating_credito_original(score):
    if score >= 800: return 'A (Risco Mínimo)'
    elif score >= 650: return 'B (Risco Baixo)'
    elif score >= 500: return 'C (Risco Médio)'
    elif score >= 350: return 'D (Risco Alto)'
    else: return 'E (Risco Crítico)'

def aplicar_politica_decisao_original(df):
    df['Rating'] = df['Score_Final'].apply(definir_rating_credito_original)
    df['Decisao'] = df['Rating'].apply(
        lambda x: 'REPROVADO' if x[0] in ['D', 'E'] else 'APROVADO'
    )
    return df

def aplicar_politica_decisao_original(df):
    df['Rating'] = df['Score_Final'].apply(definir_rating_credito_original)
    df['Decisao'] = df['Rating'].apply(
        lambda x: 'REPROVADO' if x[0] in ['D', 'E'] else 'APROVADO'
    )
    return df

# ===================================================================
# MOTOR 2: REGRA CALIBRADA V1 (QUARTIS)
# ===================================================================
def definir_rating_credito_quartis(score):
    if score >= 547: return 'A (Risco Mínimo)'       # Top 25% melhores
    elif score >= 536: return 'B (Risco Baixo)'      # Acima da mediana
    elif score >= 526: return 'C (Risco Médio)'      # Abaixo da mediana
    elif score >= 515: return 'D (Risco Alto)'       # Os 25% piores
    else: return 'E (Risco Crítico)'                 # A raspa do tacho (abaixo de 515)

def aplicar_politica_decisao_quartis(df):
    df['Rating'] = df['Score_Final'].apply(definir_rating_credito_quartis)
    df['Decisao'] = df['Rating'].apply(
        lambda x: 'REPROVADO' if x[0] in ['D', 'E'] else 'APROVADO'
    )
    return df

# 1. A CONSTRUÇÃO DO MOTOR (Definindo a Função de P&L)
def simular_politica_selic(y_true, prob_calote, selic_atual):
    """
    Auditoria V2: Ajusta a régua de aprovação automaticamente baseada no custo do dinheiro.
    """
    ticket_medio = 10000.00         
    taxa_cliente_aa = 0.35          
    spread_administrativo = 0.05    
    
    custo_funding = selic_atual + spread_administrativo
    
    lucro_por_bom_pagador = ticket_medio * (taxa_cliente_aa - custo_funding)
    loss_por_calote = ticket_medio 
    
    prob_bom = 1 - prob_calote
    valor_esperado = (prob_bom * lucro_por_bom_pagador) - (prob_calote * loss_por_calote)
    
    decisao = np.where(valor_esperado > 0, 'APROVADO', 'REPROVADO')
    
    df_simulacao = pd.DataFrame({
        'Calote_Real': y_true,
        'Decisao': decisao
    })
    
    aprovados = df_simulacao[df_simulacao['Decisao'] == 'APROVADO']
    
    lucro_real = (aprovados['Calote_Real'] == 1).sum() * lucro_por_bom_pagador
    prejuizo_real = (aprovados['Calote_Real'] == 0).sum() * loss_por_calote
    
    lucro_liquido = lucro_real - prejuizo_real
    taxa_aprovacao = len(aprovados) / len(df_simulacao)
    
    return lucro_liquido, taxa_aprovacao, (df_simulacao['Decisao'] == 'REPROVADO').sum()