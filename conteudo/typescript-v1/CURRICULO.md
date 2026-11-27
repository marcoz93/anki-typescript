# Escada de TypeScript: conteúdo completo, do valor à iteração

Versão editorial 1, 27/11/2026. Base de integração: `83a1aff2c794fb74dc83857eb3b6c444a3335c81` de `marcoz93/anki-typescript`.

## Origem e alcance

A ordem dos quinze degraus e os 74 cartões vêm de `fontes/anki_typescript_v1.tsv`, material anterior desta conversa. O caso integrado vem de `fontes/reembolsos.ts`. Esses dois arquivos estão preservados sem alteração. As explicações ampliadas, os vínculos entre conceitos, as rubricas e as variantes deste pacote são uma expansão editorial própria para entregar o conteúdo à IA implementadora. Não constituem um currículo oficial do Mathua nem do Math Academy.

Esta é a escada completa combinada para este recorte. Ela termina em `for...of`. Não pretende cobrir toda a linguagem TypeScript. Classes, módulos, tipos genéricos, promessas e máquinas de estados pertencem a outros recortes.

Os três conceitos do piloto atual cobrem somente partes dos degraus 1, 2 e 3. Eles não comprovam que esses degraus inteiros já foram estudados. Primeiro completamos os conteúdos que faltam nesses degraus e depois seguimos a ordem abaixo.

## Como ler a escada

Um **degrau** organiza o ensino. Um **conceito** delimita o que identificar ou compreender. Uma **habilidade** diz o que fazer com esse conteúdo. Uma **família de exercícios** fixa a tarefa e seu critério. Uma **variante** muda dados ou contexto, preservando a tarefa e o critério.

Nesta escada, a explicação do significado precede a cobrança da notação. Isso é uma ordem de ensino. Não é uma descrição da ordem de processamento de um compilador. A numeração dos degraus não é uma hierarquia de espécies nem uma prova de necessidade lógica.

| Degrau | Conteúdo | O aluno passa a conseguir |
| --- | --- | --- |
| 01 | Valor e literal | Representar diretamente números, textos e valores booleanos |
| 02 | Tipo | Distinguir `number`, `string` e `boolean` |
| 03 | Vinculação | Declarar nomes, inicializar valores e ler anotações de tipo |
| 04 | Expressão e operador | Produzir e interpretar resultados de operações |
| 05 | Composição de dados | Formar objetos e arrays e acessar suas partes |
| 06 | Declaração de tipos | Nomear uma forma de dados com `type` |
| 07 | Definição de função | Especificar parâmetros, corpo e retorno |
| 08 | Invocação | Fornecer argumentos e distinguir retorno de efeito |
| 09 | Composição de funções | Usar a saída de uma função como entrada de outra |
| 10 | Função como valor | Referenciar, vincular e passar funções |
| 11 | União | Restringir resultados a alternativas declaradas |
| 12 | Seleção condicional | Selecionar um ramo e cobrir os resultados previstos |
| 13 | Ausência e narrowing | Tratar `undefined` antes de usar um valor |
| 14 | Operações sobre coleções | Escolher e usar `map`, `filter` e `find` |
| 15 | Iteração explícita | Executar uma operação para cada elemento com `for...of` |

## Caso comum aos degraus

Representamos pedidos de reembolso por um identificador textual e uma quantia numérica. Para o exercício, adotamos a política: **um reembolso exige revisão quando sua quantia é estritamente maior que 10.000**. O limite de 10.000 é uma política do exemplo, não uma verdade da linguagem. Nas variantes, outro limite pode ser informado explicitamente.

O programa didático calcula a necessidade de revisão. Ele não aprova pagamentos, não verifica documentos e não executa um reembolso. Não confunda a classificação calculada com a realização dessas outras funções.

Os exemplos usam números finitos, inteiros e pequenos, texto sem escapes especiais e arrays densos e finitos. Essa restrição mantém o foco nos conceitos estudados. Não é uma especificação de dinheiro para produção.

## D01 — Valor e literal

**Finalidade.** Representar no código um dado concreto antes de lhe dar um nome ou executar uma operação.

