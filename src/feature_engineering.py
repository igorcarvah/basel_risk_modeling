import sys
from pathlib import Path
import pandas as pd
import numpy as np


def padronizar_tempo_emprego(df, coluna='emp_length'):
    """
    Auditoria: Limpa a string de tempo de emprego e converte para Float.
    """
    # Usamos .copy() apenas na série temporária para evitar avisos do Pandas, 
    # não na base inteira.
    serie_limpa = (
        df[coluna]
        .str.replace(r'\+ years|\+years| years| year', '', regex=True)
        .str.replace('< 1', '0')
        .str.replace('<1', '0') # Cobre as duas variações de espaçamento
        .str.replace('n/a', '0')
    )
    
    return pd.to_numeric(serie_limpa, errors='coerce')


def calcular_historico_credito(df, coluna_data_str, data_corte='2017-12-01'):
    """
    Auditoria: Transforma string de data em meses de histórico absolutos e corrige bug do século.
    """
    data_ref = pd.to_datetime(data_corte)
    dt_temp = pd.to_datetime(df[coluna_data_str], format='%b-%y')
    
    # Matemática de Safra
    meses_brutos = ((data_ref.year - dt_temp.dt.year) * 12) + (data_ref.month - dt_temp.dt.month)
    
    # Trava de Segurança (+1200)
    meses_corrigidos = np.where(meses_brutos < 0, meses_brutos + 1200, meses_brutos)
    
    return meses_corrigidos
