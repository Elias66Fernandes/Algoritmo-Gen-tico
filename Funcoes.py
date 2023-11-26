import random


def gerar_genoma():
    # Define as características
    nacionalidades = ['Noruegues', 'Ingles', 'Sueco', 'Dinamarques', 'Alemao']
    cores = ['Vermelha', 'Verde', 'Branca', 'Amarela', 'Azul']
    animais = ['Cachorros', 'Passaros', 'Gatos', 'Cavalos', 'Peixes']
    bebidas = ['Cha', 'Cafe', 'Leite', 'Cerveja', 'Agua']
    cigarros = ['Blends', 'Pall Mall', 'Dunhill', 'Bluemaster', 'Prince']
    num_casa = [1, 2, 3, 4, 5]

    # Criar um genoma
    genoma = []

    # Adiciona os números das casa, nacionalidades, cores, animais, bebidas, e cigarros (Gera 30 genes)
    for i in range(5):
        genoma.append(num_casa[i])
        genoma.append(random.choice(list(set(nacionalidades) - set(genoma))))
        genoma.append(random.choice(list(set(cores) - set(genoma))))
        genoma.append(random.choice(list(set(animais) - set(genoma))))
        genoma.append(random.choice(list(set(bebidas) - set(genoma))))
        genoma.append(random.choice(list(set(cigarros) - set(genoma))))
    return genoma

# Gera uma população com vários genomas
def gerar_populacao(tamanho_populacao):
    populacao = [gerar_genoma() for k in range(tamanho_populacao)]
    return populacao


def avaliar_genoma(genoma):
    vizinhas = lambda casa1, casa2: abs(int(casa1['Numero']) - int(casa2['Numero'])) == 1

    regra1 = lambda casas: casas[0]['Nacionalidade'] == 'Noruegues'
    regra2 = lambda casas: next((casa for casa in casas if casa['Nacionalidade'] == 'Ingles'
                                and casa['Cor'] == 'Vermelha'), None) is not None
    regra3 = lambda casas: next((casa for casa in casas if casa['Nacionalidade'] == 'Sueco'
                                and casa['Animal'] == 'Cachorros'), None) is not None
    regra4 = lambda casas: next((casa for casa in casas if casa['Nacionalidade'] == 'Dinamarques'
                                and casa['Bebida'] == 'Cha'), None) is not None
    regra5 = lambda casas: next((True for casa1, casa2 in zip(casas, casas[1:]) if casa1['Cor'] == 'Verde'
                                and casa2['Cor'] == 'Branca' and abs(int(casa1['Numero']) - int(casa2['Numero'])) == 1), False)
    regra6 = lambda casas: next((True for casa in casas if casa['Cor'] == 'Verde' and casa['Bebida'] == 'Cafe'), False)
    regra7 = lambda casas: next((True for casa in casas if casa['Cigarro'] == 'Pall Mall' and casa['Animal'] == 'Passaros'), False)
    regra8 = lambda casas: next((True for casa in casas if casa['Cor'] == 'Amarela' and casa['Cigarro'] == 'Dunhill'), False)
    regra9 = lambda casas: next((casa for casa in casas if casa['Bebida'] == 'Leite' and casa['Numero'] == 3), None) is not None
    regra10 = lambda casas: next((True for casa1, casa2 in zip(casas, casas[1:]) if casa1['Cigarro'] == 'Blends'
                                and casa2['Animal'] == 'Gatos'), True)
    regra11 = lambda casas: next((True for casa1, casa2 in zip(casas, casas[1:]) if casa1['Animal'] == 'Cavalos'
                             and casa2['Cigarro'] == 'Dunhill' or casa1['Cigarro'] == 'Dunhill' and casa2['Animal'] == 'Cavalos'), False)
    regra12 = lambda casas: next((True for casa in casas if casa['Cigarro'] == 'Bluemaster' and casa['Bebida'] == 'Cerveja'), False)
    regra13 = lambda casas: next((True for casa in casas if casa['Nacionalidade'] == 'Alemao' and casa['Cigarro'] == 'Prince'), False)
    regra14 = lambda casas: next((True for casa1, casa2 in zip(casas, casas[1:]) if casa1['Nacionalidade'] == 'Noruegues'
                                and casa2['Cor'] == 'Azul' and abs(int(casa1['Numero']) - int(casa2['Numero'])) == 1), False)
    #regra15 = lambda casas: any((casa1['Cigarro'] == 'Blends' and vizinhas(casa1, casa2) and casa2['Bebida'] == 'Agua') or
                            #(casa2['Cigarro'] == 'Blends' and vizinhas(casa1, casa2) and casa1['Bebida'] == 'Agua')
                            #for casa1, casa2 in zip(casas, casas[1:]))
    regra15 = lambda casas: next(( True for casa1, casa2 in zip(casas, casas[1:]) if
                             (casa1['Cigarro'] == 'Blends' and vizinhas(casa1, casa2) and casa2['Bebida'] == 'Agua') or
                             (casa2['Cigarro'] == 'Blends' and vizinhas(casa1, casa2) and casa1['Bebida'] == 'Agua')), False)

    


    casas = [
        {'Numero': genoma[i], 'Nacionalidade': genoma[i+1], 'Cor': genoma[i+2],
         'Animal': genoma[i+3], 'Bebida': genoma[i+4], 'Cigarro': genoma[i+5]}
        for i in range(0, len(genoma), 6)
    ]

    # Avaliação usando as expressões lambda
    nota_total = sum([regra1(casas), regra2(casas), regra3(casas), regra4(casas),
                    regra5(casas), regra6(casas), regra7(casas), regra8(casas),
                    regra9(casas), regra10(casas), regra11(casas), regra12(casas),
                    regra13(casas), regra14(casas), regra15(casas)])
    
    return nota_total



