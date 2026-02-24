import pandas as pd
from pathlib import Path
import sys

def carregar_base_basileia(nome_arquivo='loan_data_2007_2014.csv'):
    """
    Auditoria: Mapeia a rota do disco dinamicamente e carrega a base.
    """
    # GPS Inteligente embutido no motor
    raiz = Path.cwd() if Path.cwd().joinpath('src').exists() else Path.cwd().parent
    
    # Rota direta para o cofre de dados (sem duplicar o nome da pasta raiz)
    file_path = raiz / 'data' / nome_arquivo
    
    if file_path.exists():
        print(f"STATUS: Rota confirmada. Iniciando leitura de {nome_arquivo}...")
        df = pd.read_csv(file_path, low_memory=False) 
        print(f"SUCESSO: {len(df)} linhas extraídas para a RAM.")
        return df
    else:
        print(f"STATUS: LOSS OPERACIONAL. Arquivo não encontrado em: {file_path}")
        sys.exit("Execução abortada por falta de dados.")