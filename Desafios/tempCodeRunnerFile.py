from datetime import date, datetime
import textwrap


class IteradorDasContas:
  def __init__(self, contas):
    self.contas = contas
    self._index = 0

  def __iter__(self):
    return self

  def __next__(self):
    try:
      conta = self.contas[self._index]
      texto = f"""
      Agência: {conta.agencia}
      Número: {conta.numero}
      Titular: {conta.cliente.nome}
      Saldo: {conta.saldo}
      """
      return texto
    except IndexError:
      raise StopIteration
    finally:
      self._index += 1

def listar_contas(contas):
  if not contas:
    print("Não tem nenhuma conta cadastrada")

  for conta in IteradorDasContas(contas):
    print(textwrap.dedent((conta)))


class Cliente:
  def __init__(self, endereco):
    self.endereco = endereco
    self.contas = []


class Conta:
  def __init__(self, numero, cliente):
    self.cliente = cliente
    self.numero = numero
    self.agencia = "0001"
    self.saldo = 0

  def _deposito(self, valor):
    if valor > 0:
      self.saldo += valor
      print(f"Operação concluida deposito de {valor}")
    else:
      print("Valor inválido")
      return


def realizar_deposito(clientes):
  cpf = input("Digite o cpf: ")

  if len(cpf) < 11 or len(cpf) > 11:
    print("Cpf inválido")
    return
  else:
    cliente = filtrar_clientes(cpf, clientes)

  if not cliente:
    print("Cliente não existente")
    return

  valor = float(input("Digite o valor do deposito: "))

  transacao = Conta._deposito(valor)


class ContaCorrente(Conta):
  def __init__(self, numero, cliente, limite=500, limite_saques=3):
    super().__init__(numero, cliente)
    self.limite_saques = limite_saques
    self.limite = limite

  @classmethod
  def nova_conta(cls, numero, cliente, limite, limite_saques):
    return cls(numero, cliente, limite, limite_saques)



class PessoaFisica(Cliente):
  def __init__(self, nome, data_nascimento, cpf, endereco):
    super().__init__(endereco)
    self.nome = nome
    self.data_nascimento = data_nascimento
    self.cpf = cpf


def filtrar_clientes(cpf, clientes):
  clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
  return clientes_filtrados[0] if clientes_filtrados else None


def criar_cliente(clientes):

  cpf = input('Digite seu CPF (somente número) ')
  if len(cpf) > 11 or len(cpf) < 11:
    print('CPF inválido')
    return

  cliente = filtrar_clientes(cpf, clientes)
  
  if cliente:
    print(" Cliente ja existente com esse CPF!  ")
    return

  nome = input('Informe seu nome completo ')
  data_nascimento = input('informe a data de nascimento (dd/mm/aaaa) ')
  endereco = input('Informe seu endereço (bairro, cidade, estado, logradouro, nro) ')

  cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, endereco=endereco, cpf=cpf)
  clientes.append(cliente)

  print('Operação concluida com sucesso')

def criar_conta(numero_conta, clientes, contas):
  cpf = input('Informe seu CPF (somente número) ')
  if len(cpf) > 11 or len(cpf) < 11:
    print('CPF inválido')
    return

  cliente = filtrar_clientes(cpf, clientes)

  if not cliente:
    print('Cliente não encontrado(a)')
    return

  conta = ContaCorrente.nova_conta(numero=numero_conta, cliente=cliente, limite_saques=50, limite=500)
  contas.append(conta)
  cliente.contas.append(conta)
  print(conta.numero, conta.cliente.nome, conta.limite_saques, conta.limite, cliente.contas)
  

def menu():
  menu = """
  ================ Selecione ================
  [D] Depositar
  [S] Sacar
  [NC] Nova conta
  [LC] Listar contas
  [NU] Novo usuario
  [Q] Sair
  """
  return input(textwrap.dedent(menu))


def main():
  clientes = []
  contas = []
  while True:
    opcao = menu()

    if opcao.upper() == 'D':
      realizar_deposito(clientes)
    elif opcao.upper() == 'S':
      pass
    elif opcao.upper() == 'NC':
      numero_conta = len(contas) + 1
      criar_conta(numero_conta, clientes, contas)
    elif opcao.upper() == 'LC':
      listar_contas(contas)
    elif opcao.upper() == 'NU':
      criar_cliente(clientes)
    elif opcao.upper() == 'Q':
      print(f'Sistema encerrado {datetime.now()}')
      break
    else:
      print('Opcão invalida tente novamente')
  

main()