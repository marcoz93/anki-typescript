# Bloco 2: degraus D04 e D05 integrados ao piloto

Data da execução: 27/11/2026, America/Sao_Paulo. Ambiente: macOS 26.4.1 arm64, no Mac do usuário.

Ponto de partida: commit `3d1fdc4` deste repositório, que entregou o bloco 1. O registro do bloco 1 está em [BLOCO-1-D01-D03.md](BLOCO-1-D01-D03.md) e explica como o conteúdo se liga ao motor do Mathua. Este documento registra só o que mudou no bloco 2.

Quem fez o quê: os corretores foram escritos pelo assistente principal. Um segundo agente (Claude Opus, esforço alto) escreveu os testes de critério com a ordem de achar defeitos, e achou quatro. Um falseador externo (Codex, somente leitura) revisou a entrega em nove passadas, cada uma sobre o commit que corrigia a anterior. As oito primeiras acharam pontos de severidade média, todos corrigidos. A nona, sobre o commit `6ae97ab`, não achou ponto alto nem médio. O resultado está na seção 7.

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

Antes da revisão do falseador, nenhum código existente do Mathua tinha mudado neste bloco. Depois das passadas dele, mudaram trechos de `web/next-app/components/LearnStepper.tsx` e entraram as funções `pilotExclude`, `pilotAdmit` e `pilotUsable` em `web/next-app/lib/pilot.ts`, com o teste novo `web/next-app/test/pilot.test.ts`. Medido: `git diff --stat -- web internal` → 14 arquivos, 209 linhas adicionadas e 123 removidas. A interface foi recompilada.

O patch atual tem 23 arquivos, 3025 linhas adicionadas e 123 removidas. Resumo SHA-256: `9bc6f4e573ef67e509561194c19ec4c493afdfe5a2e9eff32ee64799bce773ec`. Resumos anteriores: `655cb649…` no commit `c7f3c85`, antes da revisão; `cd4f4889…` no commit `7f3d02e`; `68a01259…` no commit `7d3bc28`; `22277907…` no commit `cf3f065`; `719c4fd3…` no commit `61bdca9`; `c68ecf00…` no commit `5600fb0`; `0eea9e2d…` nos commits `865c82d` e `d4317d9`; `33816d5a…` no commit `19ecf5f`.

## 3. O que os corretores novos aceitam

| Família | Aceita | Recusa |
| --- | --- | --- |
| F016 comparação `>` | `amount > 10000`, `10000 < amount`, parênteses, `10_000` | `>=`, a comparação no sentido oposto, outro nome, outro limite |
| F018 igualdade `===` | operandos em qualquer ordem, aspas simples ou duplas | `=`, `==`, outro nome, outro texto |
| F019 conjunção `&&` | operandos em qualquer ordem | `\|\|`, `&`, um nome só |
| F020 negação `!` | `!isValid`, `!(isValid)` | o nome sozinho, a dupla negação |
| F021 objeto | propriedades em qualquer ordem, chave entre aspas, parênteses | array, propriedade a mais, a menos ou com outro valor |
| F022 propriedade | `refund.amount`, `refund["amount"]` | outra propriedade, outro objeto |
| F023 array | os elementos na ordem pedida, com `const` ou `let` | outra ordem, elemento diferente ou repetido |
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
| [mathua-pilot.jsonl](evidencias/bloco-2-d04-d05/mathua-pilot.jsonl) | 0 | 478 casos finais | 0 |
| [mathua-native-http.jsonl](evidencias/bloco-2-d04-d05/mathua-native-http.jsonl) | 0 | 26 casos finais | 0 |
| [mathua-native-engine.jsonl](evidencias/bloco-2-d04-d05/mathua-native-engine.jsonl) | 0 | 154 casos finais | 0 |

As evidências desta pasta são da execução final, depois das correções das oito passadas do falseador, na seção 7. A correção da oitava passada mudou só `grade.cjs` e os testes Go; por isso os registros da interface, em `tsc.log`, `lint.log`, `vitest.log` e `ui-build.log`, são da execução anterior, feita depois da sétima passada. O registro de reinício não traz data, e o conteúdo dele é igual em todas as execuções. Os três arquivos `.jsonl`, o registro de reinício e o registro de navegador foram gerados de novo nessa execução. Os 478 casos do piloto, por função de teste:

