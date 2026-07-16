# =============================================================================
# ARQUIVO: nivel_0_hardware/v1_bits_e_bytes.py
# SEMANA 1 — PARTE 1 — Bits e Bytes: a base de tudo
# =============================================================================

print("=" * 60)
print("  BITS E BYTES — A BASE DE TUDO")
print("=" * 60)

# =============================================================================
# JORNADA
# =============================================================================
#
# Computador
#     │
#     ├── Hardware
#     │      │
#     │      ├── Bits        ← Estamos aqui
#     │      ├── Bytes       ← Estamos aqui
#     │      └── Memória
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
# Antes de falar em memória, precisamos entender do que ela é feita.
# Memória é, no fundo, uma quantidade gigantesca de bits organizados
# em grupos de 8 (bytes). Esta é a fundação de tudo que vem depois.
# =============================================================================

# =============================================================================
# CONTEXTO
# =============================================================================
#
# O computador não entende letras, números decimais, imagens ou sons.
#
# O computador entende exatamente uma coisa: presença ou ausência de
# corrente elétrica. Ligado ou desligado. 1 ou 0.
#
# Cada uma dessas unidades mínimas se chama BIT (Binary Digit).
#
# Sozinho, um bit representa muito pouco — só duas possibilidades.
# Por isso os bits são agrupados em conjuntos de 8, formando um BYTE.
#
# Um byte, com seus 8 bits, consegue representar 256 combinações
# diferentes (2 elevado a 8). É justamente por isso que, mais para
# frente, cada posição da nossa "memória" (o bytearray) só aceita
# valores de 0 a 255 — é o limite físico de um byte.
#
# Antes de simularmos memória, endereços e alocação, precisamos
# treinar o olho para enxergar números da forma que o computador
# enxerga: em binário.
# =============================================================================

# =============================================================================
# O PROBLEMA
# =============================================================================
#
# Nós pensamos em números na base 10 (decimal): 0, 1, 2, ..., 9, e
# depois "viramos a casa" (10, 11, 12...).
#
# O computador só tem dois símbolos disponíveis: 0 e 1. Ou seja, ele
# pensa na base 2 (binário).
#
# Isso gera duas perguntas imediatas:
#
# • Como transformar um número que pensamos em decimal (como 10)
#   para a forma que o computador entende (1010)?
#
# • Como fazer o caminho inverso: pegar algo em binário e entender
#   que valor decimal ele representa?
#
# Sem resolver isso, não conseguimos nem começar a "ler" o que está
# guardado dentro de uma memória.
# =============================================================================

# =============================================================================
# A SOLUÇÃO
# =============================================================================
#
# Para ir de decimal para binário, existe um método clássico e manual:
# a divisão sucessiva por 2.
#
# A ideia é simples: dividimos o número por 2 repetidamente, anotando
# o resto de cada divisão. Quando não dá mais para dividir, os restos
# anotados — lidos de trás para frente — formam o número binário.
#
# Exemplo com o número 10:
#
#     10 ÷ 2 = 5   resto 0   ← bit menos significativo
#      5 ÷ 2 = 2   resto 1
#      2 ÷ 2 = 1   resto 0
#      1 ÷ 2 = 0   resto 1   ← bit mais significativo
#
# Lendo os restos de baixo para cima: 1010.
#
# Para o caminho inverso (binário → decimal), a lógica se inverte:
# cada posição do número binário vale uma potência de 2, e somamos
# apenas as posições que têm o bit 1.
#
# Representação visual do número 5 em binário (8 bits):
#
#     |  0   |  0  |  0   |  0   |  0   |  1   |  0   |  1   |
#     |  128 |  64 |  32  |  16  |  8   |  4   |  2   |  1   |
#
# Cada bit representa uma potência de 2, da direita para a esquerda:
# o bit mais à direita vale 2⁰ = 1, o próximo vale 2¹ = 2, e assim
# por diante até o bit mais à esquerda, que vale 2⁷ = 128.
#
# Agora que entendemos a ideia por trás das duas conversões, podemos
# implementá-las.
# =============================================================================

# =============================================================================
# IMPLEMENTAÇÃO
# =============================================================================