Um valor é aquilo com que o programa opera. Um literal é uma forma de escrever diretamente um valor no código. O valor numérico quinze mil e o trecho `15000` que o representa não são a mesma coisa: um é o conteúdo representado, o outro é a expressão escrita.

```ts
15000
"reembolso-01"
false
```

`15000` representa um valor numérico. As aspas delimitam o texto `reembolso-01` e não fazem parte desse texto. `false` representa o valor booleano falso. O outro valor booleano é `true`. Não use aspas para escrever os literais booleanos.

**Contrastes.** `"15000"` representa texto; `15000` representa um número. `"false"` é texto; `false` é booleano. `10000 + 5000` chega ao mesmo valor que `15000`, mas envolve uma operação e não é um único literal. `15_000` é outra escrita permitida do mesmo literal numérico.

**Tarefa resolvida.** “Escreva o literal textual do identificador reembolso-01.” Resposta: `"reembolso-01"`. `reembolso-01` sem aspas não atende ao pedido de um literal textual.

**Aceite do conteúdo.** Distinguir representação e valor; escrever um literal do tipo solicitado; preservar o conteúdo pedido. Nos exercícios de código, aspas simples ou duplas são equivalentes para estes textos, desde que a sintaxe seja válida.

**Cartões de origem:** C001–C004. O piloto já cobre C002 pelo conceito `ts.value.numeric_literal`.

## D02 — Tipo

**Finalidade.** Distinguir que valores uma posição do programa admite.

No recorte inicial, usamos três tipos gerais: `number` para números, `string` para textos e `boolean` para `true` e `false`. Um tipo fornece informação para verificar operações e compatibilidade. A palavra `number` nomeia um tipo; `15000` representa um valor admitido por esse tipo.

| Valor escrito | Tipo geral usado neste degrau |
| --- | --- |
| `15000` | `number` |
| `"15000"` | `string` |
| `"reembolso-01"` | `string` |
| `true` e `false` | `boolean` |

**Contraste.** O texto `"15000"` contém algarismos, mas isso não o torna um número. Escrever um tipo ao lado de um nome não converte texto em número. Conversão não é ensinada nem exigida neste bloco.

**Tarefa resolvida.** “Qual tipo geral admite `true` e `false`?” Resposta: `boolean`, e não um dos dois valores isoladamente.

**Precisão.** O TypeScript também tem tipos literais mais específicos. Portanto, a pergunta deste degrau pede o tipo geral usado para representar a categoria, não afirma que toda inferência do compilador dará sempre esse tipo geral. Os tipos literais são estudados no degrau 11.

**Aceite do conteúdo.** Identificar o tipo geral correto e não confundir o nome de um tipo com um valor desse tipo.

**Cartões de origem:** C005–C008. O piloto já cobre C005 por `ts.type.number`.

## D03 — Vinculação, inicialização e anotação

**Finalidade.** Dar um nome a um valor para poder referenciá-lo em outras expressões.

```ts
const amount: number = 15000;
const id: string = "reembolso-01";
```

Em cada declaração, `const` estabelece uma vinculação que não pode ser reatribuída depois da inicialização. `amount` e `id` são identificadores. `: number` e `: string` são anotações de tipo. O `=` introduz a expressão inicializadora. O ponto e vírgula encerra a declaração na forma escrita que usamos.

Aqui, `=` não pergunta se dois valores são iguais. Ele participa da inicialização. A igualdade estrita será escrita com `===` no degrau seguinte.

```ts
const amount = 15000;
```

Esta forma também declara a constante pedida quando o enunciado permite omitir a anotação. O TypeScript infere um tipo. Uma tarefa que exige explicitamente a anotação cobra uma habilidade adicional e deve dizer isso no enunciado.

**Contraste.** Após `const amount = 15000;`, escrever `amount = 5000;` tenta reatribuir a vinculação e é rejeitado. `let` permite reatribuição, mas não atende a um exercício que pede uma declaração `const`. A diferença entre reatribuir um nome e modificar uma propriedade aparecerá no degrau 5.

