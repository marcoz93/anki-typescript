# Bloco 1: degraus D01 a D03 integrados ao piloto

Data da execução: 27/11/2026, America/Sao_Paulo. Ambiente: macOS 26.4.1 arm64, no Mac do usuário.

Ponto de partida: commit `2ec2f30c05b87eeb50e97860ff407a05d1625980` deste repositório, com o conteúdo em `conteudo/typescript-v1/`. Mathua no commit-base `2bd4a4e0e160653e274521f6de3df2e61e29c7f7`.

Os testes de `conteudo/typescript-v1/` conferem o conteúdo. Este documento registra a integração desse conteúdo ao aplicativo, que é outra verificação.

## 1. Conteúdo que entrou

O piloto lê `curriculo.json` e `exercicios.json` direto de `conteudo/typescript-v1/`. Não existe cópia do conteúdo dentro do patch. Os arquivos lidos nesta execução têm estes resumos SHA-256, gravados em [ambiente.txt](evidencias/bloco-1-d01-d03/ambiente.txt):

```text
exercicios.json  906b2c9333d253824396dd0bcc6f74515a8e40864eb2968f526bdef56858f1bb
curriculo.json   6f38a98a4f169e71761c851cdd9ad1cd086c3d0dbe8707a8c5b272bd17997f23
```

Entraram **13 conceitos, 14 famílias e 84 casos**. Mensagem do servidor na partida:

```text
Content typescript-escada-v1 from <repositório>/conteudo/typescript-v1: stages 1 to 3, 13 concepts, 14 families, 84 cases, every model answer accepted by its grader
```

| Degrau | Conceito | Pré-requisitos | Família e formato |
| --- | --- | --- | --- |
| D01 | `ts.value.literal_notation` | nenhum | F001, alternativas |
| D01 | `ts.value.numeric_literal` (já existia) | nenhum | F002, código |
| D01 | `ts.value.string_literal` | `ts.value.literal_notation` | F003, código |
| D01 | `ts.value.boolean_literal` | `ts.value.literal_notation` | F004, código |
| D02 | `ts.type.number` (já existia) | nenhum | F005, nome de tipo |
| D02 | `ts.type.string` | `ts.value.string_literal` | F006, nome de tipo |
| D02 | `ts.type.boolean` | `ts.value.boolean_literal` | F007, nome de tipo |
| D02 | `ts.type.value_type_distinction` | `ts.type.number`, `ts.type.string` | F008, alternativas |
| D03 | `ts.binding.const_semantics` | `ts.value.numeric_literal` | F009 e F013, alternativas |
| D03 | `ts.binding.const_number` (já existia) | `ts.value.numeric_literal`, `ts.type.number` | F010, código |
| D03 | `ts.binding.const_string` | `ts.value.string_literal`, `ts.type.string`, `ts.binding.const_semantics` | F011, código |
| D03 | `ts.binding.annotation` | `ts.type.number`, `ts.binding.const_number` | F012, símbolo |
| D03 | `ts.binding.assignment_compatibility` | `ts.type.value_type_distinction`, `ts.binding.const_number` | F014, alternativas |

Os três conceitos que já existiam mantêm o mesmo ID e os mesmos pré-requisitos. O progresso fica gravado por ID de conceito, então continua ligado a eles. Os enunciados desses três conceitos mudaram: agora são os seis casos de F002, F005 e F010 do pacote, e não mais os enunciados sorteados do piloto anterior.

## 2. Como o conteúdo foi ligado ao motor existente

| Elemento do pacote | Mecanismo existente do Mathua |
| --- | --- |
| Conceito e pré-requisitos | Conceito do grafo, com os mesmos IDs e arestas |
| Família, isto é, uma tarefa com um critério | Uma seção da aula do conceito |
| Caso, isto é, uma pergunta concreta | Um problema do gerador do conceito |
| Aula do degrau | Aula de cada conceito do degrau, uma vez por seção |
| Alternativas | Blocos `A) ...` no enunciado, que a tela existente já desenha como botões |
| Relato de pergunta ruim | Mecanismo de relato existente, sem armazenamento novo |

A família vira seção porque a tela existente mantém o aluno na mesma seção depois de um erro. Assim, a variante depois do erro é da mesma família.

O limite `integratedThroughStage = 3`, em `cmd/typescript-pilot/content.go`, define até qual degrau o piloto serve. Na partida, o piloto corrige o gabarito de cada caso servido com o próprio corretor. Uma família sem corretor, ou um gabarito recusado, impede a partida.

### Mudanças no código

Arquivos do piloto, em `cmd/typescript-pilot/`: `content.go` é novo; `main.go`, `grade.cjs`, `main_test.go` e `README.md` mudaram; a pasta `lessons/`, com cinco arquivos, saiu, porque as aulas agora vêm do pacote.

