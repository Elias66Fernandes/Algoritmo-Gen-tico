import random
from Funcoes import *


if __name__ == "__main__":
    
    tamanho_populacao = 1000
    taxa_sobrevivencia = 0.8 
    taxa_selecao_pais = 0.40 # Quantos por cento dos sobreviventes serão pais
    taxa_mutacao = 0.8 # A chance que os individuos tem de mutar
    taxa_imigracao = 0.20 
    
    # Listas para acompanhar o progresso
    melhores_avaliacoes = []
    medias_avaliacoes = []
    
    
    populacao = gerar_populacao(tamanho_populacao)
    geracao = 0
    
    
    while True:
           
       # Avalia a aptidão de cada genoma na população
        avaliacoes = [avaliar_genoma(genoma) for genoma in populacao]

        # Informações para acompanhamento
        melhor_avaliacao = max(avaliacoes)
        media_avaliacao = sum(avaliacoes) / len(avaliacoes)
        melhores_avaliacoes.append(melhor_avaliacao)
        medias_avaliacoes.append(media_avaliacao)
        
        # Verificar se alguma solução atende a todos os critérios
        if melhor_avaliacao == 15:  # (Número total de regras)
            melhor_genoma = populacao[avaliacoes.index(15)]
            print("Solução encontrada na geração:", geracao + 1)
            print("Melhor Genoma:", melhor_genoma)
            print("Avaliação:", avaliar_genoma(melhor_genoma))
            
            print("\nFenótipo:\n")
            
            for i in range(0, len(melhor_genoma),6):
                print(f'Casa Número: {melhor_genoma[i]}\nNacionalidade: {melhor_genoma[i+1]} | Cor: {melhor_genoma[i+2]} | Animal: {melhor_genoma[i+3]} | Bebida: {melhor_genoma[i+4]} | Cigarro: {melhor_genoma[i+5]}')
            break
        
        if len(populacao) > 10000:
            sobreviventes = sobrevive_proporcional(populacao, 0.2)
        else:
            # Seleciona os sobreviventes
            sobreviventes = sobrevive_proporcional(populacao, taxa_sobrevivencia)
        
        # Seleciona os pais para o cruzamento
        pais = selecao_pais(sobreviventes, taxa_selecao_pais)
        
        # Gera os filhos
        descendentes = realizar_crossover(pais)
        
        #para ocorrer uma mutação
        possivel_mutacao = int(len(sobreviventes) * 0.1) # Quantos individuos podem ou não mutar
        # Passo 1: Seleciona aleatoriamente índices na listas de sobreviventes
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
        
        
        melhores_avaliacoes.clear()
        medias_avaliacoes.clear()
        avaliacoes.clear()