# Validação em macOS: comandos e saídas

Data da execução: 27/11/2026, America/Sao_Paulo.

Este registro cobre só as execuções feitas no Mac do usuário. As execuções em Linux estão em [COMANDOS-E-SAIDAS.md](COMANDOS-E-SAIDAS.md) e pertencem à rodada anterior, com o patch anterior. As alterações desta rodada (teclado, textos em português e menus) foram validadas somente em macOS.

Todos os arquivos citados estão em [evidencias/mac/](evidencias/mac/). Os caminhos da pasta pessoal foram trocados por `<repositório>` e `~` nos arquivos gravados.

## 1. Ambiente medido

Fonte: [evidencias/mac/ambiente.txt](evidencias/mac/ambiente.txt).

```text
sistema: macOS 26.4.1 (arm64)
go: go version go1.26.6 darwin/arm64
node da compilação da interface: v24.22.3
npm da compilação: 11.19.1
node da execução (PATH padrão): v24.14.1
exigência declarada em web/next-app/package.json engines.node: ^22.23.4 || ^24.22.1 || ^26.12.1
web/next-app/.npmrc: engine-strict=true
typescript do corretor: 5.9.3
playwright: Version 1.62.1
commit-base do Mathua: 2bd4a4e0e160653e274521f6de3df2e61e29c7f7
```

### Versão testada e versão exigida

| Etapa | Versão exigida | Fonte da exigência | Versão testada neste Mac |
| --- | --- | --- | --- |
| Compilar a interface (`npm ci` e `npm run build` em `web/next-app`) | `^22.23.4 \|\| ^24.22.1 \|\| ^26.12.1` | `web/next-app/package.json`, campo `engines.node`, com `engine-strict=true` em `web/next-app/.npmrc` | Node `24.22.3` |
| Executar o servidor e o corretor (`./pilot-bin`, que chama `node grade.cjs`) | Nenhuma faixa declarada | `cmd/typescript-pilot/package.json` não tem campo `engines` | Node `24.14.1` |
| Compilar o executável | Go `1.26.6` | `go.mod` do Mathua | Go `1.26.6` |

A versão testada não é a versão mínima. Só foram testadas as versões da última coluna. Nenhuma outra versão de Node foi testada neste Mac.

O Node `24.22.3` foi baixado de `https://nodejs.org/dist/v24.22.3/node-v24.22.3-darwin-arm64.tar.gz` para a pasta `mathua/.local-node/`, dentro do clone ignorado pelo Git. O arquivo passou na conferência `shasum -a 256 -c` contra o `SHASUMS256.txt` oficial. A instalação global de Node do usuário não foi alterada.

## 2. Aplicação do patch

Comandos, a partir de `pilotos/mathua/`:

```sh
git clone https://github.com/chuma-beep/mathua.git
cd mathua
git checkout 2bd4a4e0e160653e274521f6de3df2e61e29c7f7
git apply --check ../mathua-typescript-pilot.patch
git apply ../mathua-typescript-pilot.patch
```

Saída: `git apply --check` terminou sem mensagem e com código 0. Em uma segunda cópia limpa do commit-base, os 26 arquivos produzidos pelo patch ficaram idênticos aos arquivos testados (`cmp` em cada arquivo: 0 diferenças).

## 3. Compilação da interface com a chave do piloto

Comando, com Node `24.22.3` no `PATH`:

```sh
npm ci --prefix cmd/typescript-pilot --ignore-scripts
npm ci --prefix web/next-app
NEXT_PUBLIC_TS_PILOT=1 NEXT_PUBLIC_SAME_ORIGIN_API=1 NEXT_TELEMETRY_DISABLED=1 npm run build --prefix web/next-app
```

Saída: código 0. Trecho de [evidencias/mac/ui-build.log](evidencias/mac/ui-build.log):

```text
✓ Compiled successfully in 1091ms
  Generating static pages using 9 workers (0/60) ...
stamp-sw: out/sw.js -> v2-...
```

## 4. Verificações estáticas e testes unitários da interface

Comandos em `web/next-app`, com Node `24.22.3`. Os testes unitários rodam sem a chave do piloto. Eles mostram que a interface original não mudou de comportamento.

