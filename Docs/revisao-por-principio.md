# Revisão de TypeScript pelo mesmo princípio em outro contexto

## 1. Mapa Macro das decisões

**Análise encerrada.** O objetivo era poder rever o mesmo princípio em perguntas diferentes. O piloto já escolhe exercícios de um banco com seis casos por família, incluindo a pergunta-base. A decisão é usar o comportamento existente. O mapa, o grafo e a DSM preservam as alternativas examinadas. A eficácia dessas variações contra a memorização do enunciado permanece uma questão empírica (E5). [Banco de exercícios](../conteudo/typescript-v1/exercicios.json)

| ID | Objeto focal | Pergunta sobre o produto | Estado |
| --- | --- | --- | --- |
| P | Finalidade | O que o aluno deve poder reencontrar na revisão? | **Decidida.** Poder rever o mesmo princípio em enunciados diferentes. A pergunta original também participa do banco. |
| Q1 | Equivalência | O que dois exercícios devem preservar? | **Decidida.** A estrutura de solução e, ao revisar um erro específico, a condição que torna esse erro visível. |
| Q8 | Reencontro com o original | Em qual revisão do mesmo conceito a pergunta errada deve reaparecer? | **Decidida.** Manter a seleção atual, em que a original pode voltar. |
| Q6 | Alvo de uma variação | O que deve orientar a geração quando a resposta admite mais de uma explicação? | Aberta, arquivada com a hipótese de geração adicional |
| Q3 | Novidade | Que mudança de contexto é suficiente para evitar a memorização do enunciado? | Aberta, arquivada com a hipótese de geração adicional |
| Q7 | Aceite do exercício | Que evidências permitem aceitar uma variação como equivalente, nova e corrigível? | Aberta, arquivada com a hipótese de geração adicional |

**Decisão de fronteira.** Q2 (prática da aula e retomada imediata), Q4 (crédito do acerto para o progresso) e Q5 (data e ordem dos conceitos devidos) ficam sob as políticas existentes do Mathua e do piloto. Q8 trata de qual enunciado o aluno encontra quando o motor já escolheu o conceito. Os identificadores preservam o histórico. A decisão de produto aqui é conservar esse comportamento. Os detalhes de funcionamento abaixo vêm do código inspecionado.

### Como o piloto responde ao erro hoje

