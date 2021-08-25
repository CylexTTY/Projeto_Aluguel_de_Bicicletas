from emprestimoBicicletas import Cliente, Loja
from unittest import TestCase, main


def mostrar(txt, cor='red'):
    cores = {'red': '\033[31m', 'green': '\033[32m', 'limpa': '\033[m'}
    print(f"\n{cores[cor]}{txt}{cores['limpa']}\n")


class Testes(TestCase):

    def setUp(self):
        self.cliLucas = Cliente('lucas')
        self.cliAna = Cliente('Ana')
        self.cliJose = Cliente('   jose')
        self.cliPedro = Cliente('pedro')
        self.cliJoao = Cliente('  joao   ')
        self.cliMaria = Cliente('maria')
        self.cliJosefa = Cliente('josefa')
        self.cliBrian = Cliente('Brian')
        self.cliNulo = Cliente(' ')

    def test01MostraBikes(self):
        mostrar('Mostra que cliente visualiza corretamente estoque de bikes.',
                'green')
        self.assertEqual(self.cliLucas.mostrarBicicletasDisponiveis(),
                         Loja().mostrarEstoque())

    def test02AlugarBicicletaSucesso(self):
        # Ambiente onde tudo está de acordo.
        mostrar('Ambiente onde todos os pedidos são realizados com sucesso.',
                'green')
        self.assertTrue(
            self.cliLucas.alugarBilicletas(3, 'hora', '11/02/2021 12'))
        self.assertTrue(
            self.cliAna.alugarBilicletas(1, 'dia', '21/02/2021 12'))
        self.assertTrue(
            self.cliJose.alugarBilicletas(1, 'semana', '05/03/2021 09'))
        self.assertTrue(
            self.cliPedro.alugarBilicletas(1, 'dia', '15/06/2021 20'))
        self.assertTrue(
            self.cliMaria.alugarBilicletas(1, 'semana', '01/09/2021 15'))

    def test03AlugarBicicletaValidacaoNome(self):
        # Nao permite nome de cliente vazio.
        mostrar('Nao permite nome de cliente vazio ou apenas espacos.')
        self.assertFalse(
            self.cliNulo.alugarBilicletas(2, 'hora', '14/04/2021 12'))
        # Nao permite outro pedido do mesmo cliente se ainda nao finalizou o aluguel.
        mostrar(
            'Nao permite um aluguel da mesma pessoa se ainda nao finalizou a'
            ' conta.')
        self.assertFalse(
            self.cliAna.alugarBilicletas(2, 'hora', '20/06/2021 12'))

    def test04AlugarBicicletaErroData(self):
        # Nao permite data fora do padrao de data 'dd/mm/yyyy H'.
        mostrar(
            'Nao permite um aluguel com o padrao de data estabelecido inválido.')
        self.assertFalse(
            self.cliJosefa.alugarBilicletas(3, 'hora', '20210325 12'))
        # Nao permite data inexistente na entrada.
        mostrar('Nao permite alugar bicicletas com data inexistente.')
        self.assertFalse(
            self.cliJosefa.alugarBilicletas(3, 'hora', '31/04/2021 12'))
        # Nao permite hora inexistente na entrada.
        mostrar('Nao permite alugar bicicletas com hora inexistente.')
        self.assertFalse(
            self.cliJosefa.alugarBilicletas(3, 'hora', '30/04/2021 25'))

    def test05AlugarBicicletaErroPlano(self):
        # Nao permite plano invalido.
        mostrar('Nao permite alugar bicicletas com um plano inexistente.')
        self.assertFalse(
            self.cliJosefa.alugarBilicletas(2, 'anual', '14/04/2021 12'))

    def test06AlugarBicicletasErroEstoque(self):
        # Nao permite quantidade superior ao estoque atual de bicicletas ou <= 0.
        # OBS: Estoque disponível atualmente aqui = 3
        mostrar('Nao permite alugar quantidade superior ao estoque disponível')
        self.assertFalse(
            self.cliJosefa.alugarBilicletas(4, 'hora', '14/04/2021 12'))
        mostrar('Nao permite alugar quantidade negativa.')
        self.assertFalse(
            self.cliJosefa.alugarBilicletas(-2, 'hora', '15/05/2021 15'))
        mostrar('Nao permite alugar 0 bicicletas.')
        self.assertFalse(
            self.cliJosefa.alugarBilicletas(0, 'hora', '15/05/2021 15'))

    def test07FinalizarPedidoSucesso(self):
        # Ambiente onde tudo está de acordo.
        mostrar('Finaliza pedido com dados enviado corretos normalmente.',
                'green')
        self.assertTrue(self.cliJose.finalizarConta('19/03/2021 19')[
                            0])  # 2 semanas e 10 hora -> 3 semanas

    def test08FinalizarPedidoValorCorreto(self):
        # Ambiente onde tudo está de acordo.
        mostrar(
            'Finzaliza pedidos corretamente com contas calculadas por hora',
            'green')
        self.assertEqual(self.cliLucas.finalizarConta('11/02/2021 15')[1],
                         31.5)  # 3 horas 3 bikes -> 45 * 0.7 -> R$31.5
        mostrar(
            'Finzaliza pedidos corretamente com contas calculadas por dia',
            'green')
        self.assertEqual(
            self.cliAna.finalizarConta('28/02/2021 13')[1],
            200)  # 7 dias + 1 hora == 8 dias -> R$175
        mostrar(
            'Finzaliza pedidos corretamente com contas calculadas por semana',
            'green')
        self.assertTrue(self.cliMaria.finalizarConta('08/09/2021 15')[1],
                        100)  # 1 semana -> R$100

    def test09FinzalizarPedidoValorCorretoPLanoFamilia(self):
        mostrar(
            'Finzaliza pedidos corretamente com plano familia (3 bikes ou mais).',
            'green')
        self.cliJoao.alugarBilicletas(3, 'dia', '11/09/2021 12')
        self.assertEqual(self.cliJoao.finalizarConta('14/09/2021 12')[1],
                         157.5)  # 3 dias 3 bikes -> 3 * 75 * 0.7 -> R$157.5

    def test10QuantidadeEstoqueDevolvidaAposFinalizar(self):
        # Faz um pedido normalmente
        mostrar('Faz pedido normalmente e mostra estoque', 'green')
        mostrar(
            f'Estoque atual: {self.cliJosefa.mostrarBicicletasDisponiveis()}',
            'green')
        mostrar('Fazendo pedido de 3 bikes...', 'green')
        self.assertTrue(
            self.cliJosefa.alugarBilicletas(3, 'hora', '11/02/2021 12'))
        mostrar(
            f'Estoque atualizado após alugar 3 bikes: '
            f'{self.cliJosefa.mostrarBicicletasDisponiveis()}', 'green')
        self.assertTrue(self.cliJosefa.finalizarConta('11/02/2021 19'))
        mostrar(
            f'Estoque atualizado após finalizar aluguel de 3 bikes: '
            f'{self.cliJosefa.mostrarBicicletasDisponiveis()}', 'green')
        # Depois de finalizado, retorna quatidade alugada ao estoque.
        self.assertEqual(self.cliJosefa.mostrarBicicletasDisponiveis(),
                         Loja().mostrarEstoque())

    def test11FinzalizarSemNomeNaListaErro(self):
        # Se cliente nao alugou bike, nao permite que ele finalize a conta.
        mostrar('Nao permite finalizar conta de cliente que nao fez aluguel.')
        self.assertFalse(self.cliBrian.finalizarConta('02/12/2021'))

    def test12FinzalizarDataHoraErro(self):
        # Se tentar finalizar no mesmo dia e horario que alugou, não permite.
        mostrar(
            'Nao permite finzalizar pedido no mesmo dia e horario do aluguel')
        self.assertFalse(self.cliPedro.finalizarConta('15/06/2021 20'))
        # Se tentar finalizar antes do dia/horario que alugou, não permite.
        mostrar(
            'Nao permite finzalizar pedido com data e hora menor do que dia do aluguel')
        self.assertFalse(self.cliPedro.finalizarConta('14/06/2021 20'))
        # Nao permite data fora do padrao de data 'dd/mm/yyyy H'.
        mostrar(
            'Nao permite finzalizar com o padrao de data estabelecido inválido.')
        self.assertFalse(
            self.cliJosefa.alugarBilicletas(3, 'hora', '16062021 12h'))
        # Nao permite data inexistente na entrada.
        mostrar(
            'Nao permite finzalizar aluguel de bicicletas com data inexistente.')
        self.assertFalse(
            self.cliJosefa.alugarBilicletas(3, 'hora', '31/06/2021 12'))
        # Nao permite hora inexistente na entrada.
        mostrar(
            'Nao permite finzalizar aluguel de bicicletas com hora inexistente.')
        self.assertFalse(
            self.cliJosefa.alugarBilicletas(3, 'hora', '30/06/2021 -1'))

    def test13FinalizarPedidoFinzalizado(self):
        # Se pede para finalizar um cliente que ja fechou a conta, não sobrescreve.
        mostrar(
            'Nao permite finalizar pedido já finzalizado, e nao sobrescreve'
            ' data final.')
        # Primeira finalizacao foi as 15h, R$31.50
        self.assertFalse(self.cliLucas.finalizarConta('11/02/2021 22'))

    def test14AlugarBikesComNomeFinalizado(self):
        # Apos finalizar o pedido, ai sim aceita novamente o mesmo cliente e
        # abre uma nova conta.
        mostrar('Permite mesmo nome de cliente alugar novamente se o mesmo já'
                ' finalizou sua conta em aberto.', 'green')
        self.assertTrue(
            self.cliLucas.alugarBilicletas(2, 'hora', '21/06/2021 12'))
        mostrar(
            'Permite que o cliente tambem finzalize o pedido sem conflitos com'
            ' nome ja exitente.', 'green')
        self.assertTrue(self.cliLucas.finalizarConta('21/06/2021 20'))


if __name__ == '__main__':
    main()