| Comando | Código de saída | Saída |
| --- | --- | --- |
| `npx tsc --noEmit -p .` | 0 | Nenhuma mensagem |
| `npm run lint` | 0 | `✖ 7 problems (0 errors, 7 warnings)` em [lint.log](evidencias/mac/lint.log) |
| `npm test` | 0 | `Test Files  198 passed (198)` e `Tests  1885 passed (1885)` em [vitest.log](evidencias/mac/vitest.log) |

Os 7 avisos do lint não foram comparados com o commit-base. Nenhum aviso aponta para uma linha alterada por este patch.

Um teste existente falhou na primeira tentativa desta rodada: `test/navCoverage.test.ts > gives the profile sidebar its own theme control`. Esse teste lê o código-fonte e exige o texto literal `aria-label="Toggle theme"`. A causa foi a tradução desse atributo. O atributo voltou ao texto original e o teste passou. O texto visível do botão continua traduzido.

## 5. Testes Go

Comandos na raiz do clone, com Node `24.14.1` no `PATH`:

```sh
go build -o pilot-bin ./cmd/typescript-pilot
go test -json ./cmd/typescript-pilot -count=1
go test -json ./internal/server -run 'Test(Practice_|StudyAnswer_|MyReports|AdminReport|Report)' -count=1
go test -json ./internal/mastery ./internal/scheduler ./internal/repair -count=1
```

| Arquivo de evidência | Código de saída | Casos finais aprovados | Falhas | Ignorados |
| --- | --- | --- | --- | --- |
| [mathua-pilot.jsonl](evidencias/mac/mathua-pilot.jsonl) | 0 | 29 | 0 | 0 |
| [mathua-native-http.jsonl](evidencias/mac/mathua-native-http.jsonl) | 0 | 26 | 0 | 0 |
| [mathua-native-engine.jsonl](evidencias/mac/mathua-native-engine.jsonl) | 0 | 154 | 0 | 0 |

A contagem usa os casos finais da árvore de testes. As suítes-pai não entram de novo.

A suíte geral `go test ./... -count=1` não foi repetida com o patch desta rodada. Na rodada anterior, uma execução no Mac passou (60 pacotes `ok`, 4 sem testes). O teste `TestWave23QuestionVariety` é intermitente no commit-base limpo: 495 aprovações e 5 falhas em 500 execuções neste Mac. Uma execução aprovada da suíte geral não prova estabilidade.

## 6. Programa de reinício

Comando, a partir de `pilotos/mathua/`:

```sh
python3 scripts/process-smoke.py --mathua ./mathua --output evidencias/mac/mathua-process-script.json
```

Saída: código 0. Trecho de [mathua-process-script.json](evidencias/mac/mathua-process-script.json): `passed: true`, `processes_started: 2`, `old_bearer_token_accepted: true`, `persisted_attempts: 1`.

## 7. Teste de navegador pela tela

Comando, a partir de `pilotos/mathua/`, com Node `24.14.1`:

```sh
node scripts/browser-smoke.mjs --mathua ./mathua --output evidencias/mac/mathua-browser-smoke.json --screenshots evidencias/mac/capturas
```

Saída: código 0. Em [mathua-browser-smoke.json](evidencias/mac/mathua-browser-smoke.json): `passed: true`, `platform: darwin arm64`, `node: v24.14.1`, `browser: 151.0.7922.34`, 14 verificações, `page_errors: []`, `api_errors: []`.

O teste usa a API real e um banco SQLite temporário. Ele não simula respostas de rede e não grava progresso direto no banco.

