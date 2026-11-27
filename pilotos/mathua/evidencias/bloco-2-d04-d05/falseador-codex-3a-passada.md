# Relatório do falseador, terceira passada (Codex, somente leitura)

Execução: 27/11/2026, sobre o commit 7d3bc28. O texto abaixo é a saída do Codex, sem edição além da troca do caminho da pasta pessoal. Uma primeira tentativa desta passada foi interrompida pelo filtro de segurança do Codex depois de 34 comandos; o pedido foi reescrito e rodou até o fim, com 107 comandos.

Sim. Confirmei um achado novo de severidade média em `main@7d3bc28`. Nenhum de severidade alta.

## ACHADOS CONFIRMADOS

1. **Média. F002-V5 pode aparecer duas vezes seguidas.** Com seis casos reais, React e HTTP simulado, uma busca atrasada devolveu V5 antes de o efeito que atualiza o histórico rodar. O componente recolocou V5 na fila e a consumiu na chamada seguinte. Isso contraria a garantia de admissão da seção 7 e a regra de trocar o caso após erro. [Bloco 2, §7](<repositório>/pilotos/mathua/BLOCO-2-D04-D05.md:175) · [Contrato, linha 80](<repositório>/conteudo/typescript-v1/CONTRATO-DE-CORRECAO.md:80)

   ```sh
   rtk proxy node -e 'const fs=require("node:fs"),p="./pilotos/mathua/mathua/",dep=p+"web/next-app/node_modules/";
   const React=require(dep+"react"),{JSDOM}=require(dep+"jsdom");
   const dom=new JSDOM("<div></div>");
   global.window=dom.window;global.document=dom.window.document;
   const {createRoot}=require(dep+"react-dom/client"),{act}=React;
   process.env.NEXT_PUBLIC_TS_PILOT="1";
   const pilot=require(p+"web/next-app/lib/pilot.ts"),ts=require(p+"cmd/typescript-pilot/node_modules/typescript");
   const src=fs.readFileSync(p+"web/next-app/components/LearnStepper.tsx","utf8"),part=(a,b)=>src.slice(src.indexOf(a),src.indexOf(b));
   const bank=require("./conteudo/typescript-v1/exercicios.json").families[1].cases.map(c=>({id:c.id,question:c.prompt}));
   const pending=[],ctl={},ids=qs=>qs.map(q=>q.id);
   const fetch=(_,count,{exclude})=>new Promise(resolve=>pending.push(i=>{
    const questions=Array.from({length:18},(_,j)=>bank[(i+j)%6]).filter(q=>!exclude.includes(q.question)).slice(0,count);
    resolve({questions});return ids(questions);
   }));
   const body=`
   const {TS_PILOT,pilotExclude,pilotFresh,pilotAdmit}=pilot,{useState,useRef,useEffect,useCallback}=React;
   return function Harness(){
    const kpIndex=0,conceptId="ts.value.numeric_literal",practiceEpochRef=useRef(1),seenRef=useRef(bank.slice(0,3).map(q=>q.question)),shownRef=useRef(new Map());
    const [buffer,setBuffer]=useState(bank.slice(1,3)),[entries,setEntries]=useState([{kind:"q",key:1,kpIndex,q:bank[0]}]);
    ${part("  const countedRef = ","  const load = ")}
    ${part("  async function takeNext(","  function appendAfter(")}
    ctl.next=async()=>{const q=await takeNext(0.3);setEntries(prev=>[...prev,{kind:"q",key:prev.length+1,kpIndex,q}]);return q};
    ctl.read=()=>({exibidas:entries.map(e=>e.q.id),fila:buffer.map(q=>q.id)});
    return null;
   }`;
   const Harness=new Function("React","pilot","bank","getLessonPractice","ctl",ts.transpileModule(body,{compilerOptions:{target:ts.ScriptTarget.ES2022}}).outputText)(React,pilot,bank,fetch,ctl);
   (async()=>{
    global.IS_REACT_ACT_ENVIRONMENT=true;
    const root=createRoot(document.createElement("div"));
    await act(async()=>root.render(React.createElement(Harness)));
    const next=()=>act(async()=>{await ctl.next()});
    await next();await next();await act(async()=>{pending.shift()(3)});await next();await next();
    global.IS_REACT_ACT_ENVIRONMENT=false;
    const taking=ctl.next(),late=pending.shift()(5);
    console.log("retirada",(await taking).id,"lote atrasado",JSON.stringify(late));
    for(let i=0;i<2;i++) await new Promise(setImmediate);
    global.IS_REACT_ACT_ENVIRONMENT=true;
    console.log(JSON.stringify(ctl.read()));
    await next();
    console.log(JSON.stringify(ctl.read()));
    await act(async()=>root.unmount());
   })().catch(e=>{console.error(e);process.exitCode=1});'
   ```

   ```text
   retirada F002-V5 lote atrasado ["F002-V5","F002-V3","F002-V4"]
   {"exibidas":["F002-V0","F002-V1","F002-V2","F002-V3","F002-V4","F002-V5"],"fila":["F002-V5"]}
   {"exibidas":["F002-V0","F002-V1","F002-V2","F002-V3","F002-V4","F002-V5","F002-V5"],"fila":[]}
   ```