def para_binario(numero, largura=8):
    """
    para_binario()

    Pergunta que este método responde:
    Como transformar um número decimal na sequência de bits que
    o computador realmente enxerga?

    A largura default é 8 — sempre teremos 8 bits, mesmo que o
    número seja pequeno. Exemplo: o número 5 vira "00000101".
    """

    if numero == 0:
        return "0" * largura

    restos = []
    n = numero

    # Divisão sucessiva por 2 — método tradicional de conversão.
    while n > 0:
        restos.append(n % 2)
        n //= 2

    # Os restos foram coletados do último bit para o primeiro,
    # então precisamos inverter a ordem.
    restos_invertidos = reversed(restos)

    bits = [str(bit) for bit in restos_invertidos]
    binario = "".join(bits)

    # Completa com zeros à esquerda até atingir a largura desejada.
    return binario.zfill(largura)


def para_decimal(binario_str):
    """
    para_decimal()

    Pergunta que este método responde:
    Dado algo que o computador enxerga (binário), como descobrir
    o valor decimal que isso representa para nós?

    Percorremos a string da esquerda para a direita, e para cada
    bit "1" somamos a potência de 2 correspondente à sua posição.
    """

    total = 0
    comprimento = len(binario_str)

    for i, bit in enumerate(binario_str):
        if bit == "1":
            # O índice i cresce da esquerda para a direita, mas a
            # potência de 2 cresce da direita para a esquerda.
            # Por isso a conversão: potencia = comprimento - 1 - i
            potencia = comprimento - 1 - i
            total += 2 ** potencia

    return total


# =============================================================================
# DEMONSTRAÇÃO
# =============================================================================

print("\nNúmeros de 0 a 20 em binário (8 bits):")
for i in range(21):
    binario = para_binario(i)
    print(f"{i:2d} em decimal = {binario} em binário")

print("\nNúmeros binários convertidos para decimal:")
lista = ["00000000", "00000001", "00000010", "00000011", "00000100",
         "00000101", "00000110", "00000111", "00001000", "00001001",
         "00001010", "00001011", "00001100", "00001101", "00001110",
         "00001111", "00010000", "00010001", "00010010", "00010011", "00010100"]

for binario in lista:
    decimal = para_decimal(binario)
    print(f"{binario} em binário = {decimal} em decimal")

# =============================================================================
# O QUE APRENDEMOS
# =============================================================================
#
# • O computador só entende 0 e 1 (bits).
# • Um byte é um grupo de 8 bits e representa 256 valores (0-255).
# • Conseguimos converter decimal → binário dividindo por 2.
# • Conseguimos converter binário → decimal somando potências de 2.
# =============================================================================

# =============================================================================
# PRÓXIMA ETAPA
# =============================================================================
#
# Sabemos converter números. Mas e se quisermos inverter todos os
# bits de um número de uma só vez? Existe uma forma de fazer isso
# sem escrever um laço manual, bit por bit?
# =============================================================================


# =============================================================================
# CONTEXTO
# =============================================================================
#
# Em muitas situações — como veremos futuramente ao lidar com
# máscaras de memória e sinalizadores (flags) — precisamos inverter
# todos os bits de um número: onde havia 1, passa a haver 0, e
# onde havia 0, passa a haver 1.
# =============================================================================

# =============================================================================
# O PROBLEMA
# =============================================================================
#
# Poderíamos percorrer bit a bit e trocar manualmente cada um.
# Mas existe alguma forma aritmética mais direta de fazer isso?
# =============================================================================

# =============================================================================
# A SOLUÇÃO
# =============================================================================
#
# Em binário, cada posição só tem dois estados possíveis: 0 ou 1.
# Se subtrairmos um número de 255 (11111111 em binário), cada bit
# é forçado a trocar de estado:
#
#     posição:    7  6  5  4  3  2  1  0
#     255       = 1  1  1  1  1  1  1  1
#     204       = 1  1  0  0  1  1  0  0
#                 ↓  ↓  ↓  ↓  ↓  ↓  ↓  ↓
#     resultado = 0  0  1  1  0  0  1  1  = 51
#
# Onde o número tinha 1, o resultado tem 0 (porque 1 - 1 = 0).
# Onde o número tinha 0, o resultado tem 1 (porque 1 - 0 = 1).
#
# O valor 255 garante que toda posição tenha um 1 disponível para
# subtrair, então todos os bits acabam invertidos. Se usássemos 254
# (11111110), o último bit não inverteria.
# =============================================================================

