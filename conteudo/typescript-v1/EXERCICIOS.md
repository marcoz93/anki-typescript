# Exercícios completos e critérios

Os 74 cartões originais estão preservados nas fontes. Cada família abaixo tem seis instâncias completas em `exercicios.json`. A instância 0 parte do cartão original. Enunciados adaptados tornam explícito o formato de resposta. Questões de significado e diagnóstico com resposta discursiva foram convertidas para escolhas fechadas, com alternativas revisáveis, sem um avaliador de prosa por palavras-chave.

Os critérios e contraexemplos abaixo se referem ao caso-base. Nas variantes, nomes e valores acompanham o enunciado. Uma resposta que é válida em outra tarefa não é, por isso, correta na tarefa atual.

## C001 / F001 — semantico

**Degrau:** D01. **Conceito:** `ts.value.literal_notation`. **Resposta na aplicação:** `choice`.

**Enunciado de origem:** O que é um literal em código?

**Gabarito de origem:**

```text
Uma notação que expressa diretamente um valor.
```

**Critério de aceite:** Identificar o literal como escrita que representa diretamente um valor.

**Explicação para o aluno:** Um literal escreve diretamente um valor; um identificador referencia uma vinculação, e uma operação pode combinar valores.

**Contraexemplo:** `Um nome declarado em outro lugar.`

**Por que não atende:** O nome referencia uma vinculação; não é a definição de literal.

**Variações prontas:** F001-V0 a F001-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C002 / F002 — construtivo

**Degrau:** D01. **Conceito:** `ts.value.numeric_literal`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Escreva o literal numérico que representa quinze mil.

**Gabarito de origem:**

```text
15000
```

**Critério de aceite:** Um literal numérico do valor pedido; aceitar separadores numéricos válidos; não aceitar texto nem cálculo.

**Explicação para o aluno:** O número pedido é representado diretamente, sem aspas. Uma conta com o mesmo resultado não é um único literal.

**Contraexemplo:** `"15000"`

**Por que não atende:** As aspas produzem texto. O pedido é um literal numérico.

**Variações prontas:** F002-V0 a F002-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C003 / F003 — construtivo

**Degrau:** D01. **Conceito:** `ts.value.string_literal`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Escreva o literal textual que representa o identificador reembolso-01.

**Gabarito de origem:**

```text
"reembolso-01"
```

**Critério de aceite:** Um literal textual do conteúdo exato; aceitar aspas simples ou duplas válidas.

**Explicação para o aluno:** As aspas delimitam o texto; elas não fazem parte do conteúdo representado. Sem elas, o trecho não representa o texto pedido.

**Contraexemplo:** `reembolso-01`

**Por que não atende:** Sem aspas, isso não escreve o literal textual pedido.

**Variações prontas:** F003-V0 a F003-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C004 / F004 — construtivo

**Degrau:** D01. **Conceito:** `ts.value.boolean_literal`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Escreva o literal booleano que representa falsidade.

**Gabarito de origem:**

```text
false
```

**Critério de aceite:** O literal booleano pedido, sem aspas e sem inverter o valor.

**Explicação para o aluno:** Os dois valores booleanos são true e false. Escrevê-los entre aspas produziria texto.

**Contraexemplo:** `"false"`

**Por que não atende:** Texto e booleano são valores de tipos diferentes.

**Variações prontas:** F004-V0 a F004-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C005 / F005 — semantico

**Degrau:** D02. **Conceito:** `ts.type.number`. **Resposta na aplicação:** `token`.

**Enunciado de origem:** Qual é o tipo usado para valores numéricos como 15000?

**Gabarito de origem:**

```text
number
```

**Critério de aceite:** O nome exato do tipo numérico geral: number.

**Explicação para o aluno:** number é o nome do tipo numérico geral. O trecho numérico mostrado representa um valor admitido por esse tipo.

**Contraexemplo:** `15000`

**Por que não atende:** Isso escreve um valor, não o nome do tipo solicitado.

**Variações prontas:** F005-V0 a F005-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C006 / F006 — semantico

**Degrau:** D02. **Conceito:** `ts.type.string`. **Resposta na aplicação:** `token`.

**Enunciado de origem:** Qual é o tipo usado para textos como "reembolso-01"?

**Gabarito de origem:**

```text
string
```

**Critério de aceite:** O nome exato do tipo textual geral: string.

**Explicação para o aluno:** string é o nome do tipo textual geral. O conteúdo entre aspas continua sendo texto, mesmo quando contém algarismos.

**Contraexemplo:** `number`

**Por que não atende:** Algarismos dentro de aspas continuam sendo texto.

**Variações prontas:** F006-V0 a F006-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C007 / F007 — semantico

**Degrau:** D02. **Conceito:** `ts.type.boolean`. **Resposta na aplicação:** `token`.

**Enunciado de origem:** Qual é o tipo cujos valores são true e false?

**Gabarito de origem:**

```text
boolean
```

**Critério de aceite:** O nome exato do tipo dos dois valores booleanos: boolean.

**Explicação para o aluno:** boolean é o tipo geral dos valores true e false; os nomes do tipo e dos valores têm papéis diferentes.

**Contraexemplo:** `true`

**Por que não atende:** Isso é um dos valores; o pedido é o nome do tipo.

**Variações prontas:** F007-V0 a F007-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C008 / F008 — semantico

**Degrau:** D02. **Conceito:** `ts.type.value_type_distinction`. **Resposta na aplicação:** `choice`.

**Enunciado de origem:** Qual é a diferença de tipo entre 15000 e "15000"?

**Gabarito de origem:**

```text
O primeiro é numérico; o segundo, textual.
```

**Critério de aceite:** Distinguir number no primeiro caso e string no segundo.

**Explicação para o aluno:** A presença de aspas distingue o texto do número neste par. Os mesmos algarismos podem aparecer em valores de tipos diferentes.

**Contraexemplo:** `Os dois são number porque têm os mesmos algarismos.`

**Por que não atende:** A notação com aspas representa texto.

**Variações prontas:** F008-V0 a F008-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C009 / F009 — semantico

**Degrau:** D03. **Conceito:** `ts.binding.const_semantics`. **Resposta na aplicação:** `choice`.

**Enunciado de origem:** O que const impede depois da inicialização?

**Gabarito de origem:**

```text
A reatribuição do identificador.
```

**Critério de aceite:** Reconhecer a proibição de reatribuir a vinculação const após sua inicialização.

**Explicação para o aluno:** const proíbe reatribuir a vinculação depois da inicialização. Isso não impede ler o valor nem, por si só, modificar uma propriedade de um objeto.

**Contraexemplo:** `const torna qualquer objeto completamente imutável.`

**Por que não atende:** A proibição é da reatribuição do nome. A mudança de propriedades é outra operação.

**Variações prontas:** F009-V0 a F009-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C010 / F010 — construtivo

**Degrau:** D03. **Conceito:** `ts.binding.const_number`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Declare amount como constante numérica de valor 15000.

**Gabarito de origem:**

```text
const amount: number = 15000;
```

**Critério de aceite:** Uma declaração const com nome e valor pedidos; anotação number opcional.

