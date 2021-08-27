from tabulate import tabulate


def validaEntradaCorreta(letra, numero):
    """
    Confere se as coordenadas recebidas estão dentro das opções válidas
    Parâmetros: letra, numero
    Retorno: True(Opção válida)/False(Opção inválida)
    """
    return letra in ["A", "B", "C"] and numero in ["1", "2", "3"]


def validaEntradaDisponivel(tabuleiro, letra, numero):
    """
    Confere se a coordenada recebida está disponível
    Parâmetros: tabuleiro, letra, numero
    Retorno: True(Disponivel)/False(Indisponivel)
    """
    return tabuleiro[letra][numero - 1] == ""


def validaEntrada(tabuleiro, letraNumero):
    """
    Valida entrada do usuário para possíveis erros de digitação, cordenadas inválidas ou já utilizadas
    Parâmetros: tabuleiro, letraNumero (coordenadas da jogada)
    Retorno: letra e numero (coordenadas da jogada validadas)
    """
    # Valida digitações fora do esperado
    try:
        letra, numero = letraNumero.upper().split()
    except (Exception,):
        return validaEntrada(tabuleiro, input(
            f"Coordenada inválida, digite uma válida: "))
    # Se entrada correta e disponível retorna, caso contrário chama a função novamente
    if validaEntradaCorreta(letra, numero):
        if validaEntradaDisponivel(tabuleiro, letra, int(numero)):
            return letra, int(numero)
        else:
            return validaEntrada(tabuleiro, input(
                f"Coordenadas indisponíveis, digite uma livre: "))
    else:
        return validaEntrada(tabuleiro, input(
            f"Coordenada inválida, digite uma válida: "))


def jogada(tabuleiro, jogador):
    """
    Pede a jogada ao usuario e aplica ao tabuleiro
    :param tabuleiro: tabuleiro atual.
    :param jogador: jogador atual.
    :return: tabuleiro com jogada do usuário.
    """
    letra, numero = validaEntrada(tabuleiro, input(f"Vez do jogador: "))

    tabuleiro[letra][numero - 1] = jogador

    return tabuleiro


def parabenizaGanhador(tabuleiro, jogadorGanhou):
    """
    Imprime o tabuleiro e parabeniza o ganhador
    Parâmetros: tabuleiro e jogador que ganhou
    """
    imprimiTabuleiro(tabuleiro)
    # Parabenização invertida pois jogador da vez veio depois da jogada onde a vitória ocorreu
    if jogadorGanhou == "X":
        print("A máquina ganhou!")
    else:
        print("Você ganhou!")


def imprimiTabuleiro(tabuleiro):
    """
    Imprime o tabuleiro utilizando o tabulate para estilização
    Parâmetros: tabuleiro
    """
    print(tabulate(tabuleiro, headers="keys", tablefmt="fancy_grid"))


def confereGanhador(tabuleiro, jogador):
    """
    Confere linhas, colunas e diagonais pelo padrão de vitória
    :param tabuleiro: tabuleiro atual.
    :param jogador: jogador que fez ultima jogada.
    :return: True(se vitória) / False(se não vitória).
    """
    vitoria = [
        # Confere colunas
        bool([True for col in ["A", "B", "C"] if tabuleiro[col].count(jogador) == 3]),
        # Confere linhas
        bool([True for i in range(3) if tabuleiro["A"][i] == tabuleiro["B"][i] == tabuleiro["C"][i] == jogador]),
        # Confere diagonais
        jogador == tabuleiro["A"][0] == tabuleiro["B"][1] == tabuleiro["C"][2],
        jogador == tabuleiro["A"][2] == tabuleiro["B"][1] == tabuleiro["C"][0]
    ]

    if True in vitoria:
        parabenizaGanhador(tabuleiro, jogador)
        return True
    return False


def confereEmpate(tabuleiro):
    """
    Confere se há espaços disponíveis no tabuleiro
    Parâmetros: tabuleiro
    Retorno: True(Empate)/False(Sem empate)
    """
    if "" not in tabuleiro["A"] + tabuleiro["B"] + tabuleiro["C"]:
        imprimiTabuleiro(tabuleiro)
        print("O jogo empatou!")
        return True
    return False


