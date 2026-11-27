#!/usr/bin/env python3
"""Expande o conteúdo editorial fixo. Não gera conteúdo por IA nem altera o aplicativo."""
import csv
import hashlib
import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Ordem, significado e agrupamento vêm dos quinze grupos do TSV original.
STAGES = [
    ('Valor e literal', [], 'Representar valores por literais, distinguindo número, texto e booleano.'),
    ('Tipo', [1], 'Distinguir nomes de tipos gerais e valores admitidos por eles.'),
    ('Vinculação', [1, 2], 'Declarar, inicializar e anotar uma vinculação const.'),
    ('Expressão e operador', [1, 2, 3], 'Construir e interpretar operações que produzem valores.'),
    ('Composição de dados', [1, 2, 3], 'Construir objetos e arrays e acessar suas partes.'),
    ('Declaração de tipos', [2, 5], 'Declarar aliases de tipos de objeto e tipos de arrays.'),
    ('Definição de função', [3, 4, 6], 'Distinguir parâmetros, corpo e retorno e definir uma operação.'),
    ('Invocação', [7], 'Fornecer argumentos e distinguir retorno de efeito.'),
    ('Composição de funções', [7, 8], 'Passar o resultado de uma função a outra com tipos compatíveis.'),
    ('Função como valor', [3, 6, 7, 8], 'Referenciar, vincular, definir e passar funções como valores.'),
    ('União e tipos literais', [1, 2, 6], 'Delimitar alternativas de tipo e reconhecer valores fora delas.'),
    ('Seleção condicional', [4, 7, 8, 11], 'Escolher um ramo e devolver o resultado em cada caminho previsto.'),
    ('Ausência e narrowing', [6, 11, 12], 'Excluir undefined pelo fluxo antes de acessar propriedades.'),
    ('Operações sobre coleções', [4, 5, 6, 8, 10, 13], 'Escolher e usar map, filter e find pelo resultado necessário.'),
    ('Iteração explícita', [5, 8], 'Percorrer valores com for...of, incluindo o caso vazio.'),
]

# As arestas abaixo são decisões pedagógicas desta expansão, não necessidades lógicas.
# Os três IDs e as duas arestas já usadas pelo piloto são preservados.
CONCEPTS = [
    ('ts.value.literal_notation', 'Valor e sua escrita literal', 1, [], [1]),
    ('ts.value.numeric_literal', 'Literal numérico', 1, [], [2]),
    ('ts.value.string_literal', 'Literal textual', 1, ['ts.value.literal_notation'], [3]),
    ('ts.value.boolean_literal', 'Literal booleano', 1, ['ts.value.literal_notation'], [4]),
    ('ts.type.number', 'Tipo number', 2, [], [5]),
    ('ts.type.string', 'Tipo string', 2, ['ts.value.string_literal'], [6]),
    ('ts.type.boolean', 'Tipo boolean', 2, ['ts.value.boolean_literal'], [7]),
    ('ts.type.value_type_distinction', 'Número e texto numérico', 2, ['ts.type.number', 'ts.type.string'], [8]),
    ('ts.binding.const_semantics', 'Vinculação const e reatribuição', 3, ['ts.value.numeric_literal'], [9, 13]),
    ('ts.binding.const_number', 'Declaração const numérica', 3, ['ts.value.numeric_literal', 'ts.type.number'], [10]),
    ('ts.binding.const_string', 'Declaração const textual', 3, ['ts.value.string_literal', 'ts.type.string', 'ts.binding.const_semantics'], [11]),
    ('ts.binding.annotation', 'Anotação de tipo', 3, ['ts.type.number', 'ts.binding.const_number'], [12]),
    ('ts.binding.assignment_compatibility', 'Compatibilidade do inicializador', 3, ['ts.type.value_type_distinction', 'ts.binding.const_number'], [14]),
    ('ts.expression.value', 'Expressão como produtora de valor', 4, ['ts.value.literal_notation', 'ts.binding.const_number'], [15]),
    ('ts.expression.greater_than', 'Comparação estritamente maior', 4, ['ts.binding.const_number', 'ts.type.boolean', 'ts.expression.value'], [16, 17]),
    ('ts.expression.strict_equality', 'Igualdade estrita', 4, ['ts.binding.const_string', 'ts.type.boolean', 'ts.expression.value'], [18]),
    ('ts.expression.boolean_and', 'Conjunção de booleanos', 4, ['ts.type.boolean', 'ts.binding.const_semantics', 'ts.expression.value'], [19]),
    ('ts.expression.boolean_not', 'Negação de booleano', 4, ['ts.type.boolean', 'ts.binding.const_semantics', 'ts.expression.value'], [20]),
    ('ts.data.object', 'Objeto com propriedades', 5, ['ts.binding.const_number', 'ts.binding.const_string'], [21]),
    ('ts.data.property', 'Acesso a propriedade', 5, ['ts.data.object'], [22]),
    ('ts.data.array', 'Array ordenado', 5, ['ts.binding.const_number'], [23]),
    ('ts.data.array_index', 'Acesso por índice', 5, ['ts.data.array'], [24]),
    ('ts.data.binding_vs_property', 'Vinculação e propriedade', 5, ['ts.data.object', 'ts.data.property', 'ts.binding.const_semantics'], [25]),
    ('ts.type.object_alias', 'Alias de tipo de objeto', 6, ['ts.data.object', 'ts.type.number', 'ts.type.string'], [26, 28, 29]),
    ('ts.type.array', 'Tipo de array', 6, ['ts.data.array', 'ts.type.object_alias'], [27]),
    ('ts.function.parameter', 'Parâmetro', 7, ['ts.binding.const_number', 'ts.expression.value'], [32]),
    ('ts.function.return_type', 'Tipo de retorno', 7, ['ts.type.boolean', 'ts.binding.annotation', 'ts.expression.value'], [33]),
    ('ts.function.return', 'Retorno da função', 7, ['ts.expression.greater_than'], [31, 34]),
    ('ts.function.definition', 'Definição de função', 7, ['ts.type.object_alias', 'ts.data.property', 'ts.function.parameter', 'ts.function.return_type', 'ts.function.return'], [30]),
    ('ts.function.invocation', 'Invocação de função', 8, ['ts.function.definition'], [35, 36]),
    ('ts.function.argument', 'Argumento de uma chamada', 8, ['ts.function.parameter', 'ts.function.invocation'], [37]),
    ('ts.effect.console_output', 'Saída no console', 8, ['ts.function.invocation'], [38]),
    ('ts.function.composition', 'Composição de funções', 9, ['ts.function.invocation', 'ts.data.property', 'ts.expression.greater_than'], [39, 40, 41, 42]),
    ('ts.function.value', 'Referência ao valor função', 10, ['ts.function.invocation', 'ts.binding.const_semantics'], [43, 44]),
    ('ts.function.arrow', 'Arrow function', 10, ['ts.function.definition', 'ts.expression.greater_than'], [45]),
    ('ts.type.function', 'Tipo de função', 10, ['ts.function.parameter', 'ts.function.return_type', 'ts.type.object_alias'], [46]),
    ('ts.function.callback', 'Função recebida como argumento', 10, ['ts.function.value', 'ts.type.function', 'ts.function.invocation'], [47]),
    ('ts.type.literal', 'Tipo literal textual', 11, ['ts.type.string'], [51]),
    ('ts.type.union', 'União de tipos', 11, ['ts.type.object_alias', 'ts.type.literal'], [48, 49, 50]),
    ('ts.control.if_else', 'Seleção e caminhos de retorno', 12, ['ts.expression.greater_than', 'ts.type.union', 'ts.function.return', 'ts.function.invocation'], [52, 53, 54, 55]),
    ('ts.type.optional_result', 'União com undefined', 13, ['ts.type.object_alias', 'ts.type.union'], [56]),
    ('ts.control.narrowing', 'Estreitamento por fluxo', 13, ['ts.type.optional_result', 'ts.control.if_else', 'ts.data.property'], [57, 58, 59, 60]),
    ('ts.collection.map', 'Transformação por map', 14, ['ts.data.array', 'ts.function.callback', 'ts.expression.value'], [61, 62, 63]),
    ('ts.collection.filter', 'Seleção por filter', 14, ['ts.data.array', 'ts.function.callback', 'ts.expression.greater_than'], [64, 65, 66]),
    ('ts.collection.find', 'Primeiro resultado ou ausência', 14, ['ts.type.array', 'ts.function.callback', 'ts.expression.strict_equality', 'ts.control.narrowing'], [67, 68, 69, 70]),
    ('ts.iteration.for_of', 'Percurso explícito dos valores', 15, ['ts.data.array', 'ts.effect.console_output'], [71, 72, 73, 74]),
]

