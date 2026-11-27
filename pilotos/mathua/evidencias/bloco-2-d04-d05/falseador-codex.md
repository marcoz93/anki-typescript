# Relatório do falseador (Codex, somente leitura)

Execução: 27/11/2026, sobre os commits 3d1fdc4 (bloco 1) e c7f3c85 (bloco 2). O texto abaixo é a saída do Codex, sem edição além da troca do caminho da pasta pessoal.
Uma primeira tentativa foi recusada pelo filtro de segurança do Codex, porque o pedido usava vocabulário de teste de invasão. O pedido foi reescrito como revisão de qualidade.

## ACHADOS CONFIRMADOS

Comandos executados na raiz de `anki-typescript`, em modo somente leitura.

1. **Média — F002-V1 aprova uma resposta que o TypeScript rejeita.** A diretiva referencia uma biblioteca inexistente. O corretor dá nota 1 e o TypeScript 5.9.3 emite `TS2726`. Isso contraria a exigência de compilação em modo estrito do `CONTRATO-DE-CORRECAO.md`, linha 40.

   ```sh
   rtk proxy node -e 'const p="./pilotos/mathua/mathua/cmd/typescript-pilot/",g=require(p+"grade.cjs");
   const {families}=require("./conteudo/typescript-v1/exercicios.json");
   function job(f,v,answer){const k=families[f-1].cases[v];return {family:families[f-1].id, mode:families[f-1].mode, expected:k.answer, context_code:k.context_code, code_form:k.code_form, answer};}
   const ts=require(p+"node_modules/typescript"), file="/__qa_answer__.ts";
   function check(j){
    const opts={strict:true,noEmit:true,types:[],target:ts.ScriptTarget.ES2022}, host=ts.createCompilerHost(opts), read=host.getSourceFile.bind(host);
    host.getSourceFile=(name,v)=>name===file?ts.createSourceFile(name,j.context_code+"\n"+j.answer,v,true):read(name,v);
    console.log(j.family,JSON.stringify(g.grade(j)),"tsc="+JSON.stringify(ts.getPreEmitDiagnostics(ts.createProgram([file],opts,host)).map(d=>d.code)));
   }
   check(job(2,1,"/// <reference lib=\"invalidlib\" />\n18_000"));'
   ```

   ```text
   F002 {"correct":true,"score":1,"feedback":"Correto. O literal representa o valor solicitado."} tsc=[2726]
   ```

2. **Média — Quatro variantes recusam código válido.** F010-V1 e F011-V2 têm anotações compatíveis. F021-V1 cria as duas propriedades pedidas, e F022-V2 acessa a chave textual pedida com colchetes. As quatro respostas compilam com o contexto real do caso. As recusas contrariam o `CONTRATO-DE-CORRECAO.md`, linhas 49 e 53.

   ```sh
   rtk proxy node -e 'const p="./pilotos/mathua/mathua/cmd/typescript-pilot/",g=require(p+"grade.cjs");
   const {families}=require("./conteudo/typescript-v1/exercicios.json");
   function job(f,v,answer){const k=families[f-1].cases[v];return {family:families[f-1].id, mode:families[f-1].mode, expected:k.answer, context_code:k.context_code, code_form:k.code_form, answer};}
   const ts=require(p+"node_modules/typescript"), file="/__qa_answer__.ts";
   function check(j){
    const opts={strict:true,noEmit:true,types:[],target:ts.ScriptTarget.ES2022}, host=ts.createCompilerHost(opts), read=host.getSourceFile.bind(host);
    host.getSourceFile=(name,v)=>name===file?ts.createSourceFile(name,j.context_code+"\n"+j.answer,v,true):read(name,v);
    console.log(j.family,JSON.stringify(g.grade(j)),"tsc="+JSON.stringify(ts.getPreEmitDiagnostics(ts.createProgram([file],opts,host)).map(d=>d.code)));
   }
   check(job(10,1,"const total: 18000 = 18_000;"));
   check(job(11,2,"const id: (string) = \"reembolso-21\";"));
   check(job(21,1,"const expense = { [\"id\"]: \"r11\", total: 18000 };"));
   check(job(22,2,"request[(\"value\")]"));'
   ```

   ```text
   F010 {"correct":false,"score":0,"feedback":"Neste exercício, omita a anotação ou use number."} tsc=[]
   F011 {"correct":false,"score":0,"feedback":"Neste exercício, omita a anotação ou use string."} tsc=[]
   F021 {"correct":false,"score":0,"feedback":"O objeto deve ter exatamente as propriedades id e total."} tsc=[]
   F022 {"correct":false,"score":0,"feedback":"Escreva o acesso à propriedade value, com ponto ou com colchetes e o nome entre aspas."} tsc=[]
   ```

