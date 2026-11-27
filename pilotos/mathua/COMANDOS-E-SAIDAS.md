# Interface do piloto: comandos e saídas em Linux

> Este registro é da rodada em Linux de 26/11/2026 e usa o patch anterior (sha256 `c8d12f0d2263289580d581acdf0bc8c31827834141a97b7ff650c24adbcf4a83`). Os rótulos em inglês e os comandos de compilação abaixo são dessa rodada. A rodada em macOS, com o patch atual, está em [COMANDOS-E-SAIDAS-MAC.md](COMANDOS-E-SAIDAS-MAC.md).

Data de referência da rodada: 26/11/2026, America/Sao_Paulo.

Esta rodada parte do pacote publicado em `1d5c7f8ab063dcfe75686e9c2d6147b923ec165f` e do Mathua em `2bd4a4e0e160653e274521f6de3df2e61e29c7f7`. Os comandos abaixo foram executados no ambiente Linux do assistente. Os caminhos absolutos identificam esse ambiente, não o Mac do usuário. Para instalar em outra máquina, use os comandos relativos de [LEIA-ME.md](LEIA-ME.md).

## 1. Ambiente medido e versão do Node

Comandos executados na raiz do clone do Mathua:

```sh
uname -srm
node --version
npm --version
python3 --version
/workspace/scratch/66d296bb0a09/runtime-go/go/bin/go version
node - <<'JS'
const p = require('./web/next-app/package.json');
const semver = require('./web/next-app/node_modules/semver');
console.log('frontend engines.node = '+p.engines.node);
for (const v of ['24.22.3','24.14.1','26.7.0']) console.log(v+': '+semver.satisfies(v,p.engines.node));
console.log('TypeScript grader = '+require('./cmd/typescript-pilot/node_modules/typescript/package.json').version);
JS
```

Saída:

```text
Linux 6.18.57 x86_64
v24.22.3
11.19.1
Python 3.12.14
go version go1.26.6 linux/amd64
frontend engines.node = ^22.23.4 || ^24.22.1 || ^26.12.1
24.22.3: true
24.14.1: false
26.7.0: false
TypeScript grader = 5.9.3
```

Conclusão limitada: o `24.22.3` registrado era o Node deste ambiente. As duas versões informadas para o Mac não satisfazem a faixa declarada pela interface. Isso não é um teste de execução nesses dois Nodes. Não foram reduzidas as exigências do Mathua.

## 2. Compilação da interface existente

Diretório: `/workspace/scratch/66d296bb0a09/mathua-review/web/next-app`.

```sh
NEXT_PUBLIC_SAME_ORIGIN_API=1 NEXT_TELEMETRY_DISABLED=1 npm run build > /workspace/scratch/66d296bb0a09/verification/mathua-ui-build.log 2>&1
```

Código de saída: `0`. Trechos da saída:

```text
▲ Next.js 16.4.6 (Turbopack)
✓ Compiled successfully in 13.8s
  Running TypeScript ...
  Finished TypeScript in 13.5s ...
✓ Generating static pages using 8 workers (60/60) in 1353ms
├ ○ /learn
○  (Static)  prerendered as static content
stamp-sw: out/sw.js -> v2-20261127T024659Z
```

O carimbo do service worker está em UTC. A saída completa desta compilação está em [mathua-ui-build.log](evidencias/mathua-ui-build.log), incluindo os avisos do projeto. A interface usa a API da mesma origem por uma opção que já existia em `lib/apiBase.ts`.

## 3. Compilação e testes do piloto

Diretório: `/workspace/scratch/66d296bb0a09/mathua-review`.

```sh
/workspace/scratch/66d296bb0a09/runtime-go/go/bin/gofmt -w cmd/typescript-pilot/main.go
/workspace/scratch/66d296bb0a09/runtime-go/go/bin/go build -o pilot-bin ./cmd/typescript-pilot
/workspace/scratch/66d296bb0a09/runtime-go/go/bin/go test -json ./cmd/typescript-pilot -count=1 > /workspace/scratch/66d296bb0a09/verification/mathua-ui-go-tests.jsonl
```

Código de saída: `0`. A compilação não imprimiu saída. Evento final do teste:

```json
{"Action":"pass","Package":"github.com/chuma-beep/mathua/cmd/typescript-pilot","Elapsed":18.765}
```

Contagem das folhas da árvore de testes: `29 pass`, `0 fail`, `0 skip`. Suítes-pai não foram contadas novamente. O JSON completo está em [mathua-pilot-ui.jsonl](evidencias/mathua-pilot-ui.jsonl).

## 4. Navegador com API real e banco temporário

Diretório: `/workspace/scratch/66d296bb0a09/anki-typescript-work`.

```sh
node pilotos/mathua/scripts/browser-smoke.mjs --mathua /workspace/scratch/66d296bb0a09/mathua-review --chromium-module /workspace/scratch/66d296bb0a09/verification/browser-runtime/node_modules/@sparticuz/chromium/build/index.js --output pilotos/mathua/evidencias/mathua-browser-smoke.json
```

