# Relatório do falseador, quarta passada (Codex, somente leitura)

Execução: 27/11/2026, sobre o commit cf3f065. O texto abaixo é a saída do Codex, sem edição além da troca do caminho da pasta pessoal. Foram 91 comandos.

Sim. Confirmei dois achados novos de severidade média em `main@cf3f065`. Nenhum de severidade alta.

## ACHADOS CONFIRMADOS

1. **Média. A seção pode encerrar após um erro com três perguntas inéditas na fila.** Em React, com seis casos reais e HTTP simulado, a correção começou com a fila vazia. Uma busca preencheu a fila antes do avanço. O avanço usou a fila antiga, pediu outro lote, descartou o único caso recebido e encerrou a seção. Isso contraria a regra de apresentar outra variante após um erro avaliado. [Contrato, linha 80](<repositório>/conteudo/typescript-v1/CONTRATO-DE-CORRECAO.md:80)

   ```sh
   rtk proxy node -e 'const fs=require("node:fs"),p="./pilotos/mathua/mathua/",dep=p+"web/next-app/node_modules/";
   const React=require(dep+"react"),{JSDOM}=require(dep+"jsdom"),ts=require(p+"cmd/typescript-pilot/node_modules/typescript");
   const dom=new JSDOM("<div></div>");global.window=dom.window;global.document=dom.window.document;global.IS_REACT_ACT_ENVIRONMENT=true;
   const {createRoot}=require(dep+"react-dom/client"),{act}=React;
   process.env.NEXT_PUBLIC_TS_PILOT="1";
   const pilot=require(p+"web/next-app/lib/pilot.ts"),src=fs.readFileSync(p+"web/next-app/components/LearnStepper.tsx","utf8");
   const part=(a,b)=>src.slice(src.indexOf(a),src.indexOf(b));
   const bank=require("./conteudo/typescript-v1/exercicios.json").families[1].cases.map(c=>({id:c.id,question:c.prompt}));
   const requests=[],timers=[],ctl={},ids=qs=>qs.map(q=>q.id);
   const fetch=(_,count,{exclude})=>new Promise(resolve=>requests.push(i=>{
    const batch=Array.from({length:6},(_,j)=>bank[(i+j)%6]).filter(q=>!exclude.includes(q.question)).slice(0,count);
    resolve({questions:batch});return {excluidas:ids(exclude.map(s=>bank.find(q=>q.question===s))),lote:ids(batch)};
   }));
   const body=`
   const {TS_PILOT,pilotExclude,pilotFresh,pilotAdmit,pilotDiagnosis,pt}=pilot,{useState,useRef,useEffect,useCallback}=React;
   const kpIndex=0,conceptId="ts.value.numeric_literal",difficulty=0.4,misses=0,kps=[{}];
   const noop=()=>{},setServedFormat=noop,setAnsweredCount=noop,setCorrectCount=noop,setBand=noop,setConsecutive=noop,setMisses=noop,setDifficulty=noop;
   const submitStudyAnswer=async()=>({correct:false}),appendAfter=(_,fn)=>timers.push(fn);
   let key=1;const nextKey=()=>++key;
   return function Harness(){
    const practiceEpochRef=useRef(1),seenRef=useRef(bank.slice(0,3).map(q=>q.question)),shownRef=useRef(new Map());
    const [buffer,setBuffer]=useState(bank.slice(1,3)),[entries,setEntries]=useState([{kind:"q",key:1,kpIndex,q:bank[0]}]);
    ${part("  const countedRef = ","  const load = ")}
    ${part("  async function takeNext(","  function appendAfter(")}
    ${part("  function setEntry(","  // Which sections")}
    ctl.next=()=>continueInSection(entries.at(-1),difficulty);
    ctl.answer=()=>setEntry(entries.at(-1).key,{answer:"0"});
    ctl.check=()=>handleCheck(entries.at(-1).key);
    ctl.read=()=>({exibidas:ids(entries.filter(e=>e.kind==="q").map(e=>e.q)),fila:ids(buffer),fim:entries.at(-1).note??null});
    return null;
   }`;
   const Harness=new Function("React","pilot","bank","getLessonPractice","ctl","timers",ts.transpileModule(body,{compilerOptions:{target:ts.ScriptTarget.ES2022}}).outputText)(React,pilot,bank,fetch,ctl,timers);
   (async()=>{
    const root=createRoot(document.createElement("div"));await act(async()=>root.render(React.createElement(Harness)));
    await act(()=>ctl.next());await act(()=>ctl.next());await act(()=>ctl.answer());await act(()=>ctl.check());
    console.log("ao corrigir",JSON.stringify(ctl.read()));
    await act(async()=>{requests[0](3)});
    console.log("antes do avanço",JSON.stringify(ctl.read()));
    await act(async()=>{const next=timers[0]();console.log("busca",JSON.stringify(requests[2](0)));await next});
    console.log("depois do avanço",JSON.stringify(ctl.read()));
    await act(async()=>root.unmount());
   })().catch(e=>{console.error(e);process.exitCode=1});'
   ```

   ```text
   ao corrigir {"exibidas":["F002-V0","F002-V1","F002-V2"],"fila":[],"fim":null}
   antes do avanço {"exibidas":["F002-V0","F002-V1","F002-V2"],"fila":["F002-V3","F002-V4","F002-V5"],"fim":null}
   busca {"excluidas":["F002-V2","F002-V1","F002-V3","F002-V4","F002-V5"],"lote":["F002-V0"]}
   depois do avanço {"exibidas":["F002-V0","F002-V1","F002-V2"],"fila":[],"fim":"This topic ran out of new questions, so the section ended here."}
   ```