# =============================================================================
# IMPLEMENTAÇÃO
# =============================================================================

def inverter_bits(numero):
    """
    inverter_bits()

    Pergunta que este método responde:
    Como inverter todos os bits de um número de uma só vez?
    """
    resultado = 255 - numero
    return resultado


# =============================================================================
# DEMONSTRAÇÃO
# =============================================================================

print("\nInvertendo bits:")
for n in [0, 204, 170, 255]:
    invertido = inverter_bits(n)
    print(f"{para_binario(n)} ({n}) → {para_binario(invertido)} ({invertido})")

# =============================================================================
# O QUE APRENDEMOS
# =============================================================================
#
# • É possível inverter todos os bits de um número com uma simples
#   subtração de 255, sem precisar de laços manuais.
# =============================================================================

# =============================================================================
# PRÓXIMA ETAPA
# =============================================================================
#
# Já sabemos representar números em binário. Mas o computador
# também guarda letras e textos. Como um número pode virar uma
# letra?
# =============================================================================


# =============================================================================
# CONTEXTO
# =============================================================================
#
# Os caracteres que vemos na tela (letras, símbolos) são, para o
# computador, apenas números. Ele não sabe o que é a letra "A" — ele
# só sabe que existe o valor 65.
#
# Essa correspondência entre número e caractere é definida por uma
# tabela padronizada chamada ASCII (American Standard Code for
# Information Interchange).
# =============================================================================

# =============================================================================
# O PROBLEMA
# =============================================================================
#
# Como saber qual caractere corresponde a um determinado byte?
# E o que acontece quando o byte representa um caractere que não
# existe na tabela ASCII (como "á", com acento)?
# =============================================================================

# =============================================================================
# A SOLUÇÃO
# =============================================================================
#
# A tabela ASCII define os valores de 0 a 127. Python já nos dá
# acesso a essa tabela através de duas funções prontas:
#
# • ord('A') retorna o código ASCII do caractere ('A' → 65)
# • chr(65) retorna o caractere correspondente ao código (65 → 'A')
#
# O valor 65, em binário, é 01000001 — ou seja, por trás de toda
# letra existe, no fim das contas, um byte comum.
#
# Só que ASCII não cobre tudo: valores acima de 127 não têm um
# caractere único e fixo — eles fazem parte de codificações maiores,
# como o UTF-8, que veremos a seguir.
# =============================================================================

# =============================================================================
# IMPLEMENTAÇÃO
# =============================================================================

def para_caracteres(byte):
    """
    para_caracteres()

    Pergunta que este método responde:
    Dado um byte (0-255), qual caractere ele representa — e o que
    fazer quando ele está fora do alcance do ASCII puro?
    """
    if byte <= 127:
        return chr(byte)
    else:
        return "(multi-byte)"


# =============================================================================
# DEMONSTRAÇÃO
# =============================================================================

print("\n\n" + "=" * 30)
print("TABELA ASCII PARCIAL")
print(f"\n{'Char':^6} | {'Decimal':^7} | {'Binario':^10}")
print("=" * 30)

lista_maiusculas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for letra in lista_maiusculas:
    codigo_decimal = ord(letra)
    binario = para_binario(codigo_decimal)
    print(f"{letra:^6} | {codigo_decimal:^7} | {binario:^10}")

lista_minusculas = "abcdefghijklmnopqrstuvwxyz"
for letra in lista_minusculas:
    codigo_decimal = ord(letra)
    binario = para_binario(codigo_decimal)
    print(f"{letra:^6} | {codigo_decimal:^7} | {binario:^10}")

# =============================================================================
# O QUE APRENDEMOS
# =============================================================================
#
# • Todo caractere é, por baixo dos panos, um número (byte).
# • A tabela ASCII define esse mapeamento para os valores 0-127.
# • ord() e chr() fazem a conversão nos dois sentidos.
# =============================================================================

