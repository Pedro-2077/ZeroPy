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


# =============================================================================
# CONTEXTO (continuação — controle de espaço livre)
# =============================================================================
#
# Só criar a memória não basta. Precisamos também saber, desde o
# início, quanto dela está livre — porque, no mundo real, quando o
# Python cria um objeto, ele não pede pro programador escolher o
# endereço na mão. Alguém dentro do Python decide isso sozinho.
#
# Esse "alguém" é o alocador — a parte do sistema responsável por
# decidir onde cada novo dado vai morar dentro da memória.
#
# Para o alocador tomar essa decisão, ele precisa de uma informação
# básica: quais partes da memória já estão ocupadas e quais ainda
# estão livres.
# =============================================================================
 
# =============================================================================
# O PROBLEMA (continuação)
# =============================================================================
#
# Imagine uma memória de 16 bytes, totalmente vazia.
#
# Se pedirmos um espaço de 4 bytes para um "objeto A", onde ele deve
# ser colocado?
#
# E se, logo depois, pedirmos mais 6 bytes para um "objeto B"?
#
# O alocador precisa responder a estas perguntas:
#
# • Quanto da memória ainda está livre?
#
# • Onde exatamente começa cada pedaço livre?
#
# • Depois de reservar um pedaço para o objeto A, como o alocador
#   "lembra" que aquele espaço não está mais disponível?
#
# Sem alguma forma de rastrear isso, o alocador correria o risco de
# entregar o mesmo endereço para dois objetos diferentes — o que
# faria um deles sobrescrever o outro.
# =============================================================================
 
# =============================================================================
# A SOLUÇÃO (continuação)
# =============================================================================
#
# A ideia é simples: manter uma lista com todos os pedaços de
# memória que ainda estão livres. Essa lista é chamada de free list.
#
# Cada item dessa lista guarda duas informações:
#
# • em que endereço aquele pedaço livre começa;
# • quantos bytes esse pedaço livre tem.
#
# No começo, antes de qualquer alocação, a memória inteira é um
# único pedaço livre. Para uma memória de 16 bytes, a free list
# começaria assim:
#
#     [(0, 16)]
#
# Ou seja: "existe um único bloco livre, começando no endereço 0,
# com 16 bytes de tamanho".
#
# Quando o alocador reserva espaço para o objeto A (4 bytes), esse
# bloco livre muda: os primeiros 4 bytes passam a pertencer ao
# objeto A, e o restante continua livre, mas agora começando em um
# endereço diferente:
#
# (4, 12)
# │   │
# │   └── tamanho: 12 bytes de espaço livre
# └────── início: começa no endereço 4
#
# "Sobrou um bloco livre, começando no endereço 4, com 12 bytes."
#
# Repare que a free list não guarda os dados em si — ela só guarda
# a contabilidade de onde há espaço disponível. É um mapa da
# memória, não a memória.


# =============================================================================
# CONTEXTO
# =============================================================================
#
# Agora temos uma memória e uma free list que sabe, corretamente,
# que a memória inteira está livre.
#
# Mas isso ainda não resolve nada sozinho. Ter o mapa não é o mesmo
# que usá-lo.
#
# Precisamos agora da peça que realmente decide onde um novo objeto
# vai morar: o alocador.
# =============================================================================

# =============================================================================
# O PROBLEMA
# =============================================================================
#
# Imagine que pedimos 4 bytes para um "objeto A".
#
# A free list atual é: [(0, 16)] — um único bloco livre, de 16 bytes,
# começando no endereço 0.
#
# O alocador precisa:
#
# • encontrar, dentro da free list, algum bloco livre que seja
#   grande o suficiente para caber os 4 bytes pedidos;
#
# • decidir em qual endereço exato o objeto vai começar;
#
# • atualizar a free list, para que aquele espaço não seja
#   entregue de novo para outro objeto no futuro.
#
# E se existir mais de um bloco livre na free list? Qual deles o
# alocador deveria escolher primeiro?
# =============================================================================

