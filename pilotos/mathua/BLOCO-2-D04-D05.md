# Bloco 2: degraus D04 e D05 integrados ao piloto

Data da execução: 27/11/2026, America/Sao_Paulo. Ambiente: macOS 26.4.1 arm64, no Mac do usuário.

Ponto de partida: commit `3d1fdc4` deste repositório, que entregou o bloco 1. O registro do bloco 1 está em [BLOCO-1-D01-D03.md](BLOCO-1-D01-D03.md) e explica como o conteúdo se liga ao motor do Mathua. Este documento registra só o que mudou no bloco 2.

Quem fez o quê: os corretores foram escritos pelo assistente principal. Um segundo agente (Claude Opus, esforço alto) escreveu os testes de critério com a ordem de achar defeitos, e achou quatro. Um falseador externo (Codex, somente leitura) revisou a entrega depois; o resultado dele está na seção 7.

## 1. Conteúdo que entrou

O piloto passou a servir os degraus 1 a 5: **23 conceitos, 25 famílias e 150 casos**. Mensagem do servidor na partida:

```text
Content typescript-escada-v1 from <repositório>/conteudo/typescript-v1: stages 1 to 5, 23 concepts, 25 families, 150 cases, every model answer accepted by its grader
```

Entraram neste bloco 10 conceitos, 11 famílias e 66 casos:

| Degrau | Conceito | Pré-requisitos | Família e formato |
| --- | --- | --- | --- |
| D04 | `ts.expression.value` | `ts.value.literal_notation`, `ts.binding.const_number` | F015, alternativas |
| D04 | `ts.expression.greater_than` | `ts.binding.const_number`, `ts.type.boolean`, `ts.expression.value` | F016, código; F017, resultado |
| D04 | `ts.expression.strict_equality` | `ts.binding.const_string`, `ts.type.boolean`, `ts.expression.value` | F018, código |
| D04 | `ts.expression.boolean_and` | `ts.type.boolean`, `ts.binding.const_semantics`, `ts.expression.value` | F019, código |
| D04 | `ts.expression.boolean_not` | `ts.type.boolean`, `ts.binding.const_semantics`, `ts.expression.value` | F020, código |
| D05 | `ts.data.object` | `ts.binding.const_number`, `ts.binding.const_string` | F021, código |
| D05 | `ts.data.property` | `ts.data.object` | F022, código |
| D05 | `ts.data.array` | `ts.binding.const_number` | F023, código |
| D05 | `ts.data.array_index` | `ts.data.array` | F024, resultado |
| D05 | `ts.data.binding_vs_property` | `ts.data.object`, `ts.data.property`, `ts.binding.const_semantics` | F025, alternativas |

Os arquivos de conteúdo lidos são os mesmos do bloco 1. Os resumos SHA-256 estão em [ambiente.txt](evidencias/bloco-2-d04-d05/ambiente.txt).

## 2. O que mudou no código

Só arquivos do piloto, em `cmd/typescript-pilot/`:

- `grade.cjs`: sete corretores de código novos (F016, F018, F019, F020, F021, F022, F023) e o corretor do formato de resultado, `value`, para número e booleano. A resposta de código agora é verificada pelo compilador depois do código de contexto que a pergunta mostra.
- `content.go`: `integratedThroughStage` passou de 3 para 5.
- `main_test.go`: três funções de teste novas e três casos novos no teste do bloco 1.
- `README.md`: escopo e tabela de critérios.

O teste de navegador, em `scripts/browser-smoke.mjs`, ganhou um passo para o degrau 4.

Nenhum código existente do Mathua mudou neste bloco. Medido: `git diff --stat -- web internal` → os mesmos 14 arquivos, 162 linhas adicionadas e 110 removidas do bloco 1. A interface não foi recompilada.

O patch atual tem 22 arquivos, 2667 linhas adicionadas e 110 removidas. Resumo SHA-256: `655cb649282f2efa7dc45d452ac24e0948ad3669e4e83a533e366b242938ad8e`.

## 3. O que os corretores novos aceitam

| Família | Aceita | Recusa |
| --- | --- | --- |
| F016 comparação `>` | `amount > 10000`, `10000 < amount`, parênteses, `10_000` | `>=`, a comparação no sentido oposto, outro nome, outro limite |
| F018 igualdade `===` | operandos em qualquer ordem, aspas simples ou duplas | `=`, `==`, outro nome, outro texto |
| F019 conjunção `&&` | operandos em qualquer ordem | `\|\|`, `&`, um nome só |
| F020 negação `!` | `!isValid`, `!(isValid)` | o nome sozinho, a dupla negação |
| F021 objeto | propriedades em qualquer ordem, chave entre aspas, parênteses | array, propriedade a mais, a menos ou com outro valor |
| F022 propriedade | `refund.amount`, `refund["amount"]` | outra propriedade, outro objeto |
| F023 array | os elementos na ordem pedida | outra ordem, elemento diferente ou repetido |
| F017 e F024 resultado | `true`, `false`, `15000`, `15_000` | o valor entre aspas, a própria expressão do contexto |
| F015 e F025 alternativas | a letra da alternativa correta | outra alternativa |

