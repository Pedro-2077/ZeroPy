# =============================================================================
# ARQUIVO: nivel_0_hardware/v2_memoria.py
# SEMANA 1 — Memória: como bytes são armazenados e acessados
# =============================================================================

# =============================================================================
# JORNADA
# =============================================================================
#
# Computador
#     │
#     ├── Hardware
#     │      │
#     │      ├── Bits
#     │      ├── Bytes
#     │      └── Memória   ← Estamos aqui
#     │
#     ├── Sistema Operacional
#     │
#     └── Python
#            │
#            ├── Objetos
#            ├── Inteiros
#            ├── Strings
#            └── Listas
#
# Nesta etapa vamos entender como a memória funciona antes de
# descobrir como o Python cria seus objetos.
# =============================================================================

# =============================================================================
# CONTEXTO
# =============================================================================
#
# Antes de entendermos como o Python cria objetos como:
#
#     x = 10
#     nome = "Pedro"
#     lista = [1, 2, 3]
#
# precisamos entender onde esses objetos são armazenados.
#
# Todo objeto criado pelo Python precisa ocupar um espaço na memória.
#
# Mas o Python não é dono da memória do computador.
#
# Quem controla toda a memória RAM é o Sistema Operacional
# (Windows, Linux, macOS...).
#
# Quando o Python precisa de memória, ele solicita uma região ao Sistema
# Operacional. Depois que essa região é entregue, o próprio Python passa
# a administrá-la.
#
# Nesta aula vamos construir uma versão simplificada desse gerenciamento.
#
# Ainda NÃO estamos implementando o pymalloc do CPython.
#
# Nosso objetivo é entender os conceitos fundamentais:
#
# • memória
# • endereços
# • bytes
# • alocação
# • free list
# • fragmentação
#
# Quando esses conceitos estiverem claros, ficará muito mais fácil
# entender como o CPython realmente funciona internamente.
# =============================================================================

# =============================================================================
# O PROBLEMA
# =============================================================================
#
# Já sabemos que o Python recebeu uma região de memória do
# Sistema Operacional.
#
# Mas como podemos representar essa região de memória utilizando
# Python?
#
# Não podemos usar uma lista comum, um dicionário ou uma string,
# porque essas estruturas não representam o funcionamento da memória RAM.
#
# Precisamos de uma estrutura que seja o mais parecida possível
# com a memória real.
#
# Essa estrutura deve responder às seguintes perguntas:
#
# • Como representar os bytes da memória?
#
# • Como acessar um endereço específico?
#
# • Como alterar o conteúdo de um endereço?
#
# • Como garantir que cada posição represente exatamente 1 byte?
#
# Antes de começarmos a implementar nossa memória,
# precisamos responder essa pergunta.
# =============================================================================

# =============================================================================
# A SOLUÇÃO
# =============================================================================
#
# Vamos pensar com calma no que a memória RAM realmente é.
#
# A memória do computador pode ser imaginada como uma longa fileira
# de "caixinhas" numeradas, uma do lado da outra.
#
# Cada caixinha:
#
# • tem um número (o endereço);
# • guarda um valor pequeno (exatamente 1 byte, ou seja, de 0 a 255);
# • pode ser lida a qualquer momento;
# • pode ser alterada a qualquer momento.
#
# Ou seja, precisamos de uma estrutura que seja:
#
# • sequencial (uma posição depois da outra);
# • indexável (conseguimos acessar pelo número da posição);
# • mutável (conseguimos alterar o valor guardado);
# • limitada a 1 byte por posição (não podemos guardar um valor gigante
#   numa única casa da memória).
#
# Precisamos, então, de algo parecido com uma lista, mas com uma
# restrição importante: cada posição só pode guardar um número entre
# 0 e 255. Isso porque um byte tem exatamente 8 bits, e 8 bits
# permitem representar no máximo 256 valores diferentes (2 elevado a 8).
#
# Se tentássemos guardar, por exemplo, o número 300 em uma posição,
# estaríamos violando a própria definição de byte.
#
# Python já possui uma estrutura pronta que representa exatamente
# essa ideia: uma sequência contínua de bytes, mutável, onde cada
# posição vai de 0 a 255.
#
# Essa estrutura se chama bytearray.
#
# Não estamos escolhendo o bytearray porque "é fácil" ou porque
# "já existe pronto". Estamos escolhendo porque ele é a representação
# que mais se aproxima do comportamento real da memória RAM.
#
# Agora que entendemos por que o bytearray é a ferramenta certa,
# podemos finalmente implementar nossa primeira simulação de memória.
# =============================================================================