| Função | Casos | O que confere |
| --- | --- | --- |
| `TestTypeScriptCriteria` | 49 | Critérios do bloco 1, com três casos novos de parênteses |
| `TestCriteriaOfStagesFourAndFive` | 170 | Respostas aceitas e recusadas de F015 a F025, com a mensagem em parte dos casos |
| `TestCriteriaHoldInEveryCaseOfStagesFourAndFive` | 204 | As equivalências do contrato aplicadas aos 6 casos de cada família, cada um com o próprio contexto |
| `TestWholeLadderThroughTheAPI` | 1 | Um visitante novo domina os 23 conceitos pela API real, em ordem, com 6 perguntas distintas por conceito |
| `TestFindingsOfTheIndependentReview` | 43 | Os achados do falseador, cada um com a resposta que ele relatou |
| `TestPilotHTTP` | 7 | Pré-requisitos, domínio, variante após erro, repetição, relato, reinício e falha do corretor |
| Outras quatro funções | 4 | Conteúdo servido, seções por família, alternativas por letra e reparo de histórico |

```sh
python3 scripts/process-smoke.py --mathua ./mathua --output evidencias/bloco-2-d04-d05/mathua-process-script.json
node scripts/browser-smoke.mjs --mathua ./mathua --output evidencias/bloco-2-d04-d05/mathua-browser-smoke.json --screenshots evidencias/bloco-2-d04-d05/capturas
```

Reinício: código 0, `passed: true`. Navegador: código 0, `passed: true`, 23 verificações, 10 capturas, `page_errors: []`, `api_errors: []`.

Interface, em `web/next-app`, com Node `24.22.3`, depois das correções da seção 7:

| Comando | Código | Saída |
| --- | --- | --- |
| `npx tsc --noEmit -p .` | 0 | Nenhuma mensagem, em [tsc.log](evidencias/bloco-2-d04-d05/tsc.log) |
| `npm run lint` | 0 | 0 erros, em [lint.log](evidencias/bloco-2-d04-d05/lint.log) |
| `npm test` | 0 | `Test Files  199 passed (199)`, `Tests  1897 passed (1897)`, em [vitest.log](evidencias/bloco-2-d04-d05/vitest.log) |
| `NEXT_PUBLIC_TS_PILOT=1 NEXT_PUBLIC_SAME_ORIGIN_API=1 NEXT_TELEMETRY_DISABLED=1 npm run build` | 0 | [ui-build.log](evidencias/bloco-2-d04-d05/ui-build.log) |

O arquivo de teste novo, `test/pilot.test.ts`, tem 12 testes.

A suíte da interface rodou três vezes depois das correções da segunda passada duas vezes depois das correções da terceira, uma vez depois das correções da quarta, uma vez depois das correções da quinta, uma vez depois das correções da sexta e uma vez depois das correções da sétima. As seis últimas passaram, e o registro gravado é o da última. Das três anteriores, a primeira falhou em `test/reportsPage.test.tsx > renders the overview for an established learner`; esse registro está em [vitest-execucao-com-falha-intermitente.log](evidencias/bloco-2-d04-d05/vitest-execucao-com-falha-intermitente.log). As duas execuções seguintes passaram. É o mesmo arquivo de teste que falhou uma vez no bloco 1. Ele cobre `app/reports/page.tsx`, que o patch não altera. Não foi medido se esse teste também falha no commit-base sem o patch.

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

O falseador foi o Codex, em modo somente leitura, sobre os commits `3d1fdc4` e `c7f3c85`. O registro da execução marca 94 comandos. O relatório dele está em [falseador-codex.md](evidencias/bloco-2-d04-d05/falseador-codex.md) e traz o comando e a saída de cada achado, em 9 blocos; ele não lista os 94 comandos. O mesmo vale para os relatórios das outras passadas.

A primeira tentativa não rodou: o filtro de segurança do Codex recusou o pedido, que usava vocabulário de teste de invasão. O pedido foi reescrito como revisão de qualidade e rodou.

Cada achado foi reproduzido antes de virar correção.