**Explicação para o aluno:** const declara a vinculação e o inicializador fornece o valor. A anotação number explicita o tipo, mas o enunciado também admite a inferência.

**Contraexemplo:** `let amount = 15000;`

**Por que não atende:** O enunciado pede const. let permite reatribuição.

**Variações prontas:** F010-V0 a F010-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C011 / F011 — construtivo

**Degrau:** D03. **Conceito:** `ts.binding.const_string`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Declare id como constante textual com valor reembolso-01.

**Gabarito de origem:**

```text
const id: string = "reembolso-01";
```

**Critério de aceite:** Uma declaração const textual com nome e conteúdo pedidos; anotação string opcional.

**Explicação para o aluno:** O inicializador textual precisa de aspas. const declara a vinculação, e a anotação string pode explicitar o tipo.

**Contraexemplo:** `const id = 15000;`

**Por que não atende:** O valor fornecido é numérico, não o texto pedido.

**Variações prontas:** F011-V0 a F011-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C012 / F012 — semantico

**Degrau:** D03. **Conceito:** `ts.binding.annotation`. **Resposta na aplicação:** `token`.

**Enunciado de origem:** Qual elemento introduz uma anotação de tipo nesta declaração?

```ts
const amount: number = 15000;
```

**Gabarito de origem:**

```text
: (dois-pontos).
```

**Critério de aceite:** Identificar o token : como introdutor da anotação nesta declaração.

**Explicação para o aluno:** Nesta declaração, os dois-pontos introduzem a anotação de tipo; o sinal de igual introduz a expressão inicializadora.

**Contraexemplo:** `=`

**Por que não atende:** Aqui = introduz o inicializador; : introduz a anotação.

**Variações prontas:** F012-V0 a F012-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C013 / F013 — diagnostico

**Degrau:** D03. **Conceito:** `ts.binding.const_semantics`. **Resposta na aplicação:** `choice`.

**Enunciado de origem:** Por que a segunda linha é rejeitada?

```ts
const amount = 15000;
amount = 5000;
```

**Gabarito de origem:**

```text
Uma vinculação const não pode ser reatribuída.
```

**Critério de aceite:** Identificar a tentativa de reatribuição da vinculação const.

**Explicação para o aluno:** A segunda linha tenta atribuir um novo valor a uma vinculação const. A magnitude do número não muda essa proibição.

**Contraexemplo:** `O número 5000 é grande demais.`

**Por que não atende:** O problema independe da magnitude do novo número.

**Variações prontas:** F013-V0 a F013-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C014 / F014 — diagnostico

**Degrau:** D03. **Conceito:** `ts.binding.assignment_compatibility`. **Resposta na aplicação:** `choice`.

**Enunciado de origem:** Por que a inicialização é rejeitada?

```ts
const amount: number = "15000";
```

**Gabarito de origem:**

```text
O valor é string, incompatível com number.
```

**Critério de aceite:** Identificar string no inicializador contra number na anotação.

**Explicação para o aluno:** A anotação pede number, mas o inicializador entre aspas tem tipo string. Anotar não executa uma conversão.

**Contraexemplo:** `A anotação transforma automaticamente o texto em número.`

**Por que não atende:** Anotar o tipo não executa conversão.

**Variações prontas:** F014-V0 a F014-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C015 / F015 — semantico

**Degrau:** D04. **Conceito:** `ts.expression.value`. **Resposta na aplicação:** `choice`.

**Enunciado de origem:** O que é uma expressão?

**Gabarito de origem:**

```text
Uma construção que, quando avaliada normalmente, produz um valor.
```

**Critério de aceite:** Reconhecer a produção de valor quando a avaliação da expressão termina normalmente.

**Explicação para o aluno:** Uma expressão produz um valor quando sua avaliação termina normalmente. Declarar uma vinculação é outro papel da linguagem.

**Contraexemplo:** `Toda expressão apenas declara um nome.`

**Por que não atende:** Declaração e expressão exercem papéis diferentes.

**Variações prontas:** F015-V0 a F015-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C016 / F016 — construtivo

**Degrau:** D04. **Conceito:** `ts.expression.greater_than`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Escreva uma expressão que verifica se amount é estritamente maior que 10000.

```ts
const amount = 15000;
```

**Gabarito de origem:**

```text
amount > 10000
```

**Critério de aceite:** Construir a comparação com > entre o identificador e o limite pedidos; aceitar L < amount como equivalente.

**Explicação para o aluno:** O operador > exige que o primeiro número ultrapasse o segundo. Quando são iguais, a condição é falsa.

**Contraexemplo:** `amount >= 10000`

**Por que não atende:** >= inclui igualdade e altera a fronteira da regra.

**Variações prontas:** F016-V0 a F016-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C017 / F017 — interpretativo

**Degrau:** D04. **Conceito:** `ts.expression.greater_than`. **Resposta na aplicação:** `value`.

**Enunciado de origem:** Qual valor esta expressão produz?

```ts
10000 > 10000
```

**Gabarito de origem:**

```text
false
```

**Critério de aceite:** Calcular o booleano da comparação mostrada, incluindo a igualdade no limite.

**Explicação para o aluno:** Compare os dois operandos: > só produz true quando o primeiro é estritamente maior que o segundo; a igualdade produz false.

**Contraexemplo:** `true`

**Por que não atende:** Na igualdade, > é falso. Em outras variantes, confira os dois operandos.

**Variações prontas:** F017-V0 a F017-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C018 / F018 — construtivo

**Degrau:** D04. **Conceito:** `ts.expression.strict_equality`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Escreva uma expressão que verifica a igualdade estrita de id com o texto r1.

```ts
const id: string = "r1";
```

**Gabarito de origem:**

```text
id === "r1"
```

**Critério de aceite:** Construir igualdade estrita com === e os valores pedidos; aceitar inversão dos operandos.

**Explicação para o aluno:** === verifica igualdade estrita. O sinal = isolado serve à atribuição ou inicialização, conforme o contexto.

**Contraexemplo:** `id = "r1"`

**Por que não atende:** Atribuição não verifica igualdade estrita.

**Variações prontas:** F018-V0 a F018-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C019 / F019 — construtivo

**Degrau:** D04. **Conceito:** `ts.expression.boolean_and`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Escreva uma expressão que exige simultaneamente isSigned e hasPages.

```ts
const isSigned: boolean = true;
const hasPages: boolean = false;
```

**Gabarito de origem:**

```text
isSigned && hasPages
```

**Critério de aceite:** Construir && entre os booleanos pedidos; aceitar a troca de ordem destes operandos sem efeitos.

**Explicação para o aluno:** Com estes operandos booleanos, && produz true somente quando ambos são true. Se qualquer um for false, o resultado é false.

**Contraexemplo:** `isSigned `

**Por que não atende:** | hasPages|A disjunção admite apenas uma condição verdadeira; a tarefa exige ambas.

**Variações prontas:** F019-V0 a F019-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C020 / F020 — construtivo

**Degrau:** D04. **Conceito:** `ts.expression.boolean_not`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Escreva uma expressão que nega o valor de isValid.

```ts
const isValid: boolean = true;
```