2. **Média. F023 recusa declarações válidas com `let`.** As duas respostas compilam em modo estrito e declaram o array pedido, com o nome e os elementos na ordem solicitada. Usei o critério publicado do exercício para avaliar as respostas. O corretor exige `const`. [Contrato, linha 53](<repositório>/conteudo/typescript-v1/CONTRATO-DE-CORRECAO.md:53) · [Critério de F023](<repositório>/conteudo/typescript-v1/EXERCICIOS.md:541)

   ```sh
   rtk proxy node -e 'const p="./pilotos/mathua/mathua/cmd/typescript-pilot/", {grade}=require(p+"grade.cjs"),ts=require(p+"node_modules/typescript"),{families}=require("./conteudo/typescript-v1/exercicios.json");
   const f=families.find(x=>x.id==="F023");
   for(const c of f.cases.slice(0,2)){
    const answer=c.answer.replace(/^const /,"let "),name="student.ts",options={strict:true,noEmit:true,types:[]};
    const host=ts.createCompilerHost(options),get=host.getSourceFile.bind(host);
    host.getSourceFile=(file,version,...args)=>file===name?ts.createSourceFile(file,answer,version,true):get(file,version,...args);
    const program=ts.createProgram([name],options,host);
    console.log(JSON.stringify({id:c.id,criterio:c.criterion,answer,ts:ts.version,diagnosticos:ts.getPreEmitDiagnostics(program).map(d=>d.code),veredito:grade({family:f.id,mode:f.mode,expected:c.answer,context_code:c.context_code,code_form:c.code_form,answer})}));
   }'
   ```

   ```text
   {"id":"F023-V0","criterio":"Declarar o array com os elementos na ordem solicitada.","answer":"let amounts = [15000, 5000, 10000];","ts":"5.9.3","diagnosticos":[],"veredito":{"correct":false,"score":0,"feedback":"Declare com const, como nas declarações deste material."}}
   {"id":"F023-V1","criterio":"Declarar o array com os elementos na ordem solicitada.","answer":"let totals = [18000, 4000, 12000];","ts":"5.9.3","diagnosticos":[],"veredito":{"correct":false,"score":0,"feedback":"Declare com const, como nas declarações deste material."}}
   ```