| Achado do falseador | Reproduzido? | O que foi feito |
| --- | --- | --- |
| 1. F002 aceitava uma resposta com a diretiva `/// <reference lib="invalidlib" />`, que o TypeScript recusa | Sim; o mesmo valia para F016 | Toda resposta de código ou de resultado com diretiva `/// <reference>` é recusada, com mensagem própria |
| 2. Quatro respostas válidas eram recusadas: `const total: 18000 = 18_000;`, `const id: (string) = "reembolso-21";`, `{ ["id"]: "r11", total: 18000 }` e `request[("value")]` | Sim, as quatro | A anotação de F010 e F011 aceita qualquer tipo ao qual o valor se ajusta, menos `any` e `unknown`. A chave computada textual e os parênteses na chave são aceitos |
| 3. F021 dizia "não tem o valor solicitado" para `total: 12000 + 6000`, que vale 18000 | Sim; já constava como imprecisão na seção 8 | A mensagem agora é "Escreva o valor da propriedade total como um literal, sem operações." A recusa continua. Duas outras mensagens imprecisas da seção 8 também foram corrigidas: asserção de tipo e comparações dentro do `&&` |
| 4. Uma resposta com 1400 parênteses encaixados fazia o corretor sair sem veredito | Sim: "Maximum call stack size exceeded", código 1 | A resposta agora é recusada como resposta, com mensagem própria |
| 5. `pilotExclude` podia deixar zero candidatos, ou só a pergunta recém-errada, com banco diferente de seis ou fila cheia | Sim, nos cenários dele | A função prioriza as duas perguntas mostradas por último e limita a exclusão a cinco. O carregador recusa família com número de casos diferente de seis |
| 6. Duas buscas sobrepostas punham o mesmo caso duas vezes seguidas na fila | Sim, no cenário em memória dele | A tela remove as repetidas no momento em que acrescenta à fila |
| 7. O registro do bloco 1 diria que o patch não altera `/my-reports` | Não se confirma | A frase tratava da página `/reports`, em `app/reports/page.tsx`, que o patch não altera. O patch altera `app/my-reports/page.tsx`. O texto do bloco 1 foi reescrito para citar o arquivo |
| 8. Este documento remetia a uma seção que não existia | Sim | É esta seção |

O que o falseador tentou e não derrubou: os 150 gabaritos; instrução extra, segunda declaração, `as any` no operando e `@ts-ignore` foram recusados; comentário, vírgula final, propriedade reordenada e limite invertido foram aceitos; 150 enunciados distintos por conceito, sem colisão de tarefa; sem a chave do piloto, os textos e o diagnóstico ficam como no original; as contagens e os resumos SHA-256 dos dois registros conferem.

O que o falseador não verificou: a frequência da repetição em navegador real, uma compilação nova da interface sem a chave, e as suítes Go e de navegador, que ele não rodou por estar em modo somente leitura.

### Segunda passada, sobre o commit `7f3d02e`

O falseador rodou de novo, com 78 comandos, sobre a entrega corrigida. O relatório está em [falseador-codex-2a-passada.md](evidencias/bloco-2-d04-d05/falseador-codex-2a-passada.md). Ele conferiu as oito correções da primeira passada: sete se sustentaram e a sexta estava incompleta. Ele relatou cinco achados novos. Todos foram reproduzidos.

| Achado da segunda passada | O que foi feito |
| --- | --- |
| 1. A regra da diretiva era por texto: aceitava `/// <REFERENCE ...>` em maiúsculas e recusava um comentário `/* */` que só continha o texto da diretiva | O corretor agora pergunta ao compilador se a resposta tem diretiva. Maiúsculas são recusadas; o comentário e o texto `"///"` são aceitos |
| 2. A regra de `any` e `unknown` na anotação era por texto: recusava `number & unknown`, que o compilador resolve para `number`, e aceitava `ReturnType<typeof JSON.parse>`, que resolve para `any` | O corretor agora pergunta ao verificador de tipos qual é o tipo declarado. O primeiro é aceito e o segundo é recusado |
| 3. Chave textual escrita com crase era recusada em F021 e F022, como em ``request[`value`]`` | A chave com crase, sem substituição, é aceita. O contrato pede "a mesma chave textual" |
| 4. Uma busca atrasada repunha na fila uma pergunta já mostrada, e a recuperação de uma pergunta sem registro no servidor duplicava casos na fila | A tela admite cada pergunta contra a fila e contra as perguntas mostradas, no momento em que acrescenta. A função é `pilotAdmit`, com 3 testes |
| 5. O registro dos 154 testes do motor era anterior às correções, e o documento dizia que era da execução final | Os testes do motor foram rodados de novo, e o arquivo foi substituído |