def sobrevive_proporcional(populacao, taxa_sobrevivencia):
    populacao_ordenada = sorted(populacao, key=lambda genoma: avaliar_genoma(genoma), reverse=True)
    pontuacoes = [avaliar_genoma(genoma) for genoma in populacao_ordenada]
    total_pontuacao = sum(pontuacoes)
    probabilidades = [pontuacao / total_pontuacao for pontuacao in pontuacoes]
    num_sobreviventes = int(len(populacao) * taxa_sobrevivencia)

    sobreviventes = []
    while len(sobreviventes) < num_sobreviventes:
        # random.choices para garantir a aleatoriedade na roleta
        indice_sobrevivente = random.choices(range(len(populacao_ordenada)), weights=probabilidades, k=1)[0]
        
        # Evita repetições
        if indice_sobrevivente not in sobreviventes:
            sobreviventes.append(indice_sobrevivente)

    #lista final de sobreviventes
    sobreviventes = [populacao_ordenada[i] for i in sobreviventes]

    return sobreviventes


def selecao_pais(populacao, taxa_selecao_pais):
    # Ordena a população por pontuação em ordem decrescente
    populacao_ordenada = sorted(populacao, key=lambda genoma: avaliar_genoma(genoma), reverse=True)
    
    # Calcula as probabilidades de seleção proporcional à pontuação
    pontuacoes = [avaliar_genoma(genoma) for genoma in populacao_ordenada]
    total_pontuacao = sum(pontuacoes)
    probabilidades = [pontuacao / total_pontuacao for pontuacao in pontuacoes]
    
    # Calcula o número de pais com base na taxa de seleção de pais
    num_pais = int(len(populacao) * taxa_selecao_pais)
    
    if num_pais % 2 != 0:
        num_pais -= 1
    
    # Selecionar pais sem repetição
    pais_indices = set()
    while len(pais_indices) < num_pais:
        indice_pai = random.choices(range(len(populacao_ordenada)), weights=probabilidades, k=1)[0]
        if indice_pai not in pais_indices:
            pais_indices.add(indice_pai)
    
    # Gerar a lista final de pais
    pais = [populacao_ordenada[i] for i in pais_indices]
    
    return pais


def crossover(pai1,pai2):
    ponto_corte = random.randint(1,5)
    filho1 = []
    filho2 = []
    carac_corte_p1 = []
    carac_corte_p2 = []
    
    if ponto_corte == 5:
        for corte in range(ponto_corte, len(pai1), 6):
            carac_corte_p1.append(pai1[corte])
            carac_corte_p2.append(pai2[corte])
        cont = 0
        for n in pai1:
            filho1.append(n)
        for n in pai2:
            filho2.append(n)
        for n in range(ponto_corte, len(pai1), 6):
            filho1[n] = carac_corte_p2[cont]
            filho2[n] = carac_corte_p1[cont]
            cont += 1
        
    elif ponto_corte == 4:
        for corte in range(ponto_corte, len(pai1), 6):
            carac_corte_p1.append(pai1[corte])
            carac_corte_p1.append(pai1[corte+1])
            carac_corte_p2.append(pai2[corte])
            carac_corte_p2.append(pai2[corte+1])
        cont = 0
        for n in pai1:
            filho1.append(n)
        for n in pai2:
            filho2.append(n)
        for n in range(ponto_corte, len(pai1), 6):
            filho1[n] = carac_corte_p2[cont]
            filho2[n] = carac_corte_p1[cont]
            filho1[n+1]= carac_corte_p2[cont+1]
            filho2[n+1]= carac_corte_p1[cont+1]
            cont += 2
        
    elif ponto_corte == 3:
        for corte in range(ponto_corte, len(pai1), 6):
            carac_corte_p1.append(pai1[corte])
            carac_corte_p1.append(pai1[corte+1])
            carac_corte_p1.append(pai1[corte+2])
            carac_corte_p2.append(pai2[corte])
            carac_corte_p2.append(pai2[corte+1])
            carac_corte_p2.append(pai2[corte+2])
        cont = 0
        for n in pai1:
            filho1.append(n)
        for n in pai2:
            filho2.append(n)
        for n in range(ponto_corte, len(pai1), 6):
            filho1[n] = carac_corte_p2[cont]
            filho2[n] = carac_corte_p1[cont]
            filho1[n+1]= carac_corte_p2[cont+1]
            filho2[n+1]= carac_corte_p1[cont+1]
            filho1[n+2]= carac_corte_p2[cont+2]
            filho2[n+2]= carac_corte_p1[cont+2]
            cont += 3
    
    elif ponto_corte == 2:
        for corte in range(ponto_corte, len(pai1), 6):
            carac_corte_p1.append(pai1[corte])
            carac_corte_p1.append(pai1[corte+1])
            carac_corte_p1.append(pai1[corte+2])
            carac_corte_p1.append(pai1[corte+3])
            carac_corte_p2.append(pai2[corte])
            carac_corte_p2.append(pai2[corte+1])
            carac_corte_p2.append(pai2[corte+2])
            carac_corte_p2.append(pai2[corte+3])
        cont = 0
        for n in pai1:
            filho1.append(n)
        for n in pai2:
            filho2.append(n)
        for n in range(ponto_corte, len(pai1), 6):
            filho1[n] = carac_corte_p2[cont]
            filho2[n] = carac_corte_p1[cont]
            filho1[n+1]= carac_corte_p2[cont+1]
            filho2[n+1]= carac_corte_p1[cont+1]
            filho1[n+2]= carac_corte_p2[cont+2]
            filho2[n+2]= carac_corte_p1[cont+2]
            filho1[n+3]= carac_corte_p2[cont+3]
            filho2[n+3]= carac_corte_p1[cont+3]
            cont += 4
    
    elif ponto_corte == 1:
        for corte in range(ponto_corte, len(pai1), 6):
            carac_corte_p1.append(pai1[corte])
            carac_corte_p2.append(pai2[corte])
        cont = 0
        for n in pai1:
            filho1.append(n)
        for n in pai2:
            filho2.append(n)
        for n in range(ponto_corte, len(pai1), 6):
            filho1[n] = carac_corte_p2[cont]
            filho2[n] = carac_corte_p1[cont]
            cont += 1

    return filho1, filho2