**Diagnóstico resolvido.** `const amount: number = "15000";` fornece texto onde a anotação exige um número. O problema é incompatibilidade de tipo; a anotação não converte o inicializador.

**Aceite do conteúdo.** Uma declaração, identificador solicitado e inicializador correto. Aceitar formatação equivalente. Cobrar anotação somente quando o enunciado a exigir. Reconhecer o papel de `const`, `:`, `=` e do inicializador.

**Cartões de origem:** C009–C014. O piloto cobre a construção numérica C010 por `ts.binding.const_number`; isso não cobre automaticamente todos os outros cartões deste degrau.

## D04 — Expressões e operadores

**Finalidade.** Obter um resultado a partir de valores já disponíveis.

Uma expressão é uma construção que, quando sua avaliação termina normalmente, produz um valor. Um operador determina uma operação sobre seus operandos. O resultado pode ter um tipo diferente do tipo dos operandos.

```ts
const amount: number = 15000;
const id: string = "r1";
const isSigned: boolean = true;
const hasPages: boolean = false;

amount > 10000
id === "r1"
isSigned && hasPages
!isSigned
amount + 100
```

As cinco expressões produzem, respectivamente, `true`, `true`, `false`, `false` e `15100`. `>` compara números; `===` verifica igualdade estrita; `&&`, aplicado aos booleanos deste exercício, exige ambos verdadeiros; `!` nega um booleano; `+`, aplicado aos números deste exercício, soma.

O resultado booleano pode representar se uma condição foi satisfeita. A linguagem não decide a política de negócio: quem definiu o exemplo escolheu a condição `amount > 10000`.

| Expressão | Resultado | Motivo |
| --- | --- | --- |
| `15000 > 10000` | `true` | O primeiro valor ultrapassa o segundo |
| `10000 > 10000` | `false` | Igualdade não satisfaz “estritamente maior” |
| `5000 > 10000` | `false` | O primeiro valor está abaixo do limite |
| `10000 >= 10000` | `true` | `>=` inclui igualdade |

`>=` é apresentado como contraste de fronteira, sem criar outro degrau. `&&` e `!` são ensinados aqui com operandos booleanos. Não generalize a explicação de `&&` para operandos arbitrários da linguagem.

**Tarefa resolvida.** Para exigir simultaneamente assinatura e páginas, escreva `isSigned && hasPages`. Usar somente `isSigned` elimina uma parte da condição; usar `||` expressaria outra regra.

**Aceite do conteúdo.** Construir o operador e os operandos pedidos; interpretar casos abaixo, iguais e acima do limite; distinguir `=` de `===`; não substituir uma expressão parametrizada por um resultado fixo que só serve ao exemplo mostrado.

**Cartões de origem:** C015–C020.

## D05 — Composição de dados: objeto e array

**Finalidade.** Reunir valores que precisam ser tratados em conjunto e acessar suas partes.

```ts
const refund = { id: "r1", amount: 15000 };
const amounts = [15000, 5000, 10000];

refund.amount
amounts[0]
```

O objeto reúne propriedades nomeadas: `id` e `amount`. `refund.amount` acessa a propriedade `amount` e produz `15000`. O array reúne elementos em ordem. O primeiro índice é `0`; `amounts[0]` produz `15000`. São duas formas diferentes de localizar uma parte: nome de propriedade e índice.

O objeto de código representa, neste exemplo, um pedido de reembolso. Não é o reembolso ocorrido na realidade. A forma de representação não prova que os dados correspondem a fatos reais.

```ts
const refund = { amount: 15000 };
refund.amount = 5000;
```

Depois da atribuição, `refund.amount` vale `5000`. A vinculação `refund` continua apontando para o mesmo objeto. `const` não torna suas propriedades imutáveis. Reatribuir `refund` a outro objeto seria outra operação.

**Contrastes.** `{ id: "r1", amount: 15000 }` é um objeto com propriedades. `[15000, 5000]` é um array ordenado. A ordem dos elementos de um array faz parte do resultado cobrado; a ordem das propriedades destes objetos simples não altera o critério do exercício.

