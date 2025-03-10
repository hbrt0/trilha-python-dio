#v2.1 +limite diario (para conta corrente), -limite saques

# inserir logica de limite diario na funcao realizar_transacao da classe cliente (raiz das op), funcao de contar transaceos no Historico
#FEITO
import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

def log_funcoes(func):
    def wrapper(*args,**kwargs):
        if 'cpf' in kwargs:
            cpf = kwargs['cpf']
        elif 'cliente' in kwargs:
            cpf = kwargs['cliente'].cpf
        elif 'clientes' in kwargs:
            cpf = kwargs['clientes'][0].cpf
        resultado = func(*args,**kwargs)
        print(f"\n{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} | {func.__name__.upper()} | CPF: {cpf}")
        return resultado
    return wrapper

#ITERADOR para contas
class ContasIterador:
    def __init__(self,contas: list):
        self.contas = contas
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self.index]
            return f"""
                Agência:\t{conta.agencia}
                Número:\t{conta.numero}
                Titular:\t{conta.cliente.nome}
                Saldo:\t{conta.saldo}
            """
        except IndexError:
            raise StopIteration
        finally:
            self.index += 1

#TRANSACAO
class Transacao(ABC):

    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self,conta):
        pass

#SAQUE
class Saque(Transacao):
    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self,conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)
            return True
        return False

#DEPOSITO
class Deposito(Transacao):
    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self,conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)
            return True
        return False


#CLIENTE
class Cliente:
    def __init__(self):
        self.contas = []
        self.indice_conta = 0

    def realizar_transacao(self,conta,transacao):

        conta.reset_limite_transacao()              #diary_limit reset verify
        num_transacao = conta.historico.qnt_transacao()       #transation quantify

        # Check if the number of transactions has reached the daily limit
        if num_transacao >= conta.limite_transacao:
            print('\n! Limite de transacoes atingido !')
            return

        if transacao.registrar(conta):
            conta.limite_transacao -= 1               #decrease the limite_diario


    def adicionar_conta(self,conta):
        self.contas.append(conta)

#PESSOA FISICA
class PessoaFisica(Cliente):
    def __init__(self,nome,data_nascimento,cpf):
        super().__init__()
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    @classmethod
    @log_funcoes
    def criar_cliente_pf(cls, nome, data_nascimento, cpf):
        return cls(nome, data_nascimento, cpf)
    
#CONTA
class Conta():
    def __init__(self,numero,cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    @log_funcoes
    def criar_conta(cls,cliente,numero):
        return cls(numero,cliente)

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self,valor):
        self._saldo = valor

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico


    def sacar(self,valor):
        if self.saldo < valor:
            print('\n! Saldo insuficiente !')
        elif valor > 0:
            self.saldo -= valor
            print('\n--- Saque realizado ---')
            print('\n--- Novo saldo ---')
            print(f'\nR$ {self.saldo}')
            return True
        else:
            print('\n! Valor inválido !')
        return False


    def depositar(self,valor):
        if valor > 0:
            self.saldo += valor
            print('\n--- Depósito realizado ---')
            print('\n--- Novo saldo ---')
            print(f'\nR$ {self.saldo}')
        else:
            print('\n! Valor inválido !')
            return False
        return True

#Classe Conta Corrente
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=1000, limite_transacao=5):
        super().__init__(numero,cliente)
        self._limite = limite
        self._limite_transacao = limite_transacao

    @property
    def limite_transacao(self):
        return self._limite_transacao

    @limite_transacao.setter
    def limite_transacao(self,valor):
        self._limite_transacao = valor

    @property
    def limite(self):
        return self._limite

    @limite.setter
    def limite(self,valor):
        self._limite = valor


    def reset_limite_transacao(self):
        if self.historico.transacoes:
            last_transaction = self.historico.transacoes[-1]
            date_last = datetime.strptime(last_transaction['data'], "%d-%m-%Y %H:%M:%S").date()
            if date_last != datetime.today().date():
                self.limite_transacao = 5
                return True
            return False

    def sacar(self,valor):
        if valor > self.limite:
            print('\n! Limite para saque excedido !')
        else:
            return super().sacar(valor)
        return False

    def depositar(self,valor):
        return super().depositar(valor)

    def __str__(self):
        return f'''
        Agência:\t{self.agencia}
        C/C:\t{self.numero}
        Titular:\t{self.cliente.nome}
        '''

