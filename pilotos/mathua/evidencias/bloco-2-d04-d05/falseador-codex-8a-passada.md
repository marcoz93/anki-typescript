# Relatório do falseador, oitava passada (Codex, somente leitura)

Execução: 27/11/2026, sobre o commit 19ecf5f. O texto abaixo é a saída do Codex, sem edição além da troca do caminho da pasta pessoal. Foram 69 comandos; o relatório traz o comando e a saída de cada achado, e não todos os comandos.

Sim. Confirmei um achado novo de severidade média em `main@19ecf5f`. Nenhum de severidade alta.

## ACHADOS CONFIRMADOS

1. **Média. F005, F006, F007 e F012 aprovam respostas com comentário sem fechamento.** O scanner do TypeScript emitiu `TS1010` nas oito respostas. O corretor deu nota 1 a todas. Isso contraria a exigência de comparar o conteúdo sintático relevante. [Contrato de correção, linha 20](<repositório>/conteudo/typescript-v1/CONTRATO-DE-CORRECAO.md:20)

   Comando executado

   ```sh
   rtk proxy node -e 'const {families}=require("./conteudo/typescript-v1/exercicios.json"),p="./pilotos/mathua/mathua/cmd/typescript-pilot/",ts=require(p+"node_modules/typescript"),{grade}=require(p+"grade.cjs");
   for(const n of [5,6,7,12])for(const c of families[n-1].cases.slice(4,6)){
    const expected=c.answer,answer=expected+" /* tipo",diagnostics=[];
    const s=ts.createScanner(ts.ScriptTarget.ES2022,true,ts.LanguageVariant.Standard,answer,d=>diagnostics.push(d.code));
    while(s.scan()!==ts.SyntaxKind.EndOfFileToken){}
    console.log(JSON.stringify({id:c.id,answer,diagnostics,...grade({family:families[n-1].id,mode:"token",expected,answer})}));
   }'
   ```

   Saída

   ```text
   {"id":"F005-V4","answer":"number /* tipo","diagnostics":[1010],"correct":true,"score":1,"feedback":"Correto."}
   {"id":"F005-V5","answer":"number /* tipo","diagnostics":[1010],"correct":true,"score":1,"feedback":"Correto."}
   {"id":"F006-V4","answer":"string /* tipo","diagnostics":[1010],"correct":true,"score":1,"feedback":"Correto."}
   {"id":"F006-V5","answer":"string /* tipo","diagnostics":[1010],"correct":true,"score":1,"feedback":"Correto."}
   {"id":"F007-V4","answer":"boolean /* tipo","diagnostics":[1010],"correct":true,"score":1,"feedback":"Correto."}
   {"id":"F007-V5","answer":"boolean /* tipo","diagnostics":[1010],"correct":true,"score":1,"feedback":"Correto."}
   {"id":"F012-V4","answer":": /* tipo","diagnostics":[1010],"correct":true,"score":1,"feedback":"Correto."}
   {"id":"F012-V5","answer":": /* tipo","diagnostics":[1010],"correct":true,"score":1,"feedback":"Correto."}
   ```

2. **Baixa. A seção 8 enumera três casos com testes da mensagem de recusa.** `satisfies` é o quarto caso e tem dois testes. Isso contradiz a frase “Três deles têm teste da mensagem de recusa atual”. [Bloco 2, linha 239](<repositório>/pilotos/mathua/BLOCO-2-D04-D05.md:239)

   Comando executado

   ```sh
   rtk proxy rg -n 'Três deles têm teste da mensagem|f02[13]_satisfies_is_named_as_satisfies' pilotos/mathua/BLOCO-2-D04-D05.md pilotos/mathua/mathua/cmd/typescript-pilot/main_test.go
   ```

   Saída

   ```text
   pilotos/mathua/BLOCO-2-D04-D05.md:239:Nenhum destes casos tem teste que force a aceitação ou a recusa como regra do contrato. Três deles têm teste da mensagem de recusa atual: `as const`, a conta no lugar do valor e as comparações dentro do `&&`. O comportamento atual está indicado. A decisão é de quem escreve o conteúdo.
   pilotos/mathua/mathua/cmd/typescript-pilot/main_test.go:1089:		{"f021_satisfies_is_named_as_satisfies", "F021", "", expense, expense[:len(expense)-1] + " satisfies { id: string; total: number };", false, "satisfies"},
   pilotos/mathua/mathua/cmd/typescript-pilot/main_test.go:1090:		{"f023_satisfies_is_named_as_satisfies", "F023", "", "const totals = [18000, 4000, 12000];", "const totals = [18000, 4000, 12000] satisfies number[];", false, "satisfies"},
   ```

