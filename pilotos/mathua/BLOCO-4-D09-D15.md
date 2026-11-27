# Bloco 4 · Composição, tipos, controle de fluxo e coleções

Os degraus D09 a D15 acrescentam 14 conceitos, 36 famílias e 216 perguntas ao piloto. O aplicativo lê os 15 degraus do pacote `typescript-escada-v1`, com 46 conceitos, 74 famílias e 444 perguntas. O ponto de partida foi o bloco 3 em `76e286d`.

| Degrau | Prática | Perguntas |
| --- | --- | ---: |
| D09 | Compor duas chamadas e acompanhar o resultado intermediário | 24 |
| D10 | Referenciar funções, escrever uma arrow function e passar uma callback | 30 |
| D11 | Declarar uniões de tipos literais | 24 |
| D12 | Classificar um valor com `if` e interpretar o ramo executado | 24 |
| D13 | Tratar `undefined` e refinar o tipo antes de ler uma propriedade | 30 |
| D14 | Transformar com `map`, selecionar com `filter` e buscar com `find` | 60 |
| D15 | Percorrer os valores com `for...of` e contar as iterações | 24 |

## O que mudou para o aluno

A rota de prática reconhece a quarta seção quando ela existe na aula. Isso dá acesso à última família de composição, de `if`, de refinamento, de `find` e de iteração. A tela recebe em cada pergunta a indicação de que o editor deve aceitar várias linhas. Nos exercícios de função condicional e de laço, Enter insere uma linha e o botão **Verificar** envia o código.

Os novos corretores leem a sintaxe e verificam o código no contexto da pergunta com TypeScript 5.9.3 em modo estrito. Em D09, exigem que a função interna forneça o argumento da externa. Em D12, verificam a comparação e o retorno de cada ramo. Em D14, aceitam uma callback com outro nome de parâmetro, a chamada direta do método ou o resultado guardado em uma variável.

Uma resposta de valor pode ser um rótulo com ou sem aspas, um array literal ou `undefined`. No array, a ordem, o tipo e as repetições contam. Para o tipo do resultado de uma busca, `number | undefined` e `undefined | number` recebem a mesma correção. O exercício usa o tipo da instância, que também pode ser textual ou um tipo de objeto.

Em D15, duas famílias aceitam a resposta numérica `0`. Elas compartilham a comparação desse valor. A pergunta servida continua identificando o caso, a explicação e a família que fornecerá a variante após um erro.

## Resultados medidos em 27/11/2026

| Verificação | Resultado |
| --- | --- |
| Partida do servidor | Carregou os 46 conceitos e aceitou os 444 gabaritos |
| Correção nas 36 famílias novas | Uma resposta válida e uma incorreta por instância, totalizando 432 vereditos esperados em 216 casos |
| Piloto Go | 570 casos finais aprovados, incluindo 54 testes de critério novos. Os 46 conceitos chegaram a `MASTERED` pela API real |
| Suítes Go do projeto | 60 pacotes aprovados e cinco sem testes na varredura. A suíte de casos do piloto rodou em separado |
| Interface | 199 arquivos e 1.897 testes aprovados. Build e verificação de tipos aprovados. O lint terminou com sete avisos e zero erros |
| Chromium 151.0.7922.34 | 64 verificações aprovadas. O estudante de teste dominou os 46 conceitos pela tela. As 36 famílias novas apareceram. O script registrou zero erros de página e zero erros HTTP nas rotas de aulas |
| Atualização de D08 para D15 | Dois processos usaram o mesmo banco de teste. O novo executável recuperou a resposta anterior e o token, corrigiu a pergunta pendente e terminou com duas tentativas após o reenvio |
| Distribuição | O patch foi aplicado ao commit-base limpo. Os 26 arquivos resultantes coincidiram byte a byte com os arquivos testados |

Na quarta seção de D09, o navegador errou F042-V0, recebeu F042-V1 e acertou a variante. Em D15, chegou a F074 e submeteu `0` pela tela. Os registros preservam os resultados dos testes e as perguntas sintéticas. [Navegador](evidencias/bloco-4-d09-d15/navegador.json) · [Suítes Go](evidencias/bloco-4-d09-d15/go.json) · [Atualização do banco](evidencias/bloco-4-d09-d15/atualizacao.json)

O SHA-256 do patch é `86c9069394eab06cf755062880254ce74a2e5aadb7369a808b01a0ca51a1f912`.

## Como reproduzir

Aplique o [patch completo](mathua-typescript-pilot.patch) ao commit-base do Mathua indicado no [guia de instalação](LEIA-ME.md#reprodução). Os comandos abaixo partem da raiz desse clone. Instale as dependências do piloto e da interface conforme o guia.

```sh
go build -o pilot-bin ./cmd/typescript-pilot
go test ./cmd/typescript-pilot -count=1 -timeout 20m
go test ./internal/server ./internal/generator ./internal/mastery ./internal/scheduler ./internal/repair -count=1
NEXT_PUBLIC_TS_PILOT=1 NEXT_PUBLIC_SAME_ORIGIN_API=1 NEXT_TELEMETRY_DISABLED=1 npm run build --prefix web/next-app
npm test --prefix web/next-app
node ../scripts/browser-smoke.mjs --mathua . --output /tmp/mathua-navegador.json
```

O ensaio de atualização usa a versão D08 para gravar uma tentativa e servir uma pergunta em um banco temporário. D15 abre esse mesmo banco e usa o token anterior para recuperar a resposta gravada e corrigir a pergunta pendente. Para reproduzir, passe o clone D08 e o clone atual a `scripts/process-smoke.py` conforme o [procedimento do bloco 3](BLOCO-3-D06-D08.md#reprodução).

O corretor reconhece as construções e equivalências do [contrato](../../conteudo/typescript-v1/CONTRATO-DE-CORRECAO.md). Programas arbitrários que produzem o mesmo resultado podem usar construções fora dessa rubrica. O teste de domínio usa um estudante simulado. A rodada de integração foi executada em macOS arm64.