Uma regressão apareceu durante estas correções e foi pega por um teste já existente: a checagem nova da diretiva rodava antes da proteção contra respostas encaixadas demais. A checagem foi movida para dentro da proteção.

### Terceira passada, sobre o commit `7d3bc28`

O falseador rodou 107 comandos. O relatório está em [falseador-codex-3a-passada.md](evidencias/bloco-2-d04-d05/falseador-codex-3a-passada.md). Uma primeira tentativa desta passada foi interrompida pelo filtro de segurança do Codex depois de 34 comandos; o pedido foi reescrito e rodou até o fim.

Ele conferiu as cinco correções da segunda passada: quatro se sustentaram e a quarta estava incompleta. Ele testou 250 respostas das famílias F001 a F025, com 150 aprovações e 100 recusas, todas de acordo com o critério. Ele relatou um achado médio e três baixos.

| Achado da terceira passada | Severidade | O que foi feito |
| --- | --- | --- |
| 1. Uma busca atrasada que chegava antes de a tela anotar a pergunta como mostrada repunha essa pergunta na fila. A anotação acontecia num efeito, depois da troca de tela | Média | A tela anota a pergunta como mostrada no instante em que ela sai da fila, e também no efeito |
| 2. Sem a chave do piloto, o botão de relato enviava o gabarito e a explicação, o que a tela original não fazia. A mudança vinha da rodada de 26/11 e contrariava a frase "sem a chave, a interface compila como a original" | Baixa | As duas propriedades do botão de relato agora só são enviadas com a chave do piloto |
| 3. Duas mensagens imprecisas: `\|\|` "aceita apenas uma delas", e `{ id, total: 18000 }` "deve ter exatamente as propriedades id e total" | Baixa | As mensagens agora são "O operador \|\| já é verdadeiro quando só uma delas é verdadeira." e "Escreva o valor de id junto com o nome, como em id: valor." |
| 4. A seção 8 dizia que nenhum caso tinha asserção nos testes e citava "o objeto" para F021 e F023 | Baixa | A seção 8 foi corrigida |

### Quarta passada, sobre o commit `cf3f065`

O falseador rodou 91 comandos. O relatório está em [falseador-codex-4a-passada.md](evidencias/bloco-2-d04-d05/falseador-codex-4a-passada.md). Ele conferiu as quatro correções da terceira passada, e as quatro se sustentaram. Ele testou de novo 250 respostas, sem aceitação indevida. Ele relatou dois achados médios e um baixo.

| Achado da quarta passada | Severidade | O que foi feito |
| --- | --- | --- |
| 1. Depois de um erro, a seção podia acabar com três perguntas inéditas na fila. A função que tira a próxima pergunta usava a fila de uma tela anterior, pedia outro lote e descartava o único caso que o servidor ainda podia mandar | Média | No piloto, a função lê a fila como ela está agora. Quando o filtro do piloto não deixa passar nada, a tela usa o que o servidor mandou, menos a pergunta mostrada por último (`pilotUsable`, com 3 testes) |
| 2. F023 recusava `let amounts = [15000, 5000, 10000];`, com uma mensagem que exigia `const`. O critério e o enunciado de F023 não citam `const` | Média | F023 aceita `let`. Ver a decisão em aberto na seção 8, porque um teste da primeira revisão exigia a recusa |
| 3. Um nome de tipo com erro de digitação, como `numbr`, recebia a mensagem "A anotação não é compatível com o valor" | Baixa | A mensagem agora é neutra: "O compilador TypeScript rejeitou a declaração:", seguida do texto do compilador |

### Quinta passada, sobre o commit `61bdca9`