3. **Baixa. F010 e F011 atribuem um erro de digitação a incompatibilidade de tipo.** As recusas estão corretas. O TypeScript aponta um nome de tipo desconhecido (`TS2552`). A primeira frase do feedback atribui o erro à incompatibilidade com o valor. [Contrato, linha 76](<repositório>/conteudo/typescript-v1/CONTRATO-DE-CORRECAO.md:76)

   ```sh
   rtk proxy node -e 'const p="./pilotos/mathua/mathua/cmd/typescript-pilot/",{grade}=require(p+"grade.cjs"),ts=require(p+"node_modules/typescript"),{families}=require("./conteudo/typescript-v1/exercicios.json");
   for(const [n,ty] of [[10,"numbr"],[11,"strng"]]){
    const f=families[n-1],c=f.cases[0],answer=c.answer.replace(/: (number|string)/,": "+ty),name="student.ts",options={strict:true,noEmit:true,types:[]};
    const host=ts.createCompilerHost(options),get=host.getSourceFile.bind(host);
    host.getSourceFile=(file,version,...args)=>file===name?ts.createSourceFile(file,answer,version,true):get(file,version,...args);
    const program=ts.createProgram([name],options,host);
    console.log(JSON.stringify({id:c.id,answer,diagnosticos:ts.getPreEmitDiagnostics(program).map(d=>d.code),veredito:grade({family:f.id,mode:f.mode,expected:c.answer,answer})}));
   }'
   ```

   ```text
   {"id":"F010-V0","answer":"const amount: numbr = 15000;","diagnosticos":[2552],"veredito":{"correct":false,"score":0,"feedback":"A anotação não é compatível com o valor: Cannot find name 'numbr'. Did you mean 'number'?"}}
   {"id":"F011-V0","answer":"const id: strng = \"reembolso-01\";","diagnosticos":[2552],"veredito":{"correct":false,"score":0,"feedback":"A anotação não é compatível com o valor: Cannot find name 'strng'. Did you mean 'string'?"}}
   ```

## CORREÇÕES CONFERIDAS

1. **Busca atrasada.** Repeti o cenário da terceira passada e resolvi a busca adicional. V5 saiu da fila, o lote atrasado foi descartado e a próxima pergunta foi V0.
2. **Relato sem a chave.** O botão original e o atual enviaram o mesmo JSON, sem os campos `expected` e `explanation`.
3. **Feedback de F019 e F021.** As três respostas seguiram recusadas com nota 0. F019 explicou quando `||` já é verdadeiro. F021 pediu o valor de `id` nos dois casos.
4. **Seção 8.** As recusas de `as const` citaram “o objeto” em F021 e “o array” em F023. Os dois testes conferem essas mensagens.

## TENTATIVAS QUE NÃO ACHARAM PROBLEMA

- F001–F025, casos V0 e V1, com gabarito e quatro variações por caso. Foram 250 respostas, 128 aceitas e 122 recusadas. Os 50 gabaritos passaram. Nenhuma aceitação indevida na amostra.
- Em 3.829.849 pares de histórico e fila com seis casos, `pilotExclude` sempre deixou candidato no servidor e sempre excluiu a última pergunta mostrada. `pilotFresh` e `pilotAdmit` devolveram `[]` quando o lote inteiro já estava na fila ou no histórico recente.
- Na recuperação por HTTP 409, V4 substituiu V1 e a fila ficou V2, V3, V5. Nenhuma repetição imediata nos cenários reproduzidos.
- Sem `NEXT_PUBLIC_TS_PILOT`, os textos, o diagnóstico e o destino `/graph` amostrados coincidiram com os originais.
- Seção 2. O patch bateu com a árvore aplicada. Recontei 23 arquivos, 2.894 adições e 113 remoções. O diff rastreado em `web internal` deu 14 arquivos, 177 adições e 113 remoções. Os quatro SHA-256 conferiram.
- Seções 4 e 7 e `resultados.json`. Recontei 462, 26 e 154 testes-folha Go, sem falhas ou pulos. A API registrou 23 conceitos com seis casos distintos cada. O navegador registrou 23 verificações, 10 capturas e nove conceitos. O reinício registrou dois processos.
- Os logs registram 199 arquivos e 1.894 testes Vitest aprovados, zero erros de lint, `exit_tsc=0` e build concluído. `pilot.test.ts` tem nove testes, três de `pilotAdmit`. Os relatórios têm oito, cinco e quatro achados. Recontei 20 correções documentadas e sete decisões em aberto.

## NÃO VERIFICADO

- Equivalência visual de um novo build sem a chave e frequência da corrida em navegador real. A execução em React usou JSDOM e HTTP simulado.
- Novas execuções das suítes Go, Vitest, navegador e reinício. Conferi os registros existentes em modo somente leitura. O JSON de reinício é idêntico ao de `c7f3c85` e não registra a data da execução.
- Os totais históricos de 94, 78 e 107 comandos, o total de execuções do Vitest e a medição de 14,3 segundos de partida. Os três relatórios trazem, respectivamente, 9, 3 e 4 blocos de shell.
