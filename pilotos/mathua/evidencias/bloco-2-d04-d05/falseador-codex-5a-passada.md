# Relatório do falseador, quinta passada (Codex, somente leitura)

Execução: 27/11/2026, sobre o commit 61bdca9. O texto abaixo é a saída do Codex, sem edição além da troca do caminho da pasta pessoal. Foram 106 comandos; o relatório traz o comando e a saída de cada achado, e não todos os comandos.

Sim. Confirmei um achado novo de severidade média em `main@61bdca9`. Nenhum de severidade alta.

## ACHADOS CONFIRMADOS

1. **Média. A recuperação após HTTP 409 pode ficar sem candidata com quatro perguntas na fila.** Em React, com seis casos reais de F002 e HTTP simulado, a busca de recuperação devolveu `V5`. O filtro descartou `V5` porque ela já estava na fila. A tela manteve `V1` e informou que não conseguiu carregar uma substituta. Isso contraria o fluxo documentado de reapresentar uma questão após o 409. [Mathua, documentação do fluxo de correção](<repositório>/pilotos/mathua/mathua/docs/system-design.md:497)

   ```sh
   rtk proxy node -e 'const fs=require("node:fs"),p="./pilotos/mathua/mathua/",dep=p+"web/next-app/node_modules/";
   const React=require(dep+"react"),{JSDOM}=require(dep+"jsdom"),ts=require(p+"cmd/typescript-pilot/node_modules/typescript");
   const dom=new JSDOM("<div></div>");global.window=dom.window;global.document=dom.window.document;global.IS_REACT_ACT_ENVIRONMENT=true;
   const {createRoot}=require(dep+"react-dom/client"),{act}=React;
   process.env.NEXT_PUBLIC_TS_PILOT="1";
   const pilot=require(p+"web/next-app/lib/pilot.ts"),src=fs.readFileSync(p+"web/next-app/components/LearnStepper.tsx","utf8");
   const part=(a,b)=>src.slice(src.indexOf(a),src.indexOf(b));
   const bank=require("./conteudo/typescript-v1/exercicios.json").families[1].cases.map(c=>({id:c.id,question:c.prompt}));
   const ctl={},ids=qs=>qs.map(q=>q.id);
   const fetch=async(_,count,{exclude})=>{
     const questions=bank.filter(q=>!exclude.includes(q.question)).slice(0,count);
     console.log(JSON.stringify({excluidas:ids(exclude.map(s=>bank.find(q=>q.question===s))),servidor:ids(questions)}));
     return {questions};
   };
   const code=`
   const {TS_PILOT,pilotExclude,pilotFresh,pilotAdmit,pilotUsable,pt}=pilot,{useState,useRef,useEffect,useCallback}=React;
   const kpIndex=0,conceptId="ts.value.numeric_literal",difficulty=0.4,setServedFormat=()=>{};
   const getTopicLockedPrerequisites=()=>null,getErrorStatus=e=>e.status;
   const submitStudyAnswer=async()=>{throw {status:409}};
   return function Harness(){
     const practiceEpochRef=useRef(1),seenRef=useRef(bank.slice(0,3).map(q=>q.question)),shownRef=useRef(new Map());
     const [buffer,setBuffer]=useState(bank.slice(1,3)),[entries,setEntries]=useState([{kind:"q",key:1,kpIndex,q:bank[0]}]);
     ${part("  const countedRef = ","  const load = ")}
     ${part("  async function takeNext(","  function appendAfter(")}
     ${part("  function setEntry(","  /**\n   * Move to the next knowledge point")}
     ${part("  async function handleCheck(","  // Which sections")}
     ctl.next=async()=>{const q=await takeNext(difficulty);setEntries(old=>[...old,{kind:"q",key:2,kpIndex,q,answer:"0",servedAt:Date.now()}])};
     ctl.check=()=>handleCheck(2);
     ctl.read=()=>({naTela:entries.at(-1).q.id,fila:buffer.map(q=>q.id),erro:entries.at(-1).error??null});
     return null;
   }`;
   const Harness=new Function("React","pilot","bank","getLessonPractice","ctl",ts.transpileModule(code,{compilerOptions:{target:ts.ScriptTarget.ES2022}}).outputText)(React,pilot,bank,fetch,ctl);
   (async()=>{const root=createRoot(document.createElement("div"));await act(()=>root.render(React.createElement(Harness)));await act(()=>ctl.next());console.log("antes",JSON.stringify(ctl.read()));await act(()=>ctl.check());console.log("depois",JSON.stringify(ctl.read()));await act(()=>root.unmount());})().catch(e=>{console.error(e);process.exitCode=1});'
   ```

   ```text
   {"excluidas":["F002-V0","F002-V1","F002-V2"],"servidor":["F002-V3","F002-V4","F002-V5"]}
   antes {"naTela":"F002-V1","fila":["F002-V2","F002-V3","F002-V4","F002-V5"],"erro":null}
   {"excluidas":["F002-V1","F002-V0","F002-V2","F002-V3","F002-V4"],"servidor":["F002-V5"]}
   depois {"naTela":"F002-V1","fila":["F002-V2","F002-V3","F002-V4","F002-V5"],"erro":"That question could not be graded and no replacement could be loaded. Press Check to try again or reload the lesson."}
   ```

