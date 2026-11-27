# Piloto do Mathua com TypeScript

O piloto serve D01 a D15, com 46 conceitos, 74 famílias e 444 casos. O [registro do bloco final](BLOCO-4-D09-D15.md) cobre D09 a D15. O [registro dos degraus D06 a D08](BLOCO-3-D06-D08.md) descreve a correção e os testes. Os registros de [D01 a D03](BLOCO-1-D01-D03.md) e [D04 a D05](BLOCO-2-D04-D05.md) documentam as duas entregas anteriores.

Para rodar, o executável precisa do diretório `conteudo/typescript-v1` deste repositório. Ele o encontra sozinho quando o clone do Mathua está em `pilotos/mathua/mathua/`. Em outro local, use a opção `-content`.

**Rodada inicial (27/11/2026, macOS)** — a tela existente do Mathua está ajustada para estudar TypeScript. O campo de resposta não mostra mais o teclado de símbolos matemáticos. O percurso de estudo e o menu lateral estão em português. Os menus que levavam ao catálogo de matemática estão ocultos. A página de relatos mostra os relatos do visitante.

O teste de navegador no Mac passou com 14 verificações: abrir o endereço, ler a explicação, responder, receber a correção, receber uma variante após errar, avançar após os pré-requisitos, relatar uma pergunta, consultar o relato, recarregar a página e reiniciar o servidor sem perder o progresso. Os **29 cenários do piloto** e os **1885 testes unitários da interface** passaram no Mac. O registro está em [COMANDOS-E-SAIDAS-MAC.md](COMANDOS-E-SAIDAS-MAC.md).

**Linux e Mac são execuções separadas.** As execuções em Linux são da rodada de 26/11/2026 e usaram o patch anterior. Elas não foram repetidas com o patch atual. As alterações da tela desta rodada foram validadas só em macOS.

**A suíte geral não ficou integralmente aprovada na rodada em Linux.** Foram 59 pacotes aprovados, um reprovado e cinco sem testes. `TestWave23QuestionVariety` falhou por receber apenas quatro perguntas distintas em 12 sorteios. O mesmo teste também falhou no commit-base sem o patch, ao repeti-lo 500 vezes. Consulte [comandos, saídas e escopo](COMANDOS-E-SAIDAS.md). Na rodada inicial, os 180 testes existentes selecionados tinham passado. Esse resultado histórico não substitui o resultado atual da suíte geral. No Mac, o mesmo teste falhou 5 vezes em 500 execuções no commit-base limpo. A suíte geral não foi repetida no Mac com o patch atual.

Datas de referência: 26/11/2026 para as execuções em Linux e 27/11/2026 para as execuções em macOS, America/Sao_Paulo.

## O que mudou

No código Go existente, o patch acrescenta **uma linha** em `internal/server/server.go` para transmitir `ungraded` quando o corretor falha. O motor já preservava o histórico na falha do corretor. O contrato do campo opcional está documentado abaixo.

Na interface existente, o patch altera **13 arquivos** de `web/next-app` e acrescenta **um arquivo**, `web/next-app/lib/pilot.ts`. Esse arquivo lê a chave de compilação `NEXT_PUBLIC_TS_PILOT=1` e guarda os textos em português. Sem a chave, a tela se comporta como a original: os testes unitários existentes passam sem a chave, e desde 27/11/2026 as duas propriedades do botão de relato também dependem da chave. As duas mudanças no servidor Go, o campo `ungraded` e a exclusão da pergunta inteira, não dependem da chave. Com a chave, a tela muda em quatro pontos:

1. O campo de resposta deixa de mostrar o teclado de símbolos matemáticos. O componente original já tinha a opção `showPalette`; o patch só a desliga.
2. Os textos do percurso de estudo aparecem em português: campo de resposta, correção, continuar, praticar novamente, pré-requisitos e relato de problema.
3. O menu lateral deixa de mostrar o grafo de conceitos, o glossário e o grupo `Resources`, e o rodapé some. Esses itens mostravam o catálogo de matemática ou a documentação do Mathua. Continuam no menu: Estudar, Domínios, Ranking, Histórico, Relatório de progresso, Configurações e Meus relatos e avisos.
4. A página `/my-reports` passa a carregar os relatos do visitante. A API já devolvia esses relatos; a página só os pedia para usuários com conta.

As duas propriedades do `ReportButton`, que transmitem a resposta esperada e a explicação, continuam no patch. A lista de arquivos e de linhas está em `resultados.json`, no campo `mudancas`.

Há onze arquivos novos em `cmd/typescript-pilot/`, sem mudança nesta rodada além da documentação e da mensagem de compilação: os seis da versão inicial e cinco arquivos de conteúdo para carregar as explicações dos três conceitos. O comando também serve a exportação estática de `web/next-app` e redireciona `/` para a página existente `/learn`. O projeto mantém o motor, o agendamento, os pré-requisitos e o fluxo de feedback do Mathua.