**Gabarito de origem:**

```text
!isValid
```

**Critério de aceite:** Negar o booleano pedido usando !.

**Explicação para o aluno:** ! inverte um valor booleano: true passa a false e false passa a true.

**Contraexemplo:** `isValid`

**Por que não atende:** A referência isolada mantém o valor, não o nega.

**Variações prontas:** F020-V0 a F020-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C021 / F021 — construtivo

**Degrau:** D05. **Conceito:** `ts.data.object`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Declare refund como objeto com id igual a r1 e amount igual a 15000.

**Gabarito de origem:**

```text
const refund = { id: "r1", amount: 15000 };
```

**Critério de aceite:** Declarar const com objeto, propriedades e valores pedidos; ordem das propriedades é livre.

**Explicação para o aluno:** O objeto agrupa propriedades nomeadas. Cada propriedade associa o nome indicado ao valor pedido.

**Contraexemplo:** `const refund = ["r1", 15000];`

**Por que não atende:** Um array posicional não é o objeto com as propriedades solicitadas.

**Variações prontas:** F021-V0 a F021-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C022 / F022 — construtivo

**Degrau:** D05. **Conceito:** `ts.data.property`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Escreva uma expressão que obtém a propriedade amount.

```ts
const refund = { id: "r1", amount: 15000 };
```

**Gabarito de origem:**

```text
refund.amount
```

**Critério de aceite:** Acessar a propriedade pedida; aceitar ponto ou colchetes com literal textual correspondente.

**Explicação para o aluno:** O acesso à propriedade obtém a parte nomeada do objeto. Acessar outra propriedade pode produzir outro valor e outro tipo.

**Contraexemplo:** `refund.id`

**Por que não atende:** Essa propriedade é outra parte do objeto.

**Variações prontas:** F022-V0 a F022-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C023 / F023 — construtivo

**Degrau:** D05. **Conceito:** `ts.data.array`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Declare amounts como array contendo, em ordem, 15000, 5000 e 10000.

**Gabarito de origem:**

```text
const amounts = [15000, 5000, 10000];
```

**Critério de aceite:** Declarar o array com os elementos na ordem solicitada.

**Explicação para o aluno:** O array mantém a sequência de elementos. Mudar a ordem muda o array solicitado.

**Contraexemplo:** `const amounts = [5000, 15000, 10000];`

**Por que não atende:** A ordem pedida faz parte do resultado.

**Variações prontas:** F023-V0 a F023-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C024 / F024 — interpretativo

**Degrau:** D05. **Conceito:** `ts.data.array_index`. **Resposta na aplicação:** `value`.

**Enunciado de origem:** Qual valor é obtido ao acessar o índice 0?

```ts
const amounts = [15000, 5000, 10000];
amounts[0]
```

**Gabarito de origem:**

```text
15000
```

**Critério de aceite:** Obter o elemento no índice mostrado, contando a partir de zero.

**Explicação para o aluno:** O índice inicial de um array é zero. O índice 1 aponta para o segundo elemento, e assim por diante.

**Contraexemplo:** `5000`

**Por que não atende:** Na variante original, índice 0 designa 15000. Recalcule com o índice de cada variante.

**Variações prontas:** F024-V0 a F024-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C025 / F025 — interpretativo

**Degrau:** D05. **Conceito:** `ts.data.binding_vs_property`. **Resposta na aplicação:** `choice`.

**Enunciado de origem:** Qual valor tem refund.amount depois da segunda linha?

```ts
const refund = { amount: 15000 };
refund.amount = 5000;
```

**Gabarito de origem:**

```text
5000. const protege a vinculação, não a propriedade.
```

**Critério de aceite:** Reconhecer o valor da propriedade após a atribuição e distinguir a vinculação const.

**Explicação para o aluno:** A atribuição modifica uma propriedade do objeto. A vinculação const continua apontando para esse mesmo objeto.

**Contraexemplo:** `A propriedade continua 15000 porque o nome é const.`

**Por que não atende:** const não impede esta atribuição à propriedade mutável.

**Variações prontas:** F025-V0 a F025-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C026 / F026 — construtivo

**Degrau:** D06. **Conceito:** `ts.type.object_alias`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Declare o tipo Refund, com id textual e amount numérico.

**Gabarito de origem:**

```text
type Refund = { id: string; amount: number };
```

**Critério de aceite:** Declarar type com nome, propriedades obrigatórias e tipos pedidos; ordem das propriedades é livre.

**Explicação para o aluno:** type introduz um nome para o tipo descrito. As propriedades declaradas sem marcador de opcionalidade são obrigatórias neste exemplo.

**Contraexemplo:** `const Refund = { id: "r1", amount: 15000 };`

**Por que não atende:** Isso cria um valor, não declara o alias de tipo solicitado.

**Variações prontas:** F026-V0 a F026-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C027 / F027 — construtivo

**Degrau:** D06. **Conceito:** `ts.type.array`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Declare refunds como um array vazio de Refund.

```ts
type Refund = { id: string; amount: number };
```

**Gabarito de origem:**

```text
const refunds: Refund[] = [];
```

**Critério de aceite:** Declarar array vazio com o tipo de elementos Refund; aceitar Refund[] ou Array<Refund>.

**Explicação para o aluno:** O tipo do array descreve seus elementos. Refund[] e Array<Refund> são duas notações para esse tipo de array.

**Contraexemplo:** `const refunds: Refund = [];`

**Por que não atende:** Refund é o tipo de um objeto, não o tipo do array.

**Variações prontas:** F027-V0 a F027-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C028 / F028 — diagnostico

**Degrau:** D06. **Conceito:** `ts.type.object_alias`. **Resposta na aplicação:** `choice`.

**Enunciado de origem:** Por que este objeto não satisfaz o tipo Refund?

```ts
type Refund = { id: string; amount: number };
const refund: Refund = { id: "r1" };
```

**Gabarito de origem:**

```text
Falta a propriedade obrigatória amount.
```

**Critério de aceite:** Identificar a propriedade obrigatória ausente.

**Explicação para o aluno:** Para satisfazer o tipo mostrado, o objeto precisa ter todas as propriedades obrigatórias com tipos compatíveis.

**Contraexemplo:** `O nome r1 precisa ser numérico.`

**Por que não atende:** O id já é textual como o tipo pede; falta amount.

**Variações prontas:** F028-V0 a F028-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C029 / F029 — semantico

**Degrau:** D06. **Conceito:** `ts.type.object_alias`. **Resposta na aplicação:** `choice`.

**Enunciado de origem:** Declarar type Refund cria um objeto disponível em execução?

```ts
type Refund = { id: string; amount: number };
```

**Gabarito de origem:**

```text
Não. Declara um nome de tipo, usado na verificação estática.
```

**Critério de aceite:** Distinguir declaração de nome de tipo de criação de objeto em execução.

**Explicação para o aluno:** O alias nomeia um tipo para a verificação estática; não cria um objeto em execução.

**Contraexemplo:** `Sim, type cria um objeto vazio.`

**Por que não atende:** A declaração de alias participa da verificação estática.

**Variações prontas:** F029-V0 a F029-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C030 / F030 — construtivo