**Aceite do conteúdo.** Construir a forma pedida, acessar a parte correta e distinguir vinculação de propriedade. Os exercícios de índices usam índices existentes; ausência fora do array não é introduzida silenciosamente.

**Cartões de origem:** C021–C025.

## D06 — Declarar e usar um tipo nomeado

**Finalidade.** Dar um nome reutilizável à forma de dados que o programa espera.

```ts
type Refund = {
  id: string;
  amount: number;
};

const refunds: Refund[] = [];
```

`type Refund = ...` declara um nome de tipo. As propriedades `id` e `amount` são obrigatórias nesta forma. `Refund[]` designa um array de valores compatíveis com `Refund`; `[]` é o array vazio usado como valor inicial.

A declaração de tipo não cria um objeto em execução. Criar um valor continua sendo outra operação, como escrever `{ id: "r1", amount: 15000 }`.

**Diagnóstico resolvido.** `const refund: Refund = { id: "r1" };` não satisfaz a forma declarada porque falta `amount`. Um tipo estrutural descreve requisitos de forma; o nome `Refund` não confere, sozinho, identidade comercial nem validade do pedido.

**Limite.** `amount: number` não garante uma quantia positiva, um documento válido ou a necessidade de revisão. Essas propriedades exigem critérios adicionais, quando fizerem parte da tarefa.

**Aceite do conteúdo.** Declarar o alias solicitado, propriedades e tipos corretos; escrever `Refund[]`; distinguir declaração de tipo de criação de valor. Não rejeitar um alias válido apenas porque o aluno ordenou as propriedades de outro modo.

**Cartões de origem:** C026–C029.

## D07 — Definir uma função

**Finalidade.** Definir uma operação que recebe entradas e produz uma saída ao ser chamada.

```ts
type Refund = { id: string; amount: number };

function getRefundAmount(item: Refund): number {
  return item.amount;
}
```

`function` introduz a definição; `getRefundAmount` é seu nome; `item` é um parâmetro; `Refund` é o tipo de entrada declarado; `number` depois de `)` é o tipo de retorno; `{ ... }` delimita o corpo. A expressão `item.amount` lê uma parte da entrada. `return` encerra essa execução da função e fornece o valor da expressão à chamada.

Definir a função não executa seu corpo. A invocação é estudada no degrau seguinte.

```ts
function isPositive(amount: number): boolean {
  return amount > 0;
}
```

O contrato de tipos informa entrada numérica e saída booleana. O corpo especifica qual relação será calculada: ser estritamente maior que zero. O tipo de retorno, sozinho, não garante que a implementação calcula essa relação corretamente.

**Diagnóstico resolvido.** Retornar `"sim"` em uma função declarada para retornar `boolean` fornece `string`, não `boolean`.

**Aceite do conteúdo.** Identificar parâmetro e retorno, definir a função pedida e produzir a saída correta. Compilar é uma condição de aceite para o código, mas não basta para comprovar seu comportamento.

**Cartões de origem:** C030–C034.

## D08 — Invocar uma função: argumento, retorno e efeito

**Finalidade.** Realizar a operação definida, fornecendo uma entrada concreta.

```ts
function isPositive(amount: number): boolean {
  return amount > 0;
}

isPositive(5000);
isPositive(0);
```

`amount` é o parâmetro na definição. `5000` e `0` são argumentos fornecidos nas respectivas invocações. A primeira chamada devolve `true`; a segunda, `false`. Os parênteses indicam a chamada. O nome da função sem os parênteses pode referenciar a própria função, assunto do degrau 10.

```ts
const amount = 15000;
console.log(amount);
```

`console` é um objeto fornecido pelo ambiente e `log` é uma função acessada como propriedade. A chamada apresenta o valor no console: esse é seu efeito observável. O valor apresentado não é o valor de retorno da chamada; neste exemplo, o retorno é `undefined`.

`isPositive` calcula um resultado sem apresentar texto nem modificar dados externos. `console.log` produz um efeito de saída. A definição de função não implica que toda função seja pura.