2. **Baixa. O envio de relato muda mesmo sem a flag.** O botão recebe e repassa `expected` e `explanation` após a correção. Medi os dados entregues a `submitReport` com um relato simulado. A diferença contraria a descrição de equivalência da interface sem a chave. O texto e o diagnóstico amostrados coincidiram com os originais. [LEIA-ME, linha 23](<repositório>/pilotos/mathua/LEIA-ME.md:23)

   ```sh
   rtk proxy node -e 'const fs=require("node:fs"),{execFileSync}=require("node:child_process");
   const p="./pilotos/mathua/mathua/",name="web/next-app/components/LearnStepper.tsx";
   const get=a=>a.match(/<ReportButton\b[^]*?\/>/g).find(x=>x.includes("question={qe.q.question}"));
   const base=get(execFileSync("rtk",["proxy","git","-C",p,"show","HEAD:"+name],{stdio:["ignore","pipe","ignore"]}).toString()),current=get(fs.readFileSync(p+name,"utf8"));
   delete process.env.NEXT_PUBLIC_TS_PILOT;
   const pilot=require(p+"web/next-app/lib/pilot.ts");
   console.log("flag",pilot.TS_PILOT,"texto",pilot.pt("Check"),"diagnóstico",pilot.pilotDiagnosis({correct:false,diagnosis:"original",feedback:"novo"}));
   const qe={feedback:{expected:"4",text:"Dois mais dois."}},component=fs.readFileSync(p+"web/next-app/components/ReportButton.tsx","utf8");
   const handler=component.slice(component.indexOf("  async function handleSubmit()"),component.indexOf("  if (sent) {"));
   const mock=(props)=>new Function("props","submitReport",`const sending=false,sent=false,reason="wrong_answer",detail="",setSending=()=>{},setError=()=>{},setSent=()=>{},setOpen=()=>{};${handler};return handleSubmit()`)(props,async payload=>console.log(JSON.stringify(payload)));
   (async()=>{
    for(const [label,tag] of [["base",base],["atual",current]]){
     const props={kind:"question",question:"2 + 2",source:"practice"};
     for(const [,key,expr] of tag.matchAll(/\b(expected|explanation)=\{([^}]+)\}/g)) props[key]=new Function("qe","return "+expr)(qe);
     process.stdout.write(label+" ");
     await mock(props);
    }
   })().catch(e=>{console.error(e);process.exitCode=1});'
   ```

   ```text
   flag false texto Check diagnóstico original
   base {"kind":"question","question":"2 + 2","source":"practice","reason":"wrong_answer","detail":""}
   atual {"kind":"question","question":"2 + 2","expected":"4","explanation":"Dois mais dois.","source":"practice","reason":"wrong_answer","detail":""}
   ```