A escolha foi reutilizar a tela existente. Foi necessário carregar as aulas, servir os arquivos compilados junto da API e completar os dados do botão de feedback. Os enunciados, as explicações e os controles do percurso de estudo estão em português. As páginas `/my-reports`, `/history`, `/reports`, `/domains`, `/profile` e `/settings` mantêm o texto original em inglês. O menu `Ranking` e o botão do assistente continuam visíveis. O teste cobre a página de estudo e a página de relatos do piloto, sem afirmar adaptação integral de todas as páginas do Mathua.

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

Na rodada em Linux, o navegador enviou `let limit = 14011;` e recebeu uma rejeição. A variante seguinte pediu `amount` com valor `5517`. O navegador enviou `const amount = 5517;`, recebeu aceitação e registrou um relato com essa resposta e a resposta esperada `const amount: number = 5517;`. A evidência completa está em [mathua-browser-smoke.json](evidencias/mathua-browser-smoke.json), gerada pela versão anterior do programa incluído. Na rodada em macOS, o navegador digitou `let limit = 4062;`, recebeu `✗ Ainda não.`, recebeu a variante `reviewLimit` com valor `1937` e acertou com `const reviewLimit = 1937;`. Essa evidência está em [evidencias/mac/mathua-browser-smoke.json](evidencias/mac/mathua-browser-smoke.json).

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

A partir de `pilotos/mathua/` deste repositório, use Git, npm, Go `1.26.6` e um Node compatível com a interface.

**Versão exigida.** A compilação da interface exige Node `^22.23.4 || ^24.22.1 || ^26.12.1`. A fonte é o campo `engines.node` de `web/next-app/package.json`, com `engine-strict=true` em `web/next-app/.npmrc`. As versões `24.14.1` e `26.7.0` estão fora dessa faixa. O corretor, em `cmd/typescript-pilot/package.json`, não declara faixa de Node.

**Versão testada.** No Linux, a compilação e a execução usaram Node `24.22.3`. No Mac, a compilação da interface usou Node `24.22.3` e a execução do servidor, do corretor e dos testes usou Node `24.14.1`. A versão testada não é a versão mínima: nenhuma outra versão foi testada.

Use um clone limpo no commit-base. Este patch é completo e substitui a versão anterior. Não o aplique sobre um clone que já tenha o patch antigo. O clone local `pilotos/mathua/mathua/` está excluído pelo `.gitignore` deste repositório.

```sh
git clone https://github.com/chuma-beep/mathua.git
cd mathua
git checkout 2bd4a4e0e160653e274521f6de3df2e61e29c7f7
git apply ../mathua-typescript-pilot.patch
npm ci --prefix cmd/typescript-pilot --ignore-scripts
npm ci --prefix web/next-app
NEXT_PUBLIC_TS_PILOT=1 NEXT_PUBLIC_SAME_ORIGIN_API=1 NEXT_TELEMETRY_DISABLED=1 npm run build --prefix web/next-app
go test ./cmd/typescript-pilot -count=1 -v
go build -o pilot-bin ./cmd/typescript-pilot
./pilot-bin
```

Abra `http://127.0.0.1:8081`. O endereço abre o primeiro conceito na tela de estudo. Selecione **Próximo** para começar. **Concluído** encerra uma seção da interface e não equivale ao estado `MASTERED` do motor. Use **Praticar novamente** para continuar praticando o conceito e o link do próximo conceito para avançar. No teste, seis respostas corretas por pré-requisito produziram `MASTERED`; essa observação não é uma medição de aprendizagem humana.

O executável precisa dos arquivos do clone e deve ser iniciado da raiz do Mathua com os caminhos padrão. A opção `-web` permite outro diretório de exportação. Sem a compilação da interface, o servidor inicia apenas a API e informa o comando que falta. `NEXT_PUBLIC_SAME_ORIGIN_API=1` faz a tela usar a API local na mesma origem. `NEXT_PUBLIC_TS_PILOT=1` liga os ajustes da tela para o piloto. Só os comandos `npm ci --prefix web/next-app` e `npm run build` precisam do Node da faixa exigida.

O progresso fica no SQLite `typescript-pilot.db`. Preserve também o arquivo adjacente `typescript-pilot.db.jwt` para manter os acessos após reiniciar. As opções `-addr`, `-db`, `-node`, `-grader` e `-web` estão em `cmd/typescript-pilot/README.md`.

### Executar os programas de verificação

Com o binário e a interface compilados, volte a `pilotos/mathua/`:

```sh
python3 scripts/process-smoke.py --mathua ./mathua --output evidencias/meu-reinicio.json
(cd mathua/web/next-app && npx playwright install chromium)
node scripts/browser-smoke.mjs --mathua ./mathua --output evidencias/meu-navegador.json --screenshots evidencias/minhas-capturas
```

