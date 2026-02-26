import pandas as pd
import sys
from pathlib import Path

# ===================================================================
# FERRAMENTA 1: EXTRAÇÃO DE DADOS
# ===================================================================
def carregar_base_basileia(nome_arquivo='loan_data_2007_2014.csv'):
    """
    Auditoria: Mapeia a rota do disco dinamicamente e carrega a base.
    """
    raiz = Path.cwd() if Path.cwd().joinpath('src').exists() else Path.cwd().parent
    file_path = raiz / 'data' / nome_arquivo
    
    if file_path.exists():
        print(f"STATUS: Rota confirmada. Iniciando leitura de {nome_arquivo}...")
        df = pd.read_csv(file_path, low_memory=False) 
        print(f"SUCESSO: {len(df)} linhas extraídas para a RAM.")
        return df
    else:
        print(f"STATUS: LOSS OPERACIONAL. Arquivo não encontrado em: {file_path}")
        sys.exit("Execução abortada por falta de dados.")


# ===================================================================
# FERRAMENTA 2: EXPURGO DE DADOS TÓXICOS (O BISTURI QUE FALTAVA)
# ===================================================================
def remover_colunas_toxicas(df, limite_toxicidade=0.50):
    """
    Auditoria: Varre a base e expurga colunas com excesso de buracos (dados faltantes).
    Regra de Negócio: Se mais de 50% da coluna é nula, ela é lixo estatístico.
    """
    # Calcula quantos dados válidos no mínimo a coluna precisa ter para sobreviver
    min_validos = int(len(df) * (1 - limite_toxicidade))
    
    # O motor do Pandas corta fora o que não atinge o limite
    df_limpo = df.dropna(thresh=min_validos, axis=1)
    
    colunas_removidas = len(df.columns) - len(df_limpo.columns)
    print(f"AUDITORIA ETL: {colunas_removidas} colunas tóxicas expurgadas da base (Limiar de corte: {limite_toxicidade*100}% nulos).")
    
    return df_limpo