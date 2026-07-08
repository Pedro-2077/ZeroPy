print('=' * 60)
print('BITS E BYTES - A BASE DE TUDO')
print('=' * 60)


# ----------------------------------------------------------------------------
# FUNÇÃO DE CONVERTER UM NUMERO DECIMAL PARA BINÁRIO MANUALMENTE
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
        return '0' * largura # Caso o numero seja zero nós vamos retornar uma string de zeros com a largura especificada ou a default que é 8.
    
    restos = []
    n = numero

    # Refatorando o código para usar um while loop para coletar os restos da divisão por 2.
    # O nome é divisão sucessiva por 2, e é o método tradicional de conversão de decimal para binário, consequimos ver esse exemplo logo no início.

    #Caso o número seja maior que 0, vamos continuar dividindo por 2 e coletando os restos.
    while n > 0:

        #Utilizamos o metodo append de todo objeto do tipo lista para adicionar o resto da divisão por 2 na lista de restos.
        restos.append(n % 2)  # Coletando o resto da divisão por 2.
        n //= 2  # Dividindo o número por 2 e atualizando o valor de n.


    # Inverte a lista, pois os restos foram coletados do último bit para o primeiro
    restos_invertidos = reversed(restos)

    # Converte a lista de restos invertidos em uma string binária
    bits = []

    for bit in restos_invertidos:
        bits.append(str(bit)) # Convertendo cada bit para o tipo primitivo string e adicionando na lista de bits.
    
    # Junta os bits em uma única string
    binario = ''.join(bits)

    # Adicionando o zero a esquerda para completar a largura especificada
    return binario.zfill(largura)  # zfill adiciona zeros à esquerda para completar a largura especificada.


# ==================== Testando a função para_binario ==========================

print('\n Numeros de 0 a 20 em binário (8 bits):')

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

def  para_decimal(binario_str):
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

    #Estamos pegando cada bit da string e pegando o indice de cada bit 
    for i, bit in enumerate(binario_str):
        
        #Se o bit for igual 1 nos fazemos o calculo da potencia de 2 como vimos no exemplo acima, porem caso seja 0 não fazemos nada pois o resultado da multiplicação será 0 e não afetará o total.
        if bit == '1':
            """
            Exemplo do que acontece abaixo:
            
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

print('\n Números binários em decimal:')

lista = ['00000000', '00000001', '00000010', '00000011', '00000100',
         '00000101', '00000110', '00000111', '00001000', '00001001', '00001010', '00001011', '00001100',
         '00001101', '00001110', '00001111', '00010000', '00010001', '00010010', '00010011', '00010100']

for binario in lista:
    decimal = para_decimal(binario)
    print(f'{binario} em binário = {decimal} em decimal')


# -----------------------------------------------------------------------------
# ASCII — Como letras viram números
# -----------------------------------------------------------------------------
# A tabela ASCII associa cada caractere a um inteiro de 0 a 127.
# ord('A') retorna o código ASCII. chr(65) retorna 'A'.

            