**Degrau:** D07. **Conceito:** `ts.function.definition`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Defina getRefundAmount: recebe um Refund e devolve sua quantia.

```ts
type Refund = { id: string; amount: number };
```

**Gabarito de origem:**

```text
function getRefundAmount(item: Refund): number {
  return item.amount;
}
```

**Critério de aceite:** Definir a função pedida com entrada Refund e saída number, lendo a propriedade correta; parâmetro pode ter outro nome consistente.

**Explicação para o aluno:** O parâmetro recebe o objeto. A expressão que acessa a propriedade numérica fornece o valor que return devolve.

**Contraexemplo:** `return item.id;`

**Por que não atende:** A propriedade id é textual e não é a quantia solicitada.

**Variações prontas:** F030-V0 a F030-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C031 / F031 — semantico

**Degrau:** D07. **Conceito:** `ts.function.return`. **Resposta na aplicação:** `choice`.

**Enunciado de origem:** Qual é o papel de return dentro de uma função?

**Gabarito de origem:**

```text
Encerra a execução da função e, se houver expressão, devolve seu valor.
```

**Critério de aceite:** Reconhecer que return encerra a função atual e fornece o valor da expressão quando presente.

**Explicação para o aluno:** return encerra a chamada atual e, quando inclui uma expressão, devolve seu valor ao ponto da chamada. Imprimir é outro efeito.

**Contraexemplo:** `return sempre imprime no console.`

**Por que não atende:** Apresentação no console é outro efeito.

**Variações prontas:** F031-V0 a F031-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C032 / F032 — semantico

**Degrau:** D07. **Conceito:** `ts.function.parameter`. **Resposta na aplicação:** `token`.

**Enunciado de origem:** Qual é o nome do parâmetro declarado nesta função?

```ts
function isPositive(amount: number): boolean {
  return amount > 0;
}
```

**Gabarito de origem:**

```text
amount.
```

**Critério de aceite:** Identificar o nome do parâmetro na definição mostrada.

**Explicação para o aluno:** O parâmetro é o nome declarado entre parênteses na definição. O tipo depois dos dois-pontos informa os valores que ele admite.

**Contraexemplo:** `number`

**Por que não atende:** number é o tipo, não o identificador do parâmetro.

**Variações prontas:** F032-V0 a F032-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C033 / F033 — semantico

**Degrau:** D07. **Conceito:** `ts.function.return_type`. **Resposta na aplicação:** `token`.

**Enunciado de origem:** Qual é o tipo de retorno declarado nesta função?

```ts
function isPositive(amount: number): boolean {
  return amount > 0;
}
```

**Gabarito de origem:**

```text
boolean.
```

**Critério de aceite:** Identificar o tipo declarado depois de ) na assinatura mostrada.

**Explicação para o aluno:** A anotação depois do fechamento dos parâmetros declara o tipo de retorno. Ela tem papel diferente das anotações dos parâmetros.

**Contraexemplo:** `amount`

**Por que não atende:** amount é um identificador, não a anotação de retorno.

**Variações prontas:** F033-V0 a F033-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C034 / F034 — diagnostico

**Degrau:** D07. **Conceito:** `ts.function.return`. **Resposta na aplicação:** `choice`.

**Enunciado de origem:** Por que o corpo não satisfaz o tipo de retorno?

```ts
function isPositive(amount: number): boolean {
  return "sim";
}
```

**Gabarito de origem:**

```text
A expressão de retorno é string, não boolean.
```

**Critério de aceite:** Identificar a incompatibilidade do retorno string com boolean.

**Explicação para o aluno:** O tipo declarado para o retorno precisa admitir o valor devolvido. O texto mostrado não é um booleano.

**Contraexemplo:** `A função tem muitos parâmetros.`

**Por que não atende:** A assinatura tem um parâmetro; o erro é o tipo retornado.

**Variações prontas:** F034-V0 a F034-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C035 / F035 — construtivo

**Degrau:** D08. **Conceito:** `ts.function.invocation`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Invoque isPositive fornecendo 5000 como argumento.

```ts
function isPositive(amount: number): boolean {
  return amount > 0;
}
```

**Gabarito de origem:**

```text
isPositive(5000);
```

**Critério de aceite:** Invocar a função solicitada com o argumento pedido.

**Explicação para o aluno:** Os parênteses realizam a invocação, e o conteúdo fornecido neles é o argumento. Referenciar só o nome não realiza a chamada.

**Contraexemplo:** `isPositive`

**Por que não atende:** Sem os parênteses, a função não foi invocada.

**Variações prontas:** F035-V0 a F035-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C036 / F036 — interpretativo

**Degrau:** D08. **Conceito:** `ts.function.invocation`. **Resposta na aplicação:** `value`.

**Enunciado de origem:** Qual valor esta invocação devolve?

```ts
function isPositive(amount: number): boolean {
  return amount > 0;
}
isPositive(0);
```

**Gabarito de origem:**

```text
false.
```

**Critério de aceite:** Calcular o valor devolvido pela invocação mostrada.

**Explicação para o aluno:** A chamada fornece um número ao parâmetro; o corpo compara esse número com zero e devolve o booleano calculado.

**Contraexemplo:** `true`

**Por que não atende:** Na chamada original com zero, a condição > 0 é falsa. Recalcule nas variantes.

**Variações prontas:** F036-V0 a F036-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C037 / F037 — semantico

**Degrau:** D08. **Conceito:** `ts.function.argument`. **Resposta na aplicação:** `value`.

**Enunciado de origem:** Qual expressão é o argumento desta invocação?

```ts
function isPositive(amount: number): boolean {
  return amount > 0;
}
isPositive(5000);
```

**Gabarito de origem:**

```text
5000.
```

**Critério de aceite:** Identificar a expressão fornecida como argumento da chamada, não o parâmetro da definição.

**Explicação para o aluno:** O argumento é a expressão fornecida na chamada concreta. O parâmetro é o nome usado na definição da função.

**Contraexemplo:** `amount`

**Por que não atende:** amount é o parâmetro. O argumento está nos parênteses da chamada concreta.

**Variações prontas:** F037-V0 a F037-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C038 / F038 — construtivo

**Degrau:** D08. **Conceito:** `ts.effect.console_output`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Apresente o valor de amount no console.

```ts
const amount = 15000;
```

**Gabarito de origem:**

```text
console.log(amount);
```

**Critério de aceite:** Invocar console.log com o valor solicitado.

**Explicação para o aluno:** console.log apresenta o valor no console. Apenas criar outra vinculação não produz essa apresentação.

**Contraexemplo:** `const shown = amount;`

**Por que não atende:** Isso vincula um valor a outro nome, sem apresentar o valor no console.

**Variações prontas:** F038-V0 a F038-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C039 / F039 — construtivo

**Degrau:** D09. **Conceito:** `ts.function.composition`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Use o resultado de getAmount como primeiro argumento de isAboveLimit, com limite 10000.

```ts
function getAmount(item: { amount: number }): number {
  return item.amount;
}
function isAboveLimit(amount: number, limit: number): boolean {
  return amount > limit;
}
const refund = { amount: 15000 };
```

