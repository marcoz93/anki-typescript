# Revisão de TypeScript pelo mesmo princípio em outro contexto

## 1. Mapa Macro das decisões

O objeto de estudo é o reencontro do aluno com algo que aprendeu ou errou no piloto de TypeScript. Há dois momentos distintos. Logo após um erro, refazer a mesma pergunta pode ser útil. Dias depois, interessa saber se o aluno consegue aplicar o princípio quando a situação já não lhe permite reconhecer o exercício de memória.

| ID | Objeto focal | Pergunta sobre o produto | Estado |
| --- | --- | --- | --- |
| P | Finalidade da revisão | O que se quer descobrir ao voltar a um conteúdo? | **Decidida neste recorte.** Queremos observar a aplicação do mesmo princípio em outro contexto ao longo do tempo. A repetição imediata após erro é admissível. |
| Q1 | Equivalência de duas tarefas | Que relações da tarefa original precisam reaparecer na revisão? | **Decidida.** Preservar a estrutura de solução. Ao revisar um erro específico, preservar também a condição que permite distingui-lo da solução correta. |
| Q2 | Retomada logo após um erro | Que oportunidade de refazer a tentativa o aplicativo deve garantir ao aluno naquele momento? | **Aberta. Em deliberação.** |
| Q3 | Novidade do contexto | Que diferença o aluno precisa encontrar para que a revisão exija uma nova aplicação do princípio? | Aberta |
| Q4 | Significado de um acerto | O que um acerto permite afirmar depois de uma correção imediata e o que permite afirmar numa revisão em outro contexto? | Aberta |
| Q5 | Compromisso na revisão posterior | O que o aluno pode esperar na data de revisão, inclusive se não houver um contexto suficientemente diferente e adequado? | Aberta |
| Q6 | Regra de equivalência por objetivo | Como delimitar o que precisa ficar fixo em cada objetivo? | Aberta. A decisão Q1 ativou esta questão. |
| Q7 | Aceite do comportamento do aplicativo | Que observações justificam aceitar que o aplicativo cumpriu a promessa de revisão e que limites têm essas observações? | Aberta |

A fronteira inclui o conteúdo de TypeScript, a tentativa após erro, a revisão posterior e a interpretação do desempenho. O agendamento existente e as referências do ecossistema Anki são dados de partida. A autoria por agente é uma possibilidade solicitada para investigação. O momento em que o aluno vê uma pergunta e o momento em que alguém a escreve podem ser diferentes.

## 2. Única decisão em deliberação · Q2

**Depois de receber a correção, o que acontece na próxima tentativa da mesma sessão?** O objeto focal é a retomada imediata de uma resposta avaliada como incorreta. A decisão é Macro. P já admite repetir a pergunta. Resta definir que oportunidade o aluno tem ao continuar, quando tanto o exercício original quanto uma variante adequada estão disponíveis.

| Alternativa | O que se privilegia | Consequência e questão suscitada |
| --- | --- | --- |
| **A · Refazer a mesma pergunta primeiro.** | O aluno pode localizar e corrigir exatamente o passo em que errou. | O enunciado e a correção estão frescos na memória. Em Q4, quanto esse acerto permite concluir? |
| **B · Receber a variante primeiro.** | O aluno pode usar a explicação imediatamente em outro contexto que ainda exponha o mesmo erro. | É preciso interpretar um novo enunciado. Em Q4, o que o acerto demonstra enquanto a explicação anterior ainda está disponível? |
| **C · O aluno escolhe entre as duas.** | Quem quer corrigir o próprio raciocínio pode refazer a original. Quem quer pô-lo à prova pode tentar a variante. | A escolha acrescenta um passo e produz experiências diferentes. Em Q4, como interpretar o acerto sabendo qual percurso o aluno escolheu? |