Os programas iniciam servidores com bancos temporários e os encerram ao terminar. Não usam seu progresso de estudo. O teste de navegador usa o Playwright instalado pelo próprio frontend. Ele exige a interface compilada com `NEXT_PUBLIC_TS_PILOT=1` e falha sem essa chave; esse controle negativo está em [evidencias/mac/controle-negativo-sem-chave.json](evidencias/mac/controle-negativo-sem-chave.json). A opção `--screenshots` grava as capturas de tela. No ambiente Linux, o download padrão do Chromium recebeu HTTP 403. A execução medida em Linux usou `@sparticuz/chromium@158.0.0` por `--chromium-module`, sem alterar as dependências do projeto. O [registro de comandos em Linux](COMANDOS-E-SAIDAS.md) mostra o caminho e a versão exatos. No Mac, o Chromium `151.0.7922.34` do Playwright já estava instalado.

## Contrato de `ungraded`

Primeiro verifique o status HTTP. Em uma resposta de submissão bem-sucedida:

| Campo recebido | Significado para a tela |
| --- | --- |
| `ungraded: true` | O corretor falhou. A resposta não foi avaliada nem contada como erro do aluno |
| `ungraded: false` ou campo ausente | A resposta foi avaliada. Leia `correct` para saber o resultado |

Com `submission_id`, o caminho normal devolve o `ResponseJSON` já gravado. Esse JSON omite `ungraded`. A devolução acontece antes do mapa JSON que contém a linha acrescentada pelo patch. A ausência foi observada na resposta bruta e o teste de reinício a registra como `ungraded_key_present_in_normal_response: false`.

A tela original já usa `if (res.ungraded)`, portanto aceita esse contrato. A decisão foi documentá-lo e manter a resposta normal gravada, incluindo a repetição idêntica para a mesma submissão. Não foi acrescentado `ungraded:false` ao histórico. O teste Go de indisponibilidade continua verificando `true` e a ausência de penalização.

## Evidências e origem

- `resultados.json`: versões, contagens, comandos e limites do teste. O campo `testes_macos` guarda o Mac e o campo `testes_linux_patch_anterior` guarda o Linux.

Execuções em macOS, de 27/11/2026, com o patch atual:

- [COMANDOS-E-SAIDAS-MAC.md](COMANDOS-E-SAIDAS-MAC.md): comandos, saídas, versões testadas e versões exigidas.
- `evidencias/mac/ambiente.txt`: sistema, Go, Node da compilação, Node da execução e exigência declarada.
- `evidencias/mac/mathua-browser-smoke.json`: teste de navegador com 14 verificações.
- `evidencias/mac/capturas/`: sete capturas de tela da mesma execução.
- `evidencias/mac/controle-negativo-sem-chave.json`: o teste de navegador falha contra a interface sem a chave do piloto.
- `evidencias/mac/mathua-process-script.json`: reinício com dois processos independentes.
- `evidencias/mac/mathua-pilot.jsonl`, `mathua-native-http.jsonl` e `mathua-native-engine.jsonl`: 29, 26 e 154 casos aprovados.
- `evidencias/mac/ui-build.log`, `lint.log` e `vitest.log`: compilação, lint e testes unitários da interface.

Execuções em Linux, de 26/11/2026, com o patch anterior:

- `evidencias/mathua-pilot-final.jsonl`: execução final dos 29 cenários do piloto.
- `evidencias/mathua-native-http.jsonl`: 26 testes existentes de API selecionados.
- `evidencias/mathua-native-engine.jsonl`: 154 testes existentes de domínio, agendamento e reparo.
- `evidencias/mathua-before-fix.jsonl`: falha reproduzida por ausência do campo `ungraded`, antes da correção.
- `evidencias/mathua-process-smoke.json`: verificação com dois processos independentes.
- `scripts/process-smoke.py` e `evidencias/mathua-process-script.json`: programa reproduzível e nova execução com o binário atual. O registro antigo acima foi preservado como histórico, sem afirmar que este arquivo é seu programa original.
- `evidencias/mathua-browser-smoke.json`: teste no navegador da interface original contra a API real, sem respostas simuladas de rede. Foi gerado pela versão anterior de `scripts/browser-smoke.mjs`, com 9 verificações e rótulos em inglês.
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

As contagens de 29 e 180 casos não incluem suítes-pai uma segunda vez. O resumo da suíte geral distingue resultados de pacote e eventos de teste, estes incluindo suítes-pai. A execução não avalia eficácia pedagógica com pessoas e não comprova retenção. A instalação no Mac do usuário está em `pilotos/mathua/mathua/`, pasta ignorada pelo Git. A geração de famílias a partir de feedback continua fora desta entrega.
