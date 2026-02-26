import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve


def auditar_tendencia_woe(df_woe_calculado, coluna_feature):
    """
    Plota a tendência do WoE e a volumetria da categoria.
    Regra de Auditoria: Ordenação por WoE para variáveis nominais e rotação de labels.
    """
    # ORDENAÇÃO DE RISCO: 
    # Em vez de ordem alfabética, ordenamos do maior WoE (Menor Risco) para o menor (Maior Risco)
    # Isso ajuda a visualizar a 'escadinha' mesmo em variáveis como 'purpose'
    df_plot = df_woe_calculado.sort_values(by='WoE', ascending=False)
    
    # Setup do painel
    fig, ax1 = plt.subplots(figsize=(12, 6)) # Aumentamos um pouco a largura
    
    # Eixo 1 (Barras): Volumetria
    sns.barplot(x=coluna_feature, y='total_obs', data=df_plot, color='lightgray', ax=ax1, alpha=0.7)
    ax1.set_ylabel('Volume de Clientes (Contagem)', color='gray')
    ax1.tick_params(axis='y', labelcolor='gray')
    
    # AJUSTE DE INFRAESTRUTURA: Rotação dos nomes das categorias
    # Isso evita o encavalamento de nomes longos como 'debt_consolidation'
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, horizontalalignment='right')
    
    # Eixo 2 (Linha): Força do Risco (WoE)
    ax2 = ax1.twinx()
    sns.lineplot(x=coluna_feature, y='WoE', data=df_plot, marker='o', color='darkred', ax=ax2, linewidth=2)
    ax2.set_ylabel('Weight of Evidence (WoE)', color='darkred')
    ax2.tick_params(axis='y', labelcolor='gray')
    
    # Linha zero (Ponto Neutro)
    ax2.axhline(0, ls='--', color='black', alpha=0.5)
    
    plt.title(f'Auditoria de Risco e Volumetria: {coluna_feature}\n(IV Total: {df_plot["IV"].sum():.4f})')
    plt.grid(False)
    
    # Ajuste automático para não cortar o texto rotacionado no salvamento/exibição
    plt.tight_layout() 
    plt.show()





def auditar_curva_roc(y_test, probabilidades, gini):
    """
    Plota o Laudo Preditivo do Scorecard (Curva ROC).
    Regra de Auditoria: Nenhuma matemática complexa aqui, apenas visualização (UI).
    """
    fpr, tpr, thresholds = roc_curve(y_test, probabilidades)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkred', lw=2, label=f'Curva ROC (GINI = {gini*100:.1f}%)')
    plt.plot([0, 1], [0, 1], color='gray', linestyle='--') # Linha do cara-ou-coroa
    plt.title('Laudo Preditivo: Capacidade de Separação do Scorecard')
    plt.xlabel('Taxa de Falsos Positivos (Bons clientes taxados como caloteiros)')
    plt.ylabel('Taxa de Verdadeiros Positivos (Caloteiros reais barrados)')
    plt.legend(loc='lower right')
    plt.grid(alpha=0.3)
    
    # Ajuste automático do layout
    plt.tight_layout()
    plt.show()