O corretor não executa o código do aluno. Os comentários `@ts-ignore`, `@ts-expect-error` e `@ts-nocheck` são neutralizados antes da verificação de tipos.

## 4. Comandos executados e saídas

Todos os arquivos citados estão em [evidencias/bloco-2-d04-d05/](evidencias/bloco-2-d04-d05/). Os comandos Go rodam na raiz do clone do Mathua, com Node `24.14.1`.

```sh
go vet ./cmd/typescript-pilot
go build -o pilot-bin ./cmd/typescript-pilot
go test -json ./cmd/typescript-pilot -count=1
go test -json ./internal/server -run 'Test(Practice_|StudyAnswer_|MyReports|AdminReport|Report)' -count=1
go test -json ./internal/mastery ./internal/scheduler ./internal/repair -count=1
```

| Evidência | Código | Aprovados | Falhas |
| --- | --- | --- | --- |
| [mathua-pilot.jsonl](evidencias/bloco-2-d04-d05/mathua-pilot.jsonl) | 0 | 435 casos finais | 0 |
| [mathua-native-http.jsonl](evidencias/bloco-2-d04-d05/mathua-native-http.jsonl) | 0 | 26 casos finais | 0 |
| [mathua-native-engine.jsonl](evidencias/bloco-2-d04-d05/mathua-native-engine.jsonl) | 0 | 154 casos finais | 0 |

Os 435 casos do piloto, por função de teste:

| Função | Casos | O que confere |
| --- | --- | --- |
| `TestTypeScriptCriteria` | 49 | Critérios do bloco 1, com três casos novos de parênteses |
| `TestCriteriaOfStagesFourAndFive` | 170 | Respostas aceitas e recusadas de F015 a F025, com a mensagem em parte dos casos |
| `TestCriteriaHoldInEveryCaseOfStagesFourAndFive` | 204 | As equivalências do contrato aplicadas aos 6 casos de cada família, cada um com o próprio contexto |
| `TestWholeLadderThroughTheAPI` | 1 | Um visitante novo domina os 23 conceitos pela API real, em ordem, com 6 perguntas distintas por conceito |
| `TestPilotHTTP` | 7 | Pré-requisitos, domínio, variante após erro, repetição, relato, reinício e falha do corretor |
| Outras quatro funções | 4 | Conteúdo servido, seções por família, alternativas por letra e reparo de histórico |

```sh
python3 scripts/process-smoke.py --mathua ./mathua --output evidencias/bloco-2-d04-d05/mathua-process-script.json
node scripts/browser-smoke.mjs --mathua ./mathua --output evidencias/bloco-2-d04-d05/mathua-browser-smoke.json --screenshots evidencias/bloco-2-d04-d05/capturas
```

Reinício: código 0, `passed: true`. Navegador: código 0, `passed: true`, 23 verificações, 10 capturas, `page_errors: []`, `api_errors: []`.

## 5. O que foi observado pela tela no degrau 4

As 16 verificações do bloco 1 continuam passando. As 7 novas, em [mathua-browser-smoke.json](evidencias/bloco-2-d04-d05/mathua-browser-smoke.json):

| Verificação | Valor observado |
| --- | --- |
| `mastery_through_browser_ts.value.boolean_literal` | 6 respostas, 6 casos distintos, `MASTERED` |
| `mastery_through_browser_ts.type.boolean` | 6 respostas, 6 casos distintos, `MASTERED` |
| `mastery_through_browser_ts.binding.const_number` | 4 respostas a mais, `MASTERED` |
| `mastery_through_browser_ts.expression.value` | 6 respostas por toque na alternativa, `MASTERED` |
| `stage_4_prerequisites_mastered_through_browser` | `ts.expression.greater_than` ficou disponível, com os três pré-requisitos atendidos |
| `greater_than_section_1_miss_names_cause_then_variant_accepts_limit_first` | Erro em F016-V3 com `quantity >= 20000`. A tela mostrou "A tarefa pede estritamente maior. Os operadores >= e <= também aceitam a igualdade." A variante foi F016-V4, e a forma `800 < requestedValue` foi aceita |
| `greater_than_section_2_value_miss_then_same_family_variant` | Erro em F017-V0, contexto `10000 > 10000`, resposta `true`. A tela mostrou "A expressão produz o outro valor booleano." A variante foi F017-V1, da mesma família |

Capturas novas: [09-secao-1-comparacao-recusada.png](evidencias/bloco-2-d04-d05/capturas/09-secao-1-comparacao-recusada.png) e [10-secao-2-valor-recusado.png](evidencias/bloco-2-d04-d05/capturas/10-secao-2-valor-recusado.png).

