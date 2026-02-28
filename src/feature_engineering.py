import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# ===================================================================
# 1. UTILITÁRIOS E GOVERNANÇA (Base)
# ===================================================================
def padronizar_tempo_emprego(df, coluna='emp_length'):
    serie_limpa = (
        df[coluna]
        .str.replace(r'\+ years|\+years| years| year', '', regex=True)
        .str.replace('< 1', '0')
        .str.replace('<1', '0')
        .str.replace('n/a', '0')
    )
    return pd.to_numeric(serie_limpa, errors='coerce')

def calcular_historico_credito(df, coluna_data_str, data_corte='2017-12-01'):
    data_ref = pd.to_datetime(data_corte)
    dt_temp = pd.to_datetime(df[coluna_data_str], format='%b-%y')
    meses_brutos = ((data_ref.year - dt_temp.dt.year) * 12) + (data_ref.month - dt_temp.dt.month)
    return np.where(meses_brutos < 0, meses_brutos + 1200, meses_brutos)

def definir_variavel_alvo(df):
    status_ruins = ['Charged Off', 'Default', 'Does not meet the credit policy. Status:Charget Off', 'Late (31-120 days)']
    df['good_bad_loan'] = np.where(df['loan_status'].isin(status_ruins), 0, 1)
    return df

def criar_variaveis_dummy(df, columns_categoricas):
    df_dummies = pd.get_dummies(df[columns_categoricas], prefix_sep=':', drop_first=True)
    df_limpo = df.drop(columns=columns_categoricas)
    return pd.concat([df_limpo, df_dummies], axis=1)

def imputar_dados_nulos(df):
    df['total_rev_hi_lim'] = df['total_rev_hi_lim'].fillna(df['funded_amnt'])
    return df

def remover_colunas_toxicas(df, limite_toxicidade=0.50):
    percentual_nulos = df.isnull().mean()
    colunas_para_ejetar = percentual_nulos[percentual_nulos > limite_toxicidade].index
    return df.drop(columns=colunas_para_ejetar)

def dividir_treino_teste(df, target_col='good_bad_loan', test_size=0.2, random_state=42):
    if target_col not in df.columns:
        raise KeyError(f"Variável alvo '{target_col}' não encontrada na base de dados!")
    X = df.drop(target_col, axis=1)
    y = df[target_col]
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

# ===================================================================
# 2. ENGENHARIA V2: HIGIENE + MÉTRICA FGV + DTI TÉCNICO
# ===================================================================
def categorizar_renda_dti(df):
    """
    Auditoria V2: Categorização de Renda e DTI sem perda de dados (Zero Data Loss).
    Régua FGV calibrada para Salário Mínimo base R$ 1.380 (Conforme documentação).
    """
    df_temp = df.copy()
    
    # Checkpoint de Segurança
    if 'good_bad_loan' not in df_temp.columns:
        raise KeyError("ERRO DE LINHAGEM: A coluna 'good_bad_loan' precisa existir!")

    # 1. TRATAMENTO SEM EXCLUSÃO (Floor Técnico)
    df_temp['annual_inc'] = np.where(df_temp['annual_inc'] < 0, 0, df_temp['annual_inc'])
    
    # 2. RÉGUA DE RENDA FGV (Calibrada conforme base do Comitê: SM R$ 1.380)
    # Valores mensais multiplicados por 12 para parear com a Renda Anual (annual_inc)
    bins_renda = [-float('inf'), 33120, 66240, 165600, 331200, float('inf')]
    labels_renda = [
        '1. Classe E (Ate 2.7k/mes)', 
        '2. Classe D (2.7k-5.5k/mes)', 
        '3. Classe C (5.5k-13.8k/mes)', 
        '4. Classe B (13.8k-27.6k/mes)', 
        '5. Classe A (>27.6k/mes)'
    ]
    df_temp['faixa_renda'] = pd.cut(df_temp['annual_inc'], bins=bins_renda, labels=labels_renda).astype(str)
    
    # 3. RÉGUA DE DTI
    bins_dti = [-float('inf'), 10.0, 20.0, 30.0, float('inf')]
    labels_dti = ['1. Saudavel (<10%)', '2. Alerta (10-20%)', '3. Risco (20-30%)', '4. Critico (>30%)']
    df_temp['faixa_dti'] = pd.cut(df_temp['dti'], bins=bins_dti, labels=labels_dti).astype(str)
    
    return df_temp


def padronizar_home_ownership(df):
    """
    Auditoria V2: Higiene de categorias de baixo volume.
    Agrupa lixos operacionais ('NONE', 'ANY') na categoria 'OTHER' 
    para garantir estabilidade estatística no cálculo do WoE.
    """
    df_temp = df.copy()
    
    # Substitui os valores tóxicos pela categoria genérica
    df_temp['home_ownership'] = df_temp['home_ownership'].replace(['NONE', 'ANY'], 'OTHER')
    
    return df_temp