**Evidência.** O ensaio com F042 registrou a sequência “erro → variante → acerto”. A política editorial também prevê uma variante após erro. Isso demonstra que o caminho B já ocorre no piloto. A escolha acima trata do compromisso a assumir com o aluno. A falha técnica de correção fica fora deste caso. [Ensaio de integração](../pilotos/mathua/BLOCO-4-D09-D15.md) · [Uso após um erro](../conteudo/typescript-v1/LEIA-ME.md#uso-após-um-erro-e-uso-dos-relatos)

### Decisão registrada · Q1

**Que estrutura lógica os dois exercícios precisam compartilhar?** O termo usado na literatura de aprendizagem é **problemas isomorfos**. Os cenários podem ter objetos, nomes e valores diferentes. Quando abstraímos esses detalhes, as relações relevantes para resolver a tarefa se correspondem. Chamamos de **invariante** aquilo que essa mudança preserva. Ao aplicar o que aprendeu à nova situação, o aluno demonstra o tipo de desempenho estudado como **transferência**. [Uso de “problemas isomorfos” em português](https://revistas.cesmac.edu.br/psicologia/article/view/1187) · [Lin e Singh, estudo sobre problemas isomorfos](https://arxiv.org/abs/1602.05689)

A questão é de nível **Macro** e seu objeto focal é o par formado pela tarefa original e pela revisão. A decisão corresponde à alternativa **Q1.C**, com um critério para a revisão de um erro específico. Ao aplicar a regra correta e a regra equivocada ao novo caso, as duas devem produzir respostas distinguíveis. Para a comparação estrita, o peso da mala e o volume no tanque ocupam o papel de valor observado. A franquia e a capacidade ocupam o papel de limite.

**Par que atende ao critério.** Uma mala de exatamente 12 kg, com franquia de 12 kg, paga excesso? Um tanque com exatamente 50 litros, cuja capacidade é de 50 litros, transborda? Em ambos os casos, `valor > limite` dá falso e `valor >= limite` dá verdadeiro. O novo contexto permite observar a mesma distinção. Com **51 litros**, ambas as expressões dão verdadeiro. Essa situação serve para praticar a comparação geral, mas o acerto ali é inconclusivo sobre o erro na igualdade.

| Alternativa para Q1 | Critério favorecido e custo | Consequência e questão que fica para depois |
| --- | --- | --- |
| **A · Conservar a tarefa e a resposta correta.** Só conta como revisão equivalente uma situação que peça a mesma ação e preserve a resposta esperada em significado. Formulações de código equivalentes continuam possíveis. | Facilita reencontrar uma resposta específica. Uma resposta constante também pode virar uma pista. | O tanque com 51 litros ficaria fora desse par. Um tanque com 49 e um com exatamente 50 produziriam a mesma resposta “não”, mas só o de 50 verificaria a igualdade. Em Q3 caberia decidir que mudança de contexto preserva essa distinção. |
| **B · Conservar a tarefa e a regra de solução.** O resultado concreto pode variar quando o aluno aplica a mesma operação a outros dados. | Permite observar se o aluno recalcula a resposta e reduz a utilidade de decorar um resultado. Um exemplo escolhido longe do limite pode deixar um erro específico invisível. | Se o alvo é aplicar a comparação estrita em geral, o tanque com 51 litros pode servir. Em Q4 caberia definir o que esse acerto permite afirmar sobre a dificuldade na igualdade. |
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
  - **Acompanhamento do aprendizado** — reúne o histórico de desempenho e a agenda de revisão. Q4 trata do significado que se pode atribuir a esse desempenho.

Q7 avalia o comportamento do conjunto. A autoria de exercícios, humana ou assistida, pode ocorrer fora da sessão. Sua posição dentro ou fora da fronteira operacional continua em aberto.

### Abstração, mantendo o objeto focal

| Objeto | Macro · finalidade ou compromisso observável | Meso · explicação lógica disponível hoje | Micro · realização encontrada |
| --- | --- | --- | --- |
| Aplicativo no recorte | Reencontrar o princípio e verificar se ele pode ser aplicado em outro contexto (P). | O motor seleciona um conceito devido. O piloto fornece uma instância. | `NextReviewQuestion` e `exercise.Generate` (E3). |
| Material de estudo | Dizer o que dois exercícios permitem demonstrar (Q1). | Um conceito pode reunir tarefas diferentes. Uma família reúne instâncias com um critério de correção. | O currículo liga `ts.expression.greater_than` a F016 e F017. O banco guarda os seis casos de cada uma (E1 e E2). |
| Retomada de uma tentativa | Esclarecer o que o aluno pode refazer após um erro (Q2). | A prática distingue tentativa incorreta de falha de avaliação e pode voltar à mesma família. | O contrato prevê `ungraded`. Há registro de navegador da sequência F042-V0 incorreta → F042-V1 correta (E4). |
| Revisão posterior | Definir o que o aluno reencontra e o que seu desempenho demonstra (Q4 e Q5). | O motor busca um conceito devido. Um conceito com várias famílias admite tarefas distintas. | A revisão chama o gerador sem indicar a seção. Nessa condição, o gerador percorre os casos de todas as famílias daquele conceito (E3). |

As colunas Meso e Micro descrevem o piloto observado. Por exemplo, o tamanho atual do banco explica por que pode haver repetição. Fazer desse tamanho uma restrição do produto exigiria uma justificativa independente.

## 4. Grafo das decisões

A tabela é a lista de arestas que fundamenta a DSM. Em cada linha, a **decisão dependente** `requires_decision_of` a **antecedente**. Para ler a ordem de resolução, percorra a aresta da antecedente para a dependente. A justificativa especifica o dado que a primeira produz e o uso que a segunda faz dele.

| Dependente | Antecedente | Vigência | Informação necessária e razão |
| --- | --- | --- | --- |
| Q1 | P | Sempre | A finalidade de testar o mesmo aprendizado determina para que se precisa comparar duas tarefas. |
| Q2 | P | Sempre | A autorização para repetir após erro delimita a retomada imediata. Ainda resta decidir que oportunidade é garantida ao aluno. |
| Q3 | Q1 | Sempre | É preciso conhecer o que deve permanecer fixo para decidir quais mudanças de contexto podem qualificar uma pergunta como nova. |
| Q6 | Q1 | Ativa por Q1.C | A política por objetivo cria a necessidade de especificar que relação cada objetivo preserva. |
| Q3 | Q6 | Ativa por Q1.C | Para aplicar o critério de novidade a um objetivo específico, é preciso saber quais mudanças preservam a tarefa naquele objetivo. |
| Q4 | Q1 | Sempre | A unidade de equivalência determina a que aprendizado o acerto pode ser atribuído. |
| Q4 | Q2 | Sempre | A oportunidade de retomar define em que condições ocorreu o acerto imediato, inclusive se a mesma pergunta pôde ser refeita. Esse contexto limita sua interpretação. |
| Q4 | Q3 | Sempre | Para atribuir um acerto à aplicação em um cenário novo, é preciso saber qual diferença de contexto satisfaz essa qualificação. |
| Q5 | Q3 | Sempre | Para prometer uma experiência quando faltam casos adequados, é preciso definir em quais circunstâncias um caso conta como novo. |
| Q7 | Q4 | Sempre | O significado permitido de um acerto define que evidência de desempenho seria pertinente no aceite. |
| Q7 | Q5 | Sempre | O compromisso com o aluno define que comportamento observar na revisão, inclusive quando a novidade prometida está indisponível. |

**Outras relações tipadas.** Estas relações ligam objetos, alternativas, compromissos ou realizações. Só a necessidade de informação entre decisões gera uma célula de precedência na DSM.

| Relação | Instância e justificativa |
| --- | --- |
| `decomposes_into` | Percurso do aluno → sessão de aprendizagem e sessão de revisão. São partes em que o estudante vive momentos distintos do percurso. |
| `triggers` | Q1.C → Q6. O resultado C ativa uma pergunta que as políticas universais A e B dispensam. |
| `constrains` | P → alternativas de Q3. Uma simples troca de identificador ainda pode deixar o enunciado reconhecível de memória. A finalidade exige considerar essa possibilidade ao definir novidade. |
| `incompatible_with` | Q1.A ↔ Q1.B, quando propostas como regra universal para a mesma população de tarefas. Para um par com a mesma operação e resultados diferentes, A exige rejeição por esse motivo e B permite aceitação. C muda o alcance da regra ao especificar o objetivo. |
| `realizes` | O ramo de `exercise.Generate` que recebe a seção → seleção de uma instância da família indicada. Esse mecanismo lógico realiza a capacidade de reencontrar a tarefa com outro exemplo. O episódio F042 evidencia o uso dessa capacidade na retomada imediata. A reaplicação independente dias depois continua sem demonstração empírica (E3 e E4). |

## 5. DSM e ordem de resolução

Leia **a linha como consumidora e a coluna como fornecedora** da informação. `●` indica dependência direta incondicional. `C` indica dependência direta agora ativa pela escolha Q1.C. `·` indica ausência de aresta direta e `—` a diagonal. P e Q1 já fornecem suas decisões. A matriz preserva essas colunas para permitir o rastreamento.

| Recebe de → | P | Q1 | Q2 | Q6 | Q3 | Q4 | Q5 | Q7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P  | — | · | · | · | · | · | · | · |
| Q1 | ● | — | · | · | · | · | · | · |
| Q2 | ● | · | — | · | · | · | · | · |
| Q6 | · | C | · | — | · | · | · | · |
| Q3 | · | ● | · | C | — | · | · | · |
| Q4 | · | ● | ● | · | ● | — | · | · |
| Q5 | · | · | · | · | ● | · | — | · |
| Q7 | · | · | · | · | · | ● | ● | — |

**Fronteira atual.** Com P e Q1 decididas, Q2 e Q6 têm zero antecedentes pendentes. São independentes. Abre-se Q2 para definir primeiro o que o aluno experimenta imediatamente depois de errar. Q6 permanece disponível para uma rodada posterior.

**Camadas topológicas das decisões restantes.** {Q2, Q6} → Q3 → {Q4, Q5} → Q7. As chaves agrupam decisões independentes. Cada questão fica disponível ao satisfazer seus próprios antecedentes. Por exemplo, decidir Q6 libera Q3 mesmo que Q2 ainda esteja em aberto. Todas as precedências ativas ficam abaixo da diagonal da DSM. Não há grupo mutuamente acoplado com mais de uma decisão.

## 6. Estado empírico e rastreabilidade

Inspeção do repositório em `26c784b98965`, com o patch distribuído para o Mathua em `2bd4a4e0e160`. Os registros de execução citados pertencem ao projeto. Esta análise consultou conteúdo, código e evidências existentes.

| ID | O que se pode sustentar hoje | Alcance para a decisão |
| --- | --- | --- |
| E1 | O pacote contém 46 conceitos, 74 famílias e 444 casos em 15 degraus. A autoria dos seis casos por família antecede a sessão de estudo. [Pacote editorial](../conteudo/typescript-v1/LEIA-ME.md) | Há exemplos concretos para Q1, Q3 e Q5. A quantidade por família é uma propriedade da entrega atual. |
| E2 | F016 conserva a formulação “estritamente maior” nos seis casos. F017 inclui igualdade, valores acima e abaixo do limite. As duas famílias pedem ações diferentes. [Instâncias](../conteudo/typescript-v1/exercicios.json) · [Critérios das famílias](../conteudo/typescript-v1/CONTRATO-DE-CORRECAO.md) | Q1 e Q6 têm casos que distinguem tarefa, princípio e resultado. Para Q3, o banco também exemplifica uma pista verbal que sobrevive à troca de valores. |
| E3 | A revisão escolhe um conceito devido e passa seu identificador ao gerador. Na revisão geral, pode sair outra família do mesmo conceito. O gerador do piloto seleciona casos do banco finito. [Motor na revisão-base](https://github.com/chuma-beep/mathua/blob/2bd4a4e0e160653e274521f6de3df2e61e29c7f7/internal/engine/engine.go#L969-L1005) · [Gerador no patch distribuído](https://github.com/marcoz93/anki-typescript/blob/26c784b98965bae668e45959e87f4f52c4ae3e97/pilotos/mathua/mathua-typescript-pilot.patch#L510-L539) | Retomar um conceito já é possível. Q1 define a equivalência exigida quando o objetivo é revisar o erro específico. O mecanismo atual, por si só, não garante essa equivalência. |
| E4 | O navegador registrou um erro seguido de outra instância da mesma família e de um acerto. A correção distingue resposta errada de falha técnica. [Ensaio de integração](../pilotos/mathua/BLOCO-4-D09-D15.md) · [Contrato de correção](../conteudo/typescript-v1/CONTRATO-DE-CORRECAO.md#explicação-variante-e-falha-técnica) | Há evidência do comportamento imediato relevante para Q2. O estudante desse ensaio era simulado. |
| E5 | O projeto registra como não verificada a calibração pedagógica com alunos reais. [Limites da entrega](../README.md#como-retomar) | **Insuficientemente conhecido** se as variantes atuais permitem distinguir, dias depois, lembrança do enunciado e aplicação independente. Essa lacuna informa Q3, Q4 e Q7. |

Dois precedentes do Anki esclarecem a fronteira. Randomized Basic conserva um cartão e permite apresentar vários enunciados preparados. AnkiTutor mantém o conceito e dá ao tutor a tarefa de formular um cenário novo. Ambos tornam a distinção entre objeto revisto e pergunta apresentada plausível. A equivalência pedagógica dos exercícios de TypeScript continua sendo uma questão do piloto. [Randomized Basic](https://github.com/Vilhelm-Ian/Interactive_And_Randomize_Anki_Note_Types#randomized-basic--randomized-cloze) · [Contrato de aprendizagem do AnkiTutor](https://github.com/MarionLiew/anki-tutor/blob/a3a1d1200b415136cfbad20c0f9719c14bef96f0/docs/learning-contract.md)

## 7. Continuidade da análise

Após a resposta a Q2, registre a formulação acordada, sua justificativa e a consequência para a próxima tentativa. Atualize a vigência das arestas, a DSM e a fronteira de decisões prontas. Uma formulação diferente das alternativas apresentadas pode exigir a revisão do mapa.

Ao abrir uma questão, registram-se seu objeto, nível, pergunta, opções admissíveis, restrições, critérios e estado. Para cada opção, acrescentam-se as consequências, as questões suscitadas e a evidência disponível. Para cada antecedente, registra-se a informação recebida. As demais questões seguem identificadas no mapa. Uma deliberação Meso só ganha conteúdo quando houver um compromisso Macro a explicar. Uma deliberação Micro requer um contrato lógico a realizar ou uma restrição concreta demonstrada. Isso vale também para a redação do prompt e a atribuição de responsabilidades a um agente.

**Referenciais aplicados**

- Rasmussen distingue a escala parte–todo da escala meios–fins. Aqui Macro, Meso e Micro são os três níveis pedidos para este projeto. O mesmo objeto pode ser descrito nos três. [Rasmussen, *Information Processing and Human-Machine Interaction*, cap. 4](https://iihm.imag.fr/blanch/ens/2006-2007/RICM3/IHM/documents/rasmussen-book.pdf)
- Zimmermann et al. distinguem questão, alternativa e resultado e modelam as relações entre eles. Aqui isso permite que uma escolha ative outra pergunta sem confundir o ramo com uma decisão tomada. [Zimmermann et al., 2009](https://doi.org/10.1016/j.jss.2009.01.039)
- MacLean et al. relacionam perguntas, opções e critérios. A ficha de Q1 mostra qual critério favorece cada opção e qual limitação ela introduz no mesmo exemplo. [MacLean et al., *Questions, Options, and Criteria*, 1991](https://doi.org/10.1080/07370024.1991.9667168)
- A DSM de Steward permite ordenar decisões pela informação que trocam e identificar dependências circulares. A DSM acima projeta as arestas da seção 4, preservando as condições de ativação. [Steward, 1981](https://doi.org/10.1109/TEM.1981.6448589)