Código existente do Mathua, além do que o patch anterior já mudava:

| Arquivo | Mudança | Motivo |
| --- | --- | --- |
| `internal/server/server.go` | 3 linhas: a rota de prática exclui a pergunta inteira | Antes, a exclusão comparava linha por linha. Uma pergunta de várias linhas, como toda pergunta de alternativas, nunca era excluída. A variante depois de um erro podia repetir a mesma pergunta |
| `web/next-app/components/LearnStepper.tsx` | A tela mostra a causa do erro informada pelo corretor; a tela exclui as perguntas mostradas, e não as buscadas | Ver seção 5. As duas mudanças só valem com `NEXT_PUBLIC_TS_PILOT=1` |
| `web/next-app/lib/pilot.ts` | Funções `pilotDiagnosis`, `pilotExclude` e `pilotFresh` | Suporte às duas mudanças acima |

O patch atual tem 22 arquivos, 2005 linhas adicionadas e 110 removidas. Resumo SHA-256 do patch: `e93777ab18e65c6fd0f61d80af3d8735f64747372fc92450b1dda3746be3020c`.

## 3. Comandos executados e saídas

Todos os arquivos citados estão em [evidencias/bloco-1-d01-d03/](evidencias/bloco-1-d01-d03/). A compilação da interface usou Node `24.22.3`. A execução do servidor, do corretor e dos testes usou Node `24.14.1`.

### Patch

```sh
git apply --check ../mathua-typescript-pilot.patch
```

Saída: sem mensagem, código 0, em uma cópia limpa do commit-base. Os 22 arquivos produzidos ficaram idênticos aos arquivos testados (`cmp`: 0 diferenças).

### Interface

Comandos em `web/next-app`:

| Comando | Código | Saída |
| --- | --- | --- |
| `NEXT_PUBLIC_TS_PILOT=1 NEXT_PUBLIC_SAME_ORIGIN_API=1 NEXT_TELEMETRY_DISABLED=1 npm run build` | 0 | [ui-build.log](evidencias/bloco-1-d01-d03/ui-build.log) |
| `npx tsc --noEmit -p .` | 0 | Nenhuma mensagem |
| `npm run lint` | 0 | 0 erros, 7 avisos, em [lint.log](evidencias/bloco-1-d01-d03/lint.log) |
| `npm test` | 0 | `Test Files  198 passed (198)`, `Tests  1885 passed (1885)`, em [vitest.log](evidencias/bloco-1-d01-d03/vitest.log) |

### Testes Go

```sh
go vet ./cmd/typescript-pilot
go build -o pilot-bin ./cmd/typescript-pilot
go test -json ./cmd/typescript-pilot -count=1
go test -json ./internal/server -run 'Test(Practice_|StudyAnswer_|MyReports|AdminReport|Report)' -count=1
go test -json ./internal/mastery ./internal/scheduler ./internal/repair -count=1
go test ./internal/server -count=1
```

| Evidência | Código | Aprovados | Falhas |
| --- | --- | --- | --- |
| [mathua-pilot.jsonl](evidencias/bloco-1-d01-d03/mathua-pilot.jsonl) | 0 | 57 casos finais | 0 |
| [mathua-native-http.jsonl](evidencias/bloco-1-d01-d03/mathua-native-http.jsonl) | 0 | 26 casos finais | 0 |
| [mathua-native-engine.jsonl](evidencias/bloco-1-d01-d03/mathua-native-engine.jsonl) | 0 | 154 casos finais | 0 |
| [mathua-server-completo.txt](evidencias/bloco-1-d01-d03/mathua-server-completo.txt) | 0 | pacote `internal/server` inteiro: `ok` | 0 |

O pacote `internal/server` inteiro foi rodado porque este bloco mudou `server.go`.

Linhas registradas pelos testes do piloto:

```text
ts.value.numeric_literal: 6 distinct submitted answers, status MASTERED
ts.type.number: 6 distinct submitted answers, status MASTERED
typescript-escada-v1: 13 concepts, 14 families, 84 cases, 84 questions identified
F001: missed F001-V2 with A, then F001-V3 accepted by letter; reference shown: Uma notação que expressa diretamente um valor.
```

### Reinício com dois processos

```sh
python3 scripts/process-smoke.py --mathua ./mathua --output evidencias/bloco-1-d01-d03/mathua-process-script.json
```

Saída: código 0, `passed: true`, `processes_started: 2`, `persisted_attempts: 1`.

### Navegador, pela tela

```sh
node scripts/browser-smoke.mjs --mathua ./mathua --output evidencias/bloco-1-d01-d03/mathua-browser-smoke.json --screenshots evidencias/bloco-1-d01-d03/capturas
```

