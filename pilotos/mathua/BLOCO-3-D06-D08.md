# Bloco 3 · Tipos de objeto, funções e chamadas

Em 27/11/2026, o piloto passou a servir D01 a D08. São **32 conceitos, 38 famílias e 228 perguntas**. Este bloco acrescentou 9 conceitos e 78 perguntas. Os IDs e pré-requisitos vêm de `conteudo/typescript-v1`.

| Degrau | O que o aluno pratica | Famílias |
| --- | --- | --- |
| D06 | Declarar um alias de objeto, identificar uma propriedade obrigatória ausente e declarar um array tipado vazio | F026–F029 |
| D07 | Definir uma função que lê um objeto, identificar parâmetro e tipo de retorno, explicar e diagnosticar um `return` | F030–F034 |
| D08 | Invocar a função, prever o resultado, identificar o argumento e apresentar o valor no console | F035–F038 |

## Correção e tela

- **Alias de objeto.** O compilador confere o alias, o nome e os tipos das propriedades obrigatórias. As chaves podem vir entre aspas e em qualquer ordem.
- **Array tipado.** O corretor aceita `const refunds: Refund[] = []`, `let refunds: Array<Refund> = []` e `new Array<Refund>()` como inicialização da variável pedida. O compilador verifica a estrutura do tipo dos elementos.
- **Definição de função.** O aluno pode escrever em várias linhas e enviar pelo botão **Verificar**. O corretor aceita parâmetro renomeado, retorno inferido, função vinculada ao nome pedido e acesso com ponto ou colchetes. Também reconhece desestruturação no parâmetro e retorno por uma variável local que guarda a propriedade. Confere a assinatura e a origem do valor devolvido sem executar o código.
- **Chamadas.** F035 pede a função e o argumento numérico da instância. F038 pede uma chamada a `console.log` com a variável do enunciado. Em F038, `console['log'](amount)` também passa. Colocar o número do exemplo diretamente na chamada recebe a orientação de usar a variável.
- As questões de escolha, nome e resultado usam os corretores existentes. O código com erro intencional em F028 e F034 aparece no enunciado para o aluno identificar o diagnóstico.

## Verificação em macOS arm64

| Execução | Resultado observado |
| --- | --- |
| Piloto Go | 516 casos finais aprovados, incluindo 38 novos testes de critério e o caso de indisponibilidade do corretor com nova tentativa |
| Escada pela API real | 32 conceitos chegaram a `MASTERED`, cada um após seis perguntas distintas |
| Modelos do pacote | Os corretores aceitaram os 228 gabaritos na verificação de partida |
| Conferência adicional das seis variantes por família | Uma resposta válida e uma incorreta para cada um dos 78 casos novos, com 156 vereditos esperados |
| Motor e rotas nativas selecionadas | 154 casos de domínio, agendamento e reparo e 26 casos HTTP aprovados |
| Interface | 199 arquivos e 1.897 testes aprovados. TypeScript e build aprovados. ESLint concluiu com 7 avisos e zero erros |
| Chromium 151.0.7922.34 e servidor real | 42 verificações aprovadas, 25 conceitos dominados pela tela, incluindo os 9 novos. As 13 famílias do bloco apareceram. Zero erros de página ou de rotas de aulas observados pelo script |
| Atualização a partir do bloco 2 | O executável anterior gravou uma resposta e serviu outra pergunta. O novo executável recuperou a resposta anterior com o mesmo token e corrigiu a pergunta pendente. O reenvio devolveu a resposta gravada. O SQLite terminou com duas tentativas |

Na tela, a resposta em várias linhas de F030-V2 devolvia um número fixo. A API recebeu as quebras de linha e a tela mostrou “Devolva a propriedade value do objeto recebido.” A próxima pergunta foi F030-V3. A sequência prosseguiu com respostas de retorno inferido. Em D08, o navegador respondeu aos seis casos diferentes de F038. Os testes usaram contas e bancos temporários. [Registro do navegador](evidencias/bloco-3-d06-d08/navegador.json)

O registro Go conserva os eventos de resultado, as contagens do conteúdo e as linhas de domínio. A contagem de casos finais exclui funções-pai quando há subtestes. O registro de atualização traz as verificações de reenvio e o número de tentativas. [Resultados Go](evidencias/bloco-3-d06-d08/go.jsonl) · [Atualização do banco](evidencias/bloco-3-d06-d08/atualizacao.json)

## Reprodução

O ponto de partida foi `anki-typescript@f028170` com Mathua em `2bd4a4e0e160653e274521f6de3df2e61e29c7f7`. O patch completo foi aplicado em outro checkout limpo desse commit. Os 24 arquivos resultantes coincidiram byte a byte com os arquivos do checkout testado. SHA-256 do patch `ad41230c31e3735b07106e6fb0a5cf9509e9f9ddf712b4cc613eed3fcf5927ca`.

Siga a instalação do [piloto](LEIA-ME.md#reprodução) para aplicar o patch, instalar as dependências e compilar o executável e a interface. Os comandos abaixo partem da raiz do clone do Mathua.

```sh
go test -json ./cmd/typescript-pilot -count=1
go test ./internal/mastery ./internal/scheduler ./internal/repair -count=1
go test ./internal/server -run 'Test(Practice_|StudyAnswer_|MyReports|AdminReport|Report)' -count=1
npm test --prefix web/next-app
npm run lint --prefix web/next-app
node ../scripts/browser-smoke.mjs --mathua .
python3 ../scripts/process-smoke.py --mathua .
```

Para reproduzir a atualização, prepare um segundo clone do mesmo commit-base do Mathua, aplique o patch de `anki-typescript@f028170`, instale as dependências do corretor e compile seu `pilot-bin`. Acrescente `--previous-mathua /caminho/do/clone-anterior` ao comando Python. A primeira partida usa esse executável e seu corretor. A segunda usa a versão atual sobre o mesmo banco temporário.

## Limites e próximo degrau

A rodada cobriu macOS e Chromium. Linux, outros navegadores e a suíte Go completa do Mathua ficaram fora da execução. A revisão independente de nove passadas pertence ao bloco 2. A verificação deste bloco foi feita pelo próprio implementador. As [nove questões editoriais do bloco 2](BLOCO-2-D04-D05.md) continuam abertas.

F030 usa um corretor estático para as formas de leitura de propriedade descritas acima. Implementações mais indiretas podem receber uma recusa mesmo quando calculam o mesmo valor. A progressão medida foi a do motor com respostas de teste.

D09 introduz **quatro famílias** em `ts.function.composition`. A rota de prática e o carregador do piloto suportam três seções por conceito. O teste de conteúdo verificou que o carregador recusa D09 inteiro. A integração seguinte precisa tornar a quarta família acessível.
