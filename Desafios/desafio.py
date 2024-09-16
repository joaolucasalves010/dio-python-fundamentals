import textwrap
from datetime import datetime
from abc import ABC, abstractclassmethod, abstractproperty

class ContasIterador:
  def __init__(self, contas):
    self.contas = contas
    self._index = 0

  def __iter__(self):
    return self

  def __next__(self):
    try:
      conta = self.contas[self._index]
      return f"""
      Agência: {conta.agencia}
      Número:  {conta.numero}
      Dono:    {conta.cliente.nome}
      Saldo:   {conta.saldo:.2f}
    """
    except IndexError:
      raise StopIteration
    finally:
      self._index += 1

class Historico:
  def __init__(self):
    self._transacoes = []

  @property
  def transacoes(self):
    return self._transacoes

  def adicionar_transacao(self, transacao):
    self._transacoes.append(
      {
        "tipo":  transacao.__class__.__name__,
        "valor": transacao.valor,
        "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
      }
    )  

  def gerar_relatorio(self, tipo_transacao=None):
    for transacao in self._transacoes:
      if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
        yield transacao 

def listar_contas(contas):
  for conta in ContasIterador(contas):
    print("=" * 100)
    print(textwrap.dedent(str(conta)))

def exibir_extrato(clientes):
  cpf = input("Informe o cpf do cliente: ")
  cliente = filtrar_clientes(clientes, cpf)

  if not cliente:
    print("Não existe cliente cadastrado com este cpf")
    return
  
  conta = recuperar_conta_cliente(cliente)

  if not conta:
    return

  print("\n================ EXTRATO ================")
  extrato=""
  tem_transacao = False
  
  for transacao in conta.historico.gerar_relatorio(tipo_transacao="saque"):
    tem_transacao = True
    extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

  if not tem_transacao:
    extrato = "Não foram realizadas movimentações"

  print(extrato)
  print(f"Saldo: {conta.saldo:.2f}")
  print("==========================================")

class Conta:
  def __init__(self, cliente, numero):
    self.cliente = cliente 
    self.numero = numero
    self.saldo = 0
    self.agencia = "0001"
    self.historico = Historico()

  @classmethod
  def nova_conta(cls, numero, cliente):
     return cls(numero, cliente)

  def depositar(self, valor):
    if valor > 0:
      self.saldo += valor
      print("Deposito realizado com sucesso")
    else:
      print("A operação falhou! O valor informado é inválido")
      return False
    
    return True

  def sacar(self, valor):
   saldo = self.saldo
   saldo_insuficiente = valor > saldo

   if saldo_insuficiente:
    print("Operação negada você não tem saldo suficiente!")
   elif valor > 0:
    self.saldo -= valor
    print("Saque realizado com sucesso")
    return True
   else:
    print("Operação inválida verifique o valor e tente novamente!")

class ContaCorrente(Conta):
  def __init__(self, numero, cliente, limite=500, limite_saques=3):
    super().__init__(cliente, numero)
    self.limite = limite
    self.limite_saques = limite_saques

class Transacao(ABC):
  @property
  @abstractproperty
  def valor(self):
    pass

  def registrar(self, conta):
    pass

class Deposito(Transacao):
  def __init__(self, valor):
    self._valor = valor

  @property  
  def valor(self):
    return self._valor 

  def registrar(self, conta):
    sucesso_transacao = conta.depositar(self.valor)

    if sucesso_transacao:
      conta.historico.adicionar_transacao(self)

class Saque(Transacao):
  def __init__(self, valor):
    self._valor = valor

  @property
  def valor(self):
    return self._valor

  def registrar(self, conta):
    sucesso_transacao = conta.sacar(self.valor)

    if sucesso_transacao:
      conta.historico.adicionar_transacao(self)

def sacar(clientes):
  cpf = input("Digite seu cpf (apenas numeros) ")
  cliente = filtrar_clientes(clientes, cpf)

  if not cliente:
    print("Não existe cliente cadastrado com este cpf!")
    return
  
  valor = float(input("Digite o valor do saque: "))
  transacao = Saque(valor)

  conta = recuperar_conta_cliente(cliente)
  if not conta:
    return

  cliente.realizar_transacao(conta, transacao)


def depositar(clientes):
  cpf = input("Digite seu cpf (apenas numeros) ")
  cliente = filtrar_clientes(clientes, cpf)

  if not cliente:
    print("Não existe cliente cadastrado com este cpf!")
    return

  valor = float(input("Digite o valor do depósito: "))
  transacao = Deposito(valor)

  conta = recuperar_conta_cliente(cliente)
  if not conta:
    return

  cliente.realizar_transacao(conta, transacao)

def recuperar_conta_cliente(cliente):
  if not cliente.contas:
    print("Este cliente não possui uma conta")
    return None
  else:
    return cliente.contas[0]

class Cliente:
  def __init__(self, endereco):
    self.endereco = endereco
    self.contas = []

  def realizar_transacao(self, conta, transacao):
    transacao.registrar(conta) 

class PessoaFisica(Cliente):
  def __init__(self, cpf, nome, data_nascimento, endereco):
      super().__init__(endereco)
      self.cpf = cpf
      self.nome = nome
      self.data_nascimento = data_nascimento
      
def criar_conta(numero_da_conta, clientes, contas):
  cpf = input("Informe seu cpf: ")
  cliente = filtrar_clientes(clientes, cpf)

  if not cliente:
    print("Não existe um cliente com este cpf")
    return

  conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_da_conta)
  contas.append(conta)
  cliente.contas.append(conta)

  print("Conta criada com sucesso")

def filtrar_clientes(clientes, cpf):
  clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
  return clientes_filtrados[0] if clientes_filtrados else None

def criar_cliente(clientes):
  cpf = input("Digite seu cpf (apenas números): ")
  
  if len(cpf) < 11 or len(cpf) > 11:
    print("Cpf inválido")
    return

  cliente = filtrar_clientes(clientes, cpf) 
  if cliente:
    print("Cliente ja existente com esse cpf")
    return

  nome = input("Digite seu nome: ")
  data_nascimento = input("Digite sua data de nascimento (dd/mm/aa): ")
  endereco = input("Digite seu endereço: ")

  cliente = PessoaFisica(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)

  clientes.append(cliente)
  print("Cliente criado com sucesso!")

def menu():
  texto = """\n
    ================MENU================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
  print(textwrap.dedent(texto))
  return input()

def main():
  clientes = []
  contas = []

  while True:
    opcao = menu()

    if opcao.lower() == 'd':
      depositar(clientes)
    elif opcao.lower() == 's':
      sacar(clientes)
      pass
    elif opcao.lower() == 'e':
      exibir_extrato(clientes)
      pass
    elif opcao.lower() == 'nc':
      numero_da_conta = len(contas) + 1
      criar_conta(numero_da_conta, clientes, contas)
      pass
    elif opcao.lower() == 'lc':
      listar_contas(contas)
      pass
    elif opcao.lower() == 'nu':
      criar_cliente(clientes)
      pass
    elif opcao.lower() == 'q':
      string_date = datetime.now()
      print(f"Execução do sistema finalizada, {datetime.strftime(string_date, "%d/%m/%Y %H:%M")}")
      break
    else:
      print("Opção inválida, tente novamente!")

main()