# =============================================================================
# A SOLUÇÃO
# =============================================================================
#
# Existem várias estratégias possíveis para escolher qual bloco
# livre usar. A mais simples de todas — e a que vamos usar aqui —
# se chama first-fit ("primeiro que serve").
#
# A ideia é direta: percorremos a free list em ordem, e assim que
# encontramos o primeiro bloco livre com tamanho suficiente, usamos
# ele. Não procuramos o bloco "perfeito" nem o "melhor" — só o
# primeiro que já resolve o pedido.
#
# (Existem outras estratégias, como best-fit — escolher o menor
# bloco que ainda serve, reduzindo desperdício — e worst-fit, mas
# cada uma tem seus próprios custos e complicações. Ficaremos com
# first-fit por ser a mais simples de entender primeiro.)
#
# Depois de encontrar o bloco certo, dois casos podem acontecer:
#
# • o bloco tem exatamente o tamanho pedido → ele é removido
#   inteiro da free list, pois não sobra nada livre ali;
#
# • o bloco é maior do que o pedido → sobra um resto livre, que
#   continua na free list, mas agora começando em um endereço mais
#   à frente (o antigo início + o tamanho que acabamos de reservar).
#
# Por exemplo: se a free list é [(0, 16)] e pedimos 4 bytes, o
# objeto vai para o endereço 0, e a free list passa a ser [(4, 12)]
# — sobrou um bloco livre menor, começando logo depois do espaço
# que acabamos de entregar.
#
#
# ------------------------------------------------------------------
# Um novo problema: e quando formos liberar esse espaço depois?
# ------------------------------------------------------------------
#
# Vamos seguir o exemplo passo a passo.
#
# Antes de alocar:
#
#     free_list = [(0, 16)]
#
# Depois de alocar 4 bytes para o objeto A:
#
#     free_list = [(4, 12)]
#
# Agora imagine que, mais tarde, alguém pede: "libere o que está no
# endereço 0".
#
# Pergunta: quantos bytes devem ser devolvidos? 1? 4? 10?
#
# Olhando só para a free_list atual — [(4, 12)] — não tem como
# responder. Ela só descreve o endereço 4 em diante. Os endereços
# 0, 1, 2 e 3 simplesmente não aparecem mais em lugar nenhum: eles
# não estão na free list (porque não estão livres), e também não
# guardamos, em nenhum outro lugar, que eles pertencem ao objeto A
# com tamanho 4.
#
# Ou seja: sabemos ONDE o objeto A começa (endereço 0), mas
# perdemos a informação de QUANTO ele ocupa.
#
#
# ------------------------------------------------------------------
# A solução: guardar as alocações em um registro separado
# ------------------------------------------------------------------
#
# A ideia é simples: toda vez que alocamos algo, também anotamos
# essa alocação em um dicionário, associando o endereço inicial ao
# tamanho reservado.
#
# Depois de alocar o objeto A (4 bytes, a partir do endereço 0),
# esse registro ficaria assim:
#
#     alocacoes = {
#         0: 4
#     }
#
# Ou seja: "no endereço 0, existem 4 bytes reservados".
#
# Agora, quando alguém pedir para liberar o endereço 0, basta
# consultar esse dicionário: `alocacoes[0]` responde imediatamente
# "4 bytes" — e agora sim sabemos exatamente quanto devolver para
# a free list.
#
#
# Por que esse registro é indispensável (e não apenas conveniente)
# ------------------------------------------------------------------
#
# Sem ele, olhando só para os bytes 0, 1, 2 e 3 ocupados, seria
# impossível saber o que realmente está ali. Poderia ser:
#
#     Cenário 1 — um único objeto de 4 bytes:
#
#         alocacoes = { 0: 4 }
#
#     Cenário 2 — dois objetos de 2 bytes cada, alocados em
#     momentos diferentes:
#
#         alocacoes = { 0: 2, 2: 2 }
#
# Fisicamente, os bytes ocupados (0 a 3) são os mesmos nos dois
# casos — mas são situações completamente diferentes. Sem o
# registro de alocações guardando cada entrada separadamente, não
# haveria como distinguir um cenário do outro.
#
# No fim, passamos a manter dois registros com propósitos
# diferentes:
#
#     free_list   → o que ainda está disponível para uso
#     alocacoes   → o que já foi entregue, e o tamanho de cada entrega
#
# Isso resolve o problema de "quanto liberar" — mas o "como
# liberar" ainda é uma pergunta em aberto, que vamos deixar para um
# capítulo futuro.
#

