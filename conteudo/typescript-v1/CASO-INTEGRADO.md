# Caso integrado: classificar pedidos de reembolso

O programa completo está em [fontes/reembolsos.ts](fontes/reembolsos.ts), preservado como foi fornecido. Use-o depois de estudar os quinze degraus. O código reúne construções ensinadas em momentos diferentes; a ordem das declarações no programa não redefine a ordem das aulas. Por exemplo, o alias `ReviewStatus` aparece no início do arquivo para ser usado adiante, mas seu conteúdo pertence ao degrau 11.

## Finalidade, regra e entrada

A finalidade é calcular quais pedidos exigem revisão. A política adotada no exemplo é: **quantia estritamente maior que 10.000 exige revisão**. A política é uma premissa do exercício, não uma exigência da linguagem.

| Pedido | Quantia |
| --- | ---: |
| `reembolso-01` | 15000 |
| `reembolso-02` | 5000 |
| `reembolso-03` | 10000 |

Cada objeto representa um pedido com `id: string` e `amount: number`. Os dados ficam em um array de `Refund`. O programa recebe esses dados já escritos no código: não consulta um banco nem valida documentos.

## Uma execução concreta, por operação

Considere `reembolso-01`, com quantia 15000.

| Operação | Entrada | Produto ou efeito | Contribuição para a finalidade |
| --- | --- | --- | --- |
| `getRefundAmount(item)` | O objeto do pedido | `15000` | Obtém a quantia que será comparada |
| `isAboveLimit(15000, 10000)` | Quantia e limite | `true` | Calcula se a regra de revisão é satisfeita |
| `isReviewRequired(item, 10000)` | Objeto e limite | `true` | Compõe a obtenção da quantia com a comparação |
| `classifyRefund(item, 10000)` | Objeto e limite | `"required"` | Representa a classificação por um dos rótulos admitidos |
| `refunds.filter(needsReview)` | A coleção e a função de condição | Array com o pedido `reembolso-01` | Reúne os pedidos cuja revisão é exigida |
| `for...of` e `console.log(item.id)` | O array selecionado | Apresenta `reembolso-01` no console | Torna visível qual pedido foi selecionado |

`needsReview` é uma função que usa o limite já vinculado a `reviewLimit`. Passá-la a `filter` fornece a operação de condição; não fornece antecipadamente seu resultado para um único pedido.

Para a quantia 10000, `10000 > 10000` é falso. Por isso `reembolso-03` recebe `"not_required"`. Trocar `>` por `>=` mudaria a política implementada, mesmo que os exemplos de 15000 e 5000 continuassem produzindo os mesmos resultados.

## Transformar, selecionar e buscar são tarefas diferentes

`map` aplica a classificação a todos os três pedidos, produzindo:

```ts
["required", "not_required", "not_required"]
```

`filter` conserva o objeto que atende à condição, produzindo:

```ts
[{ id: "reembolso-01", amount: 15000 }]
```

`find` busca `reembolso-02` e devolve seu objeto. `getReviewStatus` verifica que ele existe e devolve `"not_required"`. A busca de `reembolso-99` não encontra objeto e devolve `undefined`; `getReviewStatus` retorna `undefined` antes de tentar classificar.

O retorno `"not_required"` significa que um pedido presente não exige revisão segundo a regra adotada. `undefined` significa ausência de pedido neste percurso. O programa não transforma ausência em uma classificação negativa.

## Efeitos observados no console

Há cinco chamadas efetivas de `console.log`, nesta ordem:

| Chamada | Valor apresentado |
| --- | --- |
| 1 | O array `['required', 'not_required', 'not_required']` |
| 2 | O array com `{ id: 'reembolso-01', amount: 15000 }` |
| 3 | A string `'not_required'` |
| 4 | `undefined` |
| 5 | A string `'reembolso-01'` |

A aparência das aspas e a distribuição em linhas dependem do console. O verificador compara os valores recebidos nas chamadas, em vez de supor um formato de impressão.

## Relação com os quinze degraus

| Degraus | Papel no programa |
| --- | --- |
| 01–03 | Escrever valores, declarar seus tipos e vinculá-los a nomes |
| 04 | Comparar quantia e limite, testar identificadores e ausência |
| 05–06 | Representar objetos, coleção e seus tipos |
| 07–08 | Definir funções, fornecer argumentos e obter resultados |
| 09 | Usar a quantia obtida por uma função como entrada da comparação |
| 10 | Fornecer `needsReview` como valor função ao filtro |
| 11–12 | Restringir os rótulos e escolher o resultado pela condição |
| 13 | Tratar um resultado de busca que pode estar ausente |
| 14 | Transformar a coleção, selecionar elementos e buscar um elemento |
| 15 | Percorrer os selecionados e apresentar seus identificadores |

## Critério de aceite e alcance

O programa deve classificar corretamente quantias abaixo, iguais e acima do limite; preservar os pedidos correspondentes em `filter`; distinguir o resultado encontrado da ausência; e produzir os efeitos acima na ordem esperada. O verificador executa o arquivo original e confronta os resultados com esses critérios. O comando, a saída e o ambiente estão em [COMANDOS-E-SAIDAS.md](COMANDOS-E-SAIDAS.md).

O comportamento demonstrado termina na classificação e na apresentação dos resultados. O programa não aprova o pagamento, não efetua a transferência, não garante a autenticidade de documentos e não comprova que os dados representam pedidos reais. Essas funções não fazem parte da especificação deste exemplo.
