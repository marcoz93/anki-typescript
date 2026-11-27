# Relatório do falseador, sétima passada (Codex, somente leitura)

Execução: 27/11/2026, sobre o commit d4317d9. O texto abaixo é a saída do Codex, sem edição além da troca do caminho da pasta pessoal. Foram 111 comandos; o relatório traz o comando e a saída de cada achado, e não todos os comandos.

Sim. Confirmei um achado novo de severidade média em `main@d4317d9`. Nenhum de severidade alta.

## ACHADOS CONFIRMADOS

1. **Média. O corretor rejeita o token certo quando ele vem acompanhado de um comentário.** Em oito casos de F005, F006, F007 e F012, o scanner do TypeScript encontrou apenas o token pedido. O corretor deu nota zero e informou que o nome ou símbolo era outro. Isso contraria a linha 20, que manda comparar o conteúdo sintático relevante. [Contrato de correção](<repositório>/conteudo/typescript-v1/CONTRATO-DE-CORRECAO.md:20)

   **Comando**

   ```sh
   rtk proxy node -e 'const {families}=require("./conteudo/typescript-v1/exercicios.json");
   const ts=require("./pilotos/mathua/mathua/cmd/typescript-pilot/node_modules/typescript");
   const {grade}=require("./pilotos/mathua/mathua/cmd/typescript-pilot/grade.cjs");
   for(const n of [5,6,7,12]) for(const c of families[n-1].cases.slice(2,4)){
    const expected=c.answer,answer=expected+" /* tipo */";
    const scanner=ts.createScanner(ts.ScriptTarget.ES2022,true,ts.LanguageVariant.Standard,answer);
    scanner.scan();
    const token=scanner.getTokenText(),eof=scanner.scan()===ts.SyntaxKind.EndOfFileToken;
    console.log(JSON.stringify({id:c.id,answer,token,eof,...grade({family:families[n-1].id,mode:"token",expected,answer})}));
   }'
   ```

   **Saída**

   ```text
   {"id":"F005-V2","answer":"number /* tipo */","token":"number","eof":true,"correct":false,"score":0,"feedback":"A resposta não é o nome ou o símbolo solicitado."}
   {"id":"F005-V3","answer":"number /* tipo */","token":"number","eof":true,"correct":false,"score":0,"feedback":"A resposta não é o nome ou o símbolo solicitado."}
   {"id":"F006-V2","answer":"string /* tipo */","token":"string","eof":true,"correct":false,"score":0,"feedback":"A resposta não é o nome ou o símbolo solicitado."}
   {"id":"F006-V3","answer":"string /* tipo */","token":"string","eof":true,"correct":false,"score":0,"feedback":"A resposta não é o nome ou o símbolo solicitado."}
   {"id":"F007-V2","answer":"boolean /* tipo */","token":"boolean","eof":true,"correct":false,"score":0,"feedback":"A resposta não é o nome ou o símbolo solicitado."}
   {"id":"F007-V3","answer":"boolean /* tipo */","token":"boolean","eof":true,"correct":false,"score":0,"feedback":"A resposta não é o nome ou o símbolo solicitado."}
   {"id":"F012-V2","answer":": /* tipo */","token":":","eof":true,"correct":false,"score":0,"feedback":"A resposta não é o nome ou o símbolo solicitado."}
   {"id":"F012-V3","answer":": /* tipo */","token":":","eof":true,"correct":false,"score":0,"feedback":"A resposta não é o nome ou o símbolo solicitado."}
   ```

