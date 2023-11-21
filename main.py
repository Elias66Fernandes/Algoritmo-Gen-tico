import random
from Funcoes import *


if __name__ == "__main__":
    
    tamanho_populacao = 1000
    taxa_sobrevivencia = 0.80
    taxa_selecao_pais = 0.20
    taxa_mutacao = 0.1
    taxa_imigracao = 0.1
    possivel_mutacao = int(tamanho_populacao * 0.1)
    
    # Listas para acompanhar o progresso
    melhores_avaliacoes = []
    medias_avaliacoes = []
    
    populacao = gerar_populacao(tamanho_populacao)
    geracao = 0
    
    '''resposta_teste =    [1, 'Noruegues', 'Amarela', 'Gatos', 'Agua', 'Dunhill',
                        2, 'Dinamarques', 'Azul', 'Cavalos', 'Cha', 'Blends',
                        3, 'Ingles', 'Vermelha', 'Passaros', 'Leite', 'Pall Mall',
                        4, 'Alemao', 'Verde', 'Peixes', 'Cafe', 'Prince',
                        5, 'Sueco', 'Branca', 'Cachorros', 'Cerveja', 'Bluemaster']
    
    populacao.append(resposta_teste)'''
    
    while True:
       # Avalia a aptidão de cada genoma na população
        avaliacoes = [avaliar_genoma(genoma) for genoma in populacao]

        # Informações para acompanhamento
        melhor_avaliacao = max(avaliacoes)
        media_avaliacao = sum(avaliacoes) / len(avaliacoes)
        melhores_avaliacoes.append(melhor_avaliacao)
        medias_avaliacoes.append(media_avaliacao)
        
        # Verificar se alguma solução atende a todos os critérios
        if melhor_avaliacao == 16:  # (Número total de regras)
            melhor_genoma = populacao[avaliacoes.index(16)]
            print("Solução encontrada na geração:", geracao)
            print("Melhor Genoma:", melhor_genoma)
            print("Avaliação:", avaliar_genoma(melhor_genoma))
            break
        
        if len(populacao) > 10000:
            sobreviventes = sobrevive_proporcional(populacao, 0.1)
        else:
            # Seleciona os sobreviventes
            sobreviventes = sobrevive_proporcional(populacao, taxa_sobrevivencia)
        
        # Seleciona os pais para o cruzamento
        pais = selecao_pais(sobreviventes, taxa_selecao_pais)
        
        # Gera os filhos
        descendentes = realizar_crossover(pais)
        
        #para ocorrer uma mutação
        # Passo 1: Seleciona aleatoriamente 10 índices na listas de sobreviventes
        indices_mutacao = random.sample(range(len(sobreviventes)), possivel_mutacao)

        # Passo 2: Para cada índice selecionado, chama a função de mutação
        for indice in indices_mutacao:
            sobreviventes[indice] = mutacao(sobreviventes[indice], taxa_mutacao)
        
        
        # Adiciona os imigrantes a nova população    
        imigrantes = imigracao(len(sobreviventes), taxa_imigracao)
        
        nova_populacao = sobreviventes + descendentes + imigrantes
        
        populacao = nova_populacao
        
        print(f"Geração: {geracao + 1} | Número de Genomas: {len(populacao)} | Melhor Avaliação: {melhor_avaliacao} | Média Avaliação: {media_avaliacao:.5f}")
        
        geracao += 1