2. **Baixa. F023 pede para inicializar uma constante em duas respostas escritas com `let`.** A recusa está correta porque o valor é um número. O enunciado pede um array, e o feedback chama a variável de constante. [Contrato, linha 76](<repositório>/conteudo/typescript-v1/CONTRATO-DE-CORRECAO.md:76) · [Bloco 2, §7](<repositório>/pilotos/mathua/BLOCO-2-D04-D05.md:200)

   ```sh
   rtk proxy node -e 'const {families}=require("./conteudo/typescript-v1/exercicios.json"),{grade}=require("./pilotos/mathua/mathua/cmd/typescript-pilot/grade.cjs");
   for(const c of families[22].cases.slice(0,2)){
    const answer=c.answer.replace(/const (\w+) = \[(\d+),.*$/,"let $1 = $2;");
    console.log(JSON.stringify({id:c.id,answer,...grade({family:"F023",mode:"code",expected:c.answer,answer,context_code:c.context_code,code_form:c.code_form})}));
   }'
   ```

   ```text
   {"id":"F023-V0","answer":"let amounts = 15000;","correct":false,"score":0,"feedback":"Inicialize a constante com um array, entre colchetes, com os elementos pedidos."}
   {"id":"F023-V1","answer":"let totals = 18000;","correct":false,"score":0,"feedback":"Inicialize a constante com um array, entre colchetes, com os elementos pedidos."}
   ```

3. **Baixa. A seção 7 descreve o primeiro relatório como um registro completo dos comandos.** A seção declara 94 comandos e diz que o relatório contém cada comando e saída. O arquivo traz nove invocações explícitas de `rtk`. [Bloco 2, §7](<repositório>/pilotos/mathua/BLOCO-2-D04-D05.md:145)

   ```sh
   rtk proxy node -e 'const fs=require("node:fs"),p="pilotos/mathua/",d=p+"evidencias/bloco-2-d04-d05/",doc=fs.readFileSync(p+"BLOCO-2-D04-D05.md","utf8");
   const actual=fs.readFileSync(d+"falseador-codex.md","utf8");
   console.log(doc.split("\n").find(l=>l.includes("com cada comando e saída")));
   console.log("blocos shell:",[...actual.matchAll(/^\s*```sh$/gm)].length,"invocações rtk:",[...actual.matchAll(/^\s*rtk\b/gm)].length);'
   ```

   ```text
   O falseador foi o Codex, em modo somente leitura, sobre os commits `3d1fdc4` e `c7f3c85`. Ele rodou 94 comandos. O relatório dele, com cada comando e saída, está em [falseador-codex.md](evidencias/bloco-2-d04-d05/falseador-codex.md).
   blocos shell: 9 invocações rtk: 9
   ```

## CORREÇÕES CONFERIDAS

- **Fila após o erro.** O cenário da quarta passada exibiu `V3`, manteve `V4` e `V5` na fila e deixou a seção aberta. O roteiro passou a resolver a terceira busca somente se ela fosse aberta.
- **F023 com `let`.** As respostas originais de `V0` e `V1` foram aceitas, com nota 1 e zero diagnósticos do TypeScript.
- **F010 e F011 com `numbr` e `strng`.** Ambas receberam nota 0 e diagnóstico `TS2552`. O feedback começou com “O compilador TypeScript rejeitou a declaração” e trouxe a mensagem do compilador.

## TENTATIVAS QUE NÃO ACHARAM PROBLEMA

- **F001–F025.** Rodei os casos `V0` e `V1` de cada família, com gabarito e quatro variações por caso. Das 250 respostas, 134 foram aceitas e 116 recusadas. Os 50 gabaritos passaram. Nenhum veredito divergiu da rubrica na amostra.
- **Fila e repetição.** Em 3.829.849 pares de histórico e fila, `pilotExclude` sempre deixou candidato e excluiu a última pergunta mostrada. `pilotFresh` e `pilotAdmit` devolveram listas vazias nos controles. `pilotUsable` recuperou uma pergunta anterior quando ela veio no lote e descartou o lote que continha só a última exibida. Nos cenários React de buscas sobrepostas, nenhuma pergunta apareceu duas vezes seguidas.
- **Sem `NEXT_PUBLIC_TS_PILOT`.** Em React com JSDOM e dependências simuladas, a base e a versão atual renderizaram a mesma introdução, pergunta, correção e próxima pergunta. As requisições, os envios e o JSON do relato coincidiram. O destino amostrado continuou `/graph`.
- **Seção 2.** O patch aplicado conferiu na checagem inversa. Recontei 23 arquivos, 2.944 adições e 116 remoções. O diff rastreado em `web internal` deu 14 arquivos, 186 adições e 116 remoções. Os cinco SHA-256 do patch conferiram.
- **Seção 4 e `resultados.json`.** Recontei 466, 26 e 154 testes-folha Go, todos aprovados. O log da API registra 23 conceitos dominados com seis perguntas distintas cada. O navegador registra 23 verificações, 10 capturas e nove conceitos. O registro de reinício indica dois processos.
- **Interface e seção 7.** Os logs registram 199 arquivos e 1.897 testes Vitest aprovados, zero erros de lint, `exit_tsc=0` e build concluído. `pilot.test.ts` tem 12 testes, três de `pilotAdmit` e três de `pilotUsable`. Recontei 8, 5, 4 e 3 achados nos relatórios, 23 correções documentadas e oito decisões em aberto.

## NÃO VERIFICADO

- Frequência do 409 em navegador real e equivalência visual de um novo build sem a flag. A comparação da interface foi feita em JSDOM. Conferi as suítes completas pelos registros existentes, sem executá-las novamente.
- Totais históricos de comandos e de execuções do Vitest, além dos 14,3 segundos de partida. Os registros disponíveis não permitem recontar esses totais. O JSON de reinício é idêntico ao de `c7f3c85` e não contém data de execução.