Saída: código 0. Em [mathua-browser-smoke.json](evidencias/bloco-1-d01-d03/mathua-browser-smoke.json): `passed: true`, `node: v24.14.1`, Chromium `151.0.7922.34`, 16 verificações, `page_errors: []`, `api_errors: []`. O teste usa a API real e um banco temporário. As respostas vêm do pacote de conteúdo, localizadas pelo enunciado visível.

## 4. Critério de aceite e o que foi observado

| Critério | Onde foi verificado | Valor observado |
| --- | --- | --- |
| Ler a aula do conceito | Navegador: `home_opens_first_concept_with_its_lesson` | HTTP 200, conceito `ts.value.literal_notation`, texto da aula do degrau D01 visível |
| Responder aos exercícios | Navegador: três conceitos até `MASTERED` | F001 por toque na alternativa; F002 digitado; F005 preenchido |
| Correção coerente com o contrato | Teste Go `TestTypeScriptCriteria`: 46 casos | Aceitos e recusados por família, na tabela da seção 5 |
| Solução válida diferente do gabarito | Navegador: `code_miss_names_the_cause_then_variant_accepts_valid_alternative` | Gabarito `const total: number = 18000;`; resposta aceita `const total = 18000` |
| Outra solução válida diferente do gabarito | Navegador: `mastery_through_browser_ts.value.numeric_literal` | Gabarito `1200`; resposta aceita `1_200` |
| Resposta incorreta | Navegador: `code_miss_names_the_cause…` | `let amount: number = 15000;` recusada; a tela mostrou "A tarefa pede const, que impede reatribuir esse nome após a inicialização. let permite reatribuição." |
| Explicação da instância no erro | Navegador: `choice_miss_shows_instance_explanation_and_same_family_variant` | Erro no caso F001-V2; a tela mostrou a explicação desse caso e o texto da alternativa correta |
| Variante da mesma família após o erro | O mesmo teste | Depois de F001-V2 veio F001-V3 |
| Variante após o erro em conceito com duas famílias | Navegador: `each_section_keeps_its_family_after_a_miss` | Seção 1: F009-V1, V2, V3. Seção 2: F013-V1, V2, V3. Um erro em cada seção, sem troca de família |
| Falha técnica do corretor distinta de erro | Teste Go `compiler_failure_is_ungraded_without_penalty_and_can_retry` | Com o Node ausente: `ungraded: true`, tentativas e progresso inalterados; a repetição depois da recuperação foi aceita |
| Família sem corretor não vira erro | Teste Go `family_without_grader_is_not_graded` | Resultado "não avaliado" |
| Registrar relato | Navegador: `report_keeps_question_reference_and_given_answer` | Relato 1 com conceito, enunciado, gabarito e resposta dada; o enunciado identifica a família F010 e o caso F010-V1 |
| Consultar relato | Navegador: `learner_reads_own_report_on_my_reports_page` | A página `/my-reports` mostrou o relato |
| Progresso ao recarregar | Navegador: `reload_preserves_identity_and_prerequisite_progress` | `eligible: true` |
| Progresso ao reiniciar | Navegador: `server_restart_preserves_progress_and_reports` | Dois processos, `eligible: true`, 1 relato |
| Conceito novo libera o dependente | Navegador: `new_concept_mastery_unlocks_its_dependent` | Depois de `ts.value.literal_notation`, o conceito `ts.value.string_literal` ficou disponível |
| Não repetir caso antes de esgotar os seis | Navegador: `mastery_through_browser_ts.value.numeric_literal` | 6 respostas, 6 casos distintos: F002-V5, V0, V1, V2, V3, V4 |

### Capturas de tela

As oito capturas estão em [evidencias/bloco-1-d01-d03/capturas/](evidencias/bloco-1-d01-d03/capturas/): aula, pré-requisitos, pergunta de alternativas, correção de alternativa, correção de código, relato, meus relatos e seção com código de contexto.

## 5. O que os corretores aceitam neste bloco

| Família | Aceita | Recusa |
| --- | --- | --- |
| F002 literal numérico | `15000`, `15_000` | `"15000"`, `10000 + 5000`, outro valor |
| F003 literal textual | `"reembolso-01"`, `'reembolso-01'` | texto sem aspas, outro conteúdo, crases, número |
| F004 literal booleano | `false`, `true;` | `"false"`, o valor oposto, `True` |
| F010 `const` numérica | com ou sem `: number`, espaços e comentário | `let`, outro nome, outro valor, texto, `: string`, instrução extra |
| F011 `const` textual | com ou sem `: string`, aspas simples ou duplas, sem ponto e vírgula | `let`, outro nome, número, `: number` |
| F005, F006, F007, F012 nome ou símbolo | o nome exato, com espaços em volta | outra grafia, como `Number` |
| F001, F008, F009, F013, F014 alternativas | a letra da alternativa correta, maiúscula ou minúscula | outra alternativa |

