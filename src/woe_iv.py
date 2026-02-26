import numpy as np
import pandas as pd

def calcular_woe_iv(df, coluna_feature, coluna_target):
    """
    Calcula Weight of Evidence (WoE) e Information Value (IV) para uma variável categórica.
    Regra de Auditoria: Inclui fator de suavização (Laplace) para evitar log(0).
    """
    df_agrupado = df.groupby(coluna_feature)[coluna_target].agg(['count', 'sum']).reset_index()
    df_agrupado.rename(columns={'count': 'total_obs', 'sum': 'bons'}, inplace=True)
    
    df_agrupado['maus'] = df_agrupado['total_obs'] - df_agrupado['bons']
    
    df_agrupado['prop_bons'] = (df_agrupado['bons'] + 0.5) / df_agrupado['bons'].sum()
    df_agrupado['prop_maus'] = (df_agrupado['maus'] + 0.5) / df_agrupado['maus'].sum()
    
    df_agrupado['WoE'] = np.log(df_agrupado['prop_bons'] / df_agrupado['prop_maus'])
    df_agrupado['IV'] = (df_agrupado['prop_bons'] - df_agrupado['prop_maus']) * df_agrupado['WoE']
    
    return df_agrupado.sort_values(by='WoE')