| Critério de aceite | Verificação no arquivo | Valor observado |
| --- | --- | --- |
| Abro o endereço e leio a explicação | `home_opens_existing_learn_page_with_lesson` | HTTP 200, conceito `ts.value.numeric_literal` |
| Sem teclado de símbolos matemáticos | `answer_field_has_no_math_palette` | `palette_buttons: 0`, campo `Sua resposta`, botão `Verificar` |
| Digito a resposta normalmente | `wrong_then_fresh_variant_then_correct` | `typed_with_key_presses: true`, resposta `const reviewLimit = 1937;` |
| Recebo a correção | `wrong_then_fresh_variant_then_correct` | `let limit = 4062;` foi rejeitada com `✗ Ainda não.` e `Resposta:` |
| Obtenho uma variante após errar | `wrong_then_fresh_variant_then_correct` | A pergunta mudou de `limit`/`4062` para `reviewLimit`/`1937` |
| Avanço quando os pré-requisitos permitem | `ui_blocks_unmet_prerequisites` e `navigation_to_ts.binding.const_number` | Antes: 0 campos de resposta. Depois de `MASTERED` nos dois pré-requisitos: o link do próximo conceito abriu `const` |
| Textos em português | `study_path_text_is_portuguese` | 21 textos originais em inglês ausentes em 6 telas |
| Navegação adequada ao piloto | `navigation_fits_the_pilot` | Ausentes: `/graph`, `/glossary`, `/docs`, `/docs/contributing`, `/how-it-works`, `/note`, `/announcements`. Presentes: `/learn`, `/domains`, `/history`, `/reports`, `/my-reports` |
| Relato de pergunta ruim | `feedback_keeps_question_expected_and_given_answer` | Relato 1 gravado com pergunta, resposta esperada e resposta dada |
| Consulto meus relatos | `learner_reads_own_report_on_my_reports_page` | A página `/my-reports` mostrou o relato para o visitante |
| Recarregar preserva o progresso | `reload_preserves_identity_and_prerequisite_progress` | `eligible: true` |
| Reiniciar o servidor preserva o progresso | `server_restart_preserves_progress_and_reports` | `processes_started: 2`, `eligible: true`, `reports: 1` |

O menu lateral observado foi: Estudar, Domínios, Ranking, Histórico, Relatório de progresso, Configurações, Meus relatos e avisos.

### Controle negativo

O mesmo teste foi rodado contra a interface compilada sem `NEXT_PUBLIC_TS_PILOT=1`. Resultado em [controle-negativo-sem-chave.json](evidencias/mac/controle-negativo-sem-chave.json): `passed: false`, código de saída 1. O teste parou na primeira verificação, à espera do botão `Próximo →`. Isso mostra que o teste falha quando os textos estão em inglês.

O controle negativo não chegou às verificações do teclado e dos menus. A presença do teclado e do link `/graph` na interface sem a chave foi medida antes, por leitura do texto da página no navegador.

## 8. Capturas de tela

As capturas vêm da mesma execução do teste de navegador da seção 7.

| Arquivo | Momento |
| --- | --- |
| [01-aula.png](evidencias/mac/capturas/01-aula.png) | Explicação do primeiro conceito e menu lateral |
| [02-pre-requisitos.png](evidencias/mac/capturas/02-pre-requisitos.png) | Conceito `const` bloqueado por pré-requisitos |
| [03-pergunta.png](evidencias/mac/capturas/03-pergunta.png) | Campo de resposta sem teclado matemático |
| [04-fim-da-secao.png](evidencias/mac/capturas/04-fim-da-secao.png) | Fim da seção, com `Praticar novamente` e o link do próximo conceito |
| [05-correcao-de-erro.png](evidencias/mac/capturas/05-correcao-de-erro.png) | Correção de uma resposta errada |
| [06-relato.png](evidencias/mac/capturas/06-relato.png) | Janela de relato de problema |
| [07-meus-relatos.png](evidencias/mac/capturas/07-meus-relatos.png) | Página com o relato enviado |

## 9. O que não foi verificado no Mac

- Outros navegadores além do Chromium `151.0.7922.34` do Playwright. O Safari e o Chrome do usuário não foram testados.
- Telas estreitas e celular.
- As páginas `/my-reports`, `/history`, `/reports`, `/domains`, `/profile` e `/settings` continuam em inglês. Só o menu que leva a elas foi traduzido.
- O menu `Ranking` e o botão do assistente continuam visíveis. Eles não levam ao catálogo de matemática e não foram testados no piloto.
- A página `/profile` mostra um botão de teste diagnóstico do Mathua. Esse fluxo não foi testado com o piloto.
- As execuções em Linux não foram repetidas com o patch desta rodada.