3. **Média — F021-V1 atribui a recusa a um valor errado.** `12000 + 6000` dá os `18000` pedidos. A mensagem contradiz a linha 76 do contrato. O `BLOCO-2-D04-D05.md`, linha 144, já registra a imprecisão.

   ```sh
   rtk proxy node -e 'const p="./pilotos/mathua/mathua/cmd/typescript-pilot/",g=require(p+"grade.cjs");
   const {families}=require("./conteudo/typescript-v1/exercicios.json");
   function job(f,v,answer){const k=families[f-1].cases[v];return {family:families[f-1].id, mode:families[f-1].mode, expected:k.answer, context_code:k.context_code, code_form:k.code_form, answer};}
   console.log(JSON.stringify(g.grade(job(21,1,"const expense = { id: \"r11\", total: 12000 + 6000 };"))));'
   ```

   ```text
   {"correct":false,"score":0,"feedback":"A propriedade total não tem o valor solicitado."}
   ```

4. **Média — F002-V1 termina sem veredito para uma resposta abaixo do limite.** Com 2.805 caracteres, o corretor sai com código 1. Pelo contrato, linha 78, isso vira falha técnica. O critério de F002 na linha 48 pede um literal, e o corretor deveria conseguir rejeitar a resposta por sua forma.

   ```sh
   rtk proxy node -e 'const p="./pilotos/mathua/mathua/cmd/typescript-pilot/",g=require(p+"grade.cjs");
   const {families}=require("./conteudo/typescript-v1/exercicios.json");
   function job(f,v,answer){const k=families[f-1].cases[v];return {family:families[f-1].id, mode:families[f-1].mode, expected:k.answer, context_code:k.context_code, code_form:k.code_form, answer};}
   const {spawnSync}=require("node:child_process");
   for(const answer of ["","x".repeat(5000),"(".repeat(1400)+"18000"+")".repeat(1400)]){
    const r=spawnSync(process.execPath,[p+"grade.cjs"],{input:JSON.stringify(job(2,1,answer)),encoding:"utf8"});
    console.log(JSON.stringify([answer.length,r.status,r.stdout||r.stderr]));
   }'
   ```

   ```text
   [0,0,"{\"correct\":false,\"score\":0,\"feedback\":\"Digite a resposta solicitada.\"}"]
   [5000,0,"{\"correct\":false,\"score\":0,\"feedback\":\"A resposta excede o tamanho deste exercício.\"}"]
   [2805,1,"Maximum call stack size exceeded\n"]
   ```

