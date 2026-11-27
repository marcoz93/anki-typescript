# Teste mínimo do Mathua com TypeScript

**Resultado atual:** a tela existente do Mathua funciona com o piloto no navegador. O teste real percorreu os três conceitos e os links de continuação, liberou `const` após os pré-requisitos, errou, recebeu uma variante, acertou, enviou feedback e recarregou a página sem perder o progresso. Os **29 cenários do piloto** passaram novamente. O programa de reinício está salvo e também passou.

**A suíte geral não ficou integralmente aprovada nesta rodada.** Foram 59 pacotes aprovados, um reprovado e cinco sem testes. `TestWave23QuestionVariety` falhou por receber apenas quatro perguntas distintas em 12 sorteios. O mesmo teste também falhou no commit-base sem o patch, ao repeti-lo 500 vezes. Consulte [comandos, saídas e escopo](COMANDOS-E-SAIDAS.md). Na rodada inicial, os 180 testes existentes selecionados tinham passado. Esse resultado histórico não substitui o resultado atual da suíte geral.

Data de referência: 26/11/2026, America/Sao_Paulo.

## O que mudou

No código existente, o patch acrescenta **uma linha** em `internal/server/server.go` para transmitir `ungraded` quando o corretor falha, e **duas propriedades** no `ReportButton` da página de estudo para transmitir a resposta esperada e a explicação depois da correção. O motor já preservava o histórico na falha do corretor. O contrato do campo opcional está documentado abaixo.

Há onze arquivos novos em `cmd/typescript-pilot/`: os seis da versão inicial e cinco arquivos de conteúdo para carregar as explicações dos três conceitos. O comando também serve a exportação estática de `web/next-app` e redireciona `/` para a página existente `/learn`. O projeto mantém o motor, o agendamento, os pré-requisitos e o fluxo de feedback do Mathua.

A escolha foi reutilizar a tela existente. Foi necessário carregar as aulas, servir os arquivos compilados junto da API e completar os dados do botão de feedback. Os enunciados e as explicações do piloto estão em português. Os controles, as outras páginas e o catálogo matemático incorporado à interface mantêm o conteúdo original. O teste cobre a página de estudo do piloto, sem afirmar adaptação integral de todos os menus do Mathua.

O patch completo está em `mathua-typescript-pilot.patch`. Sua aplicação foi verificada contra o commit-base indicado em `resultados.json`. O conteúdo TypeScript é uma adaptação própria para este teste. Não foi atribuído aos autores do Mathua nem ao Math Academy.

## Conceitos e critérios do piloto

| Conceito | Comportamento observado | Critério de aceite |
| --- | --- | --- |
| Valor e literal numérico | Representar um valor escrito por extenso | Um literal numérico do valor pedido, sem aspas ou operações |
| Tipo `number` | Identificar a palavra que nomeia o tipo numérico | Responder `number`, distinguindo nome do tipo e valor |
| Declaração `const` numérica | Criar uma constante com nome e valor determinados | Uma declaração `const`, nome correto e literal numérico correto; anotação `number` opcional |

Os dois primeiros conceitos foram configurados como pré-requisitos do terceiro. Essa relação é uma decisão pedagógica do piloto. Não é uma afirmação de necessidade lógica nem uma reorganização de todo o material original.

O motor nativo marcou cada pré-requisito como `MASTERED` após as seis respostas distintas submetidas na simulação. Uma resposta isolada não produziu esse estado. O estado é a classificação do sistema segundo suas regras atuais; este teste não mede domínio real de um aluno.

## Caso concreto da primeira rodada pela API

A API serviu este enunciado:

> Declare somente uma constante chamada refundAmount, inicializada com o literal numérico 6830. A anotação number é opcional.

A resposta simulada foi:

```ts
let refundAmount = 6830;
```

O corretor a rejeitou e explicou que a tarefa pede `const`, que impede reatribuir esse nome após a inicialização, enquanto `let` permite reatribuição.

A próxima chamada de prática excluiu o enunciado anterior. O servidor devolveu uma variante com o nome `amount` e o valor `5522`. Esta resposta foi aceita:

```ts
const amount = 5522;
```

O nome e o valor variaram. O conceito e o critério de correção permaneceram os mesmos. O teste também confirmou a aceitação de `const amount: number = 15000;`, espaços, comentários comuns e separadores numéricos.

Na rodada atual, o navegador enviou `let limit = 14011;` e recebeu uma rejeição. A variante seguinte pediu `amount` com valor `5517`. O navegador enviou `const amount = 5517;`, recebeu aceitação e registrou um relato com essa resposta e a resposta esperada `const amount: number = 5517;`. A evidência completa está em [mathua-browser-smoke.json](evidencias/mathua-browser-smoke.json), gerada pelo programa incluído.

## O que foi verificado