**Aceite do conteúdo.** Fornecer o argumento correto, interpretar o resultado e distinguir definição, invocação, parâmetro, argumento, valor de retorno e efeito.

**Cartões de origem:** C035–C038.

## D09 — Compor funções

**Finalidade.** Usar um resultado intermediário como entrada de outra operação.

```ts
function getAmount(item: { amount: number }): number {
  return item.amount;
}
function isAboveLimit(amount: number, limit: number): boolean {
  return amount > limit;
}
const refund = { amount: 15000 };

isAboveLimit(getAmount(refund), 10000);
```

Neste código, a chamada a `getAmount` produz `15000`. Esse resultado ocupa o primeiro argumento de `isAboveLimit`. Com o limite `10000`, a chamada externa produz `true`.

O produto intermediário é um número. Ele pode alimentar a segunda função porque ela admite um número nessa posição. Esta relação é composição de operações por passagem de resultado, não parte–todo entre os conceitos ensinados.

**Contraste.** Uma função `getId` que retorna `string` não pode alimentar diretamente um parâmetro que exige `number`. A ordem textual dos nomes não resolve incompatibilidade de tipos.

**Tarefa resolvida.** A construção `isAboveLimit(getAmount(refund), 10000)` preserva as duas funções e conecta suas entradas e saídas. Responder somente `true` não realiza a tarefa de construir a composição para o valor fornecido.

**Aceite do conteúdo.** Construir a composição pedida, identificar o resultado intermediário, interpretar a ordem das invocações deste exemplo e reconhecer incompatibilidades entre saída e entrada.

**Cartões de origem:** C039–C042.

## D10 — Função como valor e callback

**Finalidade.** Guardar ou fornecer uma operação para que outro trecho possa chamá-la.

```ts
function isPositive(amount: number): boolean {
  return amount > 0;
}
const check = isPositive;
```

`isPositive` sem parênteses referencia o valor função. `check` passa a referenciar essa função. Já `isPositive(5)` chama a função e produz um booleano. Guardar a função e guardar seu resultado são operações diferentes.

```ts
const isPositive = (x: number): boolean => x > 0;
type Check = (x: number) => boolean;
```

A primeira linha define um valor função por uma arrow function. O corpo de expressão devolve o resultado de `x > 0`. A segunda declara um tipo de função; ela não cria uma função executável. O contexto distingue os dois usos de `=>`.

```ts
function applyCheck(x: number, check: (value: number) => boolean): boolean {
  return check(x);
}

applyCheck(5, isPositive);
```

A função recebida em `check` é chamada com `x`. Neste exemplo, essa chamada ocorre imediatamente durante `applyCheck`. O fato de uma função ser passada como callback não a torna assíncrona.

**Aceite do conteúdo.** Referenciar sem invocar quando isso for pedido; diferenciar função de resultado; escrever uma arrow function; escrever um tipo de função e passar a função compatível como argumento.

**Cartões de origem:** C043–C047.

## D11 — Tipos literais e união

**Finalidade.** Restringir um resultado às alternativas que o recorte do programa admite.

```ts
type ReviewStatus = "required" | "not_required";
```

Na posição de tipo, `"required"` é um tipo literal que admite esse valor textual específico. `string` é mais abrangente. O operador `|` constrói uma união: um valor admitido pode satisfazer uma ou mais alternativas. Neste exemplo, os dois valores textuais são distintos; isso não significa que toda união da linguagem seja uma partição de alternativas exclusivas.

```ts
const reviewStatus: ReviewStatus = "required";
```

O inicializador satisfaz a união. `"pending"` não satisfaz nenhuma das duas alternativas declaradas.

**Contrastes.** `|` em uma posição de tipo não executa uma decisão e não é o operador lógico `||`. Declarar `ReviewStatus` não classifica nenhum reembolso. Uma função posterior realizará a classificação segundo a política escolhida.

**Aceite do conteúdo.** Escrever os tipos literais exatos, formar a união, reconhecer um valor fora dela e distinguir união de tipos de escolha de ramo em execução.

**Cartões de origem:** C048–C051.

## D12 — Seleção condicional e cobertura dos caminhos