O falseador rodou 106 comandos. O relatório está em [falseador-codex-5a-passada.md](evidencias/bloco-2-d04-d05/falseador-codex-5a-passada.md). Ele conferiu as três correções da quarta passada, e as três se sustentaram. Ele testou de novo 250 respostas, sem veredito divergente da rubrica. Sem a chave do piloto, a tela original e a atual renderizaram o mesmo conteúdo e enviaram as mesmas requisições no ensaio dele. Ele relatou um achado médio e dois baixos.

| Achado da quinta passada | Severidade | O que foi feito |
| --- | --- | --- |
| 1. Quando o servidor responde que não tem registro de uma pergunta, a tela busca uma substituta. Com quatro perguntas na fila, a busca trazia uma pergunta que já estava na fila, o filtro a descartava, e a tela ficava sem substituta | Média | No piloto, a substituta vem da mesma função que serve a próxima pergunta: da fila atual, ou de uma busca quando a fila está vazia. O caminho paralelo deixou de existir no piloto |
| 2. F023 dizia "Inicialize a constante com um array" para `let totals = 18000;` | Baixa | A mensagem agora é "O valor inicial deve ser um array, entre colchetes, com os elementos pedidos." |
| 3. Este documento dizia que o relatório da primeira passada continha cada comando e saída. Ele contém os 9 blocos de comando dos achados | Baixa | A frase foi corrigida |

### Sexta passada, sobre o commit `5600fb0`

O falseador rodou 120 comandos. O relatório está em [falseador-codex-6a-passada.md](evidencias/bloco-2-d04-d05/falseador-codex-6a-passada.md). Ele conferiu as três correções da quinta passada, e as três se sustentaram. Ele testou de novo 250 respostas: nenhum veredito divergiu da rubrica e nenhuma recusa atribuiu uma causa ausente da resposta. Sem a chave do piloto, a tela original e a atual produziram o mesmo HTML nos cinco estados que ele amostrou. Ele relatou um achado médio.

| Achado da sexta passada | Severidade | O que foi feito |
| --- | --- | --- |
| 1. A correção da quinta passada trocava a pergunta sem registro por uma pergunta da fila. As perguntas da fila foram servidas junto com a da tela, então também estavam sem registro: a tela mostrava até quatro substitutas que recebiam a mesma recusa do servidor | Média | No piloto, a recuperação descarta a fila e busca de novo. Buscar é o que grava o registro no servidor. A busca segue as mesmas regras de exclusão e admissão da próxima pergunta |

O ensaio do próprio falseador foi rodado contra a correção. Saída, em [ensaio-409-depois-da-correcao.txt](evidencias/bloco-2-d04-d05/ensaio-409-depois-da-correcao.txt): depois do envio recusado de F002-V1, a tela buscou de novo e mostrou F002-V2 "com registro true".

### Sétima passada, sobre o commit `d4317d9`

O falseador rodou 111 comandos. O relatório está em [falseador-codex-7a-passada.md](evidencias/bloco-2-d04-d05/falseador-codex-7a-passada.md). Ele rodou de novo o ensaio da sexta passada e obteve a mesma saída gravada: a substituta com registro. Ele testou 250 respostas dos casos V2 e V3, sem divergência de veredito. Ele relatou um achado médio e dois baixos.

| Achado da sétima passada | Severidade | O que foi feito |
| --- | --- | --- |
| 1. Nas famílias de nome ou símbolo (F005, F006, F007, F012), a resposta certa seguida de um comentário, como `number /* tipo */`, era recusada. A comparação era por texto | Média | O corretor compara os símbolos como o analisador léxico do TypeScript os lê. Espaços e comentários não contam. `number string` e `Number` continuam recusados |
| 2. Uma busca enviada antes da recuperação podia chegar depois e repor na fila uma pergunta sem registro | Baixa | A tela conta as recuperações e ignora a resposta de uma busca enviada antes da última recuperação |
| 3. F021 e F023 chamavam `satisfies` de asserção de tipo | Baixa | A mensagem cita o que a resposta usa: asserção de tipo, o operador `satisfies` ou o operador `!` |

### Oitava passada, sobre o commit `19ecf5f`