O corretor não executa o código do aluno. Ele analisa a sintaxe e, nas declarações, roda a verificação de tipos do TypeScript 5.9.3 com `strict`.

Uma resposta de alternativas que não é letra de nenhuma alternativa, como `Z`, conta como resposta errada.

## 6. Defeitos achados e corrigidos neste bloco

1. **Variante repetida depois do erro.** O teste Go `TestChoiceIsAnsweredByLetterThroughTheAPI` falhou com "variant after a miss: F001 F001-V2 after F001 F001-V2". A causa está na rota de prática do Mathua, que comparava a exclusão linha por linha. A correção são 3 linhas em `internal/server/server.go`. O mesmo teste passa depois da correção e fica como proteção contra a volta do defeito.

2. **Casos repetidos antes de esgotar o banco, na tela.** O teste de navegador mostrou 6 respostas com 2 casos distintos. A causa: a tela excluía as perguntas buscadas, e não as mostradas. Ela busca três e mostra duas por rodada, então as já respondidas voltavam. Com a chave do piloto, a tela agora exclui as perguntas mostradas mais recentemente. O teste de navegador passou a exigir casos distintos e registra cada busca em `practice_fetches`.

3. **Formato da alternativa.** O registro de geradores do Mathua recusou o primeiro formato de gabarito, "C) texto". O motor converte a letra tocada no texto da alternativa antes de corrigir. O gabarito de alternativas passou a ser o texto da alternativa correta, como nas perguntas de alternativas do próprio Mathua.

4. **Teste unitário intermitente da interface.** `test/reportsPage.test.tsx` falhou em 1 de 3 execuções da suíte completa e passou em 3 execuções isoladas. Esse teste cobre a página `/reports`, em `app/reports/page.tsx`, que o patch não altera. O patch altera outra página, `app/my-reports/page.tsx`. A execução gravada como evidência passou.

## 7. Limites desta verificação

- **Só macOS.** Nada deste bloco rodou em Linux.
- **Só Chromium `151.0.7922.34`.** Safari, Chrome do usuário e telas de celular não foram testados.
- **Progresso gravado por uma versão anterior.** Nenhum banco criado pelo piloto anterior foi aberto com esta versão. A preservação se apoia no fato de os três IDs não mudarem, conferido por teste. Uma pergunta servida pela versão anterior e ainda não respondida não pode ser corrigida por esta versão.
- **Suíte geral.** `go test ./...` não foi repetido com este patch. Foram rodados o piloto, o pacote `internal/server` inteiro e os pacotes `mastery`, `scheduler` e `repair`.
- **Caminho da falha técnica pela tela.** A falha do corretor foi verificada pela API real, no teste Go. Ela não foi provocada pelo navegador.
- **Conceitos percorridos pela tela.** O navegador percorreu 5 dos 13 conceitos: `literal_notation`, `numeric_literal`, `type.number`, `const_number` e `const_semantics`. Os outros 8 foram verificados pela correção do gabarito de cada caso na partida e pelos testes Go, e não pela tela.
- **Aula por degrau.** O pacote tem uma aula por degrau. Cada conceito do degrau mostra a aula inteira do degrau.
- **Dados do relato.** O relato guarda conceito, enunciado, gabarito e resposta dada. A família e o caso são recuperados pelo enunciado. A versão do conteúdo e a decisão do corretor não ficam em campos próprios do relato.
- **Revisão do relato pela tela.** O visitante do piloto não tem permissão de revisor. A reavaliação e a resolução continuam cobertas só pelo teste Go.
- **Calibração.** Aceitar o gabarito não prova que as seis variantes têm a mesma dificuldade.

## 8. O que os próximos blocos precisam

- **Corretor do formato `value`.** As 11 famílias de resultado (número, booleano, texto, array, ausência) começam no degrau D04.
- **Corretores de código com contexto.** A partir de D04, os casos de código têm `context_code`, e a correção precisa compilar a resposta junto com o contexto.
- **Conceitos com quatro famílias.** A rota de prática existente aceita seções 1 a 3. Cinco conceitos têm quatro famílias: `ts.function.composition` (D09), `ts.control.if_else` (D12), `ts.control.narrowing` (D13), `ts.collection.find` (D14) e `ts.iteration.for_of` (D15). O carregador recusa esses conceitos até existir uma decisão. As opções são aumentar o limite na rota ou juntar duas famílias em uma seção.
- **Tempo de partida.** A partida levou 6,4 segundos com 13 conceitos, medida uma vez, porque o Mathua confere cada gerador em um processo separado. Com 46 conceitos, a partida fica mais lenta. O tempo com 46 conceitos não foi medido.