# =============================================================================
# CONTEXTO (continuação — devolvendo espaço para a memória)
# =============================================================================
#
# Já sabemos alocar espaço. Mas um objeto não fica na memória para
# sempre — em algum momento ele deixa de ser usado, e o espaço que
# ele ocupava deveria poder ser reaproveitado por outra coisa.
#
# Sem essa capacidade, a memória só cresceria em uso, nunca
# diminuiria — até esgotar.
# =============================================================================
 
# =============================================================================
# O PROBLEMA (continuação)
# =============================================================================
#
# Imagine o estado atual da nossa memória de 16 bytes, depois de
# alocar o objeto A (4 bytes) e o objeto B (6 bytes):
#
#     free_list = [(10, 6)]
#     alocacoes = {0: 4, 4: 6}
#
# Agora alguém decide que não precisa mais do objeto A, e pede:
# "libere o endereço 0".
#
# O que precisa acontecer?
#
# • Precisamos descobrir quanto espaço esse endereço ocupava —
#   e é exatamente para isso que criamos o dicionário de alocações.
#
# • Depois, esse espaço precisa voltar a fazer parte da free list,
#   para que possa ser usado de novo no futuro.
#
# Mas surge uma pergunta nova: o que acontece se o espaço liberado
# for vizinho de um bloco que já estava livre? Eles deveriam virar
# um único bloco maior, ou continuar sendo tratados como dois
# blocos separados?
#
# Vamos visualizar o estado atual da nossa memória de 16 bytes,
# depois de liberar o endereço 0 (objeto A):
#
# +----------------+------------------------+------------------------+
# |     LIVRE      |        OCUPADO         |         LIVRE          |
# +----------------+------------------------+------------------------+
# |  0   1   2   3 |  4   5   6   7   8   9 | 10  11  12  13  14  15 |
# +----------------+------------------------+------------------------+
#
# Repare: os dois blocos livres (0-3 e 10-15) NÃO são vizinhos —
# entre eles existe o objeto B (4-9), ainda ocupado. Então, aqui,
# eles continuam sendo dois blocos separados, mesmo depois de
# liberar: free_list = [(10, 6), (0, 4)].
#
#
# Agora imagine um cenário diferente, onde o objeto B também já
# tivesse sido liberado antes:
#
# +----------------------------------------------------------------+
# |                           TUDO LIVRE                           |
# +----------------------------------------------------------------+
# |  0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15 |
# +----------------------------------------------------------------+
#
# Aqui sim, os blocos são vizinhos — o final de um encosta
# exatamente no início do outro. Tratar isso como dois blocos
# separados, [(0, 10), (10, 6)], seria desperdício: na prática,
# é só um único espaço livre de 16 bytes, e deveria ser registrado
# como tal: free_list = [(0, 16)].
# =============================================================================
 
