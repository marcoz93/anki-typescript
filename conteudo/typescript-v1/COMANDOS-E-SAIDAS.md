# Conteúdo da escada: comandos, saídas e limites

Rodada de 27/11/2026. Ambiente Linux x86_64 desta sessão, não o Mac do usuário. Repositório preparado em uma árvore de trabalho isolada a partir de `83a1aff2c794fb74dc83857eb3b6c444a3335c81`.

## 1. Ambiente e base

Comandos executados na raiz da árvore de trabalho:

```bash
git rev-parse HEAD
node -p 'process.version'
node -p 'require("/workspace/scratch/66d296bb0a09/mathua-review/cmd/typescript-pilot/node_modules/typescript").version'
```

Saídas, na mesma ordem:

```text
83a1aff2c794fb74dc83857eb3b6c444a3335c81
v24.22.3
5.9.3
```

O caminho absoluto identifica a instalação do TypeScript utilizada nesta sessão. Ele não é um requisito de instalação. Para reproduzir em outra máquina, aponte `--typescript` para a pasta do pacote TypeScript 5.9.3 instalado pelo piloto.

## 2. Gerar os dados a partir do conteúdo fixo

Comando executado:

```bash
python3 conteudo/typescript-v1/scripts/gerar-conteudo.py
```

Saída, código de saída 0:

```json
{
  "generated": {
    "stages": 15,
    "concepts": 46,
    "families": 74,
    "cases": 444
  },
  "skills": {
    "semantico": 20,
    "construtivo": 30,
    "diagnostico": 8,
    "interpretativo": 13,
    "seletivo": 3
  }
}
```

O gerador lê as 74 linhas de cartões, ignorando os quatro cabeçalhos do TSV. Cada cartão é ligado a uma família. Os dados do gerador são editoriais e determinísticos: esse comando não inventa perguntas nem chama um serviço de IA.

## 3. Conferir estrutura, compilação e gabaritos

Comando executado:

```bash
node conteudo/typescript-v1/scripts/verificar-conteudo.cjs --typescript /workspace/scratch/66d296bb0a09/mathua-review/cmd/typescript-pilot/node_modules/typescript
```

Saída final, código de saída 0:

```json
{
  "passed": true,
  "environment": {
    "platform": "linux",
    "arch": "x64",
    "node": "v24.22.3",
    "typescript": "5.9.3"
  },
  "counts": {
    "stages": 15,
    "concepts": 46,
    "families": 74,
    "cases": 444,
    "distinct_questions": 444,
    "compiled_files": 403,
    "code_answers": 180,
    "diagnostic_cases": 48,
    "choice_cases": 126,
    "interpreted_answers": 72,
    "type_queries": 6,
    "function_boundary_assertions": 78,
    "integrated_assertions": 9
  },
  "errors": []
}
```

O resultado completo está em [evidencias/validacao.json](evidencias/validacao.json).

### O alcance de cada contagem

| Campo | O que foi confrontado com um critério |
| --- | --- |
| `stages`, `concepts`, `families`, `cases` | Quantidades, IDs únicos, ligação entre cartões e famílias, aulas presentes, ausência de ciclos e ausência de pré-requisito de um degrau posterior |
| `distinct_questions` | Seis pares distintos de enunciado e contexto por família; mudar somente ID ou posição de alternativa não conta |
| `compiled_files` | 403 unidades de código: contextos e gabaritos combinados quando aplicável, além do programa integrado; verificação com `strict: true` |
| `code_answers` | 180 modelos de resposta de construção, seis para cada uma das 30 famílias, sem diagnóstico inesperado de compilação |
| `diagnostic_cases` | 48 contextos deliberadamente incorretos, seis por cada uma das oito famílias diagnósticas, com o diagnóstico esperado |
| `choice_cases` | 126 questões de escolha com quatro alternativas distintas e uma resposta marcada; é verificação estrutural, não avaliação automática de toda a semântica dos distratores |
| `interpreted_answers` | 66 respostas de valor ou contagem e seis seleções de ramo, comparadas à execução ou à leitura da chamada apresentada |
| `type_queries` | Seis tipos de resultado de `find`, consultados no verificador de tipos e comparados ao gabarito |
| `function_boundary_assertions` | 78 comparações de resultados de funções: extração de quantia, positividade, classificação no limite e tratamento de ausência |
| `integrated_assertions` | Cinco valores apresentados pelo programa original, três casos na fronteira da regra e um caso de ausência |

Essas contagens se sobrepõem. Não some as colunas para anunciar uma quantidade de testes independentes. Compilar o modelo não demonstra que um corretor futuro aceitará todas as soluções válidas de alunos.

## 4. Falha encontrada e correção

A primeira execução do verificador terminou com código 1. Seu registro está em [evidencias/validacao-antes-da-correcao.json](evidencias/validacao-antes-da-correcao.json).

O único erro registrado foi a resposta de tipo de F070-V2. O código inicial era:

```ts
const ids = ["r21", "r22"];
const found = ids.find((id) => id === "r22");
```

O gabarito dizia `string | undefined`. O TypeScript 5.9.3 consultado pelo verificador inferiu `"r22" | undefined`:

```text
tipo de find F070-V2
+ actual - expected
  [
+   '"r22"',
-   'string',
    'undefined'
  ]
```

O conteúdo foi corrigido tornando explícito o retorno booleano da condição:

```ts
const ids = ["r21", "r22"];
const found = ids.find((id): boolean => id === "r22");
```

A consulta passou a corresponder ao gabarito `string | undefined`, e a segunda rodada passou. Isso mantém a tarefa dentro da explicação de tipos gerais do exercício. As [notas oficiais do TypeScript 5.5](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-5.html#inferred-type-predicates) explicam as condições para inferir um predicado de tipo, incluindo a ausência de uma anotação explícita de retorno.

## 5. Preservação das fontes

O verificador compara o SHA-256 dos arquivos preservados aos valores registrados em `curriculo.json`. Valores conferidos:

```text
anki_typescript_v1.tsv
4288391e8f6a49266a82b75d0615dc61be8baa42f513128fed1feae2893f3ac7

reembolsos.ts
fc0670be7674b43817c9177aeeb5da00997f833c96ceb03a52b5d954b88df577
```

## 6. O que esta rodada não verifica

Os arquivos de conteúdo não foram integrados ao aplicativo nesta entrega. Não foram repetidos testes do servidor, da tela, do navegador, de reinício ou da suíte geral do Mathua. As evidências anteriores desses testes continuam separadas no diretório do piloto.

As explicações e os distratores foram redigidos e revisados editorialmente; o programa não demonstra que toda formulação será clara para todo aluno. Também não mede retenção, domínio, equivalência de dificuldade das variantes nem calibração por relatos reais. Essas propriedades exigem evidência da utilização e revisão do material.

O verificador executa somente os gabaritos confiáveis do repositório. Seu uso de `vm` não é uma proposta de isolamento para respostas arbitrárias de alunos. A integração deve respeitar o mecanismo de correção e seus limites no piloto.