**Gabarito de origem:**

```text
isAboveLimit(getAmount(refund), 10000);
```

**Critério de aceite:** Invocar a função externa com a saída da função interna na posição correta e o limite pedido.

**Explicação para o aluno:** A função interna obtém o número do objeto. A função externa recebe esse número e o limite para calcular a comparação.

**Contraexemplo:** `isAboveLimit(refund, 10000);`

**Por que não atende:** O primeiro parâmetro exige um número; é necessário obter a quantia do objeto.

**Variações prontas:** F039-V0 a F039-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C040 / F040 — interpretativo

**Degrau:** D09. **Conceito:** `ts.function.composition`. **Resposta na aplicação:** `token`.

**Enunciado de origem:** Qual função é invocada primeiro nesta expressão?

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

**Gabarito de origem:**

```text
getAmount.
```

**Critério de aceite:** Identificar a primeira função efetivamente invocada no exemplo fornecido.

**Explicação para o aluno:** Neste exemplo, a chamada interna precisa produzir o argumento numérico antes de a função externa ser invocada.

**Contraexemplo:** `isAboveLimit`

**Por que não atende:** A chamada interna deve produzir o argumento antes da chamada externa neste exemplo.

**Variações prontas:** F040-V0 a F040-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C041 / F041 — interpretativo

**Degrau:** D09. **Conceito:** `ts.function.composition`. **Resposta na aplicação:** `value`.

**Enunciado de origem:** Qual valor a composição devolve?

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

**Gabarito de origem:**

```text
true.
```

**Critério de aceite:** Calcular o resultado booleano da composição a partir do valor intermediário.

**Explicação para o aluno:** Primeiro se obtém a quantia do objeto; depois se compara essa quantia com o limite. O resultado final é booleano.

**Contraexemplo:** `15000`

**Por que não atende:** Esse é o resultado intermediário original, não o resultado da função externa.

**Variações prontas:** F041-V0 a F041-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C042 / F042 — diagnostico

**Degrau:** D09. **Conceito:** `ts.function.composition`. **Resposta na aplicação:** `choice`.

**Enunciado de origem:** Por que a composição é rejeitada?

```ts
function getId(): string { return "r1"; }
function isPositive(x: number): boolean { return x > 0; }
isPositive(getId());
```

**Gabarito de origem:**

```text
A saída string de getId é incompatível com a entrada number de isPositive.
```

**Critério de aceite:** Identificar saída string incompatível com entrada number.

**Explicação para o aluno:** O resultado da função interna precisa ser admitido pelo parâmetro que o recebe. Um texto não satisfaz o parâmetro numérico mostrado.

**Contraexemplo:** `Os nomes das funções precisam ser iguais.`

**Por que não atende:** A compatibilidade relevante é entre os valores e tipos conectados.

**Variações prontas:** F042-V0 a F042-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C043 / F043 — semantico

**Degrau:** D10. **Conceito:** `ts.function.value`. **Resposta na aplicação:** `token`.

**Enunciado de origem:** Qual expressão referencia isPositive sem invocá-la?

```ts
function isPositive(amount: number): boolean {
  return amount > 0;
}
```

**Gabarito de origem:**

```text
isPositive (sem parênteses).
```

**Critério de aceite:** Referenciar o valor função pelo identificador, sem chamar.

**Explicação para o aluno:** O identificador, sem os parênteses de chamada, referencia o valor função. Com parênteses e argumentos, ocorre a invocação.

**Contraexemplo:** `isPositive(5)`

**Por que não atende:** Essa expressão invoca a função e produz um booleano.

**Variações prontas:** F043-V0 a F043-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C044 / F044 — construtivo

**Degrau:** D10. **Conceito:** `ts.function.value`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Vincule a própria função isPositive a um novo identificador check, sem invocá-la.

```ts
function isPositive(amount: number): boolean {
  return amount > 0;
}
```

**Gabarito de origem:**

```text
const check = isPositive;
```

**Critério de aceite:** Vincular a própria função ao novo nome pedido, sem invocação.

**Explicação para o aluno:** A nova vinculação recebe a própria função. Se ela fosse invocada no inicializador, a vinculação receberia seu resultado.

**Contraexemplo:** `const check = isPositive(5);`

**Por que não atende:** Isso vincula o resultado booleano, não a função.

**Variações prontas:** F044-V0 a F044-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C045 / F045 — construtivo

**Degrau:** D10. **Conceito:** `ts.function.arrow`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Defina isPositive como arrow function, de number para boolean, que verifica x > 0.

**Gabarito de origem:**

```text
const isPositive = (x: number): boolean => x > 0;
```

**Critério de aceite:** Definir a arrow function pedida com entrada number e condição > 0; aceitar corpo de expressão ou return em bloco.

**Explicação para o aluno:** A arrow function recebe um número e calcula se ele é maior que zero. Um corpo de expressão devolve essa expressão; um bloco precisa de return.

**Contraexemplo:** `const isPositive = (x: number): boolean => x >= 0;`

**Por que não atende:** O zero seria aceito indevidamente por >=.

**Variações prontas:** F045-V0 a F045-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C046 / F046 — construtivo

**Degrau:** D10. **Conceito:** `ts.type.function`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Declare o tipo Check de uma função que recebe number e devolve boolean.

**Gabarito de origem:**

```text
type Check = (x: number) => boolean;
```

**Critério de aceite:** Declarar alias de tipo de função com entrada number e saída boolean; nome do parâmetro é irrelevante para a compatibilidade.

**Explicação para o aluno:** Um tipo de função descreve os parâmetros e o retorno admitidos. Declará-lo não cria uma função em execução.

**Contraexemplo:** `type Check = boolean;`

**Por que não atende:** Isso nomeia um tipo booleano, não um tipo de função.

**Variações prontas:** F046-V0 a F046-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C047 / F047 — construtivo

**Degrau:** D10. **Conceito:** `ts.function.callback`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Invoque applyCheck com o número 5 e a própria função isPositive.

```ts
function isPositive(amount: number): boolean {
  return amount > 0;
}
function applyCheck(x: number, check: (x: number) => boolean): boolean {
  return check(x);
}
```

**Gabarito de origem:**

```text
applyCheck(5, isPositive);
```

**Critério de aceite:** Passar o número e a função ao parâmetro callback; não passar o resultado da função.

**Explicação para o aluno:** A segunda entrada recebe uma função. A operação applyCheck pode invocá-la; receber um booleano já calculado não fornece essa capacidade.

**Contraexemplo:** `applyCheck(5, isPositive(5));`

**Por que não atende:** O segundo parâmetro espera uma função, não um booleano.

**Variações prontas:** F047-V0 a F047-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C048 / F048 — construtivo

**Degrau:** D11. **Conceito:** `ts.type.union`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Declare ReviewStatus permitindo somente os valores required e not_required.

**Gabarito de origem:**

```text
type ReviewStatus = "required" | "not_required";
```

**Critério de aceite:** Declarar a união dos dois tipos literais pedidos, sem ampliar para string.

**Explicação para o aluno:** A união dos dois tipos literais admite exatamente os dois textos declarados. O tipo string admitiria outros textos.

