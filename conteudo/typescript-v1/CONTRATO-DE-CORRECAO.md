# Contrato dos exercícios e da correção

Este documento especifica o comportamento pretendido da integração. Ele não afirma que os corretores novos já foram implementados no piloto.

## Entrada e saída de uma instância

Cada família contém `id`, `source_card_id`, `concept_id`, `stage`, `skill`, `mode`, `criterion`, `counterexample` e seis `cases`. Cada caso fornece `id`, `prompt`, `context_code`, `answer`, `answer_explanation`, `explanation`, `criterion` e `parameter_set`; questões de escolha também fornecem `choices`.

Apresente o enunciado e, se existir, o contexto de código. Questões de escolha precisam exibir suas quatro alternativas. `answer` guarda o código da alternativa correta nesses casos; `answer_explanation` guarda seu texto. Nos outros formatos, ambos guardam o modelo de resposta. `explanation` contém a explicação destinada ao aluno. O campo `criterion` orienta a correção; não deve aparecer como um detalhe de implementação no fluxo de estudo.

Para a integração mínima, as alternativas podem ser apresentadas no próprio enunciado e respondidas com A, B, C ou D no campo atual. Botões de escolha são opcionais; esse formato de conteúdo não exige criar outra tela.

`parameter_set` identifica um dos seis conjuntos editoriais, não a dificuldade nem o nível de domínio do aluno. O ID da família identifica a tarefa e seu critério; o ID do caso identifica a pergunta concreta. Esses papéis permanecem separados.

## Quatro formatos de resposta

| `mode` | O que o aluno fornece | Como avaliar |
| --- | --- | --- |
| `choice` | Uma alternativa | Comparar com o ID da alternativa correta desta instância, mantendo o texto visível |
| `token` | Um nome, token ou tipo solicitado | Comparar o conteúdo sintático relevante; não aplicar comparação textual rígida a tipos equivalentes |
| `value` | Um resultado: número, booleano, texto, array ou ausência | Ler o valor no formato definido abaixo e comparar com o resultado esperado |
| `code` | Código que realiza a tarefa | Verificar sintaxe, requisito de construção e comportamento descritos na rubrica |

### Nomes, tokens e tipos

Remova espaços no início e no fim. Preserve maiúsculas e minúsculas em identificadores e palavras da linguagem: `Number` não substitui `number`. F012 pede o token `:`. F032 pede o nome do parâmetro. F033 pede o tipo de retorno mostrado. F040 pede o nome da função interna invocada primeiro. F043 pede a referência à função sem chamada. F061, F064 e F067 pedem `map`, `filter` e `find`, respectivamente.

F070 pede um tipo de resultado de busca. Aceite espaços equivalentes e inversão da ordem dos membros da união, como `number | undefined` e `undefined | number`. Compare a estrutura do tipo, não apenas uma string. Use a resposta da instância: uma das variantes trabalha com texto e outra com um tipo de objeto.

### Valores

Um resultado numérico é um número, não seu texto entre aspas. Aceite separadores numéricos válidos quando o resultado for pedido como notação TypeScript; não aceite uma expressão arbitrária como substituta de um valor solicitado.

Para booleanos, aceite `true` ou `false`, sem aspas. Para a ausência, aceite `undefined`, sem aspas. Para o rótulo textual devolvido por uma função, aceite o texto do rótulo com ou sem um par de aspas simples ou duplas; o enunciado é de interpretação, não de construção de um literal. Para arrays de resultados, aceite uma notação literal de array com os elementos esperados, mantendo ordem e repetições. Não execute código do aluno para ler esse formato.

Nestas famílias, a expressão de contexto é parte da pergunta. Por exemplo, F017 inclui casos de igualdade, acima e abaixo do limite; não vincule a família inteira à resposta `false` do cartão original.

### Código

Verifique no contexto completo da instância, com TypeScript 5.9.3 e `strict: true`. Compilar é necessário para os modelos de construção deste pacote, mas insuficiente: `return "required"` pode compilar e ainda falhar na tarefa de classificar valores abaixo e iguais ao limite.

Aceite diferenças de espaços, quebras de linha e ponto e vírgula final quando a sintaxe continuar válida. Aceite aspas simples ou duplas para os mesmos textos. A ordem das propriedades dos objetos e dos aliases simples deste material não integra o critério; a ordem dos elementos dos arrays integra.

Respeite as equivalências especificadas por família:

