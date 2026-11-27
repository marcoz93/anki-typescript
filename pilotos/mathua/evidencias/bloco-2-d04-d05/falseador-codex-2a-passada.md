# Relatório do falseador, segunda passada (Codex, somente leitura)

Execução: 27/11/2026, sobre o commit 7f3d02e, que corrigiu os achados da primeira passada. O texto abaixo é a saída do Codex, sem edição além da troca do caminho da pasta pessoal.

## ACHADOS CONFIRMADOS

1. **Média — F002 ainda aceita uma diretiva que o TypeScript rejeita.** Com `<REFERENCE>` em maiúsculas, o corretor dá nota 1 e o TypeScript 5.9.3 emite `TS2726`. A mesma regra recusa um comentário `/* */` que apenas contém o texto da diretiva. Isso contraria o contrato, linha 40, a garantia do item 1 da seção 7 e a aceitação de comentários comuns descrita no README do piloto.
2. **Média — F010 e F011 classificam anotações pelo texto, com erros nos dois sentidos.** Recusam `number & unknown` e `string & unknown`, que o compilador resolve para `number` e `string`. Aceitam duas anotações com `ReturnType` que o compilador resolve para `any`. Isso contraria o contrato, linhas 49 e 66, e o item 2 da seção 7.
3. **Média — F021 e F022 recusam chaves textuais válidas com crase.** F021 afirma que faltam as propriedades exatas, embora o compilador infira `{ id: string; total: number; }`. F022 recusa o acesso à chave `value`, que compila em modo estrito. O contrato, linha 53, exige a forma e os nomes pedidos e admite colchetes com a mesma chave textual. A seção 8 já registra a decisão em aberto para F022.

**Comando dos achados 1–3**

```sh
rtk proxy node -e 'const p="./pilotos/mathua/mathua/cmd/typescript-pilot/",g=require(p+"grade.cjs"),ts=require(p+"node_modules/typescript"),{families}=require("./conteudo/typescript-v1/exercicios.json");
function job(f,v,answer){const k=families[f-1].cases[v];return {family:families[f-1].id,mode:families[f-1].mode,expected:k.answer,context_code:k.context_code,code_form:k.code_form,answer};}
function check(f,v,answer){
 const j=job(f,v,answer),file="/__qa_answer__.ts",opts={strict:true,noEmit:true,types:[],target:ts.ScriptTarget.ES2022},host=ts.createCompilerHost(opts),read=host.getSourceFile.bind(host);
 host.getSourceFile=(n,t)=>n===file?ts.createSourceFile(n,(j.context_code?j.context_code+"\n":"")+answer,t,true):read(n,t);
 const program=ts.createProgram([file],opts,host),sf=program.getSourceFile(file),d=sf.statements.at(-1)?.declarationList?.declarations[0],checker=program.getTypeChecker();
 console.log(JSON.stringify([j.family,answer,g.grade(j),ts.getPreEmitDiagnostics(program).map(d=>d.code),d?checker.typeToString(checker.getTypeAtLocation(d.name)):null]));
}
console.log("TypeScript",ts.version);
check(2,1,"/// <REFERENCE lib=\"invalidlib\" />\n18_000");
check(2,1,"/*\n/// <reference lib=\"invalidlib\" />\n*/\n18_000");
check(10,1,"const total: number & unknown = 18_000;");
check(11,2,"const id: string & unknown = \"reembolso-21\";");
check(10,1,"const total: ReturnType<typeof JSON.parse> = 18_000;");
check(11,2,"const id: ReturnType<typeof Object.create> = \"reembolso-21\";");
check(21,1,"const expense = { [`id`]: \"r11\", total: 18000 };");
check(22,2,"request[`value`]");'
```

```text
TypeScript 5.9.3
["F002","/// <REFERENCE lib=\"invalidlib\" />\n18_000",{"correct":true,"score":1,"feedback":"Correto. O literal representa o valor solicitado."},[2726],null]
["F002","/*\n/// <reference lib=\"invalidlib\" />\n*/\n18_000",{"correct":false,"score":0,"feedback":"Remova a diretiva /// <reference>. A resposta deve conter somente o que a tarefa pede."},[],null]
["F010","const total: number & unknown = 18_000;",{"correct":false,"score":0,"feedback":"any e unknown não informam o tipo do valor. Omita a anotação ou use number."},[],"number"]
["F011","const id: string & unknown = \"reembolso-21\";",{"correct":false,"score":0,"feedback":"any e unknown não informam o tipo do valor. Omita a anotação ou use string."},[],"string"]
["F010","const total: ReturnType<typeof JSON.parse> = 18_000;",{"correct":true,"score":1,"feedback":"Correto. A constante tem o nome e o valor solicitados. A anotação number é opcional neste exercício."},[],"any"]
["F011","const id: ReturnType<typeof Object.create> = \"reembolso-21\";",{"correct":true,"score":1,"feedback":"Correto. A constante tem o nome e o valor solicitados. A anotação string é opcional neste exercício."},[],"any"]
["F021","const expense = { [`id`]: \"r11\", total: 18000 };",{"correct":false,"score":0,"feedback":"O objeto deve ter exatamente as propriedades id e total."},[],"{ id: string; total: number; }"]
["F022","request[`value`]",{"correct":false,"score":0,"feedback":"Escreva o acesso à propriedade value, com ponto ou com colchetes e o nome entre aspas."},[],null]
```