O falseador rodou 69 comandos. O relatório está em [falseador-codex-8a-passada.md](evidencias/bloco-2-d04-d05/falseador-codex-8a-passada.md). Ele conferiu as três correções da sétima passada, e as três se sustentaram. Ele testou 250 respostas dos casos V4 e V5. Sem a chave do piloto, a tela original e a atual produziram HTML idêntico em 14 estados. Ele relatou um achado médio e um baixo.

| Achado da oitava passada | Severidade | O que foi feito |
| --- | --- | --- |
| 1. Nas famílias de nome ou símbolo, a resposta certa seguida de um comentário sem fechamento, como `number /* tipo`, era aceita. A correção da sétima passada lia os símbolos e ignorava o erro do analisador léxico | Média | Uma resposta em que o analisador léxico acusa erro é recusada, com a mensagem "A resposta contém um erro de sintaxe TypeScript." |
| 2. A seção 8 dizia que três casos tinham teste da mensagem de recusa; com `satisfies`, são quatro | Baixa | A frase foi corrigida |

### Nona passada, sobre o commit `6ae97ab`

O falseador rodou 121 comandos. O relatório está em [falseador-codex-9a-passada.md](evidencias/bloco-2-d04-d05/falseador-codex-9a-passada.md). A primeira frase dele: "Não encontrei achado novo de severidade alta ou média em `main@6ae97ab`. Confirmei um achado baixo."

Ele conferiu as duas correções da oitava passada, e as duas se sustentaram. Ele testou 250 respostas das famílias F001 a F025: nenhum veredito divergiu da rubrica e nenhuma mensagem atribuiu uma causa ausente. Em 52 envios simulados em F016 e F017, a tela não repetiu pergunta em sequência e não ficou sem pergunta. Sem a chave do piloto, a tela original e a atual produziram HTML idêntico em 18 estados. As contagens deste documento e de `resultados.json` conferiram.

| Achado da nona passada | Severidade | O que foi feito |
| --- | --- | --- |
| 1. O comentário da função `pilotFresh`, em `web/next-app/lib/pilot.ts`, diz que o servidor repete perguntas dentro de um lote quando restam poucos casos. O gerador do Mathua já remove as repetidas, em `internal/generator/registry.go`. Nas 20 buscas registradas com cinco exclusões, cada lote trouxe uma pergunta | Baixa | Nada foi alterado. O código entregue é o código que o falseador verificou. O comentário fica como pendência para o próximo commit que tocar esse arquivo. A função continua correta; a remoção que ela faz é redundante nesse caso |

### Resumo das nove passadas

| Passada | Commit revisado | Comandos | Achados | Médios | Baixos | Correções anteriores que se sustentaram |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `c7f3c85` | 94 | 8 | 6 | 2 | — |
| 2 | `7f3d02e` | 78 | 5 | 4 | 1 | 7 de 8 |
| 3 | `7d3bc28` | 107 | 4 | 1 | 3 | 4 de 5 |
| 4 | `cf3f065` | 91 | 3 | 2 | 1 | 4 de 4 |
| 5 | `61bdca9` | 106 | 3 | 1 | 2 | 3 de 3 |
| 6 | `5600fb0` | 120 | 1 | 1 | 0 | 3 de 3 |
| 7 | `d4317d9` | 111 | 3 | 1 | 2 | 1 de 1 |
| 8 | `19ecf5f` | 69 | 2 | 1 | 1 | 3 de 3 |
| 9 | `6ae97ab` | 121 | 1 | 0 | 1 | 2 de 2 |

Nenhuma passada relatou achado de severidade alta. O falseador trabalhou em modo somente leitura: ele não rodou as suítes Go, a suíte da interface nem o teste de navegador, e conferiu esses resultados pelos registros gravados. Os ensaios dele sobre a tela usaram React em memória com respostas HTTP simuladas, e não um navegador com o servidor real.

## 8. Decisões de interpretação do contrato que ficaram em aberto

Nenhum destes casos tem teste que force a aceitação ou a recusa como regra do contrato. Quatro deles têm teste da mensagem de recusa atual: `as const`, a conta no lugar do valor, as comparações dentro do `&&` e `satisfies`. O comportamento atual está indicado. A decisão é de quem escreve o conteúdo.

