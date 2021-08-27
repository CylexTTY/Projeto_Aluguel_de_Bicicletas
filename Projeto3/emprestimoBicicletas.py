from datetime import datetime, timedelta
from math import ceil
import csv


class Cliente(object):

    def __init__(self, nome):
        self.nome = nome.strip().title()

    def mostrarBicicletasDisponiveis(self) -> int:
        """
        Mostra e retorna o estoque atual do objeto Loja.
        :return: quantidade disponivel de bikes: int.
        """
        estoque_atual = Loja().mostrarEstoque()
        print(f'Bicicletas disponíveis: {estoque_atual}')
        return estoque_atual

    def alugarBilicletas(self, qnt_bikes: int, plano: str,
                         data_ini: str) -> bool:
        """
        Permite alugar N bicicletas de acordo com o estoque disponível.
        :param qnt_bikes: quantidade deseja de bicicletas para alugar.
        :param plano: plano desejado ('hora', 'dia', 'semana').
        :param data_ini: data atual do início do aluguel 'dd/mm/yyyy H'.
        :return: True (se pedido aceito)/ False (se pedido negado).
        """
        return Loja().receberPedido(self.nome, qnt_bikes, plano, data_ini)

    def finalizarConta(self, data_fim: str) -> bool:
        """
        Finaliza o aluguel da bicicleta, sendo necessario informar a data
        que esta sendo devolvida no padrao: 'dd/mm/yyyy H'.
        :param data_fim: data da entrega da(s) bicicleta(s) 'dd/mm/yyyy H''.
        :return: True (se pedido finalizado com sucesso)/
        False (se pedido negado).
        """
        return Loja().finalizarConta(self.nome, data_fim)