def confereFim(tabuleiro, jogador, placar):
    """
    Confere se os possiveis finais (vitória de alguma parte) ou empate ocorreram,
    se vitoria, adiciona 1 ponto no placar para jogador.
    Parâmetros: tabuleiro, jogador (que fez a última jogada)
    Retorno: True(Acabou o jogo)/ False(Não acabou o jogo)
    :param tabuleiro: tabuleiro atual.
    :param jogador: jogador que fez a última jogada.
    :param placar: placar atual.
    :return: True(se jogo acabou)/False(se jogo não acabou), placar atualizado.
    """
    acabou = confereGanhador(tabuleiro, jogador)
    if acabou:
        placar[jogador] += 1
    else:
        acabou = confereEmpate(tabuleiro)

    return acabou, placar


def tentarFinalizarPartida(tabuleiro):
    """
    Confere se as sequencias possíveis de finalização de partida são possíveis.
    :param tabuleiro: tabuleiro na situação atual do jogo.
    :return: tabuleiro atualizado com jogada vencedora se houver condição de vitória,
    senão False (jogada não possível).
    """
    if tabuleiro["A"][0] not in ["X", "O"] and \
            ((tabuleiro["A"][1] == "X" and tabuleiro["A"][2] == "X") or
             (tabuleiro["B"][0] == "X" and tabuleiro["C"][0] == "X") or
             (tabuleiro["B"][1] == "X" and tabuleiro["C"][2] == "X")):
        tabuleiro["A"][0] = "X"
    elif tabuleiro["A"][1] not in ["X", "O"] and \
            ((tabuleiro["A"][0] == "X" and tabuleiro["A"][2] == "X") or
             (tabuleiro["B"][1] == "X" and tabuleiro["C"][1] == "X")):
        tabuleiro["A"][1] = "X"
    elif tabuleiro["A"][2] not in ["X", "O"] and \
            ((tabuleiro["A"][0] == "X" and tabuleiro["A"][1] == "X") or
             (tabuleiro["B"][2] == "X" and tabuleiro["C"][2] == "X") or
             (tabuleiro["B"][1] == "X" and tabuleiro["C"][0] == "X")):
        tabuleiro["A"][2] = "X"
    elif tabuleiro["B"][0] not in ["X", "O"] and \
            ((tabuleiro["A"][0] == "X" and tabuleiro["C"][0] == "X") or
             (tabuleiro["B"][1] == "X" and tabuleiro["B"][2] == "X")):
        tabuleiro["B"][0] = "X"
    elif tabuleiro["B"][1] not in ["X", "O"] and \
            ((tabuleiro["B"][0] == "X" and tabuleiro["B"][2] == "X") or
             (tabuleiro["A"][1] == "X" and tabuleiro["C"][1] == "X") or
             (tabuleiro["C"][0] == "X" and tabuleiro["A"][2] == "X") or
             (tabuleiro["A"][0] == "X" and tabuleiro["C"][2] == "X")):
        tabuleiro["B"][1] = "X"
    elif tabuleiro["B"][2] not in ["X", "O"] and \
            ((tabuleiro["B"][0] == "X" and tabuleiro["B"][1] == "X") or
             (tabuleiro["A"][2] == "X" and tabuleiro["C"][2] == "X")):
        tabuleiro["B"][2] = "X"
    elif tabuleiro["C"][0] not in ["X", "O"] and \
            ((tabuleiro["A"][0] == "X" and tabuleiro["B"][0] == "X") or
             (tabuleiro["C"][1] == "X" and tabuleiro["C"][2] == "X") or
             (tabuleiro["B"][1] == "X" and tabuleiro["A"][2] == "X")):
        tabuleiro["C"][0] = "X"
    elif tabuleiro["C"][1] not in ["X", "O"] and \
            ((tabuleiro["C"][0] == "X" and tabuleiro["C"][2] == "X") or
             (tabuleiro["A"][1] == "X" and tabuleiro["B"][1] == "X")):
        tabuleiro["C"][1] = "X"
    elif tabuleiro["C"][2] not in ["X", "O"] and \
            ((tabuleiro["C"][0] == "X" and tabuleiro["C"][1] == "X") or
             (tabuleiro["A"][2] == "X" and tabuleiro["B"][2] == "X") or
             (tabuleiro["A"][0] == "X" and tabuleiro["B"][1] == "X")):
        tabuleiro["C"][2] = "X"
    else:
        return False
    return tabuleiro