# =============================================================================
# A SOLUÇÃO (continuação)
# =============================================================================
#
# Quando liberamos uma região da memória, queremos que ela possa ser
# utilizada novamente por futuras alocações.
#
# Para isso, o processo acontece em três etapas.
#
# ---------------------------------------------------------------------------
# 1) Descobrir o tamanho do bloco
# ---------------------------------------------------------------------------
#
# Quando recebemos apenas um endereço:
#
#     liberar(0)
#
# sabemos apenas onde o bloco começa.
#
# Mas quantos bytes devemos devolver para a memória?
#
# É exatamente por isso que existe o dicionário de alocações:
#
#     alocacoes = {
#         0: 4,
#         4: 6
#     }
#
# Consultando esse dicionário descobrimos:
#
#     endereço 0 -> bloco de 4 bytes
#     endereço 4 -> bloco de 6 bytes
#
# Então:
#
#     liberar(0)
#
# significa:
#
#     "libere o bloco que começa no endereço 0
#      e possui 4 bytes."
#
#
# ---------------------------------------------------------------------------
# 2) Remover do registro de alocações
# ---------------------------------------------------------------------------
#
# Depois de descobrir o tamanho, esse bloco deixa de existir como
# memória ocupada.
#
# Antes:
#
#     alocacoes = {
#         0: 4,
#         4: 6
#     }
#
# Depois de liberar(0):
#
#     alocacoes = {
#         4: 6
#     }
#
# Agora esse espaço não pertence mais a ninguém.
#
#
# ---------------------------------------------------------------------------
# 3) Devolver o espaço para a free list
# ---------------------------------------------------------------------------
#
# A free list guarda todas as regiões livres da memória.
#
# Imagine uma memória de 16 bytes.
#
# Antes de liberar:
#
#      0               4          10         16
#      |---------------|-----------|----------|
#      |   ocupado     |  ocupado  |  livre   |
#      |    4 bytes    |  6 bytes  | 6 bytes  |
#      |---------------|-----------|----------|
#
# free_list = [(10, 6)]
#
# Agora chamamos:
#
#     liberar(0)
#
# O bloco de 4 bytes volta a ficar livre.
#
# A memória passa a ser:
#
#      0               4          10         16
#      |---------------|-----------|----------|
#      |    livre      |  ocupado  |  livre   |
#      |    4 bytes    |  6 bytes  | 6 bytes  |
#      |---------------|-----------|----------|
#
# Então adicionamos esse novo espaço na free list:
#
#     free_list = [
#         (10, 6),
#         (0, 4)
#     ]
#
#
# ---------------------------------------------------------------------------
# Mas existe um problema...
# ---------------------------------------------------------------------------
#
# Observe a memória novamente:
#
#      0               4          10         16
#      |---------------|-----------|----------|
#      |    livre      |  ocupado  |  livre   |
#      |    4 bytes    |  6 bytes  | 6 bytes  |
#      |---------------|-----------|----------|
#
# Agora alguém pede:
#
#     alocar(8)
#
# A pergunta que o alocador faz é:
#
# "Existe ALGUM bloco livre com pelo menos 8 bytes?"
#
# Vamos verificar:
#
# primeiro bloco:
#
#     4 >= 8 ?
#
# Não.
#
# segundo bloco:
#
#     6 >= 8 ?
#
# Também não.
#
# Resultado:
#
#     MemoryError
#
# Mesmo existindo:
#
#     4 + 6 = 10 bytes livres
#
# o pedido falha.
#
# Por quê?
#
# Porque esses 10 bytes não estão juntos.
#
# É como tentar estacionar um caminhão de 8 metros usando duas vagas
# separadas de 4 metros cada.
#
# As vagas existem.
#
# O espaço total existe.
#
# Mas ele não é contínuo.
#
#
# Esse problema recebe o nome de fragmentação.
#
# A memória possui espaço suficiente, porém ele está dividido em
# vários pedaços pequenos.
#
#
# ---------------------------------------------------------------------------
# Como resolver? (fica para o próximo capítulo)
# ---------------------------------------------------------------------------
#
# Sempre que um bloco for liberado, verificamos se existe outro bloco
# livre exatamente ao lado dele.
#
# Se existir, juntamos os dois em um bloco maior.
#
# Exemplo:
#
# Antes:
#
#      |----4----|----6----|
#      |  livre  |  livre  |
#
# Depois da fusão:
#
#      |---------10---------|
#      |       livre        |
#
# Assim, um pedido de:
#
#     alocar(8)
#
# passa a funcionar normalmente.
#
# Essa junção dos blocos é chamada de merge (ou coalescência) e é uma
# das técnicas mais importantes de qualquer gerenciador de memória.
#
# Por enquanto, vamos implementar o liberar() SEM a fusão — ele vai
# funcionar corretamente, só que ainda vai sofrer com fragmentação.
# A fusão fica para o próximo capítulo do livro.
#
# Agora que entendemos o bytearray, a free list, o first-fit e como
# liberar espaço, podemos escrever a classe completa.
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
 
    Além disso, guardamos dois registros de controle:
 
    • free_list: lista de tuplas (endereco_inicio, tamanho)
      indicando quais partes da memória ainda estão livres.
 
    • alocacoes: dicionário (endereco_inicio -> tamanho) indicando
      o que já foi reservado, e o tamanho de cada reserva.
    """
 
    # -------------------------------------------------------------------------
    # __init__: cria a região de memória e sua contabilidade de espaço
    # -------------------------------------------------------------------------
    def __init__(self, tamanho_bytes: int):
        """
        __init__()
 
        Pergunta que este método responde:
        Como criamos uma região de memória, já sabendo desde o
        início quanto dela está disponível para uso?
        """
        self._dados = bytearray(tamanho_bytes)  # cria a região de memória, tudo zerado
        self._tamanho = tamanho_bytes           # guarda o tamanho total para consultas futuras
 
        # free_list: lista de tuplas (endereco_inicio, tamanho_do_bloco)
        # No começo, a memória inteira é um único bloco livre.
        self._free_list = [(0, tamanho_bytes)]
 
        # alocacoes: dicionário (endereco_inicio → tamanho reservado)
        # No começo, nada foi alocado ainda.
        self._alocacoes = {}
 
        print(f"Memória criada: {tamanho_bytes} bytes.")
        print(f"Free list inicial: {self._free_list}")
 
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
 
    def ler_byte(self, endereco: int) -> int:
        """
        ler_byte()
 
        Pergunta que este método responde:
        Como descobrir o que está guardado em um endereço específico?
        """
        if endereco < 0 or endereco >= self._tamanho:
            raise IndexError(f"Endereço {endereco} fora do intervalo da memória (0 a {self._tamanho - 1}).")
 
        return self._dados[endereco]
 
    # -------------------------------------------------------------------------
    # ALOCAR: encontra um bloco livre e reserva parte dele
    # -------------------------------------------------------------------------
    def alocar(self, tamanho: int):
        """
        alocar()
 
        Pergunta que este método responde:
        Dado um tamanho pedido, qual endereço da memória devemos
        reservar — e como atualizar a free list para refletir essa
        reserva?
 
        Vamos acompanhar um exemplo do início ao fim.
 
        Estado inicial:
 
            self._free_list = [(0, 4), (10, 6)]
            self._alocacoes = {}
 
        --------------------------------------------------------------
        Chamada 1: mem.alocar(6)
        --------------------------------------------------------------
 
        Como o for percorre a free list:
 
            for i, (inicio, tamanho_do_bloco_livre) in enumerate(self._free_list):
 
            i                      → posição do bloco dentro da free list
            inicio                 → endereço onde esse bloco livre começa
            tamanho_do_bloco_livre → quantos bytes esse bloco tem disponível
 
        1ª volta (bloco 0):
            i                      = 0
            inicio                 = 0
            tamanho_do_bloco_livre = 4
 
            Comparação: tamanho_do_bloco_livre >= tamanho
                        4 >= 6
                        False
 
            Esse bloco NÃO serve (é pequeno demais). O loop não
            entra no if, e passa para o próximo bloco.
 
        2ª volta (bloco 1):
            i                      = 1
            inicio                 = 10
            tamanho_do_bloco_livre = 6
 
            Comparação: tamanho_do_bloco_livre >= tamanho
                        6 >= 6
                        True
 
            Esse bloco vai ser usado. A partir daqui, tudo dentro
            do if vai usar as informações desse bloco para decidir
            onde o objeto será alocado e como a free list deve ser
            atualizada.
 
            endereco = inicio
            endereco = 10
 
        Segunda decisão: o que sobra do bloco?
 
            tamanho_do_bloco_livre == tamanho
            6 == 6 → True
 
            Encaixou perfeitamente: o bloco (10, 6) é removido
            inteiro da free list com self._free_list.pop(1).
 
            free_list agora: [(0, 4)] — é o que sobrou, pois o
            bloco (10, 6) foi consumido por inteiro.
 
        Por fim, a linha que registra a alocação:
 
            self._alocacoes[endereco] = tamanho
            self._alocacoes[10] = 6
 
            alocacoes agora: {10: 6}
 
        O método retorna 10 — esse é o endereço que quem chamou
        alocar() vai usar depois para escrever e ler dados de verdade.
 
        --------------------------------------------------------------
        Chamada 2: mem.alocar(2) — pedido novo
        --------------------------------------------------------------
 
        Estado da free list neste momento: [(0, 4)]
 
        1ª volta (bloco 0):
            i                      = 0
            inicio                 = 0
            tamanho_do_bloco_livre = 4
 
            Comparação: 4 >= 2 → True. Esse bloco serve.
            endereco = inicio = 0
 
        Segunda decisão: o que sobra do bloco?
 
            tamanho_do_bloco_livre == tamanho
            4 == 2 → False
 
            Sobra espaço! Calculamos o resto:
 
                novo_inicio        = inicio + tamanho
                                    = 0 + 2
                                    = 2
 
                novo_tamanho_livre = tamanho_do_bloco_livre - tamanho
                                    = 4 - 2
                                    = 2
 
            O bloco (0, 4) é substituído por (2, 2) na free list
            — o espaço encolheu e passou a começar 2 posições mais
            à frente.
 
            free_list agora: [(2, 2)]
 
        Por fim, a linha que registra a alocação:
 
            self._alocacoes[endereco] = tamanho
            self._alocacoes[0] = 2
 
            alocacoes agora: {10: 6, 0: 2}
 
        Repare que, nos dois casos (bloco removido ou bloco
        encolhido), a linha `self._alocacoes[endereco] = tamanho`
        sempre roda — é ela que garante que, não importa o que
        aconteceu com a free list, sempre saibamos depois quanto
        cada endereço alocado tem reservado.
        """
        for i, (inicio, tamanho_do_bloco_livre) in enumerate(self._free_list):
 
            # se o bloco tem espaço suficiente para o que foi pedido
            if tamanho_do_bloco_livre >= tamanho:
 
                # o objeto começa exatamente onde o bloco começa
                endereco = inicio
 
                # encaixou perfeitamente: não sobra nada livre
                if tamanho_do_bloco_livre == tamanho:
                    self._free_list.pop(i)
                else:
                    novo_inicio = inicio + tamanho
                    novo_tamanho_livre = tamanho_do_bloco_livre - tamanho
                    self._free_list[i] = (novo_inicio, novo_tamanho_livre)
 
                # registra quanto foi reservado nesse endereço
                self._alocacoes[endereco] = tamanho
 
                print(f"Alocar({tamanho}) -> endereço {endereco}")
                return endereco
 
        raise MemoryError(f"Sem espaço livre suficiente para alocar {tamanho} pedido")
 
    # -------------------------------------------------------------------------
    # LIBERAR: devolve um bloco alocado para a free list
    # -------------------------------------------------------------------------
    def liberar(self, endereco: int):
        """
        liberar()
 
        Pergunta que este método responde:
        Dado um endereço já alocado, como devolvemos esse espaço
        para a free list, para que possa ser usado de novo?
 
        Vamos acompanhar um exemplo.
 
        Estado inicial:
 
            self._free_list = [(10, 6)]
            self._alocacoes = {0: 4, 4: 6}
 
        Chamada: mem.liberar(0)
 
        Passo 1 — descobrir o tamanho:
 
            tamanho = self._alocacoes[endereco]
            tamanho = self._alocacoes[0]
            tamanho = 4
 
        Passo 2 — remover do registro de alocações:
 
            del self._alocacoes[endereco]
            del self._alocacoes[0]
 
            alocacoes agora: {4: 6}
 
        Passo 3 — devolver o espaço para a free list:
 
            self._free_list.append((endereco, tamanho))
            self._free_list.append((0, 4))
 
            free_list agora: [(10, 6), (0, 4)]
 
        Repare que, por enquanto, o bloco (0, 4) só é ADICIONADO
        à free list — ele não é fundido com nenhum outro bloco
        vizinho ainda. Essa fusão é o próximo passo do livro, e
        sem ela a memória pode sofrer com fragmentação: um pedido
        de alocar(8), por exemplo, falharia aqui, mesmo havendo
        4 + 6 = 10 bytes livres no total, porque nenhum bloco
        sozinho tem 8 bytes.
        """
        if endereco not in self._alocacoes:
            raise ValueError(f"O endereço {endereco} não está alocado")
 
        tamanho = self._alocacoes[endereco]
        del self._alocacoes[endereco]
 
        self._free_list.append((endereco, tamanho))
 
        print(f"Liberar({endereco}) -> {tamanho} bytes devolvidos")
 
 
# =============================================================================
# DEMONSTRAÇÃO
# =============================================================================
 
mem = Memoria(16)  # cria uma memória de 16 bytes, já com a free list inicial
 
print("\nEscrevendo alguns bytes:")
mem.escrever_byte(0, 65)   # escreve o byte 65 (ASCII 'A') no endereço 0
mem.escrever_byte(1, 66)   # escreve o byte 66 (ASCII 'B') no endereço 1
mem.escrever_byte(2, 255)  # escreve o byte 255 no endereço 2
 
print(f"Endereço 0: {mem.ler_byte(0)}")
print(f"Endereço 1: {mem.ler_byte(1)}")
print(f"Endereço 2: {mem.ler_byte(2)}")
 
print("\nTestando os limites:")
 
try:
    mem.escrever_byte(0, 355)  # inválido: acima de 255
except ValueError as erro:
    print(f"Erro esperado: {erro}")
 
try:
    mem.ler_byte(100)  # inválido: a memória vai só até o endereço 15
except IndexError as erro:
    print(f"Erro esperado: {erro}")
 
print("\nTestando a free_list:")
print(f"Free list após criar a memória: {mem._free_list}")
 
print("\n--- Alocando blocos ---")
 
endereco_a = mem.alocar(4)   # pede 4 bytes para um "objeto A"
print(f"Free list depois de alocar A: {mem._free_list}")
print(f"Alocações: {mem._alocacoes}")
 
endereco_b = mem.alocar(6)   # pede 6 bytes para um "objeto B"
print(f"Free list depois de alocar B: {mem._free_list}")
print(f"Alocações: {mem._alocacoes}")
 
print("\n--- Usando os endereços retornados por alocar() ---")
mem.escrever_byte(endereco_a, 65)   # escreve no espaço reservado para A
valor_lido = mem.ler_byte(endereco_a)
print(f"Endereço {endereco_a} (objeto A) agora contém: {valor_lido}")
 
print("\n--- Liberando o objeto A ---")
mem.liberar(endereco_a)
print(f"Free list depois de liberar A: {mem._free_list}")
print(f"Alocações: {mem._alocacoes}")
 
print("\n--- Testando a fragmentação ---")
print("Mesmo havendo 4 + 6 = 10 bytes livres no total, pedir 8 de")
print("uma vez falha, porque estão em blocos separados:")
try:
    mem.alocar(8)
except MemoryError as erro:
    print(f"Erro esperado: {erro}")
 
# =============================================================================
# O QUE APRENDEMOS
# =============================================================================
#
# • O alocador usa a estratégia first-fit: pega o primeiro bloco
#   livre que já resolve o pedido, sem procurar o "melhor" bloco.
# • Depois de alocar, a free list é atualizada — o bloco usado é
#   removido ou encolhido, dependendo se sobrou espaço ou não.
# • Um registro separado de alocações (endereço → tamanho) é
#   necessário porque a free list sozinha não guarda informação
#   sobre o que já foi entregue — só sobre o que ainda está livre.
# • Alocar reserva espaço, mas não escreve nada nele automaticamente
#   — escrever é um passo separado, usando o endereço retornado.
# • Liberar consulta o dicionário de alocações para descobrir o
#   tamanho, remove o registro de lá, e devolve o espaço à free list.
# • Sem fundir blocos vizinhos, a memória sofre com fragmentação:
#   pode haver espaço livre suficiente no total, mas espalhado
#   demais para atender um pedido maior.
# =============================================================================
 
# =============================================================================
# PRÓXIMA ETAPA
# =============================================================================
#
# Já sabemos alocar e liberar, mas o liberar() atual não funde
# blocos vizinhos — ele só adiciona o espaço de volta à free list,
# sem verificar se algum bloco ao lado também está livre.
#
# Como detectamos que dois blocos são vizinhos? E como unimos os
# dois em um único bloco maior, resolvendo o problema da
# fragmentação que acabamos de ver?
#
# Essa pergunta abre o próximo capítulo: a fusão de blocos (merge).
# =============================================================================
 
print("\n" + "=" * 60)
print("  Semana 1 - Parte 2 (até o liberar, sem fusão) completa!")
print("=" * 60)