# Cada linha tem critério de aceite | resposta que não atende | motivo.
RUBRIC_TEXT = r'''
1|Identificar o literal como escrita que representa diretamente um valor.|Um nome declarado em outro lugar.|O nome referencia uma vinculação; não é a definição de literal.
2|Um literal numérico do valor pedido; aceitar separadores numéricos válidos; não aceitar texto nem cálculo.|"15000"|As aspas produzem texto. O pedido é um literal numérico.
3|Um literal textual do conteúdo exato; aceitar aspas simples ou duplas válidas.|reembolso-01|Sem aspas, isso não escreve o literal textual pedido.
4|O literal booleano pedido, sem aspas e sem inverter o valor.|"false"|Texto e booleano são valores de tipos diferentes.
5|O nome exato do tipo numérico geral: number.|15000|Isso escreve um valor, não o nome do tipo solicitado.
6|O nome exato do tipo textual geral: string.|number|Algarismos dentro de aspas continuam sendo texto.
7|O nome exato do tipo dos dois valores booleanos: boolean.|true|Isso é um dos valores; o pedido é o nome do tipo.
8|Distinguir number no primeiro caso e string no segundo.|Os dois são number porque têm os mesmos algarismos.|A notação com aspas representa texto.
9|Reconhecer a proibição de reatribuir a vinculação const após sua inicialização.|const torna qualquer objeto completamente imutável.|A proibição é da reatribuição do nome. A mudança de propriedades é outra operação.
10|Uma declaração const com nome e valor pedidos; anotação number opcional.|let amount = 15000;|O enunciado pede const. let permite reatribuição.
11|Uma declaração const textual com nome e conteúdo pedidos; anotação string opcional.|const id = 15000;|O valor fornecido é numérico, não o texto pedido.
12|Identificar o token : como introdutor da anotação nesta declaração.|=|Aqui = introduz o inicializador; : introduz a anotação.
13|Identificar a tentativa de reatribuição da vinculação const.|O número 5000 é grande demais.|O problema independe da magnitude do novo número.
14|Identificar string no inicializador contra number na anotação.|A anotação transforma automaticamente o texto em número.|Anotar o tipo não executa conversão.
15|Reconhecer a produção de valor quando a avaliação da expressão termina normalmente.|Toda expressão apenas declara um nome.|Declaração e expressão exercem papéis diferentes.
16|Construir a comparação com > entre o identificador e o limite pedidos; aceitar L < amount como equivalente.|amount >= 10000|>= inclui igualdade e altera a fronteira da regra.
17|Calcular o booleano da comparação mostrada, incluindo a igualdade no limite.|true|Na igualdade, > é falso. Em outras variantes, confira os dois operandos.
18|Construir igualdade estrita com === e os valores pedidos; aceitar inversão dos operandos.|id = "r1"|Atribuição não verifica igualdade estrita.
19|Construir && entre os booleanos pedidos; aceitar a troca de ordem destes operandos sem efeitos.|isSigned || hasPages|A disjunção admite apenas uma condição verdadeira; a tarefa exige ambas.
20|Negar o booleano pedido usando !.|isValid|A referência isolada mantém o valor, não o nega.
21|Declarar const com objeto, propriedades e valores pedidos; ordem das propriedades é livre.|const refund = ["r1", 15000];|Um array posicional não é o objeto com as propriedades solicitadas.
22|Acessar a propriedade pedida; aceitar ponto ou colchetes com literal textual correspondente.|refund.id|Essa propriedade é outra parte do objeto.
23|Declarar o array com os elementos na ordem solicitada.|const amounts = [5000, 15000, 10000];|A ordem pedida faz parte do resultado.
24|Obter o elemento no índice mostrado, contando a partir de zero.|5000|Na variante original, índice 0 designa 15000. Recalcule com o índice de cada variante.
25|Reconhecer o valor da propriedade após a atribuição e distinguir a vinculação const.|A propriedade continua 15000 porque o nome é const.|const não impede esta atribuição à propriedade mutável.
26|Declarar type com nome, propriedades obrigatórias e tipos pedidos; ordem das propriedades é livre.|const Refund = { id: "r1", amount: 15000 };|Isso cria um valor, não declara o alias de tipo solicitado.
27|Declarar array vazio com o tipo de elementos Refund; aceitar Refund[] ou Array<Refund>.|const refunds: Refund = [];|Refund é o tipo de um objeto, não o tipo do array.
28|Identificar a propriedade obrigatória ausente.|O nome r1 precisa ser numérico.|O id já é textual como o tipo pede; falta amount.
29|Distinguir declaração de nome de tipo de criação de objeto em execução.|Sim, type cria um objeto vazio.|A declaração de alias participa da verificação estática.
30|Definir a função pedida com entrada Refund e saída number, lendo a propriedade correta; parâmetro pode ter outro nome consistente.|return item.id;|A propriedade id é textual e não é a quantia solicitada.
31|Reconhecer que return encerra a função atual e fornece o valor da expressão quando presente.|return sempre imprime no console.|Apresentação no console é outro efeito.
32|Identificar o nome do parâmetro na definição mostrada.|number|number é o tipo, não o identificador do parâmetro.
33|Identificar o tipo declarado depois de ) na assinatura mostrada.|amount|amount é um identificador, não a anotação de retorno.
34|Identificar a incompatibilidade do retorno string com boolean.|A função tem muitos parâmetros.|A assinatura tem um parâmetro; o erro é o tipo retornado.
35|Invocar a função solicitada com o argumento pedido.|isPositive|Sem os parênteses, a função não foi invocada.
36|Calcular o valor devolvido pela invocação mostrada.|true|Na chamada original com zero, a condição > 0 é falsa. Recalcule nas variantes.
37|Identificar a expressão fornecida como argumento da chamada, não o parâmetro da definição.|amount|amount é o parâmetro. O argumento está nos parênteses da chamada concreta.
38|Invocar console.log com o valor solicitado.|const shown = amount;|Isso vincula um valor a outro nome, sem apresentar o valor no console.
39|Invocar a função externa com a saída da função interna na posição correta e o limite pedido.|isAboveLimit(refund, 10000);|O primeiro parâmetro exige um número; é necessário obter a quantia do objeto.
40|Identificar a primeira função efetivamente invocada no exemplo fornecido.|isAboveLimit|A chamada interna deve produzir o argumento antes da chamada externa neste exemplo.
41|Calcular o resultado booleano da composição a partir do valor intermediário.|15000|Esse é o resultado intermediário original, não o resultado da função externa.
42|Identificar saída string incompatível com entrada number.|Os nomes das funções precisam ser iguais.|A compatibilidade relevante é entre os valores e tipos conectados.
43|Referenciar o valor função pelo identificador, sem chamar.|isPositive(5)|Essa expressão invoca a função e produz um booleano.
44|Vincular a própria função ao novo nome pedido, sem invocação.|const check = isPositive(5);|Isso vincula o resultado booleano, não a função.
45|Definir a arrow function pedida com entrada number e condição > 0; aceitar corpo de expressão ou return em bloco.|const isPositive = (x: number): boolean => x >= 0;|O zero seria aceito indevidamente por >=.
46|Declarar alias de tipo de função com entrada number e saída boolean; nome do parâmetro é irrelevante para a compatibilidade.|type Check = boolean;|Isso nomeia um tipo booleano, não um tipo de função.
47|Passar o número e a função ao parâmetro callback; não passar o resultado da função.|applyCheck(5, isPositive(5));|O segundo parâmetro espera uma função, não um booleano.
48|Declarar a união dos dois tipos literais pedidos, sem ampliar para string.|type ReviewStatus = string;|string admitiria outros textos além das alternativas declaradas.
49|Reconhecer união como admissão de valores de pelo menos uma alternativa.|O valor precisa satisfazer todas as alternativas ao mesmo tempo.|Essa descrição não é a de união.
50|Identificar o literal não admitido pela união declarada.|Todo texto satisfaz ReviewStatus.|A união restringe os textos possíveis.
51|Identificar o único valor admitido pelo tipo literal textual mostrado.|Admite qualquer texto não vazio.|O tipo literal admite o valor especificado, não uma classe por comprimento.
52|Definir a função com if, condição > e ambos os retornos; else ou retorno após o if são admitidos no enunciado adaptado.|return "required";|A resposta fixa não classifica os casos abaixo ou iguais ao limite.
53|Identificar o ramo executado e o texto apresentado, a partir da condição.|O ramo if imprime A quando o valor é igual ao limite.|O operador > não inclui igualdade.
54|Calcular o rótulo devolvido pela chamada apresentada.|required|No caso original, a quantia é igual ao limite e exige not_required.
55|Reconhecer o caminho que chega ao fim sem a string exigida.|Se um ramo retorna string, todos os caminhos estão cobertos.|O outro caminho também precisa satisfazer o contrato de retorno.
56|Declarar a união Refund e undefined; aceitar qualquer ordem das alternativas.|type MaybeRefund = Refund;|A alternativa de ausência foi omitida.
57|Reconhecer que item pode ser undefined antes do acesso.|Basta afirmar que item é Refund sem verificar.|Uma asserção não elimina a ausência do valor em execução.
58|Verificar explicitamente a ausência e retornar undefined antes do acesso ou usar o ramo presente; retornar a quantia se presente.|return item.amount;|O acesso não trata a alternativa undefined.
59|Reconhecer Refund no caminho que só é alcançado após excluir undefined.|number|O item continua sendo o objeto; number é o tipo de uma de suas propriedades.
60|Reconhecer refinamento do tipo conhecido pelo fluxo, sem conversão do valor.|O compilador converte undefined em objeto.|A análise exclui caminhos; não cria o objeto ausente.
61|Selecionar map quando a finalidade é produzir um resultado para cada elemento.|filter|filter conserva elementos em vez de produzir uma transformação por elemento.
62|Usar map com adição do incremento pedido, produzindo outro array; nome da variável de resultado é livre.|amounts.filter((x) => x + 100)|A callback e o método não produzem o array de valores acrescidos solicitado.
63|Calcular o array de booleanos de map, preservando quantidade e ordem do array denso mostrado.|[15000]|Isso seria um resultado de seleção, não um booleano por elemento.
64|Selecionar filter para conservar somente elementos que atendem ao predicado.|map|map preserva uma posição de resultado por elemento, sem realizar essa seleção.
65|Usar filter com a condição estrita pedida e conservar elementos e ordem.|amounts.map((x) => x > 10000)|Isso produz booleanos, não as quantias selecionadas.
66|Calcular o array filtrado, preservando ordem e repetições que satisfaçam a condição.|[true, false, false]|Esse é o formato de uma transformação em booleanos, não de seleção das quantias.
67|Selecionar find quando a finalidade é obter o primeiro elemento correspondente.|filter|filter devolve um array de correspondências, não o primeiro elemento ou ausência.
68|Usar find sobre a coleção pedida com igualdade estrita do identificador; guardar em const é opcional.|refunds.filter((item) => item.id === "r2")|O método retorna um array, mudando o tipo de resultado solicitado.
69|Reconhecer undefined quando a busca apresentada não encontra elemento.|false|Ausência de elemento não é um resultado booleano falso.
70|Identificar o tipo de elemento unido a undefined, com strictNullChecks ativo.|number|A possibilidade de não encontrar elemento precisa ser preservada.
71|Usar for...of e apresentar cada valor com console.log, na ordem; o nome local do elemento pode variar.|for (const amount in amounts) { console.log(amount); }|for...in percorre chaves; a tarefa pede os valores com for...of.
72|Reconhecer que a variável do for...of recebe o valor atual do elemento.|O índice do elemento.|O índice não é o valor entregue por esse percurso do array.
73|Contar uma execução por elemento do array finito mostrado, sem interrupções antecipadas.|Sempre 3 vezes.|A contagem depende da quantidade de elementos da variante.
74|Reconhecer zero execuções do corpo quando a coleção está vazia.|Uma vez, com undefined.|Sem elementos, o corpo não começa uma iteração.
'''

