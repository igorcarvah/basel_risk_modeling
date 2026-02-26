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


def aplicar_woe_carteira(df_principal, df_woe_calculado, coluna_feature):
    """
    Injeta o valor matemático do WoE na base principal substituindo a categoria em texto.
    Regra de Auditoria: Uso exclusivo de dicionários e .map() para O(1) de complexidade.
    Blindagem: Preenchimento de nulos com 0 (WoE neutro) para categorias não vistas.
    """
    # 1. Criação do Dicionário de De-Para (A chave do cofre)
    # Pegamos a tabela agrupada e transformamos em um dicionário { 'Categoria': Valor_WoE }
    nome_nova_coluna = f"{coluna_feature}woe"
    df_principal[nome_nova_coluna] = df_principal[coluna_feature].map(dicionario_woe)

    # 3. Mitigação de Risco Operacional (O pulo do gato do Auditor)
    # Se amanhã entrar um cliente com uma profissão que não existia na base de treino,
    # o .map() vai gerar um NaN (Nulo). Nulo quebra a Regressão Logística.
    # Preenchemos com 0, que no WoE significa "Risco Neutro" (nem bom, nem ruim).
    df_principal[nome_nova_coluna] = df_principal[nome_nova_coluna].fillna(0)

    return df_principal


def injetar_woe_na_base(df, df_tabela_woe, coluna_feature):
    """
    Substitui as categorias originais pelos seus respectivos valores de WoE.
    Regra de Auditoria: Uso de .map() para garantir complexidade O(1).
    """
    # 1. Criamos o dicionário de mapeamento (A Chave do Cofre)
    mapeamento = dict(zip(df_tabela_woe[coluna_feature], df_tabela_woe['WoE']))
    
    # 2. Aplicamos a transformação na coluna original
    # Criamos uma nova coluna para manter a rastreabilidade do dado bruto
    nome_nova_coluna = f"{coluna_feature}_woe"
    df[nome_nova_coluna] = df[coluna_feature].map(mapeamento)
    
    # 3. Blindagem contra nulos (Categorias não vistas no treino)
    # Atribuímos WoE 0 (Risco Neutro) para evitar quebra do modelo
    df[nome_nova_coluna] = df[nome_nova_coluna].fillna(0)
    
    return df





















    