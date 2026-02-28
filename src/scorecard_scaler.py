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