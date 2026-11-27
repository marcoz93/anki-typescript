# Conteúdo completo da nossa escada de TypeScript

Entrega editorial de 27/11/2026, preparada para integrar ao piloto existente. A ordem original tem **15 degraus e 74 cartões**. Este pacote organiza esses cartões em **46 conceitos, 74 famílias e 444 instâncias completas**: seis casos por família, incluindo o caso adaptado do cartão de origem. Não há geração por IA durante o estudo.

Os 15 degraus estão integrados ao piloto. Este diretório reúne a entrega editorial original. A execução do material no aplicativo está documentada no [registro de integração](../../pilotos/mathua/BLOCO-4-D09-D15.md).

## O que ler

| Arquivo | Produto entregue |
| --- | --- |
| [CURRICULO.md](CURRICULO.md) | As quinze aulas, com significado, código, aplicação, contrastes e critérios de aceite |
| [EXERCICIOS.md](EXERCICIOS.md) | Os 74 cartões de origem legíveis, gabaritos, critérios, explicações e contraexemplos |
| [curriculo.json](curriculo.json) | Aulas completas, conceitos, relações de pré-requisito e ligação com as famílias |
| [exercicios.json](exercicios.json) | As 444 perguntas completas: contexto, resposta, explicação, critério e alternativas quando aplicáveis |
| [CASO-INTEGRADO.md](CASO-INTEGRADO.md) | Leitura do programa de reembolsos, entradas, produtos intermediários e efeitos |
| [CONTRATO-DE-CORRECAO.md](CONTRATO-DE-CORRECAO.md) | Formatos de resposta, equivalências aceitas, falha do corretor e tratamento de relatos |
| [fontes/anki_typescript_v1.tsv](fontes/anki_typescript_v1.tsv) | Arquivo original preservado, com seus 74 cartões e etiquetas |
| [fontes/reembolsos.ts](fontes/reembolsos.ts) | Programa original preservado, executável como caso de consolidação |
| [COMANDOS-E-SAIDAS.md](COMANDOS-E-SAIDAS.md) | Comandos executados, saídas, ambiente e limites da verificação |
| [evidencias/validacao.json](evidencias/validacao.json) | Resultado estruturado da verificação mais recente |

## O que foi preservado e o que foi acrescentado

A ordem dos quinze degraus, as perguntas-base e os tipos de habilidade vieram do arquivo anterior. A distribuição de cartões é: 20 semânticos, 30 construtivos, 8 diagnósticos, 13 interpretativos e 3 seletivos. Cada cartão original tem exatamente uma família correspondente, de C001/F001 a C074/F074.

As explicações ampliadas, a divisão em 46 conceitos com IDs, as dependências, os critérios explícitos, os distratores e as variantes são decisões editoriais desta entrega. A sequência é a nossa organização de ensino para este recorte; não é uma taxonomia universal da linguagem nem conteúdo oficial do Mathua ou do Math Academy.

Nas perguntas discursivas de significado e diagnóstico, a versão para correção automática usa alternativas fechadas. Isso muda a operação de resposta: reconhecer a explicação correta entre alternativas não é o mesmo que formulá-la livremente. O enunciado e o gabarito abertos originais continuam preservados. As 30 famílias de construção continuam pedindo que o aluno escreva código.

Um exemplo com outros números pode continuar tendo a mesma resposta correta. As seis instâncias têm enunciado ou contexto concretamente diferente; não se contabiliza somente mudar um ID ou embaralhar alternativas. Esse controle mede diferença dos casos, sem provar equivalência de dificuldade ou diversidade pedagógica suficiente.

## Como integrar sem refazer o que já existe

O ponto de partida da tela é o commit `83a1aff2c794fb74dc83857eb3b6c444a3335c81`. Use o commit do repositório que contém este diretório, mantendo os ajustes posteriores da tela que já estiverem presentes.

Preserve os IDs e o progresso dos três conceitos já existentes:

