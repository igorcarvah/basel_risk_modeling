import numpy as np
import pandas as pd

def calcular_score_final(probabilidades, score_referencia=600, pdo=20):
    """
    Transforma probabilidades de calote em um Score de 0 a 1000.
    Logica: Quanto MAIOR o Score, MENOR o risco (Padrão Serasa/Boa Vista).
    """
    # 1. Calculamos o Odds (Chance de ser Bom / Chance de ser Mau)
    # Proteção contra divisão por zero
    odds = (1 - probabilidades) / (probabilidades + 1e-10)
    
    # 2. Fator e Offset (A régua do banco)
    fator = pdo / np.log(2)
    offset = score_referencia - (fator * np.log(1)) # Log(1) é o odds de 1:1
    
    # 3. Transformação Linear
    score = offset + (fator * np.log(odds))
    
    # 4. Ajuste de Limites (O Score não pode fugir de 0 a 1000)
    score = np.clip(score, 0, 1000)
    
    return score.astype(int)


def definir_rating_credito(score):
    """
    Classifica o cliente em faixas de risco (Rating).
    Regra de Auditoria: Baseada em Basileia II para segmentação de carteira.
    """
    if score >= 800: return 'A (Risco Mínimo)'
    elif score >= 650: return 'B (Risco Baixo)'
    elif score >= 500: return 'C (Risco Médio)'
    elif score >= 350: return 'D (Risco Alto)'
    else: return 'E (Risco Crítico)'

def aplicar_politica_decisao(df):
    """
    Define a ação automática do banco baseada no Rating.
    """
    # 1. Aplicamos o Rating
    df['Rating'] = df['Score_Final'].apply(definir_rating_credito)
    
    # 2. Definimos a Decisão (Política de Alçada)
    # Regra: Rating D e E são reprovados automaticamente.
    df['Decisao'] = df['Rating'].apply(
        lambda x: 'REPROVADO' if x[0] in ['D', 'E'] else 'APROVADO'
    )
    
    return df