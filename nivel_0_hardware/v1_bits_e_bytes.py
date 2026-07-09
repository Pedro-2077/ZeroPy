print('=' * 60)
print('BITS E BYTES - A BASE DE TUDO')
print('=' * 60)


# ----------------------------------------------------------------------------
# FUNÇÃO 01: CONVERTER UM NUMERO DECIMAL PARA BINÁRIO MANUALMENTE
# ----------------------------------------------------------------------------


def para_binario(numero, largura=8):
    """
    Converte um inteiro para string binária de 'largura' dígitos.

    Algoritmo: dividir por 2 repetidamente, guardar os restos.
    Os restos coletados de trás para frente formam o número binário.

    Exemplo com número 10:
        10 ÷ 2 = 5  resto 0  ← bit menos significativo
         5 ÷ 2 = 2  resto 1
         2 ÷ 2 = 1  resto 0
         1 ÷ 2 = 0  resto 1  ← bit mais significativo
    Resultado (invertido): 1010
    """

    # A largura default é 8, ou seja vamos ter sempre 8 bits, mesmo que o número seja menor.
    # Exemplo: para o número 5, o resultado será 00000101.

    '''
    Representação visual do número 5 em binário (8 bits):
    5 em decimal = 00000101 em binário

    |  0   |  0  |  0   |  0   |  0   |  1   |  0   |  1   |
    |  128 |  64 |  32  |  16  |  8   |  4   |  2   |  1   |

    isso é, cada bit representa uma potência de 2, da direita para a esquerda:
    - O bit mais à direita (1) representa 2^0 = 1, e assim por diante até o bit mais à esquerda (128) que representa 2^7 = 128.
    '''

    if numero == 0:
        return '0' * largura

    restos = []
    n = numero

    # Divisão sucessiva por 2 — método tradicional de conversão decimal para binário.
    while n > 0:
        restos.append(n % 2)  # Coletando o resto da divisão por 2.
        n //= 2               # Dividindo o número por 2.

    # Inverte a lista, pois os restos foram coletados do último bit para o primeiro
    restos_invertidos = reversed(restos)

    # Converte cada resto para string e junta numa única string binária
    bits = []
    for bit in restos_invertidos:
        bits.append(str(bit))

    binario = ''.join(bits)

    # Adiciona zeros à esquerda para completar a largura especificada
    return binario.zfill(largura)


# ==================== Testando a função para_binario ==========================

print('\nNumeros de 0 a 20 em binário (8 bits):')

for i in range(21):
    binario = para_binario(i)
    print(f'{i:2d} em decimal = {binario} em binário')


# ----------------------------------------------------------------------------
# FUNÇÃO 02: CONVERTER BINARIO PARA DECIMAL
# ----------------------------------------------------------------------------

# Cada posição vale uma potência de 2.
# Posição 0 (direita) = 2⁰ = 1
# Posição 1           = 2¹ = 2
# Posição 2           = 2² = 4
# ...

def para_decimal(binario_str):
    """
    Converte uma string binária para um inteiro decimal.

    Algoritmo: percorrer a string da direita para a esquerda,
    multiplicando cada bit pelo valor da potência de 2 correspondente.

    Exemplo com binário '1010':
        0 * 2⁰ = 0
        1 * 2¹ = 2
        0 * 2² = 0
        1 * 2³ = 8
    Soma = 0 + 2 + 0 + 8 = 10
    """

    total = 0
    comprimento = len(binario_str)

    for i, bit in enumerate(binario_str):

        if bit == '1':
            """
            Lê cada bit da esquerda para a direita (índice i),
            mas a potência de 2 que cada bit representa aumenta
            da direita para a esquerda. A fórmula resolve esse
            conflito: potencia = comprimento - 1 - i

            "1010"  →  comprimento = 4

            i=0  →  4 - 1 - 0 = 3  →  1 × 2³ = 8
            i=1  →  4 - 1 - 1 = 2  →  0 × 2² = 0  (ignorado)
            i=2  →  4 - 1 - 2 = 1  →  1 × 2¹ = 2
            i=3  →  4 - 1 - 3 = 0  →  0 × 2⁰ = 0  (ignorado)

            Total: 8 + 2 = 10
            """

            potencia = comprimento - 1 - i
            total += 2 ** potencia

    return total


# ==================== Testando a função para_decimal ==========================

print('\nNumeros binários convertidos para decimal:')

lista = ['00000000', '00000001', '00000010', '00000011', '00000100',
         '00000101', '00000110', '00000111', '00001000', '00001001',
         '00001010', '00001011', '00001100', '00001101', '00001110',
         '00001111', '00010000', '00010001', '00010010', '00010011', '00010100']