# Diagnósticos conceituais têm alternativas fechadas. O original aberto fica preservado.
CHOICE_DISTRACTORS = {
    1: ['Um nome que aponta para um valor declarado antes.', 'Uma operação que precisa combinar dois valores.', 'Uma regra que proíbe todos os valores.'],
    8: ['Os dois valores são numéricos.', 'O primeiro é textual; o segundo, numérico.', 'Os dois valores são booleanos.'],
    9: ['Qualquer mudança nas propriedades de um objeto.', 'A leitura do valor pelo identificador.', 'Qualquer chamada de função que use esse valor.'],
    13: ['O segundo número excede o limite permitido pelo tipo number.', 'O identificador deixa de existir na segunda linha.', 'É proibido usar números depois de const.'],
    14: ['A anotação converte o texto e por isso não há erro.', 'O identificador amount só pode ser booleano.', 'O ponto e vírgula transforma o valor em texto.'],
    15: ['Uma construção que sempre cria um novo identificador.', 'Uma construção que nunca produz resultado.', 'Uma declaração que muda obrigatoriamente um dado externo.'],
    25: ['O valor inicial permanece porque const congela toda propriedade.', 'O nome refund é reatribuído a outro objeto.', 'A propriedade passa a ser undefined.'],
    28: ['O id deveria ter o tipo number.', 'type não permite propriedades obrigatórias.', 'O objeto está errado apenas por ser declarado com const.'],
    29: ['Sim. Cria um objeto vazio disponível em execução.', 'Sim. Cria um array com um objeto.', 'Sim. Executa o corpo de uma função.'],
    31: ['Sempre imprime a expressão no console.', 'Sempre reinicia a função atual.', 'Altera automaticamente todos os parâmetros.'],
    34: ['O parâmetro precisa ser um objeto.', 'A função precisa ser chamada antes de ser verificada.', 'A função não pode ter nome.'],
    42: ['Os nomes das funções não são iguais.', 'A função interna precisa retornar duas vezes.', 'Funções nunca podem receber resultados de outras funções.'],
    49: ['Exige satisfazer todas as alternativas simultaneamente.', 'Converte um valor para a primeira alternativa.', 'Escolhe um ramo de execução imediatamente.'],
    50: ['Qualquer string satisfaz a união.', 'É proibido anotar o tipo de uma constante.', 'A ordem das alternativas torna a inicialização inválida.'],
    51: ['Admite qualquer texto não vazio.', 'Admite todos os números.', 'Admite qualquer valor booleano.'],
    53: ['O ramo if, que imprime A.', 'O ramo else, que imprime B.', 'Os dois ramos, primeiro A e depois B.'],
    55: ['Todos os caminhos estão cobertos porque existe um return.', 'Retornar uma string exige imprimir antes.', 'O parâmetro booleano impede qualquer ramo falso.'],
    57: ['O nome item não pode aparecer dentro de funções.', 'Todo objeto tem a propriedade amount em execução.', 'A união converte automaticamente a ausência em Refund.'],
    59: ['undefined. O objeto foi removido.', 'number. O item se tornou sua propriedade.', 'string. O fluxo converteu o objeto em texto.'],
    60: ['Conversão do valor ausente em objeto.', 'Exclusão de todas as condições do programa.', 'Execução antecipada de todas as funções pelo compilador.'],
    72: ['O índice do elemento.', 'O array inteiro em cada passagem.', 'O tipo declarado do array.'],
}