def impedirJogadaAdversaria(tabuleiro):
    """
    Confere se as sequencias possíveis de impedir uma futura jogada vencedora adversária são possíveis.
    :param tabuleiro: tabuleiro na situação atual do jogo.
    :return: tabuleiro atualizado com jogada defensiva se houver condição de
    impedir futura jogada vencedora adversária, senão False (jogada não possível).
    """
    # Tentar bloquear jogada casa a casa
    if tabuleiro["A"][0] not in ["X", "O"] and \
            ((tabuleiro["A"][1] == "O" and tabuleiro["A"][2] == "O") or
             (tabuleiro["B"][0] == "O" and tabuleiro["C"][0] == "O") or
             (tabuleiro["B"][1] == "O" and tabuleiro["C"][2] == "O")):
        tabuleiro["A"][0] = "X"
    elif tabuleiro["A"][1] not in ["X", "O"] and \
            ((tabuleiro["B"][1] == "O" and tabuleiro["C"][1] == "O") or
             (tabuleiro["A"][0] == "O" and tabuleiro["A"][2] == "O")):
        tabuleiro["A"][1] = "X"
    elif tabuleiro["A"][2] not in ["X", "O"] and \
            ((tabuleiro["A"][0] == "O" and tabuleiro["A"][1] == "O") or
             (tabuleiro["B"][1] == "O" and tabuleiro["C"][0] == "O") or
             (tabuleiro["B"][2] == "O" and tabuleiro["C"][2] == "O")):
        tabuleiro["A"][2] = "X"
    elif tabuleiro["B"][0] not in ["X", "O"] and \
            ((tabuleiro["A"][0] == "O" and tabuleiro["C"][0] == "O") or
             (tabuleiro["B"][1] == "O" and tabuleiro["B"][2] == "O")):
        tabuleiro["B"][0] = "X"
    elif tabuleiro["B"][1] not in ["X", "O"] and \
            ((tabuleiro["B"][0] == "O" and tabuleiro["B"][2] == "O") or
             (tabuleiro["A"][1] == "O" and tabuleiro["C"][1] == "O") or
             (tabuleiro["C"][0] == "O" and tabuleiro["A"][2] == "O") or
             (tabuleiro["A"][0] == "O" and tabuleiro["C"][2] == "O")):
        tabuleiro["B"][1] = "X"
    elif tabuleiro["B"][2] not in ["X", "O"] and \
            ((tabuleiro["A"][2] == "O" and tabuleiro["C"][2] == "O") or
             (tabuleiro["B"][0] == "O" and tabuleiro["B"][1] == "O")):
        tabuleiro["B"][2] = "X"
    elif tabuleiro["C"][0] not in ["X", "O"] and \
            ((tabuleiro["A"][0] == "O" and tabuleiro["B"][0] == "O") or
             (tabuleiro["B"][1] == "O" and tabuleiro["A"][2] == "O") or
             (tabuleiro["C"][1] == "O" and tabuleiro["C"][2] == "O")):
        tabuleiro["C"][0] = "X"
    elif tabuleiro["C"][1] not in ["X", "O"] and \
            ((tabuleiro["A"][1] == "O" and tabuleiro["B"][1] == "O") or
             (tabuleiro["C"][0] == "O" and tabuleiro["C"][2] == "O")):
        tabuleiro["C"][1] = "X"
    elif tabuleiro["C"][2] not in ["X", "O"] and \
            ((tabuleiro["A"][0] == "O" and tabuleiro["B"][1] == "O") or
             (tabuleiro["A"][2] == "O" and tabuleiro["B"][2] == "O") or
             (tabuleiro["C"][0] == "O" and tabuleiro["C"][1] == "O")):
        tabuleiro["C"][2] = "X"
    else:
        return False
    return tabuleiro