**Contraexemplo:** `type ReviewStatus = string;`

**Por que não atende:** string admitiria outros textos além das alternativas declaradas.

**Variações prontas:** F048-V0 a F048-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C049 / F049 — semantico

**Degrau:** D11. **Conceito:** `ts.type.union`. **Resposta na aplicação:** `choice`.

**Enunciado de origem:** Qual é a função de | na posição de tipo?

**Gabarito de origem:**

```text
Constrói uma união: o valor deve satisfazer pelo menos uma das alternativas.
```

**Critério de aceite:** Reconhecer união como admissão de valores de pelo menos uma alternativa.

**Explicação para o aluno:** Uma união admite um valor que satisfaça pelo menos uma alternativa. Isso não executa uma escolha de ramo nem converte o valor.

**Contraexemplo:** `O valor precisa satisfazer todas as alternativas ao mesmo tempo.`

**Por que não atende:** Essa descrição não é a de união.

**Variações prontas:** F049-V0 a F049-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C050 / F050 — diagnostico

**Degrau:** D11. **Conceito:** `ts.type.union`. **Resposta na aplicação:** `choice`.

**Enunciado de origem:** Por que a inicialização é rejeitada?

```ts
type ReviewStatus = "required" | "not_required";
const reviewStatus: ReviewStatus = "pending";
```

**Gabarito de origem:**

```text
"pending" não pertence à união ReviewStatus.
```

**Critério de aceite:** Identificar o literal não admitido pela união declarada.

**Explicação para o aluno:** O inicializador precisa pertencer a pelo menos uma alternativa da união. O literal apresentado não pertence a nenhuma delas.

**Contraexemplo:** `Todo texto satisfaz ReviewStatus.`

**Por que não atende:** A união restringe os textos possíveis.

**Variações prontas:** F050-V0 a F050-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C051 / F051 — semantico

**Degrau:** D11. **Conceito:** `ts.type.literal`. **Resposta na aplicação:** `choice`.

**Enunciado de origem:** Qual restrição adicional o tipo literal "required" impõe em relação a string?

**Gabarito de origem:**

```text
Admite apenas o valor textual "required".
```

**Critério de aceite:** Identificar o único valor admitido pelo tipo literal textual mostrado.

**Explicação para o aluno:** Um tipo literal textual admite apenas o texto indicado. string é mais abrangente e admite outros textos.

**Contraexemplo:** `Admite qualquer texto não vazio.`

**Por que não atende:** O tipo literal admite o valor especificado, não uma classe por comprimento.

**Variações prontas:** F051-V0 a F051-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C052 / F052 — construtivo

**Degrau:** D12. **Conceito:** `ts.control.if_else`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Escreva a função classify: devolva "required" se amount > 10000, senão "not_required".

```ts
type ReviewStatus = "required" | "not_required";
```

**Gabarito de origem:**

```text
function classify(amount: number): ReviewStatus {
  if (amount > 10000) {
    return "required";
  } else {
    return "not_required";
  }
}
```

**Critério de aceite:** Definir a função com if, condição > e ambos os retornos; else ou retorno após o if são admitidos no enunciado adaptado.

**Explicação para o aluno:** A condição distingue a quantia acima do limite dos demais casos. Cada caminho precisa devolver o rótulo previsto pela política do exercício.

**Contraexemplo:** `return "required";`

**Por que não atende:** A resposta fixa não classifica os casos abaixo ou iguais ao limite.

**Variações prontas:** F052-V0 a F052-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C053 / F053 — interpretativo

**Degrau:** D12. **Conceito:** `ts.control.if_else`. **Resposta na aplicação:** `choice`.

**Enunciado de origem:** Qual ramo é executado?

```ts
const amount = 10000;
if (amount > 10000) {
  console.log("A");
} else {
  console.log("B");
}
```

**Gabarito de origem:**

```text
O ramo else, que imprime B.
```

**Critério de aceite:** Identificar o ramo executado e o texto apresentado, a partir da condição.

**Explicação para o aluno:** A condição seleciona apenas um dos dois ramos. Se for true, ocorre a apresentação de A; se for false, a de B.

**Contraexemplo:** `O ramo if imprime A quando o valor é igual ao limite.`

**Por que não atende:** O operador > não inclui igualdade.

**Variações prontas:** F053-V0 a F053-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C054 / F054 — interpretativo

**Degrau:** D12. **Conceito:** `ts.control.if_else`. **Resposta na aplicação:** `value`.

**Enunciado de origem:** Qual classificação a função devolve?

```ts
type ReviewStatus = "required" | "not_required";
function classify(amount: number): ReviewStatus {
  if (amount > 10000) { return "required"; }
  return "not_required";
}
classify(10000);
```

**Gabarito de origem:**

```text
not_required.
```

**Critério de aceite:** Calcular o rótulo devolvido pela chamada apresentada.

**Explicação para o aluno:** O resultado depende da comparação estrita com o limite. Igualdade pertence ao caminho not_required, assim como valores abaixo do limite.

**Contraexemplo:** `required`

**Por que não atende:** No caso original, a quantia é igual ao limite e exige not_required.

**Variações prontas:** F054-V0 a F054-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C055 / F055 — diagnostico

**Degrau:** D12. **Conceito:** `ts.control.if_else`. **Resposta na aplicação:** `choice`.

**Enunciado de origem:** Por que esta função pode violar o tipo de retorno declarado?

```ts
function label(required: boolean): string {
  if (required) { return "required"; }
}
```

**Gabarito de origem:**

```text
Se required for false, a execução termina sem devolver uma string.
```

**Critério de aceite:** Reconhecer o caminho que chega ao fim sem a string exigida.

**Explicação para o aluno:** Quando a condição é falsa, a função chega ao fim sem devolver uma string. A existência de return no outro caminho não cobre este caso.

**Contraexemplo:** `Se um ramo retorna string, todos os caminhos estão cobertos.`

**Por que não atende:** O outro caminho também precisa satisfazer o contrato de retorno.

**Variações prontas:** F055-V0 a F055-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C056 / F056 — construtivo

**Degrau:** D13. **Conceito:** `ts.type.optional_result`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Declare MaybeRefund como união de Refund e o tipo de ausência undefined.

```ts
type Refund = { id: string; amount: number };
```

**Gabarito de origem:**

```text
type MaybeRefund = Refund | undefined;
```

**Critério de aceite:** Declarar a união Refund e undefined; aceitar qualquer ordem das alternativas.

**Explicação para o aluno:** A união permite representar um objeto presente ou sua ausência. O tipo do objeto isolado não inclui undefined no modo strict.

**Contraexemplo:** `type MaybeRefund = Refund;`

**Por que não atende:** A alternativa de ausência foi omitida.

**Variações prontas:** F056-V0 a F056-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C057 / F057 — diagnostico

**Degrau:** D13. **Conceito:** `ts.control.narrowing`. **Resposta na aplicação:** `choice`.

**Enunciado de origem:** Por que acessar item.amount é rejeitado em modo strict?

```ts
type Refund = { id: string; amount: number };
function getAmount(item: Refund | undefined): number {
  return item.amount;
}
```