class Loja(object):

    def __init__(self, estoque_definido=10):
        self.planos = {'hora': 5, 'dia': 25, 'semana': 100}
        try:
            arquivo = open('clientes.csv', 'r', encoding='UTF-8')
        except:
            self.criarArquivoCSV()
        else:
            arquivo.close()
        finally:
            self.estoqueBikes = estoque_definido - self.calcularBicicletasAlugadas()

    def mostrarEstoque(self) -> int:
        """
        Retorna o estoque atual de bicicletas disponíveis.
        :return: quantidade de bicicletas disponíveis
        """
        return self.estoqueBikes

    def receberPedido(self, cliente: str, qnt_bikes: int, plano: str,
                      data_ini: str) -> bool:
        """
        Recebe parâmetros para fazer pedido. Vverifica em outro método se são
        válidos. Se sim, grava o pedido no arquivo csv.
        :param cliente: nome do cliente
        :param qnt_bikes: quantidade de bicicletas solicitada
        :param plano: plano
        :param data_ini: data e hora inicial no padrao: 'dd/mm/yyyy H'
        :return: True (se parametros validos)/ False (se parametros invalidos)
        """
        parametros = self.validarParametros(cliente, qnt_bikes, plano,
                                            data_ini)
        if parametros is not False:
            itens_pedidos = list(parametros) + [0, 0]
            with open('clientes.csv', 'a', encoding='utf-8') as dados:
                escrita = csv.writer(dados)
                escrita.writerows([itens_pedidos])
            print('Pedido realizado com sucesso.')
            return True
        else:
            print('Não foi possível realizar o pedido.')
            return False

    def finalizarConta(self, cliente: str, data_fim: str) -> tuple[
                                                                 bool, float] | bool:
        """
        Finaliza conta do cliente se parâmetros válidos.
        :param cliente: nome do cliente.
        :param data_fim: data e hora da entrega das bikes no padrao 'dd/mm/yyyy H'.
        :return: True (se finalizado com sucesso)/ False (se dados invalidos).
        """
        nome_valido = self.checarNomeNaLista(cliente)
        if nome_valido:
            data_fim = self.validarData(data_fim)
            qnt_bikes, data_ini, plano = self.colhetarDados(cliente)
            data_delta = self.calcularDeltaDatas(data_ini, data_fim)
            if data_delta is not False:
                delta_em_horas = self.tratarDeltaDataHora(data_delta)
                # Gerar quanto deve pagar.
                valor = round(self.calcularValorConta(plano, qnt_bikes,
                                                      delta_em_horas), 2)
                print(f'Valor da conta: R${valor:.2f}')
                self.gravarFechamentoPedido(cliente, data_fim, valor)
                print('Pedido pago e finalizado. Volte sempre.')
                return True, valor
        else:
            print('Cliente não encontrado.')
        return False

    def calcularValorConta(self, plano: str, qnt_bikes: int,
                           qnt_horas: int) -> float:
        """
        Calcula valor final de acordo com os parametros informados.
        :param plano: plano.
        :param qnt_bikes: quantidade de bikes alugadas.
        :param qnt_horas: delta de data incial e data final em horas.
        :return: float de valor final.
        """
        # Uso não muito inteligente do pattern matching na versão 3.10
        match plano:
            case 'hora':
                valor = self.planos[plano] * qnt_bikes * qnt_horas
            case 'dia':
                dias = ceil(qnt_horas / 24)
                valor = self.planos[plano] * qnt_bikes * dias
            case 'semana':
                semanas = ceil(qnt_horas / 168)
                valor = self.planos[plano] * qnt_bikes * semanas
        # Dar desconto de 30% se mais de 2 bikes.
        return valor * 0.7 if qnt_bikes > 2 else valor

    def gravarFechamentoPedido(self, nome_cliente: str, data_fim: datetime,
                               valor: float) -> None:
        """
        Grava no arquivo csv os dados do fechamento do pedido.
        :param nome_cliente: nome cliente.
        :param data_fim: data de entrega das bicicletas.
        :param valor: valor total da conta.
        """
        copia = []
        with open('clientes.csv', 'r', encoding='UTF-8') as arquivo_leitura:
            leitura = csv.reader(arquivo_leitura)
            for row in leitura:
                if row[0] == nome_cliente and row[5] == '0':
                    linha = list(row)
                    linha[4] = data_fim
                    linha[5] = valor
                    copia.append(linha)
                else:
                    copia.append(row)
        with open('clientes.csv', 'w', encoding='UTF-8') as arquivo_escrita:
            escrita = csv.writer(arquivo_escrita)
            escrita.writerows(copia)
        print('Dados salvos com sucesso!')

    def colhetarDados(self, nome_cliente: str) -> tuple[int, str, str]:
        """
        Colhe os dados necessários do cliente.
        :param nome_cliente: nome do cliente
        :return: quantidade de bikes alugada, data incial, plano
        """
        with open('clientes.csv', 'r', encoding='UTF-8') as arquivo:
            leitura = csv.DictReader(arquivo)
            for row in leitura:
                if row['Cliente'] == nome_cliente and row['Total'] == '0':
                    qnt_bikes = row['Quantidade_Alugada']
                    data_ini = row['Data_Inicial']
                    plano = row['Plano']
                    break
        return int(qnt_bikes), data_ini, plano

    def tratarDeltaDataHora(self, data: timedelta) -> int:
        """
        Recebe um time delta e devolve a quantidade em horas.
        :param data: timedelta
        :return: horas
        """
        return int(data.total_seconds() / 3600)

    def checarNomeNaLista(self, nome_cliente: str) -> bool:
        """
        Checa se nome do cliente esta no arquivo csv.
        :param nome_cliente: nome do cliente
        :return: True (se nome na lista)/ False (se nome nao esta na lista)
        """
        with open('clientes.csv', 'r', encoding='utf-8') as arquivo:
            leitura = csv.DictReader(arquivo)
            for row in leitura:
                # Verifica se o cliente esta na lista, se for o mesmo nome
                # porem ja finalizou o pedido, continua verificando.
                if row['Cliente'] == nome_cliente and \
                        row['Total'] == '0':
                    return True
        return False

    def validarData(self, data: str) -> bool | datetime:
        """
        Verifica se data/hora é válida com o padrao: dd/mm/yyyy H.
        :param data: data
        :return: datetime se válido / False se inválido
        """
        try:
            data = datetime.strptime(data, '%d/%m/%Y %H')
        except Exception as erro:
            if 'day is out of range' in str(erro):
                print('Mês/Dia inexistente. Verifique data corretamente.')
            elif 'unconverted data remains' in str(erro):
                print('Hora inexistente. Verifique hora digitada novamente')
            elif 'does not match format' in str(erro):
                print('Padrão Data/Hora inválidos.\n'
                      'Por favor coloque exatamente no padrao: "dd/mm/yyyy H".')
            else:
                print(erro)
            return False
        else:
            return data

    def calcularDeltaDatas(self, data_ini: str,
                           data_fim: datetime) -> bool | timedelta:
        """
        Calcula a diferenca de tempo entre data final e data incial.
        :param data_ini: data incial
        :param data_fim: data final
        :return: timedelta se data final > data incial/ False se fim <= inicio
        """
        try:
            with open('clientes.csv', 'r', encoding='utf-8') as dados:
                escrita = csv.DictReader(dados)
                for row in escrita:
                    if row['Data_Inicial'] == data_ini:
                        data_ini = datetime.strptime(data_ini[:13],
                                                     '%Y-%m-%d %H')
                        break
            if data_ini > data_fim:
                raise Exception(
                    'ERRO: Data final menor que data inicial do aluguel.')
            if data_ini == data_fim:
                raise Exception(
                    'ERRO: Data final igual a data inicial do aluguel.')
        except Exception as erro:
            print(erro)
            return False
        else:
            return data_fim - data_ini

    def validarParametros(self, nome_cliente: str, qnt: int, plano: str,
                          data: str) -> bool | tuple[str, int, str, datetime]:
        """
        Valida parâmetros iniciais para se alugar bicicletas.
        :param nome_cliente: nome do cliente
        :param qnt: quantidade de bicicletas pedidas
        :param plano: plano ('hora', 'dia', 'semana')
        :param data: data incial
        :return: todos os parâmetros se validos/ False se inválidos
        """
        try:
            # Valida nome
            if type(nome_cliente) != str or len(nome_cliente) < 2:
                raise Exception('Nome inválido.')
            with open('clientes.csv', 'r', encoding='utf-8') as arquivo:
                leitura = csv.DictReader(arquivo)
                for row in leitura:
                    # Se o cliente ja estiver na lista e ainda nao finalizou o pedido.
                    if nome_cliente == row['Cliente'] and row['Total'] == '0':
                        raise Exception('Nome já cadastrado.'
                                        ' For favor finzalize o aluguel em'
                                        ' aberto antes de tentar alugar novas bicicletas.')

            # Valida quantidade de bikes solicitadas.
            if type(qnt) != int:
                raise Exception(
                    'Verifique se a quantidade solicitada se encontra como um '
                    'número inteiro.')
            if qnt < 1:
                raise Exception('Quantidade solicitada não pode ser menor do que um.')
            if self.estoqueBikes < qnt:
                raise Exception(
                    'Ops... parece que não temos essa quantidade disponível em estoque.\n'
                    f'Temos {self.estoqueBikes} bicicleta'
                    f'{"s disponíveis." if self.estoqueBikes > 1 else " disponível."}')

            # Valida plano.
            if plano.strip().lower() not in self.planos:
                raise Exception(f'Plano inexistente\n'
                                f'Planos: {tuple(self.planos.keys())}')

            # Valida data.
            data_ini = self.validarData(data)
            if data_ini is False:
                raise Exception('Erro de data/hora.')
        except Exception as erro:
            print(erro)
            return False
        else:
            return nome_cliente.title(), qnt, plano.strip().lower(), data_ini

    def calcularBicicletasAlugadas(self):
        with open('clientes.csv', 'r', encoding='utf-8') as arquivo:
            leitura = csv.reader(arquivo)
            bikes_alugadas = sum(int(row[1]) for row in leitura if row[5] == '0')
        return bikes_alugadas

    def criarArquivoCSV(self):
        with open('clientes.csv', 'w', encoding='utf-8') as gravar:
            header = ['Cliente', 'Quantidade_Alugada', 'Plano',
                      'Data_Inicial', 'Data_Final', 'Total']
            escrita = csv.writer(gravar)
            escrita.writerow(header)