def montarEstrategia(tabuleiro, rodada, iniciador):
    """
    Monta uma situação estratégica dependendo do inciador da partida (iniciador)
    e também da rodada atual da partida (rodada). Jogada essa tanto defensiva,
    quanto ofensiva.
    :param tabuleiro: tabuleiro na situação atual do jogo.
    :param rodada: rodada atual da partida.
    :param iniciador: iniciador da partida (0 -> bot | 1 -> usuário).
    :return: tabuleiro atualizado com jogada estratégica se for possível
    montar estratégia, senão False.
    """
    # Se o bot iniciou:
    if iniciador == 0:
        if rodada == 1:
            if tabuleiro["B"][1] not in ["X", "O"] and (
                    tabuleiro["A"][0] == "O"
                    or tabuleiro["A"][2] == "O"
                    or tabuleiro["C"][0] == "O"
                    or tabuleiro["C"][2] == "O"
            ):
                tabuleiro["B"][1] = "X"
            else:
                tabuleiro["A"][0] = "X"

        elif rodada == 2:
            if tabuleiro["B"][1] == "O":
                tabuleiro["C"][2] = "X"
            elif ((tabuleiro["B"][0] == "O" or tabuleiro["C"][0] == "O") or
                  (tabuleiro["B"][2] == "O" or tabuleiro["C"][2] == "O")):
                tabuleiro["A"][2] = "X"
            else:
                tabuleiro["C"][0] = "X"
        elif tabuleiro["B"][0] == "O" and tabuleiro["A"][1] == "O":
            tabuleiro["B"][1] = "X"
        elif tabuleiro["C"][0] not in ["X", "O"]:
            tabuleiro["C"][0] = "X"
        elif tabuleiro["A"][2] not in ["X", "O"]:
            tabuleiro["A"][2] = "X"
        else:
            tabuleiro["C"][2] = "X"
    # Se o bot nao iniciou:
    elif iniciador == 1:
        if rodada == 1:
            if tabuleiro["B"][1] == "O":
                tabuleiro["A"][0] = "X"
            else:
                tabuleiro["B"][1] = "X"
        elif rodada == 2:
            if tabuleiro["B"][0] not in ["X", "O"] and \
                    ((tabuleiro["A"][0] == "O" and tabuleiro["C"][2] == "O") or
                     (tabuleiro["C"][0] == "O" and tabuleiro["A"][2])):
                tabuleiro["B"][0] = "X"
            elif tabuleiro["A"][2] not in ["X", "O"] and \
                    ((tabuleiro["B"][1] == "O" and tabuleiro["C"][2] == "O") or
                     (tabuleiro["A"][1] == "O" and tabuleiro["B"][2] == "O") or
                     (tabuleiro["A"][1] == "O" and tabuleiro["C"][1] == "O")):
                tabuleiro["A"][2] = "X"
            elif tabuleiro["A"][0] not in ["X", "O"] and \
                    tabuleiro["A"][1] == "O" and tabuleiro["B"][0] == "O":
                tabuleiro["A"][0] = "X"
            elif tabuleiro["C"][0] not in ["X", "O"] and \
                    tabuleiro["B"][0] == "O" and tabuleiro["C"][1] == "O":
                tabuleiro["C"][0] = "X"
            elif tabuleiro["C"][2] not in ["X", "O"] and \
                    tabuleiro["B"][2] == "O" and tabuleiro["C"][1] == "O":
                tabuleiro["C"][2] = "X"
            elif tabuleiro["B"][2] not in ["X", "O"]:
                tabuleiro["B"][2] = "X"
            else:
                tabuleiro["A"][2] = "X"

        elif tabuleiro["A"][0] not in ["X", "O"] and \
                tabuleiro["A"][1] == "O" and tabuleiro["B"][0] == "O":
            tabuleiro["A"][0] = "X"
        elif tabuleiro["C"][0] not in ["X", "O"] and \
                tabuleiro["B"][0] == "O" and tabuleiro["C"][1] == "O":
            tabuleiro["C"][0] = "X"
        elif tabuleiro["C"][2] not in ["X", "O"] and \
                tabuleiro["B"][2] == "O" and tabuleiro["C"][1] == "O":
            tabuleiro["C"][2] = "X"
        elif tabuleiro["A"][2] not in ["X", "O"] and \
                ((tabuleiro["A"][1] == "O" and tabuleiro["B"][2] == "O") or
                 (tabuleiro["A"][1] == "O" and tabuleiro["B"][0] == "O" and
                  tabuleiro["C"][2] not in ["X", "O"] and
                  tabuleiro["C"][0] not in ["X", "O"])):
            tabuleiro["A"][2] = "X"
        elif tabuleiro["A"][1] not in ["X", "O"] and \
                (tabuleiro["B"][0] == "O" and tabuleiro["B"][2] == "O" and
                 tabuleiro["A"][0] not in ["X", "O"] and
                 tabuleiro["C"][1] not in ["X", "O"] or
                 (tabuleiro["B"][1] == "O" and tabuleiro["C"][2] == "O")):
            tabuleiro["A"][1] = "X"
        else:
            tabuleiro = False

    return tabuleiro