Código de saída: `0`. O programa inicia o executável, abre o Chromium e interage com a interface compilada. Não intercepta a API com respostas fictícias e não insere progresso diretamente no banco.

Campos observados da saída:

```json
{
  "passed": true,
  "node": "v24.22.3",
  "browser": "158.0.8127.0",
  "page_errors": [],
  "api_errors": []
}
```

Os nove itens de `checks` passaram:

| Verificação do programa | Saída observada |
| --- | --- |
| Abrir `/` | Página final HTTP `200`, conceito `ts.value.numeric_literal`, explicação visível |
| Abrir `const` antes dos pré-requisitos | Painel de pré-requisitos e zero campos de resposta |
| Responder literal numérico | Seis respostas, estado final `MASTERED`, chave `ungraded` ausente |
| Seguir o link da própria tela | `New: Tipo number →`, URL do conceito `ts.type.number` |
| Responder tipo `number` | Seis respostas, estado final `MASTERED`, chave `ungraded` ausente |
| Seguir o próximo link | `New: Declaração const com valor numérico →`, URL de `ts.binding.const_number` |
| Errar, receber variante e acertar | `let limit = 14011;` rejeitado; `const amount = 5517;` aceito na pergunta seguinte |
| Enviar relato pelo botão da tela | Relato `open`, esperado `const amount: number = 5517;`, fornecido `const amount = 5517;` |
| Recarregar a página | Identidade preservada e `eligible: true` para `const` |

A evidência completa é [mathua-browser-smoke.json](evidencias/mathua-browser-smoke.json). `page_errors` registra exceções JavaScript da página. `api_errors` registra apenas respostas de erro em `/api/lessons...`. Não significa que todo pedido de rede da aplicação teve sucesso: a inicialização nativa pode consultar endpoints autenticados antes de criar o acesso de visitante.

O download padrão de Chromium pelo Playwright retornou HTTP `403` neste ambiente. Foi usado `@sparticuz/chromium@158.0.0`, instalado fora do repositório. Essa troca foi apenas do executável do navegador de teste. A interface e a API não foram simuladas. O modo padrão do programa usa o Chromium instalado por `npx playwright install chromium` na máquina que o executar. Esta rodada não verificou outros navegadores, dispositivos móveis ou o Mac do usuário.

## 5. Programa de reinício agora incluído

Diretório: `/workspace/scratch/66d296bb0a09/anki-typescript-work`.

```sh
python3 pilotos/mathua/scripts/process-smoke.py --mathua /workspace/scratch/66d296bb0a09/mathua-review --binary pilot-bin --output pilotos/mathua/evidencias/mathua-process-script.json
```

Código de saída: `0`. Campos observados:

```json
{
  "passed": true,
  "test": "real_process_restart",
  "processes_started": 2,
  "old_bearer_token_accepted": true,
  "pre_restart_question_graded": true,
  "retry_body_identical": true,
  "persisted_attempts": 1,
  "ungraded_key_present_in_normal_response": false
}
```

A resposta completa está em [mathua-process-script.json](evidencias/mathua-process-script.json). O programa solicita uma pergunta antes de encerrar o primeiro processo, reabre o mesmo SQLite no segundo processo e responde com a identidade anterior. A repetição da mesma submissão devolve os mesmos bytes e mantém uma tentativa persistida.

O arquivo histórico `mathua-process-smoke.json` foi preservado. O programa novo refaz os mesmos critérios e produz uma nova evidência. Não foi apresentado como o arquivo original que gerou o registro antigo.

## 6. Contrato de `ungraded`

O comando da seção 5 recebe e registra o JSON real. A saída mostra que a resposta normal tem `correct: true` e não contém a chave `ungraded`.

A leitura do código explica o resultado:

- `internal/engine/engine.go`, função `studyAnswerResponseJSON`: monta o JSON normal sem `ungraded`.
- `internal/server/server.go`, `handleStudyAnswer`: devolve `res.ResponseJSON` quando disponível, antes de construir o mapa alternativo.
- `web/next-app/components/LearnStepper.tsx`: usa `if (res.ungraded)` para tratar a indisponibilidade.

Comandos executados na raiz do Mathua para conferir esses caminhos:

```sh
sed -n '3350,3360p' internal/server/server.go
sed -n '2294,2325p' internal/engine/engine.go
sed -n '470,478p' web/next-app/components/LearnStepper.tsx
```

Trechos da saída:

```go
if res.ResponseJSON != "" {
    w.Header().Set("Content-Type", "application/json")
    _, _ = w.Write([]byte(res.ResponseJSON))
    return
}
```

```tsx
if (res.ungraded) {
  setEntry(key, { error: 'The grader is temporarily unavailable. Your answer is kept. Press Check to retry.' })
  return
}
```

A leitura do mapa completo de `studyAnswerResponseJSON` não mostrou a chave `ungraded`. A verificação da resposta bruta na seção 5 confirma o comportamento em execução. O cenário Go aprovado foi `TestPilotHTTP/compiler_failure_is_ungraded_without_penalty_and_can_retry`.