5. **Média — `pilotExclude` pode esgotar os candidatos ou deixar apenas a última pergunta.** `Generate` usa o tamanho real da família. A tela usa seis como constante. Nos cenários sintéticos abaixo, cinco casos já vistos deixam zero candidatos. Com cinco casos na fila e `A` recém-errada, sobra apenas `A`. Uma fila com os seis casos exclui todos. Nessa condição, o servidor devolve o lote original e `pilotFresh` pode esvaziá-lo. Isso contraria a garantia de `pilot.ts`, linhas 35–39, de excluir cinco e deixar um caso diferente do recém-errado.

   ```sh
   rtk proxy node -e 'const {pilotExclude,pilotFresh}=require("./pilotos/mathua/mathua/web/next-app/lib/pilot.ts");
   for(const [bank,shown,buffer] of [
    [["A","B","C","D","E"],["A","B","C","D","E"],[]],
    [["A","B","C","D","E","F"],["A"],["B","C","D","E","F"]],
    [["A","B","C","D","E","F"],[],["A","B","C","D","E","F"]]
   ]){
    const exclude=pilotExclude(shown,buffer);
    console.log(JSON.stringify({exclude,candidates:bank.filter(q=>!exclude.includes(q)),afterFallback:pilotFresh(bank.map(question=>({question})),buffer).map(q=>q.question)}));
   }'
   ```

   ```text
   {"exclude":["A","B","C","D","E"],"candidates":[],"afterFallback":["A","B","C","D","E"]}
   {"exclude":["B","C","D","E","F"],"candidates":["A"],"afterFallback":["A"]}
   {"exclude":["A","B","C","D","E","F"],"candidates":[],"afterFallback":[]}
   ```

   ```sh
   rtk proxy rg -n '^\s*excluded\[ex\] = true|^\s*fresh = problems' pilotos/mathua/mathua/internal/server/server.go
   ```

   ```text
   2157:		excluded[ex] = true
   2253:		fresh = problems
   ```

6. **Média — Duas buscas sobrepostas fazem a tela repetir imediatamente um caso.** Executei `refill` e `takeNext` do `LearnStepper` em memória com os seis casos reais de F002 e respostas HTTP simuladas. Cada busca deduplicou contra a fila que viu ao iniciar. As duas juntas colocaram `F002-V5` em posições consecutivas. Isso contraria a exigência de mudar o caso após erro, na linha 80 do contrato.

   ```sh
   rtk proxy node -e 'const fs=require("node:fs"), p="./pilotos/mathua/mathua/";
   const ts=require(p+"cmd/typescript-pilot/node_modules/typescript");
   process.env.NEXT_PUBLIC_TS_PILOT="1";
   const pilot=require(p+"web/next-app/lib/pilot.ts");
   const src=fs.readFileSync(p+"web/next-app/components/LearnStepper.tsx","utf8");
   const refill=src.slice(src.indexOf("  const refill = "),src.indexOf("  const load = ")).replace("useCallback(","(").replace("}, [conceptId])","})");
   const take=src.slice(src.indexOf("  async function takeNext("),src.indexOf("  function appendAfter("));
   const {cases}=require("./conteudo/typescript-v1/exercicios.json").families.find(f=>f.id==="F002");
   const bank=cases.map(c=>({question:c.prompt,id:c.id}));
   const harness=`
   const {TS_PILOT,pilotExclude,pilotFresh}=pilot;
   const conceptId="ts.value.numeric_literal", difficulty=0.4, kpIndex=0;
   const bufferRef={current:bank.slice(1,3)}, seenRef={current:bank.slice(0,3).map(q=>q.question)};
   const history=[bank[0]], shownRef={current:new Map([[1,[bank[0].question]]])};
   const practiceEpochRef={current:1}, pending=[];
   let buffer=bufferRef.current;
   const setBuffer=v=>{buffer=typeof v==="function"?v(buffer):v};
   const getLessonPractice=(_id,_count,{exclude})=>new Promise(resolve=>pending.push(order=>{
    const fresh=order.map(i=>bank[i]).filter(q=>!exclude.includes(q.question));
    console.log("retorno",fresh.map(q=>q.id).join(" "));
    resolve({questions:fresh.slice(0,3)});
   }));
   ${refill}
   ${take}
   async function next(){
    bufferRef.current=buffer;
    const q=await takeNext(difficulty);
    history.push(q);
    shownRef.current.set(1,history.map(q=>q.question));
   }
   return (async()=>{
    await next(); await next();
    pending.shift()([3,4,5,0,1,2]);
    pending.shift()([5,3,4,0,1,2]);
    await new Promise(setImmediate);
    console.log("fila",buffer.map(q=>q.id).join(" "));
    for(let i=0;i<4;i++) await next();
    console.log("exibidas após erros",history.map(q=>q.id).join(" "));
   })();
   `;
   new Function("pilot","bank",ts.transpileModule(harness,{compilerOptions:{target:ts.ScriptTarget.ES2022}}).outputText)(pilot,bank);'
   ```

   ```text
   retorno F002-V3 F002-V4 F002-V5
   retorno F002-V5 F002-V3 F002-V4
   fila F002-V3 F002-V4 F002-V5 F002-V5 F002-V3 F002-V4
   exibidas após erros F002-V0 F002-V1 F002-V2 F002-V3 F002-V4 F002-V5 F002-V5
   ```