| Verificação | Resultado observado |
| --- | --- |
| Pré-requisitos | A API recusou a entrega do exercício e a submissão prematura, sem gravar tentativa |
| Progressão | Respostas submetidas por HTTP produziram o estado nativo que liberou o conceito dependente |
| Correção TypeScript | O corretor aceitou os casos previstos e rejeitou `let`, nome ou valor incorretos, texto no lugar do número, sintaxe inválida e instruções extras |
| Variação após erro | A chamada seguinte, com exclusão do enunciado anterior, recebeu uma pergunta diferente do mesmo conceito |
| Submissão repetida | O mesmo identificador devolveu a resposta original; conteúdo diferente com o mesmo identificador foi recusado |
| Feedback | O sistema guardou pergunta, resposta esperada e resposta fornecida |
| Revisão do feedback | Um usuário autorizado reavaliou a resposta pelo mesmo corretor, resolveu o relato e devolveu a resolução ao aluno |
| Separação entre revisão e aprendizagem | Registrar ou reavaliar um relato não alterou tentativas nem progresso; outro aluno não recebeu esse histórico |
| Persistência | Reiniciar o servidor e reabrir SQLite preservou relatos, respostas já gravadas e uma pergunta ainda não respondida |
| Falha do corretor | A API sinalizou resposta não avaliada, sem penalizar o aluno, e a repetição após recuperação funcionou |
| Reparo de histórico | O recurso nativo de reparo corrigiu um falso negativo simulado após uma prévia sem escrita; não inventou domínio nem recalculou XP |
| Executável em processos independentes | Um token anterior e a pergunta pendente continuaram válidos; repetir a resposta manteve uma única tentativa persistida |

Os trechos de código enviados pelo aluno foram analisados e verificados estaticamente. Não foram executados. O compilador recebeu somente a resposta virtual e suas bibliotecas padrão.

## Feedback: o que este teste entrega

O fluxo existente permite registrar uma pergunta ruim, examinar a resposta concreta, testar a correção e registrar uma resolução. O piloto também comprovou a possibilidade de reparar falsos negativos no histórico com o mecanismo nativo, em uma base temporária de teste.

**A geração automática de novas famílias a partir do feedback continua pendente.** Neste recorte há uma família por conceito. Mudar nome e valor cria variantes dessa família. Acrescentar uma tarefa como explicar o erro ou escolher entre implementações exige uma nova família e critérios próprios. Uma pessoa ainda precisa decidir a mudança de conteúdo ou de corretor.

O relato de feedback e o reparo histórico foram cenários distintos: o primeiro investigou uma dúvida sobre a anotação opcional; o segundo usou uma tentativa histórica artificialmente marcada como errada. Nenhum histórico real do usuário foi alterado.

## Reprodução

O pacote contém o patch e as evidências, sem uma cópia integral do repositório ou dependências instaladas.

A partir de `pilotos/mathua/` deste repositório, use Git, npm, Go `1.26.6` e um Node compatível com a interface. A execução registrada usou Node `24.22.3` no Linux. A interface exige `^22.23.4 || ^24.22.1 || ^26.12.1`, conforme seu `package.json`. As versões informadas `24.14.1` e `26.7.0` não satisfazem essa faixa. Não foram testadas no Mac do usuário.

Use um clone limpo no commit-base. Este patch é completo e substitui a versão anterior. Não o aplique sobre um clone que já tenha o patch antigo. O clone local `pilotos/mathua/mathua/` está excluído pelo `.gitignore` deste repositório.

```sh
git clone https://github.com/chuma-beep/mathua.git
cd mathua
git checkout 2bd4a4e0e160653e274521f6de3df2e61e29c7f7
git apply ../mathua-typescript-pilot.patch
npm ci --prefix cmd/typescript-pilot --ignore-scripts
npm ci --prefix web/next-app
NEXT_PUBLIC_SAME_ORIGIN_API=1 NEXT_TELEMETRY_DISABLED=1 npm run build --prefix web/next-app
go test ./cmd/typescript-pilot -count=1 -v
go build -o pilot-bin ./cmd/typescript-pilot
./pilot-bin
```

Abra `http://127.0.0.1:8081`. O endereço abre o primeiro conceito na tela de estudo. Selecione **Next** para começar. **Complete** encerra uma seção da interface e não equivale ao estado `MASTERED` do motor. Use **Practice again** para continuar praticando o conceito e o link do próximo conceito para avançar. No teste, seis respostas corretas por pré-requisito produziram `MASTERED`; essa observação não é uma medição de aprendizagem humana.

O executável precisa dos arquivos do clone e deve ser iniciado da raiz do Mathua com os caminhos padrão. A opção `-web` permite outro diretório de exportação. Sem a compilação da interface, o servidor inicia apenas a API e informa o comando que falta. `NEXT_PUBLIC_SAME_ORIGIN_API=1` faz a tela usar a API local na mesma origem.

O progresso fica no SQLite `typescript-pilot.db`. Preserve também o arquivo adjacente `typescript-pilot.db.jwt` para manter os acessos após reiniciar. As opções `-addr`, `-db`, `-node`, `-grader` e `-web` estão em `cmd/typescript-pilot/README.md`.