NAMES = [
    ('amount', 'amounts', 'refund', 'refunds', 'Refund', 'ReviewStatus', 'item', 'x', 'isPositive', 'getAmount', 'getRefundAmount', 'check', 'Check', 'MaybeRefund'),
    ('total', 'totals', 'expense', 'expenses', 'Expense', 'ReviewState', 'entry', 'n', 'isAboveZero', 'readTotal', 'readExpenseTotal', 'predicate', 'Predicate', 'MaybeExpense'),
    ('value', 'values', 'request', 'requests', 'RefundRequest', 'ReviewLabel', 'requestItem', 'valueItem', 'hasPositiveValue', 'extractValue', 'extractRequestValue', 'test', 'ValueTest', 'MaybeRequest'),
    ('quantity', 'quantities', 'claim', 'claims', 'Claim', 'ClaimReview', 'claimItem', 'q', 'isPositiveQuantity', 'readQuantity', 'readClaimQuantity', 'verify', 'QuantityTest', 'MaybeClaim'),
    ('requestedValue', 'requestedValues', 'refundCase', 'refundCases', 'RefundCase', 'CaseReview', 'caseItem', 'v', 'isPositiveValue', 'readRequestedValue', 'readCaseValue', 'condition', 'Condition', 'MaybeCase'),
    ('grossAmount', 'grossAmounts', 'refundItem', 'refundItems', 'RefundItem', 'ItemReview', 'record', 'a', 'isPositiveAmount', 'readGrossAmount', 'readItemAmount', 'rule', 'Rule', 'MaybeItem'),
]
NUMBERS = [(15000, 5000, 10000), (18000, 4000, 12000), (9000, 3000, 6000), (30000, 8000, 20000), (1200, 400, 800), (75000, 25000, 50000)]
WORDS = ['quinze mil', 'dezoito mil', 'nove mil', 'trinta mil', 'mil e duzentos', 'setenta e cinco mil']
NUMERIC_CASES = {17, 24, 36, 37, 41, 54, 63, 66, 69, 73, 74}
TOKEN_CASES = {5, 6, 7, 12, 32, 33, 40, 43, 61, 64, 67, 70}
EXPRESSION_CODE = {2, 3, 4, 16, 18, 19, 20, 22}
DIAGNOSTIC_CODES = {13: 2588, 14: 2322, 28: 2741, 34: 2322, 42: 2345, 50: 2322, 55: 2366, 57: 18048}