4. **Média — Buscas sobrepostas ainda repetem perguntas.** Com seis casos reais de F002 e respostas HTTP simuladas, uma busca atrasada repôs `V5` depois de ele ter sido exibido. No fluxo de recuperação de HTTP 409, duas cópias consecutivas de `V5` entraram na fila. Isso contraria o contrato, linha 80, e a garantia de deduplicação do item 6 da seção 7.

```sh
rtk proxy node -e 'const fs=require("node:fs"),p="./pilotos/mathua/mathua/",ts=require(p+"cmd/typescript-pilot/node_modules/typescript");
process.env.NEXT_PUBLIC_TS_PILOT="1";
const pilot=require(p+"web/next-app/lib/pilot.ts"),src=fs.readFileSync(p+"web/next-app/components/LearnStepper.tsx","utf8");
const part=(a,b)=>src.slice(src.indexOf(a),src.indexOf(b));
const bank=require("./conteudo/typescript-v1/exercicios.json").families[1].cases.map(c=>({id:c.id,question:c.prompt}));
const js=`
const {TS_PILOT,pilotExclude,pilotFresh,pt}=pilot,useCallback=f=>f,conceptId="ts.value.numeric_literal",kpIndex=0,difficulty=0.3;
let buffer=bank.slice(1,3),entries=[];
const history=[bank[0]],bufferRef={current:buffer},seenRef={current:bank.slice(0,3).map(q=>q.question)};
const shownRef={current:new Map([[1,[bank[0].question]]])},practiceEpochRef={current:1},pending=[];
const setBuffer=v=>{buffer=typeof v==="function"?v(buffer):v};
const setEntry=(_,patch)=>Object.assign(entries[0],patch);
const submitStudyAnswer=async()=>{throw {status:409}};
const getTopicLockedPrerequisites=()=>null,getErrorStatus=e=>e.status;
const getLessonPractice=(_,count,{exclude})=>new Promise(resolve=>pending.push(i=>{
 const qs=[...bank.slice(i),...bank.slice(0,i)].filter(q=>!exclude.includes(q.question)).slice(0,count);
 resolve({questions:qs});
}));
${part("  const refill = ","  const load = ")}
${part("  async function takeNext(","  function appendAfter(")}
${part("  async function handleCheck(","  // Which sections")}
const flush=()=>new Promise(setImmediate),ids=qs=>qs.map(q=>q.id).join(" ");
async function next(){
 bufferRef.current=buffer;
 history.push(await takeNext(0.3));
 shownRef.current.set(1,[...new Set(history.map(q=>q.question).reverse())].reverse());
}
return (async()=>{
 await next();
 if(conflict){
  entries=[{key:1,kind:"q",q:history.at(-1),answer:"1",servedAt:Date.now()}];
  bufferRef.current=buffer;
  const checking=handleCheck(1);
  await flush();pending.shift()(3);await flush();
  console.log("antes do 409",ids(buffer));
  pending.shift()(4);await checking;
  console.log("depois do 409",ids(buffer));
 }else{
  await next();pending.shift()(3);await flush();
  await next();await next();await next();
  pending.shift()(5);await flush();await next();
  console.log("exibidas",ids(history));
 }
})();`;
const run=new Function("pilot","bank","conflict",ts.transpileModule(js,{compilerOptions:{target:ts.ScriptTarget.ES2022}}).outputText);
run(pilot,bank,false).then(()=>run(pilot,bank,true)).catch(e=>{console.error(e);process.exitCode=1});'
```

```text
exibidas F002-V0 F002-V1 F002-V2 F002-V3 F002-V4 F002-V5 F002-V5
antes do 409 F002-V2 F002-V3 F002-V4 F002-V5
depois do 409 F002-V2 F002-V3 F002-V4 F002-V5 F002-V5 F002-V3
```

5. **Baixa — A evidência do motor antecede as correções.** O log dos 154 testes já estava em `c7f3c85` e é idêntico byte a byte em `7f3d02e`. Isso contraria a linha 83 do Bloco 2, que atribui as evidências da pasta à execução final após as correções.

