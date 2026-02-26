import numpy as np

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