# Explicações para o aluno. As rubricas acima são instruções para quem corrige.
EXPLANATIONS = '''
1|Um literal escreve diretamente um valor; um identificador referencia uma vinculação, e uma operação pode combinar valores.
2|O número pedido é representado diretamente, sem aspas. Uma conta com o mesmo resultado não é um único literal.
3|As aspas delimitam o texto; elas não fazem parte do conteúdo representado. Sem elas, o trecho não representa o texto pedido.
4|Os dois valores booleanos são true e false. Escrevê-los entre aspas produziria texto.
5|number é o nome do tipo numérico geral. O trecho numérico mostrado representa um valor admitido por esse tipo.
6|string é o nome do tipo textual geral. O conteúdo entre aspas continua sendo texto, mesmo quando contém algarismos.
7|boolean é o tipo geral dos valores true e false; os nomes do tipo e dos valores têm papéis diferentes.
8|A presença de aspas distingue o texto do número neste par. Os mesmos algarismos podem aparecer em valores de tipos diferentes.
9|const proíbe reatribuir a vinculação depois da inicialização. Isso não impede ler o valor nem, por si só, modificar uma propriedade de um objeto.
10|const declara a vinculação e o inicializador fornece o valor. A anotação number explicita o tipo, mas o enunciado também admite a inferência.
11|O inicializador textual precisa de aspas. const declara a vinculação, e a anotação string pode explicitar o tipo.
12|Nesta declaração, os dois-pontos introduzem a anotação de tipo; o sinal de igual introduz a expressão inicializadora.
13|A segunda linha tenta atribuir um novo valor a uma vinculação const. A magnitude do número não muda essa proibição.
14|A anotação pede number, mas o inicializador entre aspas tem tipo string. Anotar não executa uma conversão.
15|Uma expressão produz um valor quando sua avaliação termina normalmente. Declarar uma vinculação é outro papel da linguagem.
16|O operador > exige que o primeiro número ultrapasse o segundo. Quando são iguais, a condição é falsa.
17|Compare os dois operandos: > só produz true quando o primeiro é estritamente maior que o segundo; a igualdade produz false.
18|=== verifica igualdade estrita. O sinal = isolado serve à atribuição ou inicialização, conforme o contexto.
19|Com estes operandos booleanos, && produz true somente quando ambos são true. Se qualquer um for false, o resultado é false.
20|! inverte um valor booleano: true passa a false e false passa a true.
21|O objeto agrupa propriedades nomeadas. Cada propriedade associa o nome indicado ao valor pedido.
22|O acesso à propriedade obtém a parte nomeada do objeto. Acessar outra propriedade pode produzir outro valor e outro tipo.
23|O array mantém a sequência de elementos. Mudar a ordem muda o array solicitado.
24|O índice inicial de um array é zero. O índice 1 aponta para o segundo elemento, e assim por diante.
25|A atribuição modifica uma propriedade do objeto. A vinculação const continua apontando para esse mesmo objeto.
26|type introduz um nome para o tipo descrito. As propriedades declaradas sem marcador de opcionalidade são obrigatórias neste exemplo.
27|O tipo do array descreve seus elementos. Refund[] e Array<Refund> são duas notações para esse tipo de array.
28|Para satisfazer o tipo mostrado, o objeto precisa ter todas as propriedades obrigatórias com tipos compatíveis.
29|O alias nomeia um tipo para a verificação estática; não cria um objeto em execução.
30|O parâmetro recebe o objeto. A expressão que acessa a propriedade numérica fornece o valor que return devolve.
31|return encerra a chamada atual e, quando inclui uma expressão, devolve seu valor ao ponto da chamada. Imprimir é outro efeito.
32|O parâmetro é o nome declarado entre parênteses na definição. O tipo depois dos dois-pontos informa os valores que ele admite.
33|A anotação depois do fechamento dos parâmetros declara o tipo de retorno. Ela tem papel diferente das anotações dos parâmetros.
34|O tipo declarado para o retorno precisa admitir o valor devolvido. O texto mostrado não é um booleano.
35|Os parênteses realizam a invocação, e o conteúdo fornecido neles é o argumento. Referenciar só o nome não realiza a chamada.
36|A chamada fornece um número ao parâmetro; o corpo compara esse número com zero e devolve o booleano calculado.
37|O argumento é a expressão fornecida na chamada concreta. O parâmetro é o nome usado na definição da função.
38|console.log apresenta o valor no console. Apenas criar outra vinculação não produz essa apresentação.
39|A função interna obtém o número do objeto. A função externa recebe esse número e o limite para calcular a comparação.
40|Neste exemplo, a chamada interna precisa produzir o argumento numérico antes de a função externa ser invocada.
41|Primeiro se obtém a quantia do objeto; depois se compara essa quantia com o limite. O resultado final é booleano.
42|O resultado da função interna precisa ser admitido pelo parâmetro que o recebe. Um texto não satisfaz o parâmetro numérico mostrado.
43|O identificador, sem os parênteses de chamada, referencia o valor função. Com parênteses e argumentos, ocorre a invocação.
44|A nova vinculação recebe a própria função. Se ela fosse invocada no inicializador, a vinculação receberia seu resultado.
45|A arrow function recebe um número e calcula se ele é maior que zero. Um corpo de expressão devolve essa expressão; um bloco precisa de return.
46|Um tipo de função descreve os parâmetros e o retorno admitidos. Declará-lo não cria uma função em execução.
47|A segunda entrada recebe uma função. A operação applyCheck pode invocá-la; receber um booleano já calculado não fornece essa capacidade.
48|A união dos dois tipos literais admite exatamente os dois textos declarados. O tipo string admitiria outros textos.
49|Uma união admite um valor que satisfaça pelo menos uma alternativa. Isso não executa uma escolha de ramo nem converte o valor.
50|O inicializador precisa pertencer a pelo menos uma alternativa da união. O literal apresentado não pertence a nenhuma delas.
51|Um tipo literal textual admite apenas o texto indicado. string é mais abrangente e admite outros textos.
52|A condição distingue a quantia acima do limite dos demais casos. Cada caminho precisa devolver o rótulo previsto pela política do exercício.
53|A condição seleciona apenas um dos dois ramos. Se for true, ocorre a apresentação de A; se for false, a de B.
54|O resultado depende da comparação estrita com o limite. Igualdade pertence ao caminho not_required, assim como valores abaixo do limite.
55|Quando a condição é falsa, a função chega ao fim sem devolver uma string. A existência de return no outro caminho não cobre este caso.
56|A união permite representar um objeto presente ou sua ausência. O tipo do objeto isolado não inclui undefined no modo strict.
57|Antes da verificação, a entrada pode ser undefined. Nesse caso, não há objeto do qual acessar a propriedade.
58|O caminho de ausência devolve undefined; o caminho de presença acessa a propriedade numérica. Os dois resultados estão declarados no retorno.
59|O caminho em que a entrada é undefined já terminou no return. O código seguinte só é alcançado quando o objeto está presente.
60|O fluxo fornece informação para refinar o tipo conhecido naquele ponto. Isso não converte o valor nem cria um objeto ausente.
61|map produz um resultado por elemento destes arrays densos, conforme a transformação calculada pela callback.
62|A callback soma o incremento a cada quantia. map reúne esses resultados em outro array, mantendo a ordem destes elementos.
63|Cada comparação produz um booleano; map reúne esses booleanos na ordem dos elementos. Um array de entrada vazio produz outro array vazio.
64|filter conserva os elementos cujo predicado dá true, mantendo a ordem dos elementos selecionados.
65|O predicado testa a comparação estrita. filter conserva as próprias quantias que passam no teste, e não os booleanos do teste.
66|Apenas as quantias estritamente acima do limite permanecem. Repetições que passam no teste permanecem repetidas e na mesma ordem.
67|find devolve o primeiro elemento que satisfaz o predicado; se nenhum satisfizer, devolve undefined.
68|A igualdade estrita compara o identificador. find retorna o primeiro objeto correspondente, ou undefined se não houver correspondência.
69|Sem elemento correspondente, find devolve undefined. Isso difere de false e de um array vazio.
70|Com strictNullChecks, o resultado inclui o tipo do elemento e undefined, pois a busca pode não encontrar correspondência.
71|for...of percorre os valores do array. O corpo chama console.log com cada valor, na ordem do percurso.
72|A variável do for...of recebe o valor atual do elemento. O índice é outra informação e não é o que essa variável recebe.
73|Neste laço sem interrupção nem alteração da coleção, há uma execução do corpo por elemento do array.
74|Um array vazio não fornece elementos para o percurso; por isso o corpo do laço é executado zero vezes.
'''