for binario in lista:
    decimal = para_decimal(binario)
    print(f'{binario} em binário = {decimal} em decimal')


# ----------------------------------------------------------------------------
# FUNÇÃO 03: INVERTENDO CADA BIT
# ----------------------------------------------------------------------------
# Em binário, cada posição tem só dois estados possíveis: 0 ou 1.
# Quando subtraímos de 255 (11111111), cada bit é forçado a trocar:
#
#   posição:    7  6  5  4  3  2  1  0
#   255       = 1  1  1  1  1  1  1  1
#   204       = 1  1  0  0  1  1  0  0
#               ↓  ↓  ↓  ↓  ↓  ↓  ↓  ↓
#   resultado = 0  0  1  1  0  0  1  1  = 51
#
# Onde o número tem 1, o resultado tem 0 — porque 1 - 1 = 0.
# Onde o número tem 0, o resultado tem 1 — porque 1 - 0 = 1.
#
# O 255 garante que toda posição tem um 1 para subtrair, então todos os bits invertem.
# Se fosse 254 (11111110), o último bit não inverteria.

def inverter_bits(numero):
    resultado = 255 - numero
    return resultado


# ==================== Testando a função inverter_bits ==========================

print('\nInvertendo bits:')

for n in [0, 204, 170, 255]:
    invertido = inverter_bits(n)
    print(f'{para_binario(n)} ({n}) → {para_binario(invertido)} ({invertido})')


# ----------------------------------------------------------------------------
# FUNÇÃO 04: CONVERTER BYTE PARA CARACTERE
# ----------------------------------------------------------------------------
# ASCII vai de 0 a 127 — cada número tem um caractere correspondente.
# Acima de 127 o byte faz parte de um caractere especial (UTF-8 multi-byte).

def para_caracteres(byte):
    """
    Converte um byte (inteiro de 0 a 255) para seu caractere correspondente.

    Exemplo:
        65  -> 'A'
        97  -> 'a'
        195 -> (multi-byte)  parte de um caractere acentuado em UTF-8
    """
    if byte <= 127:
        return chr(byte)
    else:
        return "(multi-byte)"


# -----------------------------------------------------------------------------
# ASCII — Como letras viram números
# -----------------------------------------------------------------------------
# Os caracteres são representados por números pois o computador só entende números.
# Esses números são chamados de códigos ASCII (American Standard Code for Information Interchange).
# ord('A') retorna o código ASCII. chr(65) retorna 'A'. Esse código é 65, que em binário é 01000001.

print('\n\n')
print('=' * 30)
print('TABELA ASCII PARCIAL')
print(f'\n{"Char":^6} | {"Decimal":^7} | {"Binario":^10}')
print('=' * 30)

# MAIÚSCULAS
lista_maiusculas = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

for letra in lista_maiusculas:
    codigo_decimal = ord(letra)
    binario = para_binario(codigo_decimal)
    print(f'{letra:^6} | {codigo_decimal:^7} | {binario:^10}')

# MINÚSCULAS
lista_minusculas = 'abcdefghijklmnopqrstuvwxyz'

for letra in lista_minusculas:
    codigo_decimal = ord(letra)
    binario = para_binario(codigo_decimal)
    print(f'{letra:^6} | {codigo_decimal:^7} | {binario:^10}')


# -----------------------------------------------------------------------------
# UTF-8 — Por que 'á' precisa de 2 bytes
# -----------------------------------------------------------------------------
# ASCII só vai até 127 — sem acentos, sem símbolos especiais.
# UTF-8 resolve isso usando 2 ou mais bytes para caracteres acima de 127.

print('\n\n')
print("Exemplo de caracteres especiais com UTF-8:")

texto = 'Olá Mundo'
print(f'\nTexto: {texto}')
print(f'Comprimento (caracteres): {len(texto)}')

# ------------------------------------------------------------
# encode('utf-8') transforma a string em uma sequência de bytes.
#
# Antes (string):
#
# "Olá Mundo"
#
# len(texto) = 9
#
# Porque existem 9 caracteres:
#
# O | l | á |   | M | u | n | d | o
# 1   2   3   4   5   6   7   8   9
#
#
# Depois (bytes):
#
# b'Ol\xc3\xa1 Mundo'  — \x indica que o próximo valor é um byte em hexadecimal.
#
# Agora o len() não conta mais caracteres,
# ele conta quantos BYTES existem.
#
# O  -> 1 byte
# l  -> 1 byte
# á  -> 2 bytes (C3 A1)
# ' '-> 1 byte
# M  -> 1 byte
# u  -> 1 byte
# n  -> 1 byte
# d  -> 1 byte
# o  -> 1 byte
#
# Total:
#
# 1 + 1 + 2 + 1 + 1 + 1 + 1 + 1 + 1 = 10 bytes
#
# Por isso:
#
# len(texto)                 -> 9
# len(texto.encode('utf-8')) -> 10
# ------------------------------------------------------------

