# Relatório do falseador, nona passada (Codex, somente leitura)

Execução: 27/11/2026, sobre o commit 6ae97ab. O texto abaixo é a saída do Codex, sem edição além da troca do caminho da pasta pessoal. Foram 121 comandos; o relatório traz o comando e a saída do achado, e não todos os comandos.

Não encontrei achado novo de severidade alta ou média em `main@6ae97ab`. Confirmei um achado baixo.

## ACHADOS CONFIRMADOS

1. **Baixa.** O comentário de `pilotFresh` diz que o servidor repete perguntas dentro do lote quando restam poucos casos. O gerador elimina duplicatas antes de o servidor aplicar as exclusões. Nas 20 buscas registradas com cinco exclusões, cada lote trouxe uma única pergunta. [Comentário em pilot.ts](<repositório>/pilotos/mathua/mathua/web/next-app/lib/pilot.ts:54) · [Deduplicação no gerador](<repositório>/pilotos/mathua/mathua/internal/generator/registry.go:198)

   Comando executado

   ```sh
   rtk proxy node -e 'const {practice_fetches:f}=require("./pilotos/mathua/evidencias/bloco-2-d04-d05/mathua-browser-smoke.json");const capped=f.filter(x=>x.excluded===5);console.log(JSON.stringify({lotes:f.length,com_repeticao:f.filter(x=>new Set(x.served).size<x.served.length).length,com_cinco_exclusoes:capped.length,com_uma_questao:capped.filter(x=>x.served.length===1).length}));'
   ```

   Saída

   ```text
   {"lotes":60,"com_repeticao":0,"com_cinco_exclusoes":20,"com_uma_questao":20}
   ```

## CORREÇÕES CONFERIDAS

- **Comentários sem fechamento.** As oito respostas originais de F005, F006, F007 e F012 ainda geram `TS1010`. Todas agora recebem `correct:false`, nota 0 e “A resposta contém um erro de sintaxe TypeScript.”
- **Contagem da seção 8.** O texto lista quatro casos. Localizei seis testes de mensagem que cobrem os quatro casos.

## TENTATIVAS QUE NÃO ACHARAM PROBLEMA

- **F001–F025.** Testei V0 e V1, com gabarito e quatro variações por caso. Foram 250 respostas, 140 aprovações e 110 recusas. Os 50 gabaritos passaram. Nenhum veredito divergiu da rubrica e nenhuma mensagem atribuiu uma causa ausente.
- **Fila com seis casos.** Em 3.829.849 pares de histórico e fila, `pilotExclude` sempre preservou uma candidata e excluiu a última exibida. `pilotFresh` e `pilotAdmit` esvaziaram lotes nos controles. A tela continuou com uma pergunta disponível após 52 envios simulados em F016 e F017, sem repetição consecutiva, inclusive com uma busca atrasada.
- **Sem `NEXT_PUBLIC_TS_PILOT`.** A versão-base e a atual produziram HTML idêntico nos 18 estados amostrados em JSDOM. Coincidiram cinco buscas, oito envios e os dados entregues ao botão de relato.
- **Seção 2.** O patch versionado tem 23 arquivos, 3.025 adições e 123 remoções. O diff rastreado de `web internal` tem 14 arquivos, 209 adições e 123 remoções. Os SHA-256 conferiram. A checagem inversa saiu com código 0.
- **Seção 4 e `resultados.json`.** Recontei 478, 26 e 154 testes-folha Go aprovados, sem falhas ou pulos. Os registros também mostram 1.897 testes Vitest aprovados em 199 arquivos, 23 verificações de navegador, 10 capturas e dois processos no ensaio de reinício.
- **Seção 7 e `resultados.json`.** Recontei 8, 5, 4, 3, 3, 1, 3 e 2 achados nas oito passadas. As 32 correções documentadas e as nove decisões em aberto conferiram.

## NÃO VERIFICADO

- Novo build sem a flag, nova execução das suítes completas e fluxo em navegador com servidor real. Usei ensaios em memória e registros versionados. O sandbox recusou a abertura de uma porta local com `EPERM`.
- Totais históricos de comandos, frequência da falha intermitente do Vitest, tempo de partida e data do ensaio de reinício. Os registros disponíveis não permitem recontar ou datar esses itens.