print("=" * 60)
print("  MEMÓRIA — Como bytes são guardados")
print("=" * 60)

class Memoria:
    
    """
    Simula uma região de memória administrada pelo Python.

    Na vida real, o Python solicita memória ao Sistema Operacional.
    Depois de recebida, ele passa a administrá-la internamente.

    Aqui vamos representar essa região usando um `bytearray`.

    Cada posição do bytearray representa um endereço de memória
    e armazena exatamente 1 byte (8 bits).

    Exemplo:

        Endereço   Conteúdo
        0          00000000
        1          11101010
        2          00101101
        3          01010111
    """

    def __init__(self, tamanho_bytes: int):
        self._dados = bytearray(tamanho_bytes)  # cria a região de memória, tudo zerado
        self._tamanho = tamanho_bytes           # guarda o tamanho total para consultas futuras

        print(f"Memória criada: {tamanho_bytes} bytes.")
    
    # -------------------------------------------------------------------------
    # LER e ESCREVER bytes individuais
    # -------------------------------------------------------------------------

    def escrever_byte(self, endereco: int, valor: int):
        """
        escrever_byte()

        Pergunta que este método responde:
        Como colocar um valor em um endereço específico, garantindo
        que esse valor cabe em 1 byte e que o endereço realmente
        existe dentro da nossa memória?
        """
        
        if endereco < 0 or endereco >= self._tamanho:
            raise IndexError(f"Endereço {endereco} fora do intervalo da memória (0 a {self._tamanho - 1}).")

        if valor < 0 or valor > 255:
            raise ValueError(f"Byte deve ser 0-255, recebeu {valor}")

        self._dados[endereco] = valor


    def ler_byte(self, endereco: int) ->int:
        """
        ler_byte()

        Pergunta que este método responde:
        Como descobrir o que está guardado em um endereço específico?
        """
        
        if endereco < 0 or endereco >= self._tamanho:
            raise IndexError(f"Endereço {endereco} fora do intervalo da memória (0 a {self._tamanho - 1}).")
        
        return self._dados[endereco]
    
# =============================================================================
# DEMONSTRAÇÃO
# =============================================================================
    
mem = Memoria(16)  # cria uma memória de 16 bytes

print("\nEscrevendo alguns bytes:")
mem.escrever_byte(0, 65) # escreve o byte 65 (ASCII 'A') no endereço 0
mem.escrever_byte(1, 66) # escreve o byte 66 (ASCII 'B') no endereço 1
mem.escrever_byte(2, 255) # escreve o byte 255 no endereço 2



print(f'Endereço 0: {mem.ler_byte(0)}')
print(f'Endereço 1: {mem.ler_byte(1)}')
print(f'Endereço 2: {mem.ler_byte(2)}')


print('\nTestando os Limites:')

try:
    mem.escrever_byte(0,355) # Invalido acima de 255
except ValueError as erro:
    print(f'Erro esperado: {erro}')


try:
    mem.ler_byte(100) #Invalido pois a memoria vai ate 16 bytes
except IndexError as erro:
    print(f'Erro esperado:{erro}')

# =============================================================================
# O QUE APRENDEMOS
# =============================================================================
#
# • Uma memória precisa de duas operações básicas: ler e escrever.
# • Escrever exige validar que o valor cabe em 1 byte (0-255).
# • Tanto ler quanto escrever precisam validar que o endereço existe
#   dentro dos limites da memória — assim como acontece de verdade.
# =============================================================================