**Gabarito de origem:**

```text
item pode ser undefined; a propriedade amount não existe nessa alternativa.
```

**Critério de aceite:** Reconhecer que item pode ser undefined antes do acesso.

**Explicação para o aluno:** Antes da verificação, a entrada pode ser undefined. Nesse caso, não há objeto do qual acessar a propriedade.

**Contraexemplo:** `Basta afirmar que item é Refund sem verificar.`

**Por que não atende:** Uma asserção não elimina a ausência do valor em execução.

**Variações prontas:** F057-V0 a F057-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C058 / F058 — construtivo

**Degrau:** D13. **Conceito:** `ts.control.narrowing`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Defina getAmount: devolva undefined se item estiver ausente; caso contrário, devolva a quantia.

```ts
type Refund = { id: string; amount: number };
```

**Gabarito de origem:**

```text
function getAmount(item: Refund | undefined): number | undefined {
  if (item === undefined) { return undefined; }
  return item.amount;
}
```

**Critério de aceite:** Verificar explicitamente a ausência e retornar undefined antes do acesso ou usar o ramo presente; retornar a quantia se presente.

**Explicação para o aluno:** O caminho de ausência devolve undefined; o caminho de presença acessa a propriedade numérica. Os dois resultados estão declarados no retorno.

**Contraexemplo:** `return item.amount;`

**Por que não atende:** O acesso não trata a alternativa undefined.

**Variações prontas:** F058-V0 a F058-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C059 / F059 — semantico

**Degrau:** D13. **Conceito:** `ts.control.narrowing`. **Resposta na aplicação:** `choice`.

**Enunciado de origem:** Qual é o tipo conhecido de item após o return condicional?

```ts
type Refund = { id: string; amount: number };
function getAmount(item: Refund | undefined) {
  if (item === undefined) { return undefined; }
  // Qual é o tipo de item aqui?
  return item.amount;
}
```

**Gabarito de origem:**

```text
Refund. A alternativa undefined já encerrou a execução.
```

**Critério de aceite:** Reconhecer Refund no caminho que só é alcançado após excluir undefined.

**Explicação para o aluno:** O caminho em que a entrada é undefined já terminou no return. O código seguinte só é alcançado quando o objeto está presente.

**Contraexemplo:** `number`

**Por que não atende:** O item continua sendo o objeto; number é o tipo de uma de suas propriedades.

**Variações prontas:** F059-V0 a F059-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C060 / F060 — semantico

**Degrau:** D13. **Conceito:** `ts.control.narrowing`. **Resposta na aplicação:** `choice`.

**Enunciado de origem:** O que é narrowing no TypeScript?

**Gabarito de origem:**

```text
Refinamento do tipo conhecido de um valor por análise de condições e fluxo de controle.
```

**Critério de aceite:** Reconhecer refinamento do tipo conhecido pelo fluxo, sem conversão do valor.

**Explicação para o aluno:** O fluxo fornece informação para refinar o tipo conhecido naquele ponto. Isso não converte o valor nem cria um objeto ausente.

**Contraexemplo:** `O compilador converte undefined em objeto.`

**Por que não atende:** A análise exclui caminhos; não cria o objeto ausente.

**Variações prontas:** F060-V0 a F060-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C061 / F061 — seletivo

**Degrau:** D14. **Conceito:** `ts.collection.map`. **Resposta na aplicação:** `token`.

**Enunciado de origem:** Qual método de array produz um resultado para cada elemento de um array denso?

**Gabarito de origem:**

```text
map
```

**Critério de aceite:** Selecionar map quando a finalidade é produzir um resultado para cada elemento.

**Explicação para o aluno:** map produz um resultado por elemento destes arrays densos, conforme a transformação calculada pela callback.

**Contraexemplo:** `filter`

**Por que não atende:** filter conserva elementos em vez de produzir uma transformação por elemento.

**Variações prontas:** F061-V0 a F061-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C062 / F062 — construtivo

**Degrau:** D14. **Conceito:** `ts.collection.map`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Produza um array com cada quantia acrescida de 100, usando map.

```ts
const amounts = [15000, 5000, 10000];
```

**Gabarito de origem:**

```text
const adjusted = amounts.map((x) => x + 100);
```

**Critério de aceite:** Usar map com adição do incremento pedido, produzindo outro array; nome da variável de resultado é livre.

**Explicação para o aluno:** A callback soma o incremento a cada quantia. map reúne esses resultados em outro array, mantendo a ordem destes elementos.

**Contraexemplo:** `amounts.filter((x) => x + 100)`

**Por que não atende:** A callback e o método não produzem o array de valores acrescidos solicitado.

**Variações prontas:** F062-V0 a F062-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C063 / F063 — interpretativo

**Degrau:** D14. **Conceito:** `ts.collection.map`. **Resposta na aplicação:** `value`.

**Enunciado de origem:** Qual array esta expressão devolve?

```ts
const amounts = [15000, 5000, 10000];
amounts.map((x) => x > 10000);
```

**Gabarito de origem:**

```text
[true, false, false].
```

**Critério de aceite:** Calcular o array de booleanos de map, preservando quantidade e ordem do array denso mostrado.

**Explicação para o aluno:** Cada comparação produz um booleano; map reúne esses booleanos na ordem dos elementos. Um array de entrada vazio produz outro array vazio.

**Contraexemplo:** `[15000]`

**Por que não atende:** Isso seria um resultado de seleção, não um booleano por elemento.

**Variações prontas:** F063-V0 a F063-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C064 / F064 — seletivo

**Degrau:** D14. **Conceito:** `ts.collection.filter`. **Resposta na aplicação:** `token`.

**Enunciado de origem:** Qual método de array conserva somente os elementos que satisfazem um predicado?

**Gabarito de origem:**

```text
filter
```

**Critério de aceite:** Selecionar filter para conservar somente elementos que atendem ao predicado.

**Explicação para o aluno:** filter conserva os elementos cujo predicado dá true, mantendo a ordem dos elementos selecionados.

**Contraexemplo:** `map`

**Por que não atende:** map preserva uma posição de resultado por elemento, sem realizar essa seleção.

**Variações prontas:** F064-V0 a F064-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C065 / F065 — construtivo

**Degrau:** D14. **Conceito:** `ts.collection.filter`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Selecione as quantias estritamente maiores que 10000, usando filter.

```ts
const amounts = [15000, 5000, 10000];
```

**Gabarito de origem:**

```text
const selected = amounts.filter((x) => x > 10000);
```

**Critério de aceite:** Usar filter com a condição estrita pedida e conservar elementos e ordem.

**Explicação para o aluno:** O predicado testa a comparação estrita. filter conserva as próprias quantias que passam no teste, e não os booleanos do teste.

**Contraexemplo:** `amounts.map((x) => x > 10000)`

**Por que não atende:** Isso produz booleanos, não as quantias selecionadas.

**Variações prontas:** F065-V0 a F065-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C066 / F066 — interpretativo

**Degrau:** D14. **Conceito:** `ts.collection.filter`. **Resposta na aplicação:** `value`.

**Enunciado de origem:** Qual array esta expressão devolve?