7. **Baixa — O patch do Bloco 1 altera `/my-reports`.** O `BLOCO-1-D01-D03.md`, linha 189, afirma que o patch não altera a página. O trecho está no patch de `3d1fdc4` e é idêntico ao de `83a1aff`. A alteração veio do commit anterior.

   ```sh
   rtk proxy node -e 'const {execFileSync}=require("node:child_process");
   const page="diff --git a/web/next-app/app/my-reports/page.tsx";
   const get=commit=>execFileSync("rtk",["proxy","git","show",commit+":pilotos/mathua/mathua-typescript-pilot.patch"],{encoding:"utf8",stdio:["ignore","pipe","pipe"]}).split(/(?=^diff --git )/m).find(p=>p.startsWith(page));
   const before=get("83a1aff"), bloco=get("3d1fdc4");
   console.log(JSON.stringify({arquivoAlterado:!!bloco,mesmoDiffDoCommitAnterior:!!before&&before===bloco}));'
   ```

   ```text
   {"arquivoAlterado":true,"mesmoDiffDoCommitAnterior":true}
   ```

8. **Baixa — O Bloco 2 remete a uma seção ausente.** A linha 7 diz que o resultado da revisão está na seção 7. A linha 131 remete a uma seção “Falseador” no fim do documento. A busca pelos títulos e pela remissão encontrou apenas a remissão.

   ```sh
   rtk proxy rg -n '^Preenchida|^(##|###).*Falseador' pilotos/mathua/BLOCO-2-D04-D05.md
   ```

   ```text
   131:Preenchida depois da revisão do Codex. Ver a seção "Falseador" ao fim deste documento.
   ```

## TENTATIVAS QUE NÃO ACHARAM PROBLEMA

- Os 150 gabaritos de F001–F025 foram aceitos. O lote produziu zero erros técnicos.
- Instrução extra, segunda declaração, `as any` no operando, comparação redundante e `@ts-ignore` sobre anotação incompatível foram recusados nas sondagens.
- Comentário comum, vírgula final, propriedade reordenada, limite invertido com separador numérico e acesso direto por colchetes foram aceitos.
- `?.` e crase como chave foram recusados nas formas ensaiadas. A aceitação de anotação `any` em F021 e F023 coincide com a ambiguidade já registrada no Bloco 2.
- Respostas vazia e de 5.000 caracteres retornaram `correct:false` com código de saída 0.
- Reconstituí `questionText` e `expectedText` com os dados servidos. Encontrei 150 enunciados distintos por conceito e 58 reutilizações da chave de gabarito, sem colisão de tarefa segundo `newExercise`.
- A busca pelos diretórios ancestrais, reconstituída a partir da pasta do piloto, localizou `conteudo/typescript-v1` com os dois JSONs.
- Com a flag ausente, `pt` preservou o texto em inglês e `pilotDiagnosis` preservou o diagnóstico original. As chamadas novas de exclusão do cliente estão condicionadas à flag. A exclusão integral na rota Go é incondicional, conforme o código do achado 5.
- Recontei 57 testes-folha do piloto no Bloco 1 e 435 no Bloco 2. Cada bloco tem 26 testes HTTP e 154 do motor. Zero falhas ou pulos nos seis JSONL.
- Os registros de navegador têm 16 e 23 verificações e 8 e 10 capturas. Os SHA-256 do conteúdo e dos patches conferem com os documentos.

## NÃO VERIFICADO

- Frequência da repetição em navegador real, comportamento de uma compilação nova sem a flag e execução ponta a ponta com famílias de tamanho diferente. As sondagens de fila usaram cenários em memória.
- Nova execução das suítes Go e dos testes de reinício e navegador. Esses fluxos gravam artefatos ou bancos. Conferi os registros existentes.
