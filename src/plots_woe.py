import matplotlib.pyplot as plt
import seaborn as sns

def auditar_tendencia_woe(df_woe_calculado, coluna_feature):
    """
    Plota a tendência do WoE e a volumetria da categoria.
    Regra de Auditoria: Foco na monotonicidade. O gráfico deve contar a história do risco.
    """
    # Ordena as categorias para garantir a leitura sequencial correta
    df_plot = df_woe_calculado.sort_values(by=coluna_feature)
    
    # Setup do painel (O painel de instrumentos do avião)
    fig, ax1 = plt.subplots(figsize=(10, 5))
    
    # Eixo 1 (Barras): Volumetria de Clientes (Tem cliente suficiente nessa faixa?)
    sns.barplot(x=coluna_feature, y='total_obs', data=df_plot, color='lightgray', ax=ax1, alpha=0.7)
    ax1.set_ylabel('Volume de Clientes (Contagem)', color='gray')
    ax1.tick_params(axis='y', labelcolor='gray')
    
    # Eixo 2 (Linha): A força do Risco (O WoE)
    ax2 = ax1.twinx()
    sns.lineplot(x=coluna_feature, y='WoE', data=df_plot, marker='o', color='darkred', ax=ax2, linewidth=2)
    ax2.set_ylabel('Weight of Evidence (WoE)', color='darkred')
    ax2.tick_params(axis='y', labelcolor='darkred')
    
    # Linha zero do WoE (O ponto neutro)
    ax2.axhline(0, ls='--', color='black', alpha=0.5)
    
    plt.title(f'Auditoria de Risco e Volumetria: {coluna_feature}\n(IV Total: {df_plot["IV"].sum():.4f})')
    plt.grid(False)
    plt.show()