def plain(value):
    value = value.replace('<br>', '\n').replace('<br/>', '\n').replace('<br />', '\n')
    return html.unescape(re.sub(r'<[^>]+>', '', value)).strip()


def split_front(value):
    code = '\n\n'.join(plain(x) for x in re.findall(r'<pre><code>(.*?)</code></pre>', value, flags=re.S))
    stem = plain(re.sub(r'<pre><code>.*?</code></pre>', '', value, flags=re.S))
    return stem, code


def mapping_for(index):
    mapping = dict(zip(NAMES[0], NAMES[index]))
    high, low, limit = NUMBERS[index]
    mapping.update({'15000': str(high), '5000': str(low), '10000': str(limit),
                    'quinze mil': WORDS[index]})
    if index:
        mapping.update({'reembolso-01': f'reembolso-{index}1', 'r1': f'r{index}1', 'r2': f'r{index}2'})
    return mapping


def rewrite(text, mapping):
    keys = sorted(mapping, key=len, reverse=True)
    pattern = r'(?<![\w])(?:' + '|'.join(re.escape(k) for k in keys) + r')(?![\w])'
    return re.sub(pattern, lambda m: mapping[m.group(0)], text)


def lesson_sections():
    text = (ROOT / 'CURRICULO.md').read_text()
    parts = re.split(r'^## D(\d{2}) — (.+)\n', text, flags=re.M)
    sections = {}
    for i in range(1, len(parts), 3):
        body = parts[i + 2].split('\n## Referências para conferir')[0].strip()
        sections[int(parts[i])] = {'title': parts[i + 1], 'body_markdown': body}
    return sections