bytes_utf8 = texto.encode('utf-8')
print(f'\nBytes UTF-8: {bytes_utf8}')
print(f'Comprimento (bytes): {len(bytes_utf8)}')
print(f'\nByte a Byte:')

print(f'\n{"idx":^4}  {"decimal":^7}  {"binario":^10}  {"caractere":^12}')
print(f'{"-"*4}  {"-"*7}  {"-"*10}  {"-"*12}')

for i, byte in enumerate(bytes_utf8):
    binario = para_binario(byte)
    caractere = para_caracteres(byte)
    print(f'[{i:2d}]  {byte:7d}  {binario:^10}  {caractere:^12}')


# -----------------------------------------------------------------------------
# OPERAÇÕES BIT A BIT — como a CPU realmente opera
# -----------------------------------------------------------------------------

print('\n\n')
print('=' * 60)
print('OPERACOES BIT A BIT - COMO A CPU REALMENTE OPERA')
print('=' * 60)

a = 204
b = 170
binario_a = para_binario(a)
binario_b = para_binario(b)

print(f'\na = {a} em decimal = {binario_a} em binário')
print(f'b = {b} em decimal = {binario_b} em binário')

resultado_and   = a & b
resultado_or    = a | b
resultado_xor   = a ^ b
resultado_not_a = inverter_bits(a)

binario_and   = para_binario(resultado_and)
binario_or    = para_binario(resultado_or)
binario_xor   = para_binario(resultado_xor)
binario_not_a = para_binario(resultado_not_a)

print(f'\na   = {binario_a}')
print(f'b   = {binario_b}')
print(f'      --------')
print(f'AND = {binario_and} ({resultado_and})  ← 1 onde OS DOIS sao 1')

print(f'\na   = {binario_a}')
print(f'b   = {binario_b}')
print(f'      --------')
print(f'OR  = {binario_or} ({resultado_or})  ← 1 onde ALGUM e 1')

print(f'\na   = {binario_a}')
print(f'b   = {binario_b}')
print(f'      --------')
print(f'XOR = {binario_xor} ({resultado_xor})  ← 1 onde SAO DIFERENTES')

print(f'\na   = {binario_a}')
print(f'      --------')
print(f'NOT = {binario_not_a} ({resultado_not_a})  ← cada bit inverteu')

# ============================================================
# Operador Shift (<< e >>)
# ============================================================

c = 10

binario_c = para_binario(c)

resultado_shift_esque_1  = (c << 1) & 0xFF  # Desloca todos os bits para a esquerda (multiplica por 2)
resultado_shift_esque_2 = (c << 2) & 0xFF  # Desloca todos os bits para a esquerda (multiplica por 4)
resultado_shift_esque_3 = (c << 3) & 0xFF  # Desloca todos os bits para a esquerda (multiplica por 8)
resultado_shift_dire_1  = c >> 1  # Desloca todos os bits para a direita (divide por 2)
resultado_shift_dire_2 = c >> 2  # Desloca todos os bits para a direita (divide por 4)
resultado_shift_dire_3 = c >> 3  # Desloca todos os bits para a direita (divide por 8)

binario_shift_esque_1 = para_binario(resultado_shift_esque_1)
binario_shift_esque_2 = para_binario(resultado_shift_esque_2)
binario_shift_esque_3 = para_binario(resultado_shift_esque_3)
binario_shift_dire_1 = para_binario(resultado_shift_dire_1)
binario_shift_dire_2 = para_binario(resultado_shift_dire_2)
binario_shift_dire_3 = para_binario(resultado_shift_dire_3)

print(f'\nc      = {binario_c} ({c})')
print(f'c << 1 = {binario_shift_esque_1} ({resultado_shift_esque_1})  ← multiplicou por 2')
print(f'c << 2 = {binario_shift_esque_2} ({resultado_shift_esque_2})  ← multiplicou por 4')
print(f'c << 3 = {binario_shift_esque_3} ({resultado_shift_esque_3})  ← multiplicou por 8')
print(f'c >> 1 = {binario_shift_dire_1} ({resultado_shift_dire_1})   ← dividiu por 2')
print(f'c >> 2 = {binario_shift_dire_2} ({resultado_shift_dire_2})    ← dividiu por 4')
print(f'c >> 3 = {binario_shift_dire_3} ({resultado_shift_dire_3})    ← dividiu por 8')

print('\n' + '=' * 60)
print('Semana 1 - Parte 1 completa!')
print('=' * 60)