2. **Baixa. Uma busca pendente pode recolocar uma pergunta sem registro na fila após o 409.** No ensaio React com HTTP simulado, limpei os registros com uma resposta de busca ainda pendente. A busca nova recuperou F002-V4, que recebeu 200. A resposta antiga recolocou F002-V3 na fila. Quando exibida e respondida, ela recebeu outro 409. Após o segundo 409, a tela exibiu F002-V5. A seção 7 diz que a recuperação descarta a fila e busca de novo para gravar os registros. A resposta pendente voltou a preencher essa fila com um caso sem registro. [Bloco 2, sexta passada](<repositório>/pilotos/mathua/BLOCO-2-D04-D05.md:219)

   **Comando**

   ```sh
   rtk proxy node -e 'const fs=require("node:fs");
   const report=fs.readFileSync("pilotos/mathua/evidencias/bloco-2-d04-d05/falseador-codex-5a-passada.md","utf8");
   const q=String.fromCharCode(39);
   let js=report.split("rtk proxy node -e "+q)[1].split(q+"\n")[0];
   js=js.replace(/const fetch=async[^]*?(?=\n\s*const code=)/,`
   const anchors=new Set(bank.slice(0,3).map(q=>q.question)),pending=[],timers=[];
   window.setTimeout=fn=>timers.push(fn);
   const fetch=async(_,count,{exclude})=>{
     const start=pending.length===0?3:4;
     const candidates=Array.from({length:6},(_,i)=>bank[(start+i)%6]).filter(q=>!exclude.includes(q.question));
     const questions=Array.from({length:count},(_,i)=>candidates[i%candidates.length]);
     questions.forEach(q=>anchors.add(q.question));
     console.log("busca",ids(questions).join(","));
     return new Promise(resolve=>pending.push(()=>resolve({questions})));
   };
   `)
   .replace("const submitStudyAnswer=async()=>{throw {status:409}};",`
   const submitStudyAnswer=async(_,a,t,q)=>{
     const status=anchors.has(q)?200:409;
     console.log("envio",bank.find(b=>b.question===q).id,status);
     if(status===409)throw {status};
     return {correct:false};
   };
   const advanceSection=()=>{throw Error("seção esgotada")},nextKey=()=>3;
   const consecutive=0,misses=0,setConsecutive=()=>{},setMisses=()=>{},setAnsweredCount=()=>{},setCorrectCount=()=>{},setBand=()=>{},setDifficulty=()=>{},pilotDiagnosis=pilot.pilotDiagnosis;
   `)
   .replace("part(\"  async function handleCheck(\",","part(\"  async function continueInSection(\",")
   .replace("\",\"  function appendAfter(\")","\",\"  async function startPracticing(\")")
   .replace("ctl.check=()=>handleCheck(2);","ctl.check=()=>handleCheck(entries.at(-1).key);ctl.type=()=>setEntry(entries.at(-1).key,{answer:\"0\"});")
   .replace("\"ctl\",ts.transpileModule","\"ctl\",\"anchors\",ts.transpileModule").replace("bank,fetch,ctl);","bank,fetch,ctl,anchors);")
   .replace(/\(async\(\)=>\{const root[^]*/,`
   (async()=>{const root=createRoot(document.createElement("div"));
   await act(async()=>root.render(React.createElement(Harness)));await act(()=>ctl.next());
   anchors.clear();let recovery;
   await act(async()=>{recovery=ctl.check()});await act(async()=>pending[0]());await act(async()=>{pending[1]();await recovery});
   console.log("recuperação",ctl.read().naTela,"fila",ctl.read().fila.join(","));
   await act(async()=>ctl.type());await act(()=>ctl.check());await act(()=>timers.shift()());
   console.log("após erro avaliado",ctl.read().naTela);
   await act(async()=>ctl.type());await act(async()=>{recovery=ctl.check()});await act(async()=>{pending.at(-1)();await recovery});
   console.log("segunda recuperação",ctl.read().naTela);
   await act(async()=>root.unmount())})().catch(e=>{console.error(e);process.exitCode=1});
   `);
   new Function("require",js)(require);'
   ```

   **Saída**

   ```text
   busca F002-V3,F002-V4,F002-V5
   envio F002-V1 409
   busca F002-V4,F002-V5,F002-V2
   recuperação F002-V4 fila F002-V3,F002-V5
   envio F002-V4 200
   busca F002-V2,F002-V2,F002-V2
   após erro avaliado F002-V3
   envio F002-V3 409
   busca F002-V5,F002-V2,F002-V5
   segunda recuperação F002-V5
   ```