#HISTORICO
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self,transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S") #formato
            }
        )

    def qnt_transacao(self): #retorna quantidade de transacoes feitas pela conta
        return len(self.transacoes)

    def gerar_relatorio(self,tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao['tipo'].lower() == tipo_transacao.lower():
                yield transacao


################################################################################

def menu():
    menu = '''\n
    ================ MENU ================
    [d]  Depositar
    [s]  Sacar
    [e]  Extrato
    ------------------------
    [nc] Nova conta
    [lc] Listar contas
    [nu] Novo usuário
    [q]  Sair
    => '''
    return input(menu)

def filtrar_cliente(cpf,clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def verificar_cpf(clientes: list): #lista ja filtrada
    if clientes:
        print('\n! Já existe cliente com esse CPF !')
        print(f'\n')
        return True
    return False

def novo_cliente(clientes: list):
    cpf = input('\nInforme o CPF: ')
    cliente = filtrar_cliente(cpf,clientes)

    if verificar_cpf(cliente):
        return

    nome = input('Informe o nome: ')
    data_nascimento = input('Informe a data de nascimento: ')

    cliente = PessoaFisica.criar_cliente_pf(nome=nome,data_nascimento=data_nascimento,cpf=cpf)
    clientes.append(cliente)

    print('\n| Cliente criado com sucesso |')

def nova_conta(numero,clientes: list,contas: list):
    cpf = input('\nInforme o CPF do cliente: ')
    cliente = filtrar_cliente(cpf,clientes)

    if not cliente:
        print('\n! Cliente não encontrado, fluxo de criação de conta encerrado !')
        return
    
    conta = ContaCorrente.criar_conta(cliente=cliente,numero=numero)
    contas.append(conta)
    cliente.contas.append(conta)

    print(f'\n| Conta criada com sucesso |\n{conta}')


def get_conta(cliente):
    if not cliente.contas:
        print('\n! Cliente não possui contas !')
        return
    return cliente.contas[0]

def listar_contas(contas):
    for conta in ContasIterador(contas):
        print('=' * 100)
        print(textwrap.dedent(str(conta)))


@log_funcoes
def depositar(clientes):
    cpf = input('\nInforme o CPF do cliente: ')
    cliente = filtrar_cliente(cpf,clientes)

    if not cliente:
        print('\n! Cliente não encontrado, fluxo de depósito encerrado !')
        return

    conta = get_conta(cliente)
    if conta is None:
        return

    valor = float(input('Informe o valor do depósito: '))
    transacao = Deposito(valor)

    cliente.realizar_transacao(conta,transacao)

@log_funcoes
def sacar(clientes):
    cpf = input('\nInforme o CPF do cliente: ')
    cliente = filtrar_cliente(cpf,clientes)

    if not cliente:
        print('\n! Cliente não encontrado, fluxo de saque encerrado !')
        return

    conta = get_conta(cliente)
    if conta is None:
        return

    valor = float(input('Informe o valor do saque: '))
    transacao = Saque(valor)

    cliente.realizar_transacao(conta,transacao)

@log_funcoes
def exibir_extrato(clientes):
    cpf = input('\nInforme o CPF do cliente: ')
    cliente = filtrar_cliente(cpf,clientes)

    conta = get_conta(cliente)
    if conta is None:
        return

    if not cliente:
        print('\n! Cliente não encontrado, fluxo de extrato encerrado !')
        return

    print('\n================ EXTRATO ================')
    extrato = ""
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio():
        tem_transacao = True
        extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}\nData:\n\t{transacao['data']}"


    if not tem_transacao:
        extrato = 'Não foram realizadas movimentações.'

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print('=========================================')


def main():
    #fixme - dict para melhor eficiencia
    clientes = []
    contas = []

    while True:
        opcao = menu()

        match opcao:
            case 'd':
                depositar(clientes)
            case 's':
                sacar(clientes)
            case 'e':
                exibir_extrato(clientes)
            case 'nc':
                numero_conta = len(contas) + 1
                nova_conta(numero_conta,clientes,contas)
            case 'lc':
                listar_contas(contas)
            case 'nu':
                novo_cliente(clientes)
            case 'q':
                break

main()