| Situação | Comportamento verificado |
| --- | --- |
| Erro avaliado durante a prática da aula | A tela mostra a correção, zera a sequência de acertos **da seção** e busca prosseguir nela. Cada seção de TypeScript corresponde a uma família de exercícios. A tela consome primeiro a fila já carregada e volta a pedir perguntas quando precisa. Ao esgotar as opções disponíveis, há um caminho de encerramento da seção. [Fluxo nativo da aula](https://github.com/chuma-beep/mathua/blob/2bd4a4e0e160653e274521f6de3df2e61e29c7f7/web/next-app/components/LearnStepper.tsx#L497-L554) · [Adaptação das famílias ao Mathua](https://github.com/marcoz93/anki-typescript/blob/26c784b98965bae668e45959e87f4f52c4ae3e97/pilotos/mathua/mathua-typescript-pilot.patch#L26-L46) |
| Dois acertos seguidos ou três erros seguidos na seção | Dois acertos seguidos normalmente fazem a aula avançar de seção. Após três erros seguidos, a tela oferece apoio e consulta aos pré-requisitos disponíveis. Ela reduz a dificuldade solicitada. O gerador TypeScript percorre seis casos editoriais por família usando a seção, a semente e um contador. A dificuldade solicitada não entra nessa seleção. [Regra da aula](https://github.com/chuma-beep/mathua/blob/2bd4a4e0e160653e274521f6de3df2e61e29c7f7/web/next-app/components/LearnStepper.tsx#L500-L552) · [Seleção de casos](https://github.com/marcoz93/anki-typescript/blob/26c784b98965bae668e45959e87f4f52c4ae3e97/pilotos/mathua/mathua-typescript-pilot.patch#L510-L535) |
| Erro numa revisão espaçada | O motor marca o conceito como devido naquele momento. A próxima seleção ainda depende dos conceitos elegíveis e de suas prioridades. A revisão pede uma pergunta por conceito e pode servir outra família. Um erro de prática comum não antecipa por si só essa data. O motor inicializa a agenda quando o conceito atinge domínio pela primeira vez. [Atualização do calendário](https://github.com/chuma-beep/mathua/blob/2bd4a4e0e160653e274521f6de3df2e61e29c7f7/internal/engine/engine.go#L4176-L4251) · [Seleção da revisão](https://github.com/chuma-beep/mathua/blob/2bd4a4e0e160653e274521f6de3df2e61e29c7f7/internal/engine/engine.go#L969-L1005) |
| Falha técnica na correção | Uma tentativa marcada como `ungraded` fica fora da contagem de erros. Esse resultado tampouco fundamenta gerar um exercício dirigido a um erro do aluno. [Contrato de correção](../conteudo/typescript-v1/CONTRATO-DE-CORRECAO.md#explicação-variante-e-falha-técnica) |

**O enunciado original pode voltar hoje?** Sim, por seleção do banco. A tentativa registra o conceito, o texto exibido, a resposta enviada, o gabarito e o resultado. Ao servir uma revisão, o motor escolhe um conceito devido e chama o gerador com uma nova semente. O gerador do piloto considera os casos das famílias desse conceito. A seleção não reserva para uma revisão futura o enunciado que o aluno errou. Garantir esse retorno exigiria uma regra de escolha do exercício dentro da revisão. O registro da tentativa já oferece uma referência ao original. [Registro da tentativa](https://github.com/chuma-beep/mathua/blob/2bd4a4e0e160653e274521f6de3df2e61e29c7f7/internal/engine/engine.go#L1623-L1636) · [Seleção por conceito](https://github.com/chuma-beep/mathua/blob/2bd4a4e0e160653e274521f6de3df2e61e29c7f7/internal/engine/engine.go#L969-L1005) · [Escolha do caso no piloto](https://github.com/marcoz93/anki-typescript/blob/26c784b98965bae668e45959e87f4f52c4ae3e97/pilotos/mathua/mathua-typescript-pilot.patch#L510-L535)

O ensaio de navegador F042-V0 incorreta → F042-V1 correta documenta a prática da aula. A evidência sobre a revisão espaçada acima vem da leitura do caminho de revisão no código. [Ensaio de integração](../pilotos/mathua/BLOCO-4-D09-D15.md)

## 2. Decisão de manter a seleção atual · Q8

**Quando o conceito voltar após um erro, o aluno precisa reencontrar a pergunta original já na primeira revisão desse conceito?** A questão é Macro e trata do enunciado apresentado em uma revisão futura. P fornece a finalidade e Q5 delimita a ocasião. O motor continua a determinar as datas e a ordem dos conceitos. Para comparar as opções, considere um único erro e um aluno que continua revisando.

| Alternativa | Critério e consequência | Questão suscitada |
| --- | --- | --- |
| **A · Original na primeira revisão do conceito.** O aluno reencontra a situação exata que errou. As variantes entram em revisões posteriores. | O retorno é previsível. Refazer o mesmo enunciado permite observar a correção da tentativa original. A aplicação em outro contexto será observada mais tarde. | Como reconhecer, no aceite, que o aluno viu o mesmo exercício que havia errado? |
| **B · Original em uma revisão posterior do conceito.** Uma variante pode aparecer primeiro e a original ainda deve reaparecer. | Permite testar a lógica em outro contexto mais cedo. O compromisso de reencontro continua pendente até a exibição da original. | Como verificar que a original voltou ao longo das revisões? |

**Resultado.** A seleção atual permite o retorno da original. As alternativas A e B foram examinadas porque acrescentariam uma garantia de ordem. Para o objetivo de ter variedade nas revisões, a seleção do banco foi considerada suficiente.

### Decisão registrada · Q1

**Que estrutura lógica os dois exercícios precisam compartilhar?** O termo usado na literatura de aprendizagem é **problemas isomorfos**. Os cenários podem ter objetos, nomes e valores diferentes. Quando abstraímos esses detalhes, as relações relevantes para resolver a tarefa se correspondem. Chamamos de **invariante** aquilo que essa mudança preserva. Ao aplicar o que aprendeu à nova situação, o aluno demonstra o tipo de desempenho estudado como **transferência**. [Uso de “problemas isomorfos” em português](https://revistas.cesmac.edu.br/psicologia/article/view/1187) · [Lin e Singh, estudo sobre problemas isomorfos](https://arxiv.org/abs/1602.05689)

A questão é de nível **Macro** e seu objeto focal é o par formado pela tarefa original e pela revisão. A decisão corresponde à alternativa **Q1.C**, com um critério para a revisão de um erro específico. Ao aplicar a regra correta e a regra equivocada ao novo caso, as duas devem produzir respostas distinguíveis. Para a comparação estrita, o peso da mala e o volume no tanque ocupam o papel de valor observado. A franquia e a capacidade ocupam o papel de limite.

**Par que atende ao critério.** Uma mala de exatamente 12 kg, com franquia de 12 kg, paga excesso? Um tanque com exatamente 50 litros, cuja capacidade é de 50 litros, transborda? Em ambos os casos, `valor > limite` dá falso e `valor >= limite` dá verdadeiro. O novo contexto permite observar a mesma distinção. Com **51 litros**, ambas as expressões dão verdadeiro. Essa situação serve para praticar a comparação geral, mas o acerto ali é inconclusivo sobre o erro na igualdade.

| Alternativa para Q1 | Critério favorecido e custo | Consequência e questão que fica para depois |
| --- | --- | --- |
| **A · Conservar a tarefa e a resposta correta.** Só conta como revisão equivalente uma situação que peça a mesma ação e preserve a resposta esperada em significado. Formulações de código equivalentes continuam possíveis. | Facilita reencontrar uma resposta específica. Uma resposta constante também pode virar uma pista. | O tanque com 51 litros ficaria fora desse par. Um tanque com 49 e um com exatamente 50 produziriam a mesma resposta “não”, mas só o de 50 verificaria a igualdade. Em Q3 caberia decidir que mudança de contexto preserva essa distinção. |
| **B · Conservar a tarefa e a regra de solução.** O resultado concreto pode variar quando o aluno aplica a mesma operação a outros dados. | Permite observar se o aluno recalcula a resposta e reduz a utilidade de decorar um resultado. Um exemplo escolhido longe do limite pode deixar um erro específico invisível. | Se o alvo é aplicar a comparação estrita em geral, o tanque com 51 litros pode servir. Isoladamente, esse caso deixa a dificuldade na igualdade sem verificação. |
| **C · Fixar o invariante conforme o objetivo de aprendizagem (decidida).** Em alguns objetivos o caso de fronteira integra o alvo. Em outros, o aluno pode obter resultados diferentes aplicando a mesma regra. | Distingue uma dificuldade pontual do uso geral do conceito. Exige um objetivo preciso o bastante para dois avaliadores concordarem sobre o mesmo par. | O tanque com 51 litros é admissível para o objetivo geral e insuficiente para verificar o erro na igualdade. Essa escolha abriu Q6. |

**Restrições comuns.** A variação conserva o princípio e permite que alguém que o compreenda deduza a resposta a partir da nova situação. Alternar entre escrever código e interpretar código muda a ação exigida do aluno. Esse é outro contraste a controlar ao julgar um par. No exemplo, valeu a mesma ação nas duas perguntas.

**Evidência para ponderar a escolha.** No currículo atual, F016 pede ao aluno que **construa** uma comparação estrita. F017 pede que ele **calcule** seu resultado. As duas famílias pertencem ao mesmo conceito. Em F017 há gabaritos `true` e `false`. Em F016, duas expressões diferentes, como `peso > 12` e `12 < peso`, podem satisfazer a mesma exigência. Esses fatos mostram por que “mesma resposta” admite mais de uma leitura. A regra editorial atual é um precedente para a decisão de produto. [Famílias F016 e F017](../conteudo/typescript-v1/EXERCICIOS.md#c016--f016--construtivo) · [Contrato dos exercícios](../conteudo/typescript-v1/CONTRATO-DE-CORRECAO.md)

## 3. Parte–todo e níveis de descrição

### Partes do aplicativo no recorte

Na árvore, cada recuo significa `decomposes_into`, lido do todo para uma de suas partes. A decomposição termina onde já é possível localizar as decisões desta rodada.

- **Aplicativo de estudo de TypeScript**
  - **Material de estudo** — contém objetivos e exercícios, entre eles as situações comparadas em Q1 e Q3.
  - **Percurso do aluno**
    - **Sessão de aprendizagem** — inclui o episódio de resposta, correção e retomada de Q2.
    - **Sessão de revisão** — inclui o reencontro posterior de Q5.
  - **Acompanhamento do aprendizado** — reúne o histórico de desempenho e a agenda de revisão. A política de crédito pertence ao Mathua (Q4).

Q7 avalia o exercício produzido. A geração por agente pertence à autoria do material. O momento em que uma variante fica pronta é distinto da escolha da próxima pergunta pelo motor.

### Abstração, mantendo o objeto focal

| Objeto | Macro · finalidade ou compromisso observável | Meso · explicação lógica disponível hoje | Micro · realização encontrada |
| --- | --- | --- | --- |
| Aplicativo no recorte | Reencontrar o princípio e verificar se ele pode ser aplicado em outro contexto (P). | O motor seleciona um conceito devido. O piloto fornece uma instância. | `NextReviewQuestion` e `exercise.Generate` (E3). |
| Material de estudo | Dizer o que dois exercícios permitem demonstrar (Q1). | Um conceito pode reunir tarefas diferentes. Uma família reúne instâncias com um critério de correção. | O currículo liga `ts.expression.greater_than` a F016 e F017. O banco guarda os seis casos de cada uma (E1 e E2). |
| Retomada de uma tentativa | Prosseguir após um erro segundo a regra de prática existente (Q2). | A prática distingue tentativa incorreta de falha de avaliação e pode voltar à mesma família. | O contrato prevê `ungraded`. Há registro de navegador da sequência F042-V0 incorreta → F042-V1 correta (E4). |
| Revisão posterior | Rever conceitos conforme a agenda e o progresso existentes (Q4 e Q5). | O motor busca um conceito devido. Um conceito com várias famílias admite tarefas distintas. | A revisão chama o gerador sem indicar a seção. Nessa condição, o gerador percorre os casos de todas as famílias daquele conceito (E3). |

As colunas Meso e Micro descrevem o piloto observado. Por exemplo, o tamanho atual do banco explica por que pode haver repetição. Fazer desse tamanho uma restrição do produto exigiria uma justificativa independente.

## 4. Grafo das decisões

A tabela é a lista de arestas que fundamenta a DSM. Em cada linha, a **decisão dependente** `requires_decision_of` a **antecedente**. Para ler a ordem de resolução, percorra a aresta da antecedente para a dependente. A justificativa especifica o dado que a primeira produz e o uso que a segunda faz dele.

| Dependente | Antecedente | Vigência | Informação necessária e razão |
| --- | --- | --- | --- |
| Q1 | P | Sempre | A finalidade de testar o mesmo aprendizado determina para que se precisa comparar duas tarefas. |
| Q8 | P | Sempre | A finalidade inclui retomar o exercício e testar a mesma lógica em outro contexto. É preciso determinar quando a retomada exige o original. |
| Q6 | Q1 | Ativa por Q1.C | O critério confirmado identifica a dificuldade que uma variação dirigida precisa preservar. Falta delimitar o alvo quando só há evidência de resposta incorreta. |
| Q3 | Q1 | Sempre | Para julgar novidade, é preciso separar as relações que devem permanecer das mudanças admissíveis de cenário. |
| Q3 | Q6 | Para tentativas ambíguas | O alvo escolhido define se o novo cenário pode alterar as relações concretas presentes na tentativa original. |
| Q7 | Q1 | Sempre | O aceite requer um critério para testar equivalência e, quando aplicável, distinguir a regra correta do erro específico. |
| Q7 | Q3 | Sempre | Para aceitar uma variante como nova, é preciso saber que diferenças de contexto são suficientes. |

**Outras relações tipadas.** Estas relações ligam objetos, alternativas, compromissos ou realizações. Só a necessidade de informação entre decisões gera uma célula de precedência na DSM.

| Relação | Instância e justificativa |
| --- | --- |
| `decomposes_into` | Percurso do aluno → sessão de aprendizagem e sessão de revisão. São partes em que o estudante vive momentos distintos do percurso. |
| `triggers` | Q1.C → Q6. O resultado C ativa uma pergunta que as políticas universais A e B dispensam. |
| `constrains` | P → alternativas de Q3. Uma simples troca de identificador ainda pode deixar o enunciado reconhecível de memória. A finalidade exige considerar essa possibilidade ao definir novidade. |
| `incompatible_with` | Q1.A ↔ Q1.B, quando propostas como regra universal para a mesma população de tarefas. Para um par com a mesma operação e resultados diferentes, A exige rejeição por esse motivo e B permite aceitação. C muda o alcance da regra ao especificar o objetivo. |
| `realizes` | O ramo de `exercise.Generate` que recebe a seção → seleção de uma instância da família indicada. Esse mecanismo lógico realiza a capacidade de reencontrar a tarefa com outro exemplo. O episódio F042 evidencia o uso dessa capacidade na retomada imediata. A reaplicação independente dias depois continua sem demonstração empírica (E3 e E4). |

## 5. DSM e ordem de resolução

A DSM cobre o conteúdo da revisão. As políticas herdadas Q2, Q4 e Q5 delimitam a análise e não têm escolhas de produto pendentes. A linha recebe informação da coluna. `●` marca uma dependência direta, `C` a condição já ativada por Q1.C e `?` a dependência específica de uma tentativa ambígua.

| Recebe de → | P | Q1 | Q8 | Q6 | Q3 | Q7 |
| --- | --- | --- | --- | --- | --- | --- |
| P  | — | · | · | · | · | · |
| Q1 | ● | — | · | · | · | · |
| Q8 | ● | · | — | · | · | · |
| Q6 | · | C | · | — | · | · |
| Q3 | · | ● | · | ? | — | · |
| Q7 | · | ● | · | · | ● | — |

A fronteira de decisões ativas está vazia. P, Q1 e Q8 estão decididas. As relações entre Q6, Q3 e Q7 descrevem a hipótese arquivada de gerar conteúdo adicional. O grafo desse recorte é acíclico.

## 6. Estado empírico e rastreabilidade

Inspeção do repositório em `26c784b98965`, com o patch distribuído para o Mathua em `2bd4a4e0e160`. Os registros de execução citados pertencem ao projeto. Esta análise consultou conteúdo, código e evidências existentes.

| ID | O que se pode sustentar hoje | Alcance para a decisão |
| --- | --- | --- |
| E1 | O pacote contém 46 conceitos, 74 famílias e 444 casos em 15 degraus. A autoria dos seis casos por família antecede a sessão de estudo. [Pacote editorial](../conteudo/typescript-v1/LEIA-ME.md) | Há exemplos concretos para Q1, Q3 e Q5. A quantidade por família é uma propriedade da entrega atual. |
| E2 | F016 conserva a formulação “estritamente maior” nos seis casos. F017 inclui igualdade, valores acima e abaixo do limite. As duas famílias pedem ações diferentes. [Instâncias](../conteudo/typescript-v1/exercicios.json) · [Critérios das famílias](../conteudo/typescript-v1/CONTRATO-DE-CORRECAO.md) | Q1 e Q6 têm casos que distinguem tarefa, princípio e resultado. Para Q3, o banco também exemplifica uma pista verbal que sobrevive à troca de valores. |
| E3 | A revisão escolhe um conceito devido e passa seu identificador ao gerador. Na revisão geral, pode sair outra família do mesmo conceito. O gerador do piloto seleciona casos do banco finito. [Motor na revisão-base](https://github.com/chuma-beep/mathua/blob/2bd4a4e0e160653e274521f6de3df2e61e29c7f7/internal/engine/engine.go#L969-L1005) · [Gerador no patch distribuído](https://github.com/marcoz93/anki-typescript/blob/26c784b98965bae668e45959e87f4f52c4ae3e97/pilotos/mathua/mathua-typescript-pilot.patch#L510-L539) | Retomar um conceito já é possível. Q1 define a equivalência exigida quando o objetivo é revisar o erro específico. O mecanismo atual, por si só, não garante essa equivalência. |
| E4 | O navegador registrou um erro seguido de outra instância da mesma família e de um acerto. A correção distingue resposta errada de falha técnica. [Ensaio de integração](../pilotos/mathua/BLOCO-4-D09-D15.md) · [Contrato de correção](../conteudo/typescript-v1/CONTRATO-DE-CORRECAO.md#explicação-variante-e-falha-técnica) | Há evidência do comportamento imediato relevante para Q2. O estudante desse ensaio era simulado. |
| E5 | O projeto registra como não verificada a calibração pedagógica com alunos reais. [Limites da entrega](../README.md#como-retomar) | **Insuficientemente conhecido** se as variantes atuais permitem distinguir, dias depois, lembrança do enunciado e aplicação independente. Essa lacuna limita as conclusões sobre eficácia. Q7 tem como objeto a qualidade do exercício produzido. |

Dois precedentes do Anki esclarecem a fronteira. Randomized Basic conserva um cartão e permite apresentar vários enunciados preparados. AnkiTutor mantém o conceito e dá ao tutor a tarefa de formular um cenário novo. Ambos tornam a distinção entre objeto revisto e pergunta apresentada plausível. A equivalência pedagógica dos exercícios de TypeScript continua sendo uma questão do piloto. [Randomized Basic](https://github.com/Vilhelm-Ian/Interactive_And_Randomize_Anki_Note_Types#randomized-basic--randomized-cloze) · [Contrato de aprendizagem do AnkiTutor](https://github.com/MarionLiew/anki-tutor/blob/a3a1d1200b415136cfbad20c0f9719c14bef96f0/docs/learning-contract.md)

## 7. Encerramento da análise

O banco atende ao requisito de variedade. Nenhuma alteração de produto foi requerida. Os critérios registrados podem servir para examinar um caso concreto se surgir evidência de que determinado conjunto de perguntas permite responder de memória.

Ao abrir uma questão, registram-se seu objeto, nível, pergunta, opções admissíveis, restrições, critérios e estado. Para cada opção, acrescentam-se as consequências, as questões suscitadas e a evidência disponível. Para cada antecedente, registra-se a informação recebida. As demais questões seguem identificadas no mapa. Uma deliberação Meso só ganha conteúdo quando houver um compromisso Macro a explicar. Uma deliberação Micro requer um contrato lógico a realizar ou uma restrição concreta demonstrada. Isso vale também para a redação do prompt e a atribuição de responsabilidades a um agente.

**Referenciais aplicados**

- Rasmussen distingue a escala parte–todo da escala meios–fins. Aqui Macro, Meso e Micro são os três níveis pedidos para este projeto. O mesmo objeto pode ser descrito nos três. [Rasmussen, *Information Processing and Human-Machine Interaction*, cap. 4](https://iihm.imag.fr/blanch/ens/2006-2007/RICM3/IHM/documents/rasmussen-book.pdf)
- Zimmermann et al. distinguem questão, alternativa e resultado e modelam as relações entre eles. Aqui isso permite que uma escolha ative outra pergunta sem confundir o ramo com uma decisão tomada. [Zimmermann et al., 2009](https://doi.org/10.1016/j.jss.2009.01.039)
- MacLean et al. relacionam perguntas, opções e critérios. A ficha de Q1 mostra qual critério favorece cada opção e qual limitação ela introduz no mesmo exemplo. [MacLean et al., *Questions, Options, and Criteria*, 1991](https://doi.org/10.1080/07370024.1991.9667168)
- A DSM de Steward permite ordenar decisões pela informação que trocam e identificar dependências circulares. A DSM acima projeta as arestas da seção 4, preservando as condições de ativação. [Steward, 1981](https://doi.org/10.1109/TEM.1981.6448589)