def buscarEspacoVazio(tabuleiro):
    """
    Busca um espaço vazio no tabuleiro, nas casas:
    ( [A][1], [B][0], [B][2], [C][1] ), visto que são melhores que as casas
    das pontas.
    :param tabuleiro: tabuleiro na situação atual do jogo.
    :return: tabuleiro atualizado com a marcação na primeira casa vazia disponível.
    """
    if tabuleiro["A"][1] not in ["X", "O"]:
        tabuleiro["A"][1] = "X"
    elif tabuleiro["B"][0] not in ["X", "O"]:
        tabuleiro["B"][0] = "X"
    elif tabuleiro["B"][2] not in ["X", "O"]:
        tabuleiro["B"][2] = "X"
    else:
        tabuleiro["C"][1] = "X"
    return tabuleiro


def escolherEspacoAleatorio(tabuleiro):
    """
    Escolhe um espaço vazio aleatório no tabuleiro (usado para bot dos níveis 'easy' e 'medium'.
    :param tabuleiro: tabuleiro na situação atual do jogo.
    :return: tabuleiro atualizado com a marcação na primeira casa aleatória e vazia disponível.
    """
    from random import choice
    col = choice(["A", "B", "C"])
    lin = choice(list(range(0, 3)))
    while tabuleiro[col][lin] in ["O", "X"]:
        col = choice(["A", "B", "C"])
        lin = choice(list(range(3)))
    tabuleiro[col][lin] = "X"
    return tabuleiro

def jogadaMaquina(*parametros):
    """
    Processa a jogada que deve ser feita pela máquina de acordo com
    a rodada atual (jogada), iniciador da partida (iniciador) e nível do jogo.
    :param parametros: tabuleiro, jogada, iniciador, nivel
    :return: tabuleiro atualizado com jogada.
    """
    # tabuleiro, jogada, iniciador, nivel
    # idx: 0        1         2       3
    match parametros:
        case _, _, _, 'easy':
            return sequenciaFIMBE(parametros[0], cmd='E')
        case _, _, _, 'medium':
            return sequenciaFIMBE(tabuleiro, cmd='IE')
        case _, 1, 0, _:
            parametros[0]["A"][0] = "X"
            return parametros[0]
        case (_, 1, 1, _) | (_, 2, 0, _):
            return sequenciaFIMBE(parametros[0], parametros[1], parametros[2], 'M')
        case _, 2 | 3, _, _:
            return sequenciaFIMBE(parametros[0], parametros[1], parametros[2])
        case _, 4, _, _:
            return sequenciaFIMBE(parametros[0], cmd='FIB')
        case _, _, _, _:
            return sequenciaFIMBE(parametros[0], cmd='B')


def sequenciaFIMBE(tabuleiro, jogada=None, iniciador=None, cmd='FIMBE'):
    """
    Tenta Finalizar, Impedir jogada, Montar estratégia, Buscar um espaço vazio
    estrategico para jogar ou entao Encontrar um espaço vazio,
    seguindo toda essa ordem.
    :param tabuleiro: tabuleiro
    :param jogada: jogada maquina
    :param iniciador: iniciador da partida ( 0 -> bot 'X' | 1 -> usuario 'O" ).
    :return: tabuleiro atualizado com jogada do bot.
    """
    for comando in cmd:
        if comando == 'F':
            jogada = tentarFinalizarPartida(tabuleiro)
        elif comando == 'I':
            jogada = impedirJogadaAdversaria(tabuleiro)
        elif comando == 'M':
            jogada = montarEstrategia(tabuleiro, jogada, iniciador)
        elif comando == 'B':
            jogada = buscarEspacoVazio(tabuleiro)
        elif comando == 'E':
            return escolherEspacoAleatorio(tabuleiro)
        if jogada is False:
            continue
        else:
            return jogada



