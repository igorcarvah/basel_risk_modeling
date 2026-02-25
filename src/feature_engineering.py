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


def definir_variavel_alvo(df):
    """
    Auditoria: Centraliza a regra de negócios corporativa que define o Default (Calote).
    Cria a variável alvo 'good_bad_loan' (1 = Lucro, 0 = Loss).
    """
    # A lista oficial de status radioativos
    status_ruins = ['Charged Off', 'Default', 'Does not meet the credit policy. Status:Charget Off', 'Late (31-120 days)']

    # O motor vetorizado de alta performance
    df['good_bad_loan'] = np.where(df['loan_status'].isin(status_ruins), 0, 1)

    return df


def criar_variaveis_dummy (df, columns_categoricas):
     
     """
    Auditoria: Executa o One-Hot Encoding vetorizado e previne a Armadilha da Variável Dummy.
    Substitui as colunas de texto originais pelas binárias no DataFrame.
    """
     # 1. Cria as dummies com trava de colinearidade (drop_first=True)
     df_dummies = pd.get_dummies(df[columns_categoricas], prefix_sep=':', drop_first= True)

     #2. Remove as colunas de texto originais para não poluir o modelo
     df_limpo = df.drop(columns=columns_categoricas)

     # 3. Funde a base limpa com as novas matrizes binárias
     df_final = pd.concat([df_limpo, df_dummies], axis=1)

     return df_final


def imputar_dados_nulos(df):
    """
    Auditoria: Preenche a Dívida Técnica (NaN) usando regras de negócios corporativas (Proxies).
    Prevenção de Loss Operacional: Usa reatribuição direta, eliminando o uso de inplace=True.
    """
    # Regra 1: Limite de Crédito Rotativo
    # Racional de Negócio: Se o limiti é desconhecido, assumimos o valor do emprestimo atual.
    df['total_rev_hi_lim'] = df['total_rev_hi_lim'].fillna(df['funded_amnt'])

    # (A sala está pronta. Novas regras de imputação para outras colunas entrarão aqui abaixo no futuro)

    return df


def remover_colunas_toxicas (df, limite_toxicidade =0.50):
    """
    Auditoria: Varre a matriz e ejeta automaticamente colunas com % de Dívida Técnica (NaN) 
    acima do limite estabelecido pelo Comitê de Risco (Padrão: 50%).
    """
    # 1. Calcula i percentual de nulos de todas as colunas
    percentual_nulos = df.isnull().mean()

    # 2. Identifica os vaores alvos (colunas que estouram o limite)
    colunas_para_ejetar = percentual_nulos[percentual_nulos> limite_toxicidade].index

    # 3. Dá p write_off (baixa) nos ativos tóxicos
    df_limpo = df.drop(columns=colunas_para_ejetar)

    return df_limpo
    