**Finalidade.** Fazer a operação adequada ao resultado de uma condição.

```ts
type ReviewStatus = "required" | "not_required";

function classify(amount: number): ReviewStatus {
  if (amount > 10000) {
    return "required";
  } else {
    return "not_required";
  }
}
```

A chamada avalia a condição. Se ela for verdadeira, executa o primeiro ramo. Caso contrário, executa o `else`. O ramo escolhido devolve a classificação e encerra a execução da função. Para `15000`, a saída é `"required"`; para `10000` ou `5000`, é `"not_required"`.

Uma forma equivalente, quando o enunciado permite, é devolver no primeiro ramo e escrever o outro `return` depois do `if`. O retorno anterior faz com que esse segundo caminho só seja alcançado quando a condição foi falsa.

**Diagnóstico resolvido.** Em `function label(required: boolean): string { if (required) { return "required"; } }`, o caminho em que `required` é falso termina sem devolver uma string. Esse caminho importa mesmo que uma chamada de demonstração use somente `true`.

**Aceite do conteúdo.** Condição e fronteira corretas, rótulos corretos e retorno em todos os caminhos exigidos. Casos abaixo, iguais e acima do limite precisam ser verificados. Se o enunciado exigir `if/else`, cobrá-lo; se pedir somente o comportamento, aceitar as formas equivalentes especificadas na rubrica.

**Cartões de origem:** C052–C055.

## D13 — Ausência e estreitamento de tipos

**Finalidade.** Lidar com uma entrada que pode estar ausente sem tratá-la como um objeto presente.

```ts
type Refund = { id: string; amount: number };
type MaybeRefund = Refund | undefined;

function getAmount(item: Refund | undefined): number | undefined {
  if (item === undefined) {
    return undefined;
  }
  return item.amount;
}
```

O tipo de entrada admite um `Refund` ou `undefined`. Quando a entrada está ausente, a função retorna antes do acesso à propriedade. No caminho restante, o TypeScript sabe que a alternativa `undefined` foi excluída. Esse refinamento do tipo conhecido por condições e fluxo de controle é chamado de narrowing.

A análise não converte `undefined` em objeto nem modifica o valor. Ela estabelece que aquele caminho de execução só é alcançado com a alternativa adequada.

**Contraste de domínio.** `"not_required"` significa que uma quantia conhecida não exige revisão pela política do exemplo. `undefined`, no resultado da busca adotada aqui, significa que o item não foi encontrado na coleção consultada. Ausência de item não é uma classificação negativa da necessidade de revisão.

**Precondição da verificação.** Os exercícios são verificados com `strictNullChecks: true`, incluído em `strict: true`. Sem essa opção, a análise de ausência não tem o contrato pretendido por este bloco.

**Aceite do conteúdo.** Declarar a alternativa de ausência, testá-la e impedir acesso à propriedade nesse caminho. Não usar uma asserção de tipo como substituta da verificação solicitada.

**Cartões de origem:** C056–C060.

## D14 — Transformar, selecionar e buscar em coleções

**Finalidade.** Escolher uma operação pelo tipo de resultado necessário.

```ts
const amounts = [15000, 5000, 10000];

const adjusted = amounts.map((x) => x + 100);
const selected = amounts.filter((x) => x > 10000);
const found = amounts.find((x) => x === 5000);
```

`adjusted` recebe `[15100, 5100, 10100]`. `map` produz o resultado de uma transformação para cada elemento destes arrays densos. `selected` recebe `[15000]`. `filter` conserva os elementos para os quais a condição foi verdadeira, preservando sua ordem. `found` recebe `5000`. `find` devolve o primeiro elemento que atende à condição, ou `undefined` se nenhum atender.

| Finalidade | Operação | Resultado neste recorte |
| --- | --- | --- |
| Produzir um resultado para cada elemento | `map` | Outro array, com a mesma quantidade de elementos |
| Conservar os elementos que atendem ao critério | `filter` | Outro array, possivelmente vazio |
| Obter o primeiro elemento que atende ao critério | `find` | Um elemento ou `undefined` |