## CORREÇÕES CONFERIDAS

- **Tokens.** As oito respostas originais com `/* tipo */` receberam nota 1. `Number` e `number string` receberam nota 0.
- **Recuperação.** No ensaio React, F002-V1 recebeu 409. A substituta foi F002-V4, com F002-V5 na fila. Ambas receberam 200. F002-V3 ficou fora da fila nas duas ordens de chegada testadas.
- **`satisfies`.** F021-V2 e F023-V2 receberam nota 0. As duas mensagens citaram “o operador satisfies”. [Comandos originais da sétima passada](<repositório>/pilotos/mathua/evidencias/bloco-2-d04-d05/falseador-codex-7a-passada.md)

## TENTATIVAS QUE NÃO ACHARAM PROBLEMA

- **F001–F025.** Testei os 50 casos reais V4 e V5, com gabarito e quatro variações por caso. Foram 144 aprovações e 106 recusas. Todos os gabaritos passaram. Fora as oito aprovações do achado 1, não observei divergência de veredito nem feedback que atribuísse uma causa ausente da resposta.
- **Candidatas.** Em 3.829.849 pares de histórico e fila, `pilotExclude` sempre deixou ao menos uma candidata e excluiu a última exibida. `pilotFresh` e `pilotAdmit` esvaziaram lotes nos controles. Com a fila vazia e o servidor simulado respeitando as exclusões, `pilotUsable` devolveu uma candidata diferente da última nas 11.742 buscas.
- **Fila em React.** Conferi as duas chamadas diretas de `pilotAdmit` e a chamada via `pilotUsable`. Em 168 envios de F016 e F017 com HTTP simulado, não houve repetição consecutiva nem encerramento por falta de candidata.
- **Sem a flag.** Em JSDOM, a base do Mathua e o `LearnStepper` atual produziram HTML idêntico em 14 estados. Coincidiram cinco buscas, seis envios, os links e os dados passados ao botão de relato.
- **Seção 2.** O patch versionado tem 23 arquivos, 3.014 adições e 123 remoções. O diff rastreado de `web internal` tem 14 arquivos, 209 adições e 123 remoções. Os SHA-256 atual e históricos conferiram. A checagem inversa do patch saiu com código 0.
- **Seção 4.** Recontei 475, 26 e 154 testes-folha Go aprovados, sem falhas ou pulos. Os registros mostram 199 arquivos e 1.897 testes Vitest aprovados, 12 testes dos helpers, zero erros de lint, `exit_tsc=0` e build concluído. O navegador registrou 23 verificações aprovadas, 10 capturas e zero erros. O reinício registrou dois processos e `passed: true`.
- **Seção 7 e `resultados.json`.** Recontei 8, 5, 4, 3, 3, 1 e 3 achados nos sete relatórios. As 30 correções documentadas e as nove decisões em aberto conferiram.

## NÃO VERIFICADO

- Novo build sem a flag, nova execução das suítes completas e frequência de repetições ou de HTTP 409 no navegador com servidor real. Usei ensaios em memória e os registros existentes para preservar o modo somente leitura.
- Totais históricos de comandos e execuções do Vitest, taxa de falha intermitente e tempo de partida. Os registros disponíveis não permitem recontá-los.
- Data da nova execução do ensaio de reinício. O JSON não traz data e é idêntico ao de `c7f3c85`.
