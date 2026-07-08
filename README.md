# ZeroPy — Criando o Python do Zero

> Do transistor ao interpretador. Cada camada construída à mão, sem atalhos.

**[→ Ver apresentação completa](https://pedro-2077.github.io/ZeroPy/)**

Python parece mágica até você ver o que está por baixo. Este projeto desce todas as camadas — bits, bytes, memória, CPU, objetos, compilador — até construir um interpretador funcional do zero.

Não usamos `bin()`, não importamos parsers prontos, não chamamos `eval()`. Cada peça é implementada para entender exatamente o que acontece por baixo.

---

## Roadmap

### Nível 0 — Hardware

| Arquivo | Conteúdo | Status |
|---|---|---|
| `v1_bits_e_bytes.py` | Binário, ASCII, UTF-8, operações bit a bit | ✅ Completo |
| `v2_memoria.py` | Simulador de RAM com alocador e free list | 🔜 Em breve |
| `v3_alu.py` | Unidade Lógico-Aritmética com flags ZF/SF/CF/OF | 🔜 Em breve |
| `v4_cpu.py` | CPU com ciclo Fetch-Decode-Execute | 🔜 Em breve |
| `v6_assembly.py` | Assembler: texto legível → bytecodes | 🔜 Em breve |
| `v7_hello_assembly.py` | Hello World no hardware que construímos | 🔜 Em breve |

### Nível 1 — Objetos

| Arquivo | Conteúdo | Status |
|---|---|---|
| `v1_pyobject.py` | PyObject, reference counting, INCREF/DECREF | 🔜 Em breve |
| `v2_tipos.py` | PyLong, PyUnicode, PyList internamente | 🔜 Em breve |
| `v3_dict.py` | Hash table implementada do zero | 🔜 Em breve |

### Nível 2 — Frontend

| Arquivo | Conteúdo | Status |
|---|---|---|
| `v1_lexer.py` | Tokenizador: código-fonte → tokens | 🔜 Em breve |
| `v2_parser.py` | AST: tokens → árvore sintática | 🔜 Em breve |

### Nível 3 — Compilador

| Arquivo | Conteúdo | Status |
|---|---|---|
| `v1_compilador.py` | Caminha a AST e gera bytecodes | 🔜 Em breve |

### Nível 4 — Máquina Virtual

| Arquivo | Conteúdo | Status |
|---|---|---|
| `v1_vm.py` | Eval loop: executa bytecodes | 🔜 Em breve |
| `v2_frames.py` | Call stack, frames e escopo de variáveis | 🔜 Em breve |

### Nível 5 — Avançado

| Arquivo | Conteúdo | Status |
|---|---|---|
| `v1_gc.py` | Garbage collector com detecção de ciclos | 🔜 Em breve |
| `v2_builtins.py` | `print`, `len`, `range` implementados à mão | 🔜 Em breve |

---

## Estrutura de pastas

```
zeroPy/
├── nivel_0_hardware/    ← bits, memória, ALU, CPU, assembler
├── nivel_1_objetos/     ← PyObject, tipos primitivos, dicionário
├── nivel_2_frontend/    ← lexer, parser, árvore sintática
├── nivel_3_compilador/  ← geração de bytecodes
├── nivel_4_vm/          ← máquina virtual, call stack
├── nivel_5_avancado/    ← GC, builtins, módulos
└── programas/           ← programas .zpy rodando no interpretador
```

---

## Como rodar

Nenhuma dependência externa. Python 3.10+ é suficiente.

```bash
# Semana 1 — Bits e Bytes
python nivel_0_hardware/v1_bits_e_bytes.py
```

---

## Por que construir à mão?

`bin(10)` retorna `'0b1010'`. Mas por quê? Como funciona internamente?

Escrever a função você mesmo — dividindo por 2, coletando restos, invertendo — transforma isso de resposta decorada em conhecimento real. O mesmo vale para cada camada.

Quem entende o que o interpretador faz não tropeça no que Python "faz por baixo" — porque já viu o pano.

---

## Tecnologias

- **Python 3.10+** — a ferramenta usada para construir o interpretador
- **ZeroPy (.zpy)** — a linguagem que está sendo criada

---

*Projeto em desenvolvimento ativo. Novos módulos adicionados semanalmente.*
