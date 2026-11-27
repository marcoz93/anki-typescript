# Relatório do falseador, sexta passada (Codex, somente leitura)

Execução: 27/11/2026, sobre o commit 5600fb0. O texto abaixo é a saída do Codex, sem edição além da troca do caminho da pasta pessoal. Foram 120 comandos; o relatório traz o comando e a saída do achado, e não todos os comandos.

Sim. Confirmei um achado novo de severidade média em `main@5600fb0`.

## ACHADOS CONFIRMADOS

1. **Média. A recuperação de HTTP 409 pode mostrar quatro substitutas que também recebem 409.** Em React com HTTP simulado, expirei os registros da pergunta na tela e das quatro na fila. A tela passou de V1 a V5, todas sem registro. Só a quinta substituta, V0, tinha registro. Isso contraria o fluxo documentado de servir novamente a pergunta após o 409, operação que grava o registro usado na correção. [Fluxo do Mathua](<repositório>/pilotos/mathua/mathua/docs/system-design.md:497)

   **Comando**

   ````sh
   rtk proxy node -e 'const fs=require("node:fs");
   const report=fs.readFileSync("pilotos/mathua/evidencias/bloco-2-d04-d05/falseador-codex-5a-passada.md","utf8");
   let js=report.split("   ```sh\n")[1].split("   ```")[0];
   js=js.slice(js.indexOf("const fs"),js.lastIndexOf(String.fromCharCode(39)));
   js=js.replace("const ctl={},ids=", "const anchors=new Set(),ctl={},ids=")
    .replace("return {questions};","questions.forEach(q=>anchors.add(q.question)); return {questions};")
    .replace("const submitStudyAnswer=async()=>{throw {status:409}};", "const submitStudyAnswer=async(_,answer,t,q)=>{console.log(\"envio\",bank.find(b=>b.question===q).id,409);if(anchors.has(q))throw new Error(\"registro inesperado\");throw {status:409}};")
    .replace("ctl.check=()=>handleCheck(2);","ctl.type=()=>setEntry(2,{answer:\"0\"}); ctl.check=()=>handleCheck(2); ctl.anchored=()=>anchors.has(entries.at(-1).q.question);")
    .replaceAll("\"ctl\",ts.transpileModule","\"ctl\",\"anchors\",ts.transpileModule")
    .replace("bank,fetch,ctl);","bank,fetch,ctl,anchors);")
    .replace(/console.log\("antes".*?await act\(\(\)=>root.unmount\(\)\);/s,
    "anchors.clear(); for(let i=0;i<5&&!ctl.anchored();i++){await act(()=>ctl.type());await act(()=>ctl.check());console.log(\"substituta\",ctl.read().naTela,\"com registro\",ctl.anchored());} await act(()=>root.unmount());");
   new Function("require",js)(require);'
   ````

   **Saída**

   ```text
   {"excluidas":["F002-V0","F002-V1","F002-V2"],"servidor":["F002-V3","F002-V4","F002-V5"]}
   envio F002-V1 409
   substituta F002-V2 com registro false
   envio F002-V2 409
   substituta F002-V3 com registro false
   envio F002-V3 409
   {"excluidas":["F002-V3","F002-V2","F002-V4","F002-V5","F002-V1"],"servidor":["F002-V0"]}
   substituta F002-V4 com registro false
   envio F002-V4 409
   {"excluidas":["F002-V4","F002-V3","F002-V5","F002-V2","F002-V1"],"servidor":["F002-V0"]}
   substituta F002-V5 com registro false
   envio F002-V5 409
   {"excluidas":["F002-V5","F002-V4","F002-V0","F002-V3","F002-V2"],"servidor":["F002-V1"]}
   substituta F002-V0 com registro true
   ```

## CORREÇÕES CONFERIDAS

- No cenário original de 409, V2 substituiu V1 pela fila. V3, V4 e V5 ficaram na fila. A recuperação não abriu outra busca.
- `let amounts = 15000;` e `let totals = 18000;` receberam nota 0 com o feedback “O valor inicial deve ser um array, entre colchetes, com os elementos pedidos.”
- A seção 7 agora informa que o primeiro relatório traz nove blocos de comando. Recontei nove blocos e nove invocações de `rtk`.

## TENTATIVAS QUE NÃO ACHARAM PROBLEMA

- F001 a F025, casos V0 e V1, com gabarito e quatro variações por caso. Das 250 respostas, 146 foram aceitas e 104 recusadas. Os 50 gabaritos passaram. Nenhum veredito divergiu da rubrica e nenhuma recusa atribuiu uma causa ausente da resposta.
- Em 3.829.849 pares de histórico e fila, `pilotExclude` sempre deixou pelo menos uma candidata e excluiu a última exibida. `pilotFresh` e `pilotAdmit` puderam esvaziar um lote. `pilotUsable` recuperou uma questão anterior e devolveu vazio quando recebeu só a última exibida.
- Nos ensaios React com busca atrasada e com fila vazia, nenhuma pergunta apareceu duas vezes seguidas. A busca com fila vazia exibiu V3, enfileirou V4 e V5 e manteve a seção aberta.
- Sem `NEXT_PUBLIC_TS_PILOT`, a base e a versão atual produziram o mesmo HTML nos cinco estados amostrados em JSDOM. Coincidiram três buscas, dois envios e o JSON do relato. O destino amostrado foi `/graph`.
- Seção 2. Recontei 23 arquivos, 2.962 adições e 122 remoções no patch. O diff rastreado de `web internal` teve 14 arquivos, 200 adições e 122 remoções. Os seis SHA-256 conferiram e a checagem inversa saiu com código 0.
- Seção 4 e `resultados.json`. Recontei 467, 26 e 154 testes-folha Go aprovados, sem falhas nem pulos. A API registrou 23 conceitos com seis casos distintos cada. O navegador registrou 23 verificações, dez capturas e nove conceitos. O registro de reinício indica dois processos.
- Seções 4 e 7. Os registros mostram 199 arquivos e 1.897 testes Vitest aprovados, zero erros de lint, `exit_tsc=0` e build concluído. Recontei 12 testes dos helpers, 8, 5, 4, 3 e 3 achados nas cinco passadas, 26 correções documentadas e oito decisões em aberto.

## NÃO VERIFICADO

- Incidência da sequência de 409 com servidor e navegador reais, e equivalência visual de um novo build sem a flag. Os ensaios usaram JSDOM e HTTP simulado. As suítes completas foram conferidas pelos registros gravados.
- Totais históricos de comandos, número de execuções do Vitest e tempo de partida de 14,3 segundos. Os registros disponíveis não permitem recontá-los.
- Nova execução do teste de reinício. O JSON em `5600fb0` é idêntico ao de `c7f3c85` e não contém data de execução.