3. **Baixa. F019 e F021 dão mensagens imprecisas em respostas corretamente recusadas.** F019 diz que `||` aceita “apenas uma” condição, embora também produza `true` com as duas verdadeiras. F021 pede exatamente as propriedades que já estão escritas. O TypeScript aponta `TS18004` porque o `id` abreviado não tem valor em escopo. A rubrica exige uma explicação sustentada pela resposta. [Contrato, linha 76](<repositório>/conteudo/typescript-v1/CONTRATO-DE-CORRECAO.md:76)

   ```sh
   rtk proxy node -e 'const p="./pilotos/mathua/mathua/cmd/typescript-pilot/",{grade}=require(p+"grade.cjs"),ts=require(p+"node_modules/typescript"),{families}=require("./conteudo/typescript-v1/exercicios.json");
   for(const [n,i,answer] of [[19,1,"hasReceipt || hasId"],[21,0,"const refund = { id, amount: 15000 };"],[21,1,"const expense = { id, total: 18000 };"]]){
    const f=families[n-1],c=f.cases[i],job={family:f.id,mode:f.mode,expected:c.answer,context_code:c.context_code,code_form:c.code_form,answer};
    if(n===19){console.log(JSON.stringify([c.id,c.context_code,answer,grade(job)]));continue}
    const file="/qa.ts",opts={strict:true,noEmit:true,noLib:true,types:[]},host=ts.createCompilerHost(opts);
    const sf=ts.createSourceFile(file,answer,ts.ScriptTarget.ES2022,true);
    host.getSourceFile=name=>name===file?sf:undefined;
    const program=ts.createProgram([file],opts,host),obj=sf.statements[0].declarationList.declarations[0].initializer;
    console.log(JSON.stringify([c.id,answer,obj.properties.map(x=>x.name.getText(sf)),program.getSemanticDiagnostics(sf).map(d=>d.code),grade(job)]));
   }'
   ```

   ```text
   ["F019-V1","const hasReceipt: boolean = true;\nconst hasId: boolean = true;","hasReceipt || hasId",{"correct":false,"score":0,"feedback":"A tarefa exige as duas condições ao mesmo tempo. O operador || aceita apenas uma delas."}]
   ["F021-V0","const refund = { id, amount: 15000 };",["id","amount"],[18004],{"correct":false,"score":0,"feedback":"O objeto deve ter exatamente as propriedades id e amount."}]
   ["F021-V1","const expense = { id, total: 18000 };",["id","total"],[18004],{"correct":false,"score":0,"feedback":"O objeto deve ter exatamente as propriedades id e total."}]
   ```

4. **Baixa. A seção 8 descreve incorretamente os testes e a mensagem de F023.** A seção afirma que nenhum caso listado tem asserção nos testes e atribui aos dois exercícios a mensagem sobre “o objeto”. Há testes para `as const` nos dois, e F023 diz “o array”. [Bloco 2, §8](<repositório>/pilotos/mathua/BLOCO-2-D04-D05.md:186)

   ```sh
   rtk proxy node -e 'const fs=require("node:fs"),p="pilotos/mathua/",d=p+"mathua/cmd/typescript-pilot/",{grade}=require("./"+d+"grade.cjs");
   const doc=fs.readFileSync(p+"BLOCO-2-D04-D05.md","utf8").split("\n"),t=fs.readFileSync(d+"main_test.go","utf8").split("\n");
   console.log(doc.find(x=>x.startsWith("Nenhum destes casos")));
   for(const n of [21,23]){
    const f=require("./conteudo/typescript-v1/exercicios.json").families[n-1],c=f.cases[1],answer=c.answer.replace(/;$/," as const;");
    const i=t.findIndex(l=>l.includes("f0"+n+"_assertion_is_not_a_missing_"));
    console.log(JSON.stringify([c.id,grade({family:f.id,mode:f.mode,expected:c.answer,context_code:c.context_code,code_form:c.code_form,answer}),i+1,t[i].match(/"([^"]+)"/)[1]]));
   }'
   ```

   ```text
   Nenhum destes casos tem asserção nos testes. O comportamento atual está indicado. A decisão é de quem escreve o conteúdo.
   ["F021-V1",{"correct":false,"score":0,"feedback":"Escreva o objeto diretamente, sem asserção de tipo."},1062,"f021_assertion_is_not_a_missing_object"]
   ["F023-V1",{"correct":false,"score":0,"feedback":"Escreva o array diretamente, sem asserção de tipo."},1063,"f023_assertion_is_not_a_missing_array"]
   ```