# =============================================================================
# PRÓXIMA ETAPA
# =============================================================================
#
# ASCII só cobre 128 valores. Mas existem milhares de caracteres no
# mundo (acentos, emojis, alfabetos diferentes). Como o computador
# representa tudo isso usando apenas bytes de 0 a 255?
# =============================================================================


# =============================================================================
# CONTEXTO
# =============================================================================
#
# ASCII foi criado pensando apenas no inglês, sem acentos e sem
# símbolos especiais. Mas o mundo tem muito mais caracteres do que
# os 128 que o ASCII cobre.
# =============================================================================

# =============================================================================
# O PROBLEMA
# =============================================================================
#
# Se um byte só vai até 255, como representar caracteres que vão
# muito além disso, como "á", "€" ou emojis?
# =============================================================================

# =============================================================================
# A SOLUÇÃO
# =============================================================================
#
# A resposta é: usar mais de um byte para representar um único
# caractere quando necessário. Essa é a ideia por trás do UTF-8,
# a codificação mais usada atualmente.
#
# Em UTF-8, caracteres ASCII (até 127) continuam ocupando apenas
# 1 byte. Mas caracteres especiais, como "á", passam a ocupar 2
# bytes (ou mais).
#
# Isso muda uma coisa importante: contar CARACTERES não é o mesmo
# que contar BYTES.
#
# Exemplo com o texto "Olá Mundo":
#
#     Antes (string, contando caracteres):
#
#         O | l | á |   | M | u | n | d | o
#         1   2   3   4   5   6   7   8   9
#
#         len(texto) = 9
#
#     Depois (bytes, contando bytes reais):
#
#         b'Ol\xc3\xa1 Mundo'
#
#         O  -> 1 byte
#         l  -> 1 byte
#         á  -> 2 bytes (C3 A1)
#         ' '-> 1 byte
#         M  -> 1 byte
#         u  -> 1 byte
#         n  -> 1 byte
#         d  -> 1 byte
#         o  -> 1 byte
#
#         Total = 10 bytes
#
# Ou seja:
#
#     len(texto)                 → 9
#     len(texto.encode('utf-8')) → 10
#
# O caractere "á" sozinho já "rouba" um byte extra.
# =============================================================================

# =============================================================================
# IMPLEMENTAÇÃO
# =============================================================================
#
# Aqui não precisamos escrever um conversor do zero — o próprio
# Python já implementa UTF-8 através do método .encode('utf-8').
# Nosso trabalho agora é apenas observar, byte a byte, o que
# acontece por trás dessa conversão.
# =============================================================================

# =============================================================================
# DEMONSTRAÇÃO
# =============================================================================

print("\n\nExemplo de caracteres especiais com UTF-8:")

texto = "Olá Mundo"
print(f"\nTexto: {texto}")
print(f"Comprimento (caracteres): {len(texto)}")

bytes_utf8 = texto.encode("utf-8")
print(f"\nBytes UTF-8: {bytes_utf8}")
print(f"Comprimento (bytes): {len(bytes_utf8)}")
print("\nByte a Byte:")

print(f"\n{'idx':^4}  {'decimal':^7}  {'binario':^10}  {'caractere':^12}")
print(f"{'-'*4}  {'-'*7}  {'-'*10}  {'-'*12}")

for i, byte in enumerate(bytes_utf8):
    binario = para_binario(byte)
    caractere = para_caracteres(byte)
    print(f"[{i:2d}]  {byte:7d}  {binario:^10}  {caractere:^12}")

# =============================================================================
# O QUE APRENDEMOS
# =============================================================================
#
# • Nem todo caractere cabe em 1 byte.
# • UTF-8 usa múltiplos bytes para caracteres fora do ASCII.
# • len() de uma string conta caracteres; len() de bytes conta bytes
#   — e esses dois números podem ser diferentes.
# =============================================================================

# =============================================================================
# PRÓXIMA ETAPA
# =============================================================================
#
# Já sabemos representar números e caracteres como bytes. Mas como
# a CPU realmente manipula esses bits internamente, quando faz
# comparações e cálculos?
# =============================================================================