| Família | Equivalências ou exigências |
| --- | --- |
| F002 | Literal numérico do valor pedido, como `15000` ou `15_000`; uma conta não atende ao pedido de um literal |
| F010–F011 | `const` e nome pedido; anotação do tipo opcional, se compatível |
| F016 | `amount > limite` ou `limite < amount`, ajustando os nomes da instância; `>=` não é equivalente |
| F018 | `===` nos operandos pedidos, em qualquer ordem; `=` e `==` não atendem |
| F019 | `&&` entre os dois booleanos pedidos, em qualquer ordem, para estes operandos sem efeitos |
| F021–F023 | Forma, nomes e dados pedidos; F022 admite ponto ou colchetes com a mesma chave textual |
| F026–F027 | Declarar `type` quando solicitado; para o array, `Refund[]` e `Array<Refund>` são admitidos |
| F030 | Nome de função solicitado e acesso à propriedade correta; nome do parâmetro pode variar consistentemente |
| F035, F039, F047 | Realizar a chamada solicitada, com argumentos corretos; uma resposta fixa não a substitui |
| F043–F044 | Referenciar a própria função, sem invocá-la |
| F045 | Arrow function com teste estrito `> 0`; corpo de expressão ou bloco com `return` |
| F046 | Tipo de função com entrada e saída pedidas; nome do parâmetro pode variar |
| F048, F056 | União com os membros pedidos; a ordem dos membros pode variar; não ampliar para `string` ou `any` |
| F052 | Usar `if`, com as duas classificações; admite `else` ou retorno após o `if` que retorna no primeiro ramo |
| F058 | Verificação explícita de ausência e acesso somente no caminho presente; admite retorno antecipado ou ramos separados |
| F062, F065, F068 | Usar o método pedido, com callback adequada; o nome da variável que guarda o resultado é livre e guardá-lo é opcional |
| F071 | Usar `for...of`; o nome local do elemento pode variar; apresentar os valores na ordem |

Os gabaritos de F030 e F058 apresentam anotações explícitas. A integração pode admitir a inferência do retorno quando o enunciado não exigir anotação, desde que o contrato seja satisfeito. Não rejeite uma solução válida por utilizar nomes locais diferentes. Não aceite `any`, asserções ou supressões de erro como substitutos do tipo, da verificação ou da construção solicitada.

Um corretor para uma família deve reconhecer sua sintaxe e sua tarefa. Não use correspondência textual exata para código nem palavras-chave para avaliar uma explicação discursiva. A alternativa de escolha fechada foi preparada justamente para não depender de um corretor improvisado de prosa.

## Casos de erro intencional no contexto

As famílias F013, F014, F028, F034, F042, F050, F055 e F057 mostram código rejeitado de propósito. O aluno escolhe o diagnóstico; não precisa corrigir o programa. O campo `context_expected_diagnostic` registra o código de diagnóstico observado com TypeScript 5.9.3. Não trate esses contextos como falha do sistema nem remova o erro antes de mostrá-los.

## Explicação, variante e falha técnica

Depois de avaliar, mostre a explicação da instância e, quando pertinente, o gabarito. O contraexemplo de cada família explica um erro específico do cartão original; ele não diagnostica toda resposta errada. Não diga “você confundiu texto com número” se a resposta apresentada não sustenta essa conclusão.

Use os três estados distintos da correção: correta, incorreta e não avaliada por falha técnica. No contrato do piloto atual, `ungraded` pode estar ausente em uma resposta avaliada e aparece quando vale `true` na falha. O consumidor deve tratar `ungraded === true` como não avaliada; somente a ausência desse campo não informa se a resposta foi correta — é necessário ler também o resultado de correção da API. Não contabilize erro, acerto ou avanço com base em uma falha técnica.

Após uma resposta incorreta avaliada, a variante mantém família, conceito e critério e muda o caso concreto. Mantenha o comportamento de revisão do motor. Não conclua que uma variante ficou calibrada só porque o TypeScript aceitou seu gabarito.

## Relato de uma pergunta ruim

Reutilize o mecanismo de relato já existente. Para permitir uma revisão concreta, vincule o relato ao conceito, família, instância, versão do conteúdo, enunciado apresentado, resposta enviada e decisão do corretor. Aproveite os dados que a aplicação já guarda; não crie armazenamento paralelo sem necessidade.

O aluno pode explicar livremente o problema. As interpretações úteis à revisão são: enunciado ambíguo, informação ausente, gabarito errado, solução válida rejeitada, dificuldade inadequada ou outro problema descrito por ele. Uma sugestão de categoria não substitui o texto do relato.

Na revisão, confronte o relato com o exercício e a resposta concreta. Corrija o menor elemento necessário: texto, critério, gabarito, variante ou implementação do corretor. Registre a revisão do conteúdo. Criar uma família nova só é necessário quando houver outra tarefa ou critério a treinar; trocar o número de um exemplo cria uma variante, não uma família nova.

Este é um ciclo de revisão com participação humana. Geração automática, validação automática de conteúdo novo e adaptação de dificuldade a partir de relatos não estão implementadas por estes arquivos. Preservar o relato fornece material para calibrar essas decisões posteriormente; não demonstra, por si só, que o sistema já aprende com ele.