## 6. Defeitos achados e corrigidos neste bloco

Os quatro primeiros foram achados pelo segundo agente, com testes que tentam respostas-limite. O quinto é a mesma classe do segundo, em famílias do bloco 1.

1. **Comentário que desliga o compilador fazia uma anotação errada passar (F021, F023).** `// @ts-ignore` antes de `const refund: { id: number; amount: number } = { id: "r1", amount: 15000 };` era aceito. O contrato proíbe supressões de erro. Agora os três comentários são neutralizados antes de compilar, para todas as famílias.
2. **Parênteses válidos eram recusados (F021, F023).** `const refund = ({ id: "r1", amount: 15000 });` e `const amounts = [(15000), 5000, 10000];` eram recusados. Agora são aceitos.
3. **A mensagem de F016 culpava a igualdade quando a comparação estava no sentido oposto.** `amount <= 10000` mostrava a mensagem sobre `>=`. Agora mostra "A comparação não verifica se amount é estritamente maior que 10000."
4. **A mensagem de F023 dizia "outra ordem" para um elemento repetido.** `[15000, 15000, 10000]` agora mostra "O array tem um elemento diferente do solicitado."
5. **Parênteses em F010 e F011, do bloco 1.** `const amount = (15000);` era recusado. Medido antes da correção: "Inicialize a constante com um literal numérico, sem aspas e sem operações." Agora é aceito, e `const amount = (10000 + 5000);` continua recusado.

Cada defeito tem um teste com nome próprio, por exemplo `f021_ts_ignore_does_not_hide_wrong_annotation` e `number_const_parenthesized_literal`.

## 7. Verificação por falseador

Preenchida depois da revisão do Codex. Ver a seção "Falseador" ao fim deste documento.

## 8. Decisões de interpretação do contrato que ficaram em aberto

Nenhum destes casos tem asserção nos testes. O comportamento atual está indicado. A decisão é de quem escreve o conteúdo.

| Caso | Comportamento atual | Leitura A | Leitura B |
| --- | --- | --- | --- |
| `as const` em F021 e F023 | Recusa, com a mensagem "Inicialize a constante com um objeto", que é imprecisa | Aceitar: a asserção acrescenta e não substitui a construção | Recusar com mensagem que cite a asserção |
| Anotação `any` em F021 e F023 | Aceita | Aceitar: a tarefa não pede um tipo | Recusar: o contrato lista `any` como inaceitável |
| `refund?.amount` em F022 | Recusa | Aceitar: o resultado é o mesmo | Recusar com mensagem que cite o `?.` |
| Crase no lugar de aspas, em F018 e F022 | Recusa, como em F003 | Manter: o contrato fala em aspas simples ou duplas | Aceitar: o texto é o mesmo |
| Outras notações de número, como `1e4` e `0x2710` | Aceita | Aceitar qualquer literal de mesmo valor | Aceitar só a notação decimal |
| Conta no lugar do valor em F021, como `amount: 10000 + 5000` | Recusa, com a mensagem "não tem o valor solicitado", que é imprecisa | Aceitar: o dado é 15000 | Recusar com mensagem "sem operações" |
| `isSigned === true && hasPages === true` em F019 | Recusa, com mensagem imprecisa | Manter: o critério é `&&` entre os dois booleanos | Aceitar: o resultado é equivalente |

Um problema no próprio conteúdo, que não foi alterado: o campo `counterexample` de F019 em `exercicios.json` está quebrado. Ele tem `answer: "isSigned "` e `reason: "| hasPages|A disjunção…"`. Parece um `||` cortado na separação de colunas do arquivo de origem.

## 9. Limites desta verificação

- **Só macOS e só Chromium `151.0.7922.34`.**
- **Interface.** Os testes unitários, o lint e a compilação da interface não foram repetidos, porque nenhum arquivo de `web/next-app` mudou neste bloco.
- **Suíte geral.** `go test ./...` e o pacote `internal/server` inteiro não foram repetidos, porque nenhum arquivo de `internal/` mudou neste bloco.
- **Conceitos percorridos pela tela.** O navegador percorreu 9 dos 23 conceitos. Os 23 foram dominados pela API real no teste `TestWholeLadderThroughTheAPI`.
- **Tempo de partida.** Medido uma vez: 14,3 segundos com 23 conceitos. O Mathua confere cada gerador em um processo separado. Com 46 conceitos, a partida fica mais lenta.
- **Teste de navegador.** Passou nas execuções gravadas. Não foi medido se ele falha às vezes sem motivo.
- **Formato de resultado.** O corretor `value` cobre número e booleano. Texto, array e `undefined` pertencem a degraus posteriores e hoje resultam em "não avaliado".
- Continuam valendo os limites do bloco 1 sobre Linux, banco de versão anterior, dados do relato e revisão do relato pela tela.