# =============================================================================
# CONTEXTO
# =============================================================================
#
# Até agora tratamos bits apenas como uma forma de representar
# números. Mas a CPU também consegue operar diretamente sobre eles,
# comparando um bit contra o outro. Essas são as operações bit a
# bit — a forma mais "crua" de processamento que existe.
# =============================================================================

# =============================================================================
# O PROBLEMA
# =============================================================================
#
# Como comparar dois números posição por posição (bit por bit), e
# não como um todo? Isso é útil, por exemplo, para saber se dois
# números compartilham algum bit em comum, ou para combinar
# sinalizadores (flags) dentro de um único byte.
# =============================================================================

# =============================================================================
# A SOLUÇÃO
# =============================================================================
#
# Existem quatro operações fundamentais, e cada uma responde a uma
# pergunta diferente sobre os bits comparados:
#
# • AND (&) → o bit resultado é 1 somente se os DOIS bits forem 1.
# • OR  (|) → o bit resultado é 1 se PELO MENOS UM bit for 1.
# • XOR (^) → o bit resultado é 1 se os bits forem DIFERENTES.
# • NOT     → inverte cada bit (já vimos isso com inverter_bits).
#
# Python já implementa essas operações nativamente com os
# operadores &, | e ^ — não precisamos reescrevê-las manualmente.
# Nosso papel aqui é entender o que cada uma representa.
# =============================================================================

# =============================================================================
# IMPLEMENTAÇÃO
# =============================================================================
#
# As operações em si já existem na linguagem (&, |, ^). O código
# abaixo apenas as aplica e traduz o resultado de volta para binário,
# para conseguirmos visualizar o que aconteceu bit a bit.
# =============================================================================

a = 204
b = 170
binario_a = para_binario(a)
binario_b = para_binario(b)

resultado_and = a & b
resultado_or = a | b
resultado_xor = a ^ b
resultado_not_a = inverter_bits(a)

binario_and = para_binario(resultado_and)
binario_or = para_binario(resultado_or)
binario_xor = para_binario(resultado_xor)
binario_not_a = para_binario(resultado_not_a)

# =============================================================================
# DEMONSTRAÇÃO
# =============================================================================

print("\n\n" + "=" * 60)
print("OPERAÇÕES BIT A BIT — COMO A CPU REALMENTE OPERA")
print("=" * 60)

print(f"\na = {a} em decimal = {binario_a} em binário")
print(f"b = {b} em decimal = {binario_b} em binário")

print(f"\na   = {binario_a}")
print(f"b   = {binario_b}")
print("      --------")
print(f"AND = {binario_and} ({resultado_and})  ← 1 onde OS DOIS são 1")

print(f"\na   = {binario_a}")
print(f"b   = {binario_b}")
print("      --------")
print(f"OR  = {binario_or} ({resultado_or})  ← 1 onde ALGUM é 1")

print(f"\na   = {binario_a}")
print(f"b   = {binario_b}")
print("      --------")
print(f"XOR = {binario_xor} ({resultado_xor})  ← 1 onde SÃO DIFERENTES")

print(f"\na   = {binario_a}")
print("      --------")
print(f"NOT = {binario_not_a} ({resultado_not_a})  ← cada bit inverteu")

# =============================================================================
# O QUE APRENDEMOS
# =============================================================================
#
# • AND, OR, XOR e NOT operam bit a bit, não no número como um todo.
# • Essas operações são a base de máscaras de memória, flags e,
#   futuramente, de cálculos de endereço.
# =============================================================================

# =============================================================================
# PRÓXIMA ETAPA
# =============================================================================
#
# Além de comparar bits, também é possível "empurrar" todos os bits
# de um número para os lados. O que acontece quando fazemos isso?
# =============================================================================


# =============================================================================
# CONTEXTO
# =============================================================================
#
# Multiplicar ou dividir por 2 é uma operação tão comum para a CPU
# que existe um atalho direto em nível de bits para fazer isso: os
# operadores de deslocamento (shift).
# =============================================================================