## CORREÇÕES CONFERIDAS

1. F002-V1 recusou a diretiva maiúscula com nota 0 e aceitou o comentário de bloco com nota 1.
2. F010-V1 e F011-V2 aceitaram `number & unknown` e `string & unknown` com nota 1. As duas anotações `ReturnType` que resultam em `any` receberam nota 0.
3. F021-V1 aceitou ``[`id`]`` e F022-V2 aceitou ``request[`value`]``, ambos com nota 1.
4. Nos dois cenários anteriores, a busca que chegou após o efeito descartou V5 e a busca seguinte trouxe V0. No 409, V4 substituiu V1 e a fila ficou `V2 V3 V5`. Resolvi a busca adicional que o script antigo deixava pendente. A ordem de chegada do achado 1 ainda repete V5.
5. O log do motor mudou em relação a `7f3d02e`. O primeiro evento é de `03:11:34.695302-03:00`, após aquele commit. Recontei 154 testes-folha, zero falhas e zero pulos.

## TENTATIVAS QUE NÃO ACHARAM PROBLEMA

- F001–F025, casos V0 e V1, com gabarito e quatro variações por caso. Foram 150 aprovações e 100 recusas, todas de acordo com o critério amostrado. Os 50 gabaritos passaram.
- Em 3.829.849 pares de histórico e fila com seis perguntas, `pilotExclude` sempre deixou pelo menos um candidato no servidor e nunca deixou a última pergunta mostrada. `pilotFresh` e `pilotAdmit` puderam esvaziar o lote no cliente. Na reprodução com fila vazia, a busca seguinte entregou V0.
- O patch conferiu com a árvore aplicada. A seção 2 bateu com a recontagem de 23 arquivos, 2.879 adições e 113 remoções. O `git diff --stat -- web internal` dos arquivos rastreados deu 14 arquivos, 170 adições e 113 remoções. Os três SHA-256 do patch conferiram.
- A seção 4 e `resultados.json` bateram com 459, 26 e 154 testes-folha Go, 23 conceitos dominados pela API com seis perguntas distintas por conceito, 23 verificações de navegador, 10 capturas, nove conceitos pela tela e dois processos no reinício.
- Os logs registram 199 arquivos e 1.894 testes Vitest aprovados, zero erros de lint e compilação concluída. Recontei nove testes em `pilot.test.ts`, três deles para `pilotAdmit`. Os relatórios têm oito e cinco itens, como registra a seção 7.

## NÃO VERIFICADO

- Frequência da repetição em navegador real, equivalência visual após um build sem a flag e novas execuções das suítes Go, navegador e reinício. A revisão foi somente leitura.
- Os totais históricos de 94 e 78 comandos. Os relatórios trazem nove e três blocos de shell. Também não há saída separada do `tsc --noEmit` nem registro de todas as execuções do Vitest.
- A data de uma nova execução do teste de reinício. O JSON atual é idêntico ao de `c7f3c85` e não registra data ou commit.