### Executar os programas de verificação

Com o binário e a interface compilados, volte a `pilotos/mathua/`:

```sh
python3 scripts/process-smoke.py --mathua ./mathua --output evidencias/meu-reinicio.json
(cd mathua/web/next-app && npx playwright install chromium)
node scripts/browser-smoke.mjs --mathua ./mathua --output evidencias/meu-navegador.json
```

Os programas iniciam servidores com bancos temporários e os encerram ao terminar. Não usam seu progresso de estudo. O teste de navegador usa o Playwright instalado pelo próprio frontend. Neste ambiente, o download padrão do Chromium recebeu HTTP 403. A execução medida usou `@sparticuz/chromium@158.0.0` por `--chromium-module`, sem alterar as dependências do projeto. O [registro de comandos](COMANDOS-E-SAIDAS.md) mostra o caminho e a versão exatos.

## Contrato de `ungraded`

Primeiro verifique o status HTTP. Em uma resposta de submissão bem-sucedida:

| Campo recebido | Significado para a tela |
| --- | --- |
| `ungraded: true` | O corretor falhou. A resposta não foi avaliada nem contada como erro do aluno |
| `ungraded: false` ou campo ausente | A resposta foi avaliada. Leia `correct` para saber o resultado |

Com `submission_id`, o caminho normal devolve o `ResponseJSON` já gravado. Esse JSON omite `ungraded`. A devolução acontece antes do mapa JSON que contém a linha acrescentada pelo patch. A ausência foi observada na resposta bruta e o teste de reinício a registra como `ungraded_key_present_in_normal_response: false`.

A tela original já usa `if (res.ungraded)`, portanto aceita esse contrato. A decisão foi documentá-lo e manter a resposta normal gravada, incluindo a repetição idêntica para a mesma submissão. Não foi acrescentado `ungraded:false` ao histórico. O teste Go de indisponibilidade continua verificando `true` e a ausência de penalização.

## Evidências e origem

- `resultados.json`: versões, contagens, comandos e limites do teste.
- `evidencias/mathua-pilot-final.jsonl`: execução final dos 29 cenários do piloto.
- `evidencias/mathua-native-http.jsonl`: 26 testes existentes de API selecionados.
- `evidencias/mathua-native-engine.jsonl`: 154 testes existentes de domínio, agendamento e reparo.
- `evidencias/mathua-before-fix.jsonl`: falha reproduzida por ausência do campo `ungraded`, antes da correção.
- `evidencias/mathua-process-smoke.json`: verificação com dois processos independentes.
- `scripts/process-smoke.py` e `evidencias/mathua-process-script.json`: programa reproduzível e nova execução com o binário atual. O registro antigo acima foi preservado como histórico, sem afirmar que este arquivo é seu programa original.
- `scripts/browser-smoke.mjs` e `evidencias/mathua-browser-smoke.json`: teste no navegador da interface original contra a API real, sem respostas simuladas de rede.
- `evidencias/mathua-ui-build.log`: saída da compilação estática da interface, incluindo a verificação TypeScript.
- `evidencias/mathua-pilot-ui.jsonl`: nova execução dos 29 cenários após a integração visual.
- `evidencias/mathua-full-go-summary.json`: todos os resultados de pacote e a saída da falha da suíte geral. É um resumo extraído do JSON, não o log bruto completo.
- `evidencias/mathua-base-variety-20-summary.json` e `evidencias/mathua-base-variety-500-summary.json`: investigação do teste intermitente no commit-base limpo.
- `LICENSE-Mathua.txt`: licença do projeto-base.

Código-base consultado, sempre no mesmo commit:

- [Interface de geradores](https://github.com/chuma-beep/mathua/blob/2bd4a4e0e160653e274521f6de3df2e61e29c7f7/internal/generator/generator.go).
- [API de prática e submissão](https://github.com/chuma-beep/mathua/blob/2bd4a4e0e160653e274521f6de3df2e61e29c7f7/internal/server/server.go).
- [Registro de relatos](https://github.com/chuma-beep/mathua/blob/2bd4a4e0e160653e274521f6de3df2e61e29c7f7/internal/server/reports.go).
- [Revisão e reavaliação de relatos](https://github.com/chuma-beep/mathua/blob/2bd4a4e0e160653e274521f6de3df2e61e29c7f7/internal/server/adminv2.go).
- [Reparo de falsos negativos](https://github.com/chuma-beep/mathua/blob/2bd4a4e0e160653e274521f6de3df2e61e29c7f7/internal/repair/repair.go).

As contagens de 29 e 180 casos não incluem suítes-pai uma segunda vez. O resumo da suíte geral distingue resultados de pacote e eventos de teste, estes incluindo suítes-pai. A execução não avalia eficácia pedagógica com pessoas, não comprova retenção e não instala o programa no computador do usuário. A geração de famílias a partir de feedback continua fora desta entrega.