Uma função que calcula uma condição booleana é usada aqui como predicado. Ela pode ser passada como valor, como em `refunds.filter(needsReview)`. Isso reutiliza o degrau 10.

**Contrastes resolvidos.** `amounts.map((x) => x > 10000)` produz `[true, false, false]`; não seleciona as quantias. `amounts.filter((x) => x > 10000)` produz `[15000]`; não produz um booleano por elemento. Uma busca sem correspondência produz `undefined`, não `false` nem um array vazio.

Nos exemplos numéricos deste bloco, com `strictNullChecks`, a busca tem resultado `number | undefined`. Antes de acessar uma propriedade de um objeto encontrado, trate a alternativa de ausência.

**Precisão sobre o tipo da busca.** O tipo pode ser mais específico quando o predicado também refina o tipo do elemento. Nos exercícios que pedem o tipo geral, usamos condições que mantêm esse tipo ou anotamos explicitamente o retorno da callback como `boolean`. O gabarito precisa corresponder ao tipo efetivamente inferido para o código mostrado, na versão de TypeScript usada.

**Casos vazios.** Nestes exemplos, `[].map(...)` e `[].filter(...)` produzem arrays vazios; `[].find(...)` produz `undefined`. As callbacks usadas no material não modificam a coleção de origem. Essa é uma propriedade destas callbacks, não uma garantia de pureza de toda callback possível.

**Aceite do conteúdo.** Escolher o método correto; escrever uma callback com entrada e saída adequadas; preservar ordem; tratar ausência em `find`; distinguir array de resultados, subconjunto e elemento.

**Cartões de origem:** C061–C070.

## D15 — Iteração explícita com `for...of`

**Finalidade.** Executar uma operação para cada elemento de uma coleção.

```ts
const amounts = [15000, 5000, 10000];

for (const amount of amounts) {
  console.log(amount);
}
```

Em cada iteração, `amount` recebe o valor do elemento atual. O corpo apresenta esse valor. Neste exemplo, o console recebe `15000`, depois `5000`, depois `10000`. O identificador recebe o valor, não o índice.

O corpo é executado três vezes. Com um array vazio, é executado zero vezes. Essa contagem vale para os laços finitos deste material, sem interrupção antecipada e sem operações que alterem a quantidade de elementos durante o percurso.

**Contraste.** `map` é a escolha do material quando a finalidade é construir um array de resultados. `for...of` torna explícito o percurso para realizar uma operação no corpo. No exemplo, a finalidade é apresentar cada valor no console.

**Aceite do conteúdo.** Usar `for...of` sobre o array pedido, trabalhar com o valor do elemento e produzir os efeitos na ordem esperada. Considerar também a coleção vazia.

**Cartões de origem:** C071–C074.

## Referências para conferir a semântica da linguagem

O conteúdo original desta conversa é a base pedagógica. As fontes oficiais abaixo foram consultadas para conferir as distinções técnicas. Elas não são a origem da nossa divisão em quinze degraus.

- [TypeScript — Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html): tipos primitivos, objetos, arrays, aliases, uniões e tipos literais.
- [TypeScript — Variable Declaration](https://www.typescriptlang.org/docs/handbook/variable-declarations.html): vinculações `const` e diferença entre reatribuição e mudança de propriedades.
- [TypeScript — More on Functions](https://www.typescriptlang.org/docs/handbook/2/functions.html): definições, assinaturas e valores função.
- [TypeScript — Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html): refinamento por análise de condições e fluxo.
- [TypeScript — strictNullChecks](https://www.typescriptlang.org/tsconfig/strictNullChecks.html): tratamento estático da ausência.
- [TypeScript 5.5 — Inferred Type Predicates](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-5.html): condições sob as quais uma callback pode refinar o tipo inferido.
- [ECMAScript — Indexed Collections](https://tc39.es/ecma262/multipage/indexed-collections.html): operações `map`, `filter` e `find`.
- [TypeScript — Iterators and Generators](https://www.typescriptlang.org/docs/handbook/iterators-and-generators.html): percurso com `for...of`.
