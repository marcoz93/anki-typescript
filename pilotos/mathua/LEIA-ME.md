# Teste mínimo do Mathua com TypeScript

**Resultado:** a integração funcionou no recorte testado. Os **29 cenários do piloto** e **180 testes existentes selecionados** passaram, sem falhas ou casos ignorados nas execuções finais. O executável também foi iniciado, encerrado e iniciado novamente em processos independentes, preservando a autenticação e uma pergunta pendente.

Data de referência: 26/11/2026, America/Sao_Paulo.

## O que mudou

O código existente recebeu **uma linha**, em `internal/server/server.go`: o campo JSON `ungraded`, preenchido com `res.Ungraded`. O teste mostrou que o motor já deixava o histórico intacto quando o corretor falhava, mas a resposta HTTP omitia essa informação. Depois da correção, a API permite distinguir uma resposta não avaliada de uma resposta errada.

Foram acrescentados seis arquivos em `cmd/typescript-pilot/`: um comando que compõe os serviços existentes, um corretor TypeScript, os testes, a documentação e os dois arquivos de dependências npm. O comando e o corretor somam 243 linhas. Os testes somam 434 linhas. Nenhum motor de domínio, agendamento ou feedback foi reimplementado.

O patch completo está em `mathua-typescript-pilot.patch`. Sua aplicação foi verificada contra o commit-base indicado em `resultados.json`. O conteúdo TypeScript é uma adaptação própria para este teste. Não foi atribuído aos autores do Mathua nem ao Math Academy.

## Conceitos e critérios do piloto

| Conceito | Comportamento observado | Critério de aceite |
| --- | --- | --- |
| Valor e literal numérico | Representar um valor escrito por extenso | Um literal numérico do valor pedido, sem aspas ou operações |
| Tipo `number` | Identificar a palavra que nomeia o tipo numérico | Responder `number`, distinguindo nome do tipo e valor |
| Declaração `const` numérica | Criar uma constante com nome e valor determinados | Uma declaração `const`, nome correto e literal numérico correto; anotação `number` opcional |

Os dois primeiros conceitos foram configurados como pré-requisitos do terceiro. Essa relação é uma decisão pedagógica do piloto. Não é uma afirmação de necessidade lógica nem uma reorganização de todo o material original.

O motor nativo marcou cada pré-requisito como `MASTERED` após as seis respostas distintas submetidas na simulação. Uma resposta isolada não produziu esse estado. O estado é a classificação do sistema segundo suas regras atuais; este teste não mede domínio real de um aluno.

## Caso concreto executado

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

A partir da pasta extraída, com Git, Node.js, npm e a versão de Go declarada no `go.mod` do projeto:

```sh
git clone https://github.com/chuma-beep/mathua.git
cd mathua
git checkout 2bd4a4e0e160653e274521f6de3df2e61e29c7f7
git apply ../mathua-typescript-pilot.patch
npm ci --prefix cmd/typescript-pilot --ignore-scripts
go test ./cmd/typescript-pilot -count=1 -v
go run ./cmd/typescript-pilot
```

A documentação em `cmd/typescript-pilot/README.md` descreve as rotas usadas e as opções do comando. O piloto usa o servidor e os endpoints existentes, com autenticação e SQLite. A integração visual com a interface do Mathua e a implantação externa não fazem parte do resultado validado.

## Evidências e origem

- `resultados.json`: versões, contagens, comandos e limites do teste.
- `evidencias/mathua-pilot-final.jsonl`: execução final dos 29 cenários do piloto.
- `evidencias/mathua-native-http.jsonl`: 26 testes existentes de API selecionados.
- `evidencias/mathua-native-engine.jsonl`: 154 testes existentes de domínio, agendamento e reparo.
- `evidencias/mathua-before-fix.jsonl`: falha reproduzida por ausência do campo `ungraded`, antes da correção.
- `evidencias/mathua-process-smoke.json`: verificação com dois processos independentes.
- `LICENSE-Mathua.txt`: licença do projeto-base.

Código-base consultado, sempre no mesmo commit:

- [Interface de geradores](https://github.com/chuma-beep/mathua/blob/2bd4a4e0e160653e274521f6de3df2e61e29c7f7/internal/generator/generator.go).
- [API de prática e submissão](https://github.com/chuma-beep/mathua/blob/2bd4a4e0e160653e274521f6de3df2e61e29c7f7/internal/server/server.go).
- [Registro de relatos](https://github.com/chuma-beep/mathua/blob/2bd4a4e0e160653e274521f6de3df2e61e29c7f7/internal/server/reports.go).
- [Revisão e reavaliação de relatos](https://github.com/chuma-beep/mathua/blob/2bd4a4e0e160653e274521f6de3df2e61e29c7f7/internal/server/adminv2.go).
- [Reparo de falsos negativos](https://github.com/chuma-beep/mathua/blob/2bd4a4e0e160653e274521f6de3df2e61e29c7f7/internal/repair/repair.go).

As contagens não incluem suítes-pai uma segunda vez. A execução cobre o recorte descrito; não é a suíte completa do repositório nem uma avaliação da eficácia pedagógica com pessoas.