Decisão de projeto: preservar e documentar o contrato existente. Em HTTP bem-sucedido, `ungraded === true` significa resposta não avaliada. Ausência ou `false` significa resposta avaliada, cujo acerto é dado por `correct`. Erros HTTP continuam sendo erros de requisição. O teste Go de indisponibilidade continua verificando a chave `true` e a preservação das tentativas.

## 7. Suíte geral: falha registrada, sem ocultá-la

Diretório: `/workspace/scratch/66d296bb0a09/mathua-review`.

```sh
/workspace/scratch/66d296bb0a09/runtime-go/go/bin/go test -json ./... -count=1 > /workspace/scratch/66d296bb0a09/verification/mathua-ui-full-go.jsonl
```

Código de saída: `1`. Resultados de pacote extraídos do JSON:

```json
{"pass":59,"fail":1,"skip":5}
```

Saída do teste que falhou:

```text
=== RUN   TestWave23QuestionVariety
    wave23_test.go:159: abstract.group.permutation_character kp3: only 4 distinct questions in 12 draws
--- FAIL: TestWave23QuestionVariety (0.00s)
```

O resumo registra todos os pacotes, as saídas finais e os eventos de falha: [mathua-full-go-summary.json](evidencias/mathua-full-go-summary.json). O log bruto tinha 6.512.341 bytes. Seu SHA-256 está no resumo. O resumo não contém todo o log bruto.

Há cinco pacotes sem testes porque esta execução, depois de instalar o frontend, também encontrou o pacote Go de `web/next-app/node_modules/flatted/golang/pkg/flatted`. Os 36 eventos de testes ignorados incluem casos já condicionais do projeto. Não foi afirmado que todos os testes da suíte rodaram sem exceção.

### Verificação no commit-base sem o patch

Criado um checkout separado:

```sh
git worktree add --detach /workspace/scratch/66d296bb0a09/verification/mathua-clean-base 2bd4a4e0e160653e274521f6de3df2e61e29c7f7
```

Saída:

```text
Preparing worktree (detached HEAD 2bd4a4e)
HEAD is now at 2bd4a4e Merge pull request #478 from rolliver/fix/learnstepper-prefetch
```

Nesse checkout, sem modificações:

```sh
/workspace/scratch/66d296bb0a09/runtime-go/go/bin/go test -json ./internal/generator/abstract -run '^TestWave23QuestionVariety$' -count=20 > /workspace/scratch/66d296bb0a09/verification/mathua-clean-base-variety.jsonl
/workspace/scratch/66d296bb0a09/runtime-go/go/bin/go test -json ./internal/generator/abstract -run '^TestWave23QuestionVariety$' -count=500 > /workspace/scratch/66d296bb0a09/verification/mathua-clean-base-variety-stress.jsonl
```

A primeira execução terminou com código `0`, 20 aprovações. A segunda terminou com código `1`, 499 aprovações e uma falha:

```text
wave23_test.go:159: abstract.group.hall kp3: only 4 distinct questions in 12 draws
```

O commit e `git status --porcelain` vazio foram registrados em [mathua-base-variety-500-summary.json](evidencias/mathua-base-variety-500-summary.json). A primeira amostra está em [mathua-base-variety-20-summary.json](evidencias/mathua-base-variety-20-summary.json).

Conclusão e limite: o mesmo teste tem falha intermitente também no código-base. Nas duas falhas, os conceitos sorteados foram diferentes. O patch não altera os geradores de álgebra abstrata. Essa evidência permite registrar um problema existente no teste, sem declarar que a suíte geral desta rodada passou. Não foi feita uma nova execução completa apenas para obter uma saída verde.

## 8. Aplicação do patch e escopo das alterações

No checkout limpo do commit-base:

```sh
git apply --check /workspace/scratch/66d296bb0a09/anki-typescript-work/pilotos/mathua/mathua-typescript-pilot.patch
git status --porcelain
git rev-parse HEAD
```

Os dois primeiros comandos terminaram com código `0` e sem saída. O terceiro imprimiu:

```text
2bd4a4e0e160653e274521f6de3df2e61e29c7f7
```

No clone com a adaptação:

```sh
git diff --check
git diff --name-only -- internal/generator/abstract
git diff --stat -- cmd/typescript-pilot internal/server/server.go web/next-app/components/LearnStepper.tsx
```

Os dois primeiros comandos terminaram com código `0` e sem saída. A estatística final foi `13 files changed, 922 insertions(+)`: onze arquivos do piloto, uma linha na API original e duas propriedades no botão de feedback da interface. O patch não inclui clone completo, dependências, executáveis, banco ou credenciais.

SHA-256 do patch verificado:

```text
c8d12f0d2263289580d581acdf0bc8c31827834141a97b7ff650c24adbcf4a83
```

## O que permanece pendente

A entrega oferece estudo pelo navegador para três conceitos, com uma família de exercícios por conceito. Os testes comprovam o funcionamento descrito, não o domínio real de TypeScript por um aluno. Variação de nome e valor continua sendo variação da mesma família.

A geração automática de novas famílias a partir do feedback não foi iniciada. A revisão de conteúdo e de critérios continua humana. A instalação no Mac do usuário, a adaptação completa dos demais menus e a calibração pedagógica com alunos reais não foram verificadas.