```ts
const amounts = [15000, 5000, 10000];
amounts.filter((x) => x > 10000);
```

**Gabarito de origem:**

```text
[15000].
```

**Critério de aceite:** Calcular o array filtrado, preservando ordem e repetições que satisfaçam a condição.

**Explicação para o aluno:** Apenas as quantias estritamente acima do limite permanecem. Repetições que passam no teste permanecem repetidas e na mesma ordem.

**Contraexemplo:** `[true, false, false]`

**Por que não atende:** Esse é o formato de uma transformação em booleanos, não de seleção das quantias.

**Variações prontas:** F066-V0 a F066-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C067 / F067 — seletivo

**Degrau:** D14. **Conceito:** `ts.collection.find`. **Resposta na aplicação:** `token`.

**Enunciado de origem:** Qual método de array devolve o primeiro elemento que satisfaz um predicado?

**Gabarito de origem:**

```text
find
```

**Critério de aceite:** Selecionar find quando a finalidade é obter o primeiro elemento correspondente.

**Explicação para o aluno:** find devolve o primeiro elemento que satisfaz o predicado; se nenhum satisfizer, devolve undefined.

**Contraexemplo:** `filter`

**Por que não atende:** filter devolve um array de correspondências, não o primeiro elemento ou ausência.

**Variações prontas:** F067-V0 a F067-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C068 / F068 — construtivo

**Degrau:** D14. **Conceito:** `ts.collection.find`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Busque o primeiro reembolso cujo id seja r2, usando find.

```ts
type Refund = { id: string; amount: number };
const refunds: Refund[] = [{ id: "r1", amount: 15000 }, { id: "r2", amount: 5000 }];
```

**Gabarito de origem:**

```text
const found = refunds.find((item) => item.id === "r2");
```

**Critério de aceite:** Usar find sobre a coleção pedida com igualdade estrita do identificador; guardar em const é opcional.

**Explicação para o aluno:** A igualdade estrita compara o identificador. find retorna o primeiro objeto correspondente, ou undefined se não houver correspondência.

**Contraexemplo:** `refunds.filter((item) => item.id === "r2")`

**Por que não atende:** O método retorna um array, mudando o tipo de resultado solicitado.

**Variações prontas:** F068-V0 a F068-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C069 / F069 — interpretativo

**Degrau:** D14. **Conceito:** `ts.collection.find`. **Resposta na aplicação:** `value`.

**Enunciado de origem:** Qual valor esta busca devolve se nenhum elemento satisfaz a condição?

```ts
const amounts = [15000, 5000, 10000];
amounts.find((x) => x === 999);
```

**Gabarito de origem:**

```text
undefined.
```

**Critério de aceite:** Reconhecer undefined quando a busca apresentada não encontra elemento.

**Explicação para o aluno:** Sem elemento correspondente, find devolve undefined. Isso difere de false e de um array vazio.

**Contraexemplo:** `false`

**Por que não atende:** Ausência de elemento não é um resultado booleano falso.

**Variações prontas:** F069-V0 a F069-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C070 / F070 — semantico

**Degrau:** D14. **Conceito:** `ts.collection.find`. **Resposta na aplicação:** `token`.

**Enunciado de origem:** Qual é o tipo do resultado desta busca, com strictNullChecks habilitado?

```ts
const amounts = [15000, 5000, 10000];
const found = amounts.find((x) => x > 10000);
```

**Gabarito de origem:**

```text
number | undefined.
```

**Critério de aceite:** Identificar o tipo de elemento unido a undefined, com strictNullChecks ativo.

**Explicação para o aluno:** Com strictNullChecks, o resultado inclui o tipo do elemento e undefined, pois a busca pode não encontrar correspondência.

**Contraexemplo:** `number`

**Por que não atende:** A possibilidade de não encontrar elemento precisa ser preservada.

**Variações prontas:** F070-V0 a F070-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C071 / F071 — construtivo

**Degrau:** D15. **Conceito:** `ts.iteration.for_of`. **Resposta na aplicação:** `code`.

**Enunciado de origem:** Percorra amounts com for...of e apresente cada quantia no console.

```ts
const amounts = [15000, 5000, 10000];
```

**Gabarito de origem:**

```text
for (const amount of amounts) {
  console.log(amount);
}
```

**Critério de aceite:** Usar for...of e apresentar cada valor com console.log, na ordem; o nome local do elemento pode variar.

**Explicação para o aluno:** for...of percorre os valores do array. O corpo chama console.log com cada valor, na ordem do percurso.

**Contraexemplo:** `for (const amount in amounts) { console.log(amount); }`

**Por que não atende:** for...in percorre chaves; a tarefa pede os valores com for...of.

**Variações prontas:** F071-V0 a F071-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C072 / F072 — semantico

**Degrau:** D15. **Conceito:** `ts.iteration.for_of`. **Resposta na aplicação:** `choice`.

**Enunciado de origem:** O identificador amount recebe o índice ou o valor do elemento em for...of?

```ts
const amounts = [15000, 5000, 10000];
for (const amount of amounts) {
  console.log(amount);
}
```

**Gabarito de origem:**

```text
O valor do elemento.
```

**Critério de aceite:** Reconhecer que a variável do for...of recebe o valor atual do elemento.

**Explicação para o aluno:** A variável do for...of recebe o valor atual do elemento. O índice é outra informação e não é o que essa variável recebe.

**Contraexemplo:** `O índice do elemento.`

**Por que não atende:** O índice não é o valor entregue por esse percurso do array.

**Variações prontas:** F072-V0 a F072-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C073 / F073 — interpretativo

**Degrau:** D15. **Conceito:** `ts.iteration.for_of`. **Resposta na aplicação:** `value`.

**Enunciado de origem:** Quantas vezes o corpo da repetição é executado?

```ts
const amounts = [15000, 5000, 10000];
for (const amount of amounts) {
  console.log(amount);
}
```

**Gabarito de origem:**

```text
3 vezes.
```

**Critério de aceite:** Contar uma execução por elemento do array finito mostrado, sem interrupções antecipadas.

**Explicação para o aluno:** Neste laço sem interrupção nem alteração da coleção, há uma execução do corpo por elemento do array.

**Contraexemplo:** `Sempre 3 vezes.`

**Por que não atende:** A contagem depende da quantidade de elementos da variante.

**Variações prontas:** F073-V0 a F073-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.

## C074 / F074 — interpretativo

**Degrau:** D15. **Conceito:** `ts.iteration.for_of`. **Resposta na aplicação:** `value`.

**Enunciado de origem:** Quantas vezes o corpo da repetição é executado?

```ts
const amounts: number[] = [];
for (const amount of amounts) {
  console.log(amount);
}
```

**Gabarito de origem:**

```text
0 vezes.
```

**Critério de aceite:** Reconhecer zero execuções do corpo quando a coleção está vazia.

**Explicação para o aluno:** Um array vazio não fornece elementos para o percurso; por isso o corpo do laço é executado zero vezes.

**Contraexemplo:** `Uma vez, com undefined.`

**Por que não atende:** Sem elementos, o corpo não começa uma iteração.

**Variações prontas:** F074-V0 a F074-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.