3. **Baixa. F021 e F023 tratam `satisfies` como asserção de tipo no feedback.** O TypeScript reconheceu `satisfies` nas duas declarações, retornou `assertion:false` e não emitiu diagnósticos em modo `strict`. A mensagem atribui à resposta uma construção que ela não usa. Isso contraria a orientação da linha 76 sobre o diagnóstico. [Contrato de correção](<repositório>/conteudo/typescript-v1/CONTRATO-DE-CORRECAO.md:76)

   **Comando**

   ```sh
   rtk proxy node -e 'const {families}=require("./conteudo/typescript-v1/exercicios.json"),p="./pilotos/mathua/mathua/cmd/typescript-pilot/",ts=require(p+"node_modules/typescript"),{grade}=require(p+"grade.cjs");
   for(const i of [21,23]){
    const f=families[i-1],c=f.cases[2],answer=c.answer.slice(0,-1)+(i===21?" satisfies { id: string; value: number };":" satisfies number[];");
    const opts={strict:true,noEmit:true,target:ts.ScriptTarget.ES2022,types:[]},host=ts.createCompilerHost(opts),get=host.getSourceFile.bind(host);
    const sf=ts.createSourceFile("/qa.ts",answer,opts.target,true);
    host.getSourceFile=(name,...args)=>name==="/qa.ts"?sf:get(name,...args);
    const node=sf.statements[0].declarationList.declarations[0].initializer;
    const diagnostics=ts.getPreEmitDiagnostics(ts.createProgram(["/qa.ts"],opts,host));
    console.log(JSON.stringify({id:c.id,answer,diagnostics:diagnostics.map(d=>d.code),satisfies:ts.isSatisfiesExpression(node),assertion:ts.isAssertionExpression(node),...grade({family:f.id,mode:f.mode,expected:c.answer,answer,context_code:c.context_code,code_form:c.code_form})}));
   }'
   ```

   **Saída**

   ```text
   {"id":"F021-V2","answer":"const request = { id: \"r21\", value: 9000 } satisfies { id: string; value: number };","diagnostics":[],"satisfies":true,"assertion":false,"correct":false,"score":0,"feedback":"Escreva o objeto diretamente, sem asserção de tipo."}
   {"id":"F023-V2","answer":"const values = [9000, 3000, 6000] satisfies number[];","diagnostics":[],"satisfies":true,"assertion":false,"correct":false,"score":0,"feedback":"Escreva o array diretamente, sem asserção de tipo."}
   ```

## CORREÇÕES CONFERIDAS

- Reexecutei o ensaio original da sexta passada. Após `envio F002-V1 409`, houve nova busca e a saída foi `substituta F002-V2 com registro true`, igual à evidência gravada.

## TENTATIVAS QUE NÃO ACHARAM PROBLEMA

- F001 a F025, casos V2 e V3, com quatro variações por caso. Na amostra principal, passaram os 50 gabaritos. Houve 128 aprovações e 122 recusas, sem divergências de veredito ou de diagnóstico.
- Com seis casos, `pilotExclude` deixou ao menos uma candidata em 3.829.849 combinações de histórico e fila. `pilotFresh` e `pilotAdmit` puderam esvaziar lotes. Nas 2.676 buscas sem fila simuladas, `pilotUsable` devolveu uma candidata diferente da última exibida.
- Conferi as duas chamadas diretas de `pilotAdmit` no componente e a chamada via `pilotUsable`. Em React, 12 respostas incorretas percorreram os seis casos duas vezes, sem repetição consecutiva. A seção continuou aberta.
- Sem `NEXT_PUBLIC_TS_PILOT`, a base e a versão atual produziram o mesmo HTML nos cinco estados amostrados em JSDOM. Coincidiram duas buscas, dois envios e os dados entregues ao botão de relato.
- Seção 2. O patch tem 23 arquivos, 2.965 adições e 122 remoções. O diff rastreado de `web internal` tem 14 arquivos, 203 adições e 122 remoções. Os sete SHA-256 conferiram e a checagem inversa saiu com código 0.
- Seção 4 e `resultados.json`. Recontei 467, 26 e 154 testes-folha Go aprovados, sem falhas ou pulos. O teste da API registrou 23 conceitos dominados com seis casos distintos cada. A evidência de navegador tem 23 verificações aprovadas, dez capturas, nove conceitos e zero erros. O JSON de reinício registra dois processos.
- Seções 4 e 7. Os registros mostram 199 arquivos e 1.897 testes Vitest aprovados, 12 testes dos helpers, zero erros de lint, `exit_tsc=0` e build concluído. Recontei 8, 5, 4, 3, 3 e 1 achados nas seis passadas. As 27 correções documentadas e as oito decisões em aberto conferem com `resultados.json`.

## NÃO VERIFICADO

- Frequência do segundo 409 em navegador com servidor real. O ensaio controlou a ordem das respostas HTTP em JSDOM.
- Equivalência de um novo build sem a flag e novas execuções das suítes completas. Esses passos gravam artefatos.
- Totais históricos de comandos, frequência da falha intermitente do Vitest e tempo de partida de 14,3 segundos. Os registros disponíveis não permitem recontá-los.
- Data do ensaio de reinício da seção 4. O JSON não traz data e tem o mesmo hash Git em `c7f3c85` e `HEAD`.