| Conceito existente | Conteúdo correspondente neste pacote | Pré-requisitos existentes |
| --- | --- | --- |
| `ts.value.numeric_literal` | D01, F002: escrever o literal numérico | Nenhum |
| `ts.type.number` | D02, F005: identificar o tipo numérico geral | Nenhum |
| `ts.binding.const_number` | D03, F010: construir uma declaração `const` numérica | Os dois anteriores |

Esses três conceitos cobrem partes de D01–D03. Não marque os outros conceitos desses degraus como aprendidos por associação. Primeiro complete as lacunas de D01–D03; depois avance em D04–D15 na ordem já definida. Entregue a implementação em blocos verificáveis, com a menor alteração necessária por bloco. O conteúdo inteiro já está escrito e não precisa ser escolhido novamente.

Os pré-requisitos de `curriculo.json` descrevem conhecimentos utilizados pelos exercícios deste pacote. São decisões para o percurso didático, não afirmações de que um conceito seria logicamente impossível sem outro. Não renumere os degraus nem confunda essa relação com gênero–espécie.

As aulas contêm trechos independentes, apresentados para explicar cada operação. Não concatene todos os blocos de código de uma aula como se fossem um único programa: alguns usam de novo o mesmo identificador. Para cada exercício, o contexto compilável é o campo `context_code` da sua instância. Para o programa completo, use `fontes/reembolsos.ts`.

## Uso após um erro e uso dos relatos

No erro de uma resposta efetivamente avaliada, mostre a explicação da instância e use o mecanismo já existente para apresentar uma variante da mesma família. Mantenha o conceito, a tarefa e o critério. Não apresente como novo um caso idêntico apenas porque seu ID mudou. O banco é finito; quando os seis casos se esgotarem, a revisão deve assumir a repetição ou usar outra família disponível para aquele conceito.

Os 74 cartões não têm todos a mesma função: há distinções de significado, construção, interpretação, diagnóstico e escolha de operação. Dominar uma dessas tarefas não demonstra automaticamente domínio das demais. Use a política de progresso do motor existente sem inventar novos limiares estatísticos para esta entrega.

O relato de pergunta ruim deve continuar distinto de um erro do aluno. Ele pode indicar ambiguidade do enunciado, falha do gabarito, rejeição de uma solução válida ou dificuldade inadequada. O contrato de correção especifica como conservar a evidência necessária para revisão. A geração automática de novas famílias a partir desses relatos permanece uma etapa posterior; este pacote não a implementa nem depende dela.

## Reproduzir a verificação

Na raiz de `anki-typescript`, com Python 3, Node e TypeScript 5.9.3 instalados:

```bash
python3 conteudo/typescript-v1/scripts/gerar-conteudo.py
node conteudo/typescript-v1/scripts/verificar-conteudo.cjs \
  --typescript ./pilotos/mathua/mathua/cmd/typescript-pilot/node_modules/typescript
```

O argumento `--typescript` aponta para a instalação já usada pelo piloto. Se a cópia aplicada do Mathua estiver em outro local, ajuste somente esse caminho. O verificador não instala dependências, não inicia o servidor e não acessa o banco de progresso. As versões efetivamente usadas nesta entrega estão em `COMANDOS-E-SAIDAS.md`.

O gerador expande dados editoriais fixos e emite os dois JSON e `EXERCICIOS.md`. Não chama serviços externos. Edite `CURRICULO.md` para mudar aulas; edite `scripts/gerar-conteudo.py` para mudar exercícios, critérios, variantes ou dependências; gere novamente os arquivos e verifique o resultado. Preserve as fontes originais.

## Critério de aceite da implementação seguinte

O aluno deve conseguir ler a aula do conceito, responder aos seus exercícios, receber correção coerente com o contrato, obter uma variante após erro e registrar ou consultar seu relato. Ao recarregar ou reiniciar, o progresso anterior precisa continuar disponível. Uma falha do corretor não deve contar como erro do aluno.

Comprove o bloco integrado com comandos e saídas reais, incluindo uma solução válida diferente do gabarito quando a rubrica a admite, uma resposta incorreta e uma falha técnica de correção. Verifique também o relato e o progresso existente. Não confunda os testes de conteúdo desta entrega com testes dessa integração, documentada nos relatórios do piloto.