```sh
rtk proxy python3 -c 'import json,pathlib,subprocess
p="pilotos/mathua/evidencias/bloco-2-d04-d05/mathua-native-engine.jsonl"
a=subprocess.check_output(["rtk","proxy","git","show","c7f3c85:"+p],stderr=subprocess.DEVNULL)
b=subprocess.check_output(["rtk","proxy","git","show","7f3d02e:"+p],stderr=subprocess.DEVNULL)
print("mesmo log:",a==b==pathlib.Path(p).read_bytes())
print("primeiro evento:",json.loads(b.splitlines()[0])["Time"])
print("commit anterior:",subprocess.check_output(["rtk","proxy","git","show","-s","--format=%cI","c7f3c85"],stderr=subprocess.DEVNULL).decode().strip())'
```

```text
mesmo log: True
primeiro evento: 2026-11-27T02:30:31.695409-03:00
commit anterior: 2026-11-27T02:34:51-03:00
```

## CORREÇÕES CONFERIDAS

Reexecutei os nove blocos de comando do [relatório anterior](<repositório>/pilotos/mathua/evidencias/bloco-2-d04-d05/falseador-codex.md).

1. A diretiva original em F002 agora recebe `correct:false`, nota 0 e mensagem própria. A grafia minúscula também foi recusada em F016, F017 e F024.
2. As quatro respostas originais de F010, F011, F021 e F022 agora recebem `correct:true`, nota 1 e zero diagnósticos TypeScript.
3. F021 continua recusando `12000 + 6000` e agora pede um literal sem operações. As mensagens adicionais de F021, F023 e F019 também citaram a asserção ou os operandos.
4. A resposta original de 2.805 caracteres agora recebe `correct:false`, mensagem de encaixe excessivo e código de saída 0.
5. Nos três cenários originais, os candidatos foram `[]`, `["F"]` e `["F"]`. O primeiro cenário tem cinco casos. O carregador exige seis em todas as 25 famílias servidas, e todas têm seis.
6. A ordem original das duas respostas deixou apenas `V3 V4 V5` na fila. Os dois cenários do achado 4 ainda produziram repetição.
7. O texto do Bloco 1 agora distingue as páginas. O patch contém `app/my-reports/page.tsx` e omite `app/reports/page.tsx`.
8. A seção 7 existe. A busca pela remissão antiga retornou código 1 e saída vazia.

## TENTATIVAS QUE NÃO ACHARAM PROBLEMA

- Os 150 gabaritos foram aceitos. A seleção do carregador cobre 23 conceitos e 25 famílias, de F001 a F025.
- Parênteses, uniões de literais e interseções com `{}` passaram em F010/F011. `any`, `unknown` e tipos incompatíveis explícitos foram recusados.
- Comentários comuns `//` e `/* */` passaram. Um caso sintético de F003 com o literal `"///"` passou.
- F021 aceitou chave entre aspas, identificador com escape Unicode e chave entre parênteses. F022 aceitou colchetes com parênteses ou escape Unicode.
- Os 98 testes de comprimento e encaixe cobriram as 12 famílias de código e as duas de resultado. Todos retornaram veredito. A família sintética sem corretor retornou saída 1 sozinha e `{"error":...}` no lote, distinta de `correct:false`.
- Em 3.829.849 combinações de históricos e filas, `pilotExclude` deixou pelo menos um candidato e excluiu as duas perguntas mais recentes. `pilotFresh` devolveu `[]` quando o único candidato já estava na fila.
- Sem `NEXT_PUBLIC_TS_PILOT`, os trechos de `refill` e `takeNext` ensaiados em memória coincidiram com a base. O diff da rota Go mostra exclusão de enunciados multilinha e inclusão de `ungraded` na resposta de fallback, ambas incondicionais.
- Recontei 451, 26 e 154 testes-folha Go, sem falhas ou pulos. Conferi 23 conceitos dominados com seis perguntas distintas por conceito, 23 verificações de navegador, 10 capturas, dois processos no reinício, 199 arquivos e 1.891 testes no Vitest, seis testes em `pilot.test.ts` e zero erros de lint.
- Recontei oito achados no relatório e oito itens na seção 7. Os dois SHA-256 do patch conferem. O patch atual tem 23 arquivos, 2.818 adições e 111 remoções. `git apply --check --cached` na base e `git apply --reverse --check` na árvore de trabalho saíram com código 0. Os 23 arquivos conferem com os hashes do patch.

## NÃO VERIFICADO

- Frequência das repetições em navegador real, novo build sem a flag e novas execuções das suítes Go, reinício e navegador. A revisão foi somente leitura. As corridas foram simuladas em memória.
- O total de 94 comandos da primeira revisão. O relatório disponível contém nove blocos de shell.