def realizar_crossover(pais):
    descendentes = []
    for i in range(0, len(pais), 2):
        pai1 = pais[i]
        pai2 = pais[i + 1]
        filho1, filho2 = crossover(pai1, pai2)
        descendentes.extend([filho1, filho2])
    return descendentes


def mutacao(genoma, taxa_mutacao):
    caracteristica = random.randint(1, 5)
    mutacao = []
    genoma_mutado = genoma.copy()  # Usando uma cópia do genoma
    
    if random.random() <= taxa_mutacao:
        for ale in range(caracteristica, len(genoma), 6):
            mutacao.append(genoma[ale])
            
        random.shuffle(mutacao)

        cont = 0
        for novo in range(caracteristica, len(genoma), 6):
            genoma_mutado[novo] = mutacao[cont]
            cont += 1
    
    return genoma_mutado

def imigracao(tamanho_populacao,taxa_imigracao):
    # Adiciona novos genomas à população com base na taxa de imigração
    num_imigrantes = int(tamanho_populacao * taxa_imigracao)
    novos_genomas = gerar_populacao(num_imigrantes)
    return novos_genomas


""""
resposta_teste = [1, 'Noruegues', 'Amarela', 'Gatos', 'Agua', 'Dunhill',
                  2, 'Dinamarques', 'Azul', 'Cavalos', 'Cha', 'Blends',
                  3, 'Ingles', 'Vermelha', 'Passaros', 'Leite', 'Pall Mall',
                  4, 'Alemao', 'Verde', 'Peixes', 'Cafe', 'Prince',
                  5, 'Sueco', 'Branca', 'Cachorros', 'Cerveja', 'Bluemaster']

cromossomo_exemplo = [1, 'Dinamarques', 'Amarela', 'Gatos', 'Leite', 'Pall Mall',
                      2, 'Sueco', 'Vermelha', 'Peixes', 'Cha', 'Prince',
                      3, 'Alemao', 'Branca', 'Cavalos', 'Agua', 'Dunhill',
                      4, 'Ingles', 'Azul', 'Passaros', 'Cerveja', 'Blends',
                      5, 'Noruegues', 'Verde', 'Cachorros', 'Cafe', 'Bluemaster']

teste = [1, 'Noruegues', 'Amarela', 'Cavalos', 'Cerveja', 'Dunhill',
         2, 'Dinamarques', 'Azul', 'Passaros', 'Cha', 'Pall Mall',
         3, 'Ingles', 'Vermelha', 'Peixes', 'Leite', 'Bluemaster',
         4, 'Sueco', 'Verde', 'Cachorros', 'Cafe', 'Blends',
         5, 'Alemao', 'Branca', 'Gatos', 'Agua', 'Prince']

populacao = []

populacao.append(teste)
populacao.append(resposta_teste)


#print(melhor_genoma_encontrado)
descendetes = realizar_crossover(populacao)
melhor_genoma_encontrado = max(descendetes, key=avaliar_genoma)
print(avaliar_genoma(melhor_genoma_encontrado))"""