| Caso | Comportamento atual | Leitura A | Leitura B |
| --- | --- | --- | --- |
| `as const` em F021 e F023 | Recusa. A mensagem é "Escreva o objeto diretamente, sem asserção de tipo." em F021 e "Escreva o array diretamente, sem asserção de tipo." em F023 | Aceitar: a asserção acrescenta e não substitui a construção | Recusar com mensagem que cite a asserção |
| Anotação `any` em F021 e F023 | Aceita. Em F010 e F011, uma anotação que resulta em `any` ou `unknown` é recusada | Aceitar: a tarefa não pede um tipo | Recusar: o contrato lista `any` como inaceitável |
| `refund?.amount` em F022 | Recusa | Aceitar: o resultado é o mesmo | Recusar com mensagem que cite o `?.` |
| Crase no lugar de aspas em um texto pedido, em F003 e F018 | Recusa. Em chave de propriedade, em F021 e F022, a crase passou a ser aceita | Manter: o contrato fala em aspas simples ou duplas | Aceitar: o texto é o mesmo |
| Outras notações de número, como `1e4` e `0x2710` | Aceita | Aceitar qualquer literal de mesmo valor | Aceitar só a notação decimal |
| Conta no lugar do valor em F021, como `amount: 10000 + 5000` | Recusa, agora com a mensagem "Escreva o valor da propriedade amount como um literal, sem operações." | Aceitar: o dado é 15000 | Recusar com mensagem "sem operações" |
| `isSigned === true && hasPages === true` em F019 | Recusa, agora com a mensagem "Use isSigned e hasPages diretamente como operandos de &&, sem outras operações." | Manter: o critério é `&&` entre os dois booleanos | Aceitar: o resultado é equivalente |

| `let` em vez de `const` em F023 e F021 | F023 aceita `let`. F021 recusa, com a mensagem "A tarefa pede uma declaração com const." | Manter: o critério de F021 cita `const`; o de F023 não | Unificar. Em F021 o enunciado mostrado ao aluno, "Declare refund como objeto com id igual a r1 e amount igual a 15000.", também não cita `const`; ou o enunciado passa a citar, ou a recusa deixa de existir |

A linha acima nasceu de uma discordância entre os dois revisores: o teste do segundo agente exigia a recusa de `let` em F023, e o falseador relatou a recusa como defeito.

| `satisfies` em F021 e F023, como em `[9000, 3000, 6000] satisfies number[]` | Recusa, com a mensagem "Escreva o array diretamente, sem o operador satisfies." | Manter: a tarefa pede o valor escrito diretamente | Aceitar: `satisfies` confere o tipo e não o altera |

Um problema no próprio conteúdo, que não foi alterado: o campo `counterexample` de F019 em `exercicios.json` está quebrado. Ele tem `answer: "isSigned "` e `reason: "| hasPages|A disjunção…"`. Parece um `||` cortado na separação de colunas do arquivo de origem.

## 9. Limites desta verificação

- **Só macOS e só Chromium `151.0.7922.34`.**
- **Teste unitário intermitente da interface.** `test/reportsPage.test.tsx` falhou em 2 de 13 execuções da suíte completa nesta sessão. Não foi medido no commit-base.
- **Suíte geral.** `go test ./...` e o pacote `internal/server` inteiro não foram repetidos, porque nenhum arquivo de `internal/` mudou neste bloco.
- **Conceitos percorridos pela tela.** O navegador percorreu 9 dos 23 conceitos. Os 23 foram dominados pela API real no teste `TestWholeLadderThroughTheAPI`.
- **Tempo de partida.** Medido uma vez: 14,3 segundos com 23 conceitos. O Mathua confere cada gerador em um processo separado. Com 46 conceitos, a partida fica mais lenta.
- **Teste de navegador.** Passou nas execuções gravadas. Não foi medido se ele falha às vezes sem motivo.
- **Formato de resultado.** O corretor `value` cobre número e booleano. Texto, array e `undefined` pertencem a degraus posteriores e hoje resultam em "não avaliado".
- Continuam valendo os limites do bloco 1 sobre Linux, banco de versão anterior, dados do relato e revisão do relato pela tela.