def main():
    rows = [r for r in csv.reader((ROOT / 'fontes/anki_typescript_v1.tsv').open(), delimiter='\t') if r and not r[0].startswith('#')]
    assert len(rows) == 74
    rubrics = {}
    for line in RUBRIC_TEXT.strip().splitlines():
        number, criterion, rejected, why = line.split('|', 3)
        rubrics[int(number)] = (criterion, rejected, why)
    assert set(rubrics) == set(range(1, 75))
    explanations = {int(k): v for k, v in (line.split('|', 1) for line in EXPLANATIONS.strip().splitlines())}
    assert set(explanations) == set(rubrics)
    by_card = {}
    concepts = []
    for cid, label, stage, prereqs, cards in CONCEPTS:
        concepts.append({'id': cid, 'label': label, 'stage': stage, 'prerequisites': prereqs,
                         'prerequisite_relation': 'conhecimento_usado_nos_exercicios_deste_conceito',
                         'family_ids': [f'F{x:03}' for x in cards]})
        for card in cards:
            assert card not in by_card
            by_card[card] = cid
    assert set(by_card) == set(range(1, 75))
    sections = lesson_sections()
    stages = []
    for number, (label, dependencies, objective) in enumerate(STAGES, 1):
        stages.append({'id': f'D{number:02}', 'order': number, 'title': label,
                       'teaching_prerequisites': [f'D{x:02}' for x in dependencies],
                       'objective': objective, 'lesson_markdown': sections[number]['body_markdown'],
                       'concept_ids': [c['id'] for c in concepts if c['stage'] == number]})

    families = []
    human = ['# Exercícios completos e critérios\n',
             'Os 74 cartões originais estão preservados nas fontes. Cada família abaixo tem seis instâncias completas em `exercicios.json`. A instância 0 parte do cartão original. Enunciados adaptados tornam explícito o formato de resposta. Questões de significado e diagnóstico com resposta discursiva foram convertidas para escolhas fechadas, com alternativas revisáveis, sem um avaliador de prosa por palavras-chave.\n',
             'Os critérios e contraexemplos abaixo se referem ao caso-base. Nas variantes, nomes e valores acompanham o enunciado. Uma resposta que é válida em outra tarefa não é, por isso, correta na tarefa atual.\n']
    for number, (front, back, tags) in enumerate(rows, 1):
        stage = int(re.search(r'typescript::(\d+)_', tags).group(1))
        skill = re.search(r'habilidade::(\w+)', tags).group(1)
        stem, context = split_front(front)
        answer = plain(back)
        criterion, rejected, why = rubrics[number]
        mode = 'choice' if number in CHOICE_DISTRACTORS else 'code' if skill == 'construtivo' else 'token' if number in TOKEN_CASES else 'value'
        family = {'id': f'F{number:03}', 'source_card_id': f'C{number:03}', 'concept_id': by_card[number],
                  'stage': f'D{stage:02}', 'skill': skill, 'mode': mode,
                  'source': {'front_html': front, 'back_html': back, 'tags': tags},
                  'criterion': criterion, 'counterexample': {'answer': rejected, 'reason': why, 'scope': 'cartao_original'},
                  'feedback_policy': 'Usar a explicação da instância; só atribuir uma causa ao erro quando a resposta sustentar essa interpretação. O contraexemplo é específico do cartão original.',
                  'variation': 'Seis casos editoriais finitos, sem usar uma IA em tempo de execução.',
                  'cases': []}
        for index in range(6):
            mp = mapping_for(index)
            high, low, limit = NUMBERS[index]
            case_stem, case_context, case_answer = (rewrite(s, mp) for s in (stem, context, answer))
            amount, amounts = NAMES[index][:2]
            name = NAMES[index][8]
            # Explicit task contracts remove annotation and syntax ambiguity.
            if number in (10, 11):
                case_stem += ' A anotação de tipo é opcional.'
            if number == 52:
                case_stem += ' Use if. O else é opcional se todos os caminhos devolverem a classificação correta.'
            if number == 58:
                case_stem += ' Use uma verificação explícita de ausência antes do acesso à propriedade.'
            # Questions without a concrete instance gain one, instead of a variant ID in their wording.
            if number == 1:
                examples = ['15000', '"reembolso-11"', 'false', '30000', '"reembolso-41"', 'true']
                case_stem = f'Considere o trecho `{examples[index]}`. Qual descrição explica o que ele é como literal em código?'
            elif number == 4 and index % 2:
                case_stem = 'Escreva o literal booleano que representa verdade.'
                case_answer = 'true'
                case_stem += f' O campo do pedido reembolso-{index + 1:02} deve registrar que o documento está presente.'
            elif number == 4:
                case_stem += f' O campo do pedido reembolso-{index + 1:02} deve registrar que o documento não está presente.'
            elif number == 9:
                case_context = f'const {amount}: number = {high};'
            elif number == 15:
                examples = [f'{high} + 100', f'{high} > {limit}', f'"r{index}1" === "r{index}1"', '!true', 'true && false', f'{high}']
                case_stem = f'Considere `{examples[index]}`. Qual descrição explica o que é uma expressão?'
            elif number == 17:
                lefts = [limit, high, low, limit, high, low]
                left = lefts[index]
                case_context = f'{left} > {limit}'
                case_answer = 'true' if left > limit else 'false'
            elif number == 19:
                names = [('isSigned', 'hasPages'), ('hasReceipt', 'hasId'), ('isComplete', 'isReadable'), ('hasDate', 'hasSignature'), ('isReady', 'isChecked'), ('hasAmount', 'hasDocument')]
                first, second = names[index]
                values = [('true', 'false'), ('true', 'true'), ('false', 'true'), ('false', 'false'), ('true', 'false'), ('false', 'true')]
                a, b = values[index]
                case_stem = f'Escreva uma expressão que exige simultaneamente {first} e {second}.'
                case_context = f'const {first}: boolean = {a};\nconst {second}: boolean = {b};'
                case_answer = f'{first} && {second}'
            elif number == 20:
                variable = ['isValid', 'isReady', 'hasReceipt', 'isComplete', 'hasSignature', 'isChecked'][index]
                value = 'false' if index % 2 else 'true'
                case_stem = f'Escreva uma expressão que nega o valor de {variable}.'
                case_context = f'const {variable}: boolean = {value};'
                case_answer = f'!{variable}'
            elif number == 24:
                at = index % 3
                case_stem = f'Qual valor é obtido ao acessar o índice {at}?'
                case_context = f'const {amounts} = [{high}, {low}, {limit}];\n{amounts}[{at}]'
                case_answer = str([high, low, limit][at])
            elif number == 31:
                case_context = f'function {name}({amount}: number): boolean {{\n  return {amount} > 0;\n}}'
            elif number == 33 and index:
                return_type = ['boolean', 'number', 'string', 'boolean', 'number', 'string'][index]
                case_context = f'function readValue{index}(value: {return_type}): {return_type} {{\n  return value;\n}}'
                case_answer = return_type
            elif number == 36:
                argument = [0, 1, 25, 0, 2, 10][index]
                case_context = re.sub(rf'{name}\(0\)', f'{name}({argument})', case_context)
                case_answer = 'true' if argument > 0 else 'false'
            elif number == 41:
                value = [high, limit, low, high, low, limit][index]
                case_context = case_context.replace(str(high), str(value))
                case_answer = 'true' if value > limit else 'false'
            elif number == 49:
                case_context = f'type {NAMES[index][5]} = "required" | "not_required";'
            elif number == 51:
                literal = ['required', 'not_required', 'r21', 'r31', 'reembolso-41', 'reembolso-51'][index]
                case_stem = f'Qual restrição adicional o tipo literal "{literal}" impõe em relação a string?'
                case_answer = f'Admite apenas o valor textual "{literal}".'
            elif number == 53:
                value = [limit, high, low, high, limit, low][index]
                case_context = case_context.replace(f'= {limit};', f'= {value};', 1)
                case_answer = 'O ramo if, que imprime A.' if value > limit else 'O ramo else, que imprime B.'
            elif number == 54:
                value = [limit, high, low, high, limit, low][index]
                case_context = re.sub(r'classify\(\d+\);', f'classify({value});', case_context)
                case_answer = 'required' if value > limit else 'not_required'
            elif number == 55:
                variable = ['required', 'needsReview', 'isComplete', 'hasReceipt', 'isValid', 'isSigned'][index]
                literal = ['required', 'review', 'complete', 'present', 'valid', 'signed'][index]
                case_context = f'function label{index}({variable}: boolean): string {{\n  if ({variable}) {{ return "{literal}"; }}\n}}'
                case_answer = f'Se {variable} for false, a execução termina sem devolver uma string.'
            elif number == 60:
                cls, parameter = NAMES[index][4], NAMES[index][6]
                case_context = f'type {cls} = {{ id: string; {amount}: number }};\nfunction readValue(item: {cls} | undefined) {{\n  if (item === undefined) {{ return undefined; }}\n  return item.{amount};\n}}'
            elif number in (61, 64, 67):
                case_context = f'const {amounts} = [{high}, {low}, {limit}];'
                purpose = {61: f'produzir um booleano para cada quantia, indicando se ela ultrapassa {limit}',
                           64: f'conservar somente as quantias que ultrapassam {limit}',
                           67: f'obter a primeira quantia que ultrapassa {limit}, ou ausência se nenhuma ultrapassar'}[number]
                case_stem = f'Qual método usar para {purpose}? Responda somente o nome do método.'
            elif number in (63, 66):
                arrays = [[high, low, limit], [low, high, limit], [limit, high, high + 1], [], [high, high], [limit - 1, limit, limit + 1]]
                values = arrays[index]
                method = 'map' if number == 63 else 'filter'
                case_context = f'const {amounts}: number[] = {json.dumps(values)};\n{amounts}.{method}((x) => x > {limit});'
                observed = [x > limit for x in values] if number == 63 else [x for x in values if x > limit]
                case_answer = json.dumps(observed)
            elif number == 70 and index in (2, 5):
                if index == 2:
                    case_context = 'const ids = ["r21", "r22"];\nconst found = ids.find((id): boolean => id === "r22");'
                    case_answer = 'string | undefined'
                else:
                    cls = NAMES[index][4]
                    case_context = f'type {cls} = {{ id: string; {amount}: number }};\nconst requests: {cls}[] = [{{ id: "r51", {amount}: {high} }}];\nconst found = requests.find((item) => item.id === "r51");'
                    case_answer = f'{cls} | undefined'
            elif number == 73:
                values = [[high, low, limit], [low], [limit, high], [low, limit, high, high + 1], [], [low, limit, high, high + 1, low]][index]
                case_context = f'const {amounts}: number[] = {json.dumps(values)};\nfor (const {amount} of {amounts}) {{\n  console.log({amount});\n}}'
                case_answer = str(len(values))
            elif number == 74:
                value_type = ['number', 'string', 'boolean', NAMES[index][4], NAMES[index][5], 'number'][index]
                prefix = ''
                if index == 3:
                    prefix = f'type {value_type} = {{ id: string; {amount}: number }};\n'
                if index == 4:
                    prefix = f'type {value_type} = "required" | "not_required";\n'
                case_context = prefix + f'const {amounts}: {value_type}[] = [];\nfor (const {amount} of {amounts}) {{\n  console.log({amount});\n}}'
                case_answer = '0'

            # A model's prose is not sent to a code or token grader.
            if mode in ('token', 'value'):
                if number == 12:
                    case_answer = ':'
                elif number == 43:
                    case_answer = NAMES[index][8]
                elif number == 70:
                    case_answer = case_answer.rstrip('.')
                elif number in NUMERIC_CASES or number in TOKEN_CASES:
                    case_answer = case_answer.rstrip('.')
            if number in (73, 74):
                case_answer = re.sub(r'\s+vezes\.?$', '', case_answer)

            choices = None
            expected = case_answer
            if mode == 'choice':
                distractors = [rewrite(x, mp) for x in CHOICE_DISTRACTORS[number]]
                distractors = [x for x in distractors if x != case_answer]
                if number == 53:
                    distractors = [x for x in ['O ramo if, que imprime A.', 'O ramo else, que imprime B.', 'Os dois ramos, primeiro A e depois B.', 'Nenhum ramo é executado.'] if x != case_answer]
                values = [case_answer, *distractors[:3]]
                shift = (number + index) % len(values)
                values = values[shift:] + values[:shift]
                choices = [{'id': chr(65 + k), 'text': v} for k, v in enumerate(values)]
                expected = next(c['id'] for c in choices if c['text'] == case_answer)
                case_stem += ' Selecione uma alternativa.'
            case = {'id': f'F{number:03}-V{index}', 'prompt': case_stem, 'context_code': case_context,
                    'answer': expected, 'answer_explanation': case_answer,
                    'parameter_set': index, 'explanation': rewrite(explanations[number], mp),
                    'criterion': rewrite(criterion, mp)}
            if choices:
                case['choices'] = choices
            if mode == 'code':
                case['code_form'] = 'expression' if number in EXPRESSION_CODE else 'statements'
            if number in DIAGNOSTIC_CODES:
                case['context_expected_diagnostic'] = DIAGNOSTIC_CODES[number]
            family['cases'].append(case)

        assert len(family['cases']) == 6
        # C005–C007 têm respostas fixas, mas exemplos literais diferentes.
        if number in (7,):
            for i, case in enumerate(family['cases']):
                case['prompt'] = f'Um campo registra se o pedido reembolso-{i + 1:02} está assinado, usando true ou false. Qual é o nome do tipo geral desses dois valores?'
        if number == 5:
            for i, case in enumerate(family['cases']):
                case['prompt'] = f'Qual é o tipo geral usado para valores numéricos como {NUMBERS[i][0]}?'
        if number == 6:
            for i, case in enumerate(family['cases']):
                case['prompt'] = f'Qual é o tipo geral usado para textos como "reembolso-{i + 1:02}"?'
        # Não contar troca da letra da alternativa ou de ID como variedade do enunciado.
        assert len({(c['prompt'], c['context_code']) for c in family['cases']}) == 6, family['id']
        families.append(family)

        human.extend([f'## C{number:03} / F{number:03} — {skill}\n',
                      f'**Degrau:** D{stage:02}. **Conceito:** `{by_card[number]}`. **Resposta na aplicação:** `{mode}`.\n',
                      f'**Enunciado de origem:** {stem}\n'])
        if context:
            human.append(f'```ts\n{context}\n```\n')
        human.extend([f'**Gabarito de origem:**\n\n```text\n{answer}\n```\n',
                      f'**Critério de aceite:** {criterion}\n',
                      f'**Explicação para o aluno:** {explanations[number]}\n',
                      f'**Contraexemplo:** `{rejected}`\n\n**Por que não atende:** {why}\n',
                      f'**Variações prontas:** F{number:03}-V0 a F{number:03}-V5 em `exercicios.json`. O JSON contém o enunciado completo, o contexto, as alternativas quando aplicáveis e a resposta de cada instância.\n'])

    source_hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT / 'fontes').iterdir() if p.is_file()}
    curriculum = {'version': 'typescript-escada-v1', 'base_repository_commit': '83a1aff2c794fb74dc83857eb3b6c444a3335c81',
                  'origin': 'Ordem e cartões do material anterior; explicações, rubricas, variantes e dependências são expansão editorial própria.',
                  'existing_concepts_to_preserve': ['ts.value.numeric_literal', 'ts.type.number', 'ts.binding.const_number'],
                  'source_sha256': source_hashes, 'stages': stages, 'concepts': concepts,
                  'counts': {'stages': len(stages), 'concepts': len(concepts), 'families': len(families), 'cases': sum(len(f['cases']) for f in families)}}
    (ROOT / 'curriculo.json').write_text(json.dumps(curriculum, ensure_ascii=False, indent=2) + '\n')
    (ROOT / 'exercicios.json').write_text(json.dumps({'version': curriculum['version'], 'families': families}, ensure_ascii=False, indent=2) + '\n')
    (ROOT / 'EXERCICIOS.md').write_text('\n'.join(human))
    print(json.dumps({'generated': curriculum['counts'], 'skills': dict(Counter(f['skill'] for f in families))}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