# =============================================================================
# O PROBLEMA
# =============================================================================
#
# Multiplicar e dividir por potências de 2 usando os operadores
# aritméticos comuns (* e /) funciona, mas não mostra o que
# realmente acontece dentro da CPU. Existe uma forma de enxergar
# essa multiplicação/divisão acontecendo bit a bit?
# =============================================================================

# =============================================================================
# A SOLUÇÃO
# =============================================================================
#
# Sim — são os operadores de shift:
#
# • << (shift para a esquerda) empurra todos os bits para a
#   esquerda, preenchendo com 0 à direita. Cada posição deslocada
#   equivale a multiplicar por 2.
#
# • >> (shift para a direita) empurra todos os bits para a
#   direita. Cada posição deslocada equivale a dividir por 2
#   (descartando o resto).
#
# Como nossos números estão limitados a 8 bits (1 byte), aplicamos
# uma máscara (& 0xFF) depois do shift para a esquerda, garantindo
# que o resultado não "vaze" para além do 8º bit.
# =============================================================================

# =============================================================================
# IMPLEMENTAÇÃO
# =============================================================================

c = 10
binario_c = para_binario(c)

resultado_shift_esque_1 = (c << 1) & 0xFF  # desloca 1 posição p/ esquerda (× 2)
resultado_shift_esque_2 = (c << 2) & 0xFF  # desloca 2 posições p/ esquerda (× 4)
resultado_shift_esque_3 = (c << 3) & 0xFF  # desloca 3 posições p/ esquerda (× 8)
resultado_shift_dire_1 = c >> 1            # desloca 1 posição p/ direita (÷ 2)
resultado_shift_dire_2 = c >> 2            # desloca 2 posições p/ direita (÷ 4)
resultado_shift_dire_3 = c >> 3            # desloca 3 posições p/ direita (÷ 8)

binario_shift_esque_1 = para_binario(resultado_shift_esque_1)
binario_shift_esque_2 = para_binario(resultado_shift_esque_2)
binario_shift_esque_3 = para_binario(resultado_shift_esque_3)
binario_shift_dire_1 = para_binario(resultado_shift_dire_1)
binario_shift_dire_2 = para_binario(resultado_shift_dire_2)
binario_shift_dire_3 = para_binario(resultado_shift_dire_3)

# =============================================================================
# DEMONSTRAÇÃO
# =============================================================================

print(f"\nc      = {binario_c} ({c})")
print(f"c << 1 = {binario_shift_esque_1} ({resultado_shift_esque_1})  ← multiplicou por 2")
print(f"c << 2 = {binario_shift_esque_2} ({resultado_shift_esque_2})  ← multiplicou por 4")
print(f"c << 3 = {binario_shift_esque_3} ({resultado_shift_esque_3})  ← multiplicou por 8")
print(f"c >> 1 = {binario_shift_dire_1} ({resultado_shift_dire_1})   ← dividiu por 2")
print(f"c >> 2 = {binario_shift_dire_2} ({resultado_shift_dire_2})    ← dividiu por 4")
print(f"c >> 3 = {binario_shift_dire_3} ({resultado_shift_dire_3})    ← dividiu por 8")

# =============================================================================
# O QUE APRENDEMOS
# =============================================================================
#
# • Shift para a esquerda equivale a multiplicar por 2 (por posição).
# • Shift para a direita equivale a dividir por 2 (por posição).
# • Isso é exatamente o mecanismo que vamos usar mais para frente
#   para separar e reconstruir os 4 bytes de um número inteiro
#   maior (int32) dentro da nossa memória simulada.
# =============================================================================

# =============================================================================
# PRÓXIMA ETAPA
# =============================================================================
#
# Agora que sabemos ler e manipular bits e bytes com confiança,
# estamos prontos para a próxima pergunta do livro:
#
#     Como representar uma região de memória utilizando Python?
#
# Essa pergunta abre a Semana 1 — Parte 2.
# =============================================================================

print("\n" + "=" * 60)
print("  Semana 1 - Parte 1 completa!")
print("  Você entende como bits e bytes funcionam por dentro.")
print("=" * 60)