def jogarNovamente():
    """
    Pergunta ao usuário seja deseja continar jogando uma nova partida.
    :return: True (se usuario desejar jogar novamente |
    False (se nao deseja jogar novamente)
    """
    play_again = input('Deseja jogar mais uma partida?\n'
                       '[S | N]: ').upper().strip()
    while play_again not in ['S', 'N']:
        print('Por favor digite uma opção válida.')
        play_again = input('Deseja jogar mais uma partida?\n'
                           '[S | N]: ').upper().strip()

    return play_again == 'S'


def escolherNivel():
    """
    Usuário determina nível do bot que deseja enfrentar.
    easy -> joga em lugar aleatório que seja vazio.
    medium -> joga igual o nivel 'easy', porém prioriza impedir vitória do usuário quando possível.
    hard -> monta estratégia de jogada desde a primeira rodada, pririozando em
    ordem: vencer, impedir vitoria adversária, montar um contra-golpe, enfim empate.
    :return: nivel (string do nível que usuário selecionou ['easy', 'medium', 'hard']).
    """
    print('-' * 36)
    print('Escolha o nível do jogo.')
    niveis = {1: 'easy', 2: 'medium', 3: 'hard'}
    for cod, level in niveis.items():
        print(f'{cod} - {level.upper()}', end=' | ')
    try:
        cod_nivel = int(input('\nOPCAO: '))
        print(f'Nivel {niveis[cod_nivel].title()} selecionado.')
    except:
        print('Por favor, digite um código do item válido.')
        escolherNivel()
    else:
        return niveis[cod_nivel]


def mostrarPlacar(placar):
    """
    Mostra o placar atual do jogo do Bot vs Usuário, sem retornar nada.
    :param placar: placar atual da rodada.
    """
    print('*' * 21)
    print('Placar: ', end='')
    for k, v in placar.items():
        print(f'{k}: {v}', end=' | ')
    print()
    print('*' * 21)


# String para acompanhar qual o jogador da vez
bot = "X"
jogador = "O"
# Flag para continuar o jogo, ate usuario decidir sair
continuar = True
# Placar do jogo:
placar = {'O': 0, 'X': 0}
# Definindo quem inicia: 0 -> Bot | 1-> Usuário
iniciar = 0
# Determina o nível das partidas.
nivel = escolherNivel()

print(
    "Instruções:\nDigite as coordenadas da sua jogada no formato letra e numero (Ex: 'A 1', 'B 2', 'C 3', etc)\n")
# Loop enquanto jogo não acabar que cicla em jogada da maquina e jogada do usuario com as devidas validações de entrada e fim de jogo
while continuar:
    # Dicionário para registro do jogo
    tabuleiro = {
        " ": ["1", "2", "3"],
        "A": ["", "", ""],
        "B": ["", "", ""],
        "C": ["", "", ""]
    }
    # Flag que é acionada para definir que o jogo acabou (vitoria, derrota, empate).
    acabou = False
    rodada = 0
    mostrarPlacar(placar)
    if iniciar == 0:
        print('Máquina começa (X)')
        while not acabou:
            rodada += 1
            print(f'Rodada: {rodada}')
            tabuleiro = jogadaMaquina(tabuleiro, rodada, iniciar, nivel)
            acabou, placar = confereFim(tabuleiro, bot, placar)
            imprimiTabuleiro(tabuleiro)
            if not acabou:
                tabuleiro = jogada(tabuleiro, jogador)
                acabou, placar = confereFim(tabuleiro, jogador, placar)
    else:
        print('Você começa (O)')
        while not acabou:
            rodada += 1
            print(f'Rodada: {rodada}')
            imprimiTabuleiro(tabuleiro)
            tabuleiro = jogada(tabuleiro, jogador)
            acabou, placar = confereFim(tabuleiro, jogador, placar)
            if not acabou:
                tabuleiro = jogadaMaquina(tabuleiro, rodada, iniciar, nivel)
                acabou, placar = confereFim(tabuleiro, bot, placar)

    # Trocando a ordem do jogador.
    iniciar = (iniciar + 1) % 2
    continuar = jogarNovamente()
