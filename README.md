# Anki TypeScript

Material e experimentos para aprender TypeScript por conceitos, com variação de exercícios após erros e feedback sobre a qualidade das perguntas.

## Conteúdo completo da escada

O [pacote de conteúdo](conteudo/typescript-v1/LEIA-ME.md) preserva os **15 degraus e 74 cartões originais** e entrega as aulas, gabaritos, explicações, critérios de correção e seis instâncias por família: **444 perguntas completas**, organizadas em 46 conceitos. O [currículo legível](conteudo/typescript-v1/CURRICULO.md), o [banco de exercícios](conteudo/typescript-v1/EXERCICIOS.md) e os JSON estão prontos para a próxima IA integrar ao piloto.

**Conteúdo preparado não significa conteúdo já disponível na aplicação.** O piloto descrito abaixo continua com os três conceitos existentes. A integração deve completar as lacunas dos degraus 1–3 e seguir a ordem da escada, preservando os IDs e o progresso. A [verificação do conteúdo](conteudo/typescript-v1/COMANDOS-E-SAIDAS.md) foi executada em Linux, com Node 24.22.3 e TypeScript 5.9.3; ela é distinta dos testes da aplicação e não mede aprendizagem com alunos reais.

## Piloto disponível: Mathua

O piloto integra três conceitos ao motor existente do Mathua: literal numérico, tipo `number` e declaração `const` com valor numérico.

**Estado validado em 27/11/2026, em macOS:** a tela existente do Mathua está ajustada para estudar TypeScript. O campo de resposta não mostra o teclado de símbolos matemáticos. O percurso de estudo e o menu lateral estão em português. Os menus do catálogo de matemática estão ocultos. O teste em Chromium passou com 14 verificações: ler a explicação, responder, receber a correção, receber uma variante após errar, avançar após os pré-requisitos, relatar uma pergunta, consultar o relato, recarregar a página e reiniciar o servidor sem perder o progresso. Os 29 cenários do piloto e os 1885 testes unitários da interface passaram.

**Linux e Mac são execuções separadas.** As execuções em Linux são de 26/11/2026 e usaram o patch anterior. Os ajustes da tela desta rodada foram validados só em macOS.

**Ressalva da suíte geral, medida em Linux:** `go test -json ./... -count=1` terminou com 59 pacotes aprovados, um reprovado e cinco sem testes. A falha de `TestWave23QuestionVariety` também apareceu no commit-base sem o patch, em uma repetição de 500 execuções. No Mac, o mesmo teste falhou 5 vezes em 500 execuções no commit-base. A suíte geral não foi repetida com o patch atual. Os comandos, as saídas e os limites estão registrados abaixo.

| Material | Conteúdo |
| --- | --- |
| [Relatório e reprodução](pilotos/mathua/LEIA-ME.md) | Caso concreto, critérios, resultados, limites e comandos para reproduzir |
| [Comandos e saídas em macOS](pilotos/mathua/COMANDOS-E-SAIDAS-MAC.md) | Rodada de 27/11/2026 com o patch atual: versões testadas e exigidas, testes, controle negativo e capturas de tela |
| [Comandos e saídas em Linux](pilotos/mathua/COMANDOS-E-SAIDAS.md) | Rodada de 26/11/2026 com o patch anterior: ambiente, navegador, reinício, contrato `ungraded` e falha da suíte geral |
| [Patch completo](pilotos/mathua/mathua-typescript-pilot.patch) | Piloto, aulas, servidor da interface existente, uma linha na API e os ajustes da tela ligados pela chave `NEXT_PUBLIC_TS_PILOT=1` |
| [Resultados estruturados](pilotos/mathua/resultados.json) | Versões, contagens, comandos e escopo dos testes |
| [Evidências em Linux](pilotos/mathua/evidencias/) | Registros das execuções, falha anterior à correção e teste de reinício do executável |
| [Evidências em macOS](pilotos/mathua/evidencias/mac/) | Registros das execuções no Mac e sete capturas de tela |
| [Programas de verificação](pilotos/mathua/scripts/) | Reinício de processos e fluxo no navegador, ambos contra a API real |
| [Licença do Mathua](pilotos/mathua/LICENSE-Mathua.txt) | Licença do projeto usado como base |

## Como retomar

Leia o [relatório](pilotos/mathua/LEIA-ME.md) e siga a seção de reprodução a partir de `pilotos/mathua/`. O patch contém o código completo da adaptação e deve ser aplicado ao commit-base indicado do Mathua. O piloto depende desse projeto para compilar e executar.

A instalação compila a interface e o executável. Depois de iniciá-lo, abra `http://127.0.0.1:8081`.

Versão exigida: a compilação da interface exige Node `^22.23.4 || ^24.22.1 || ^26.12.1`, conforme o campo `engines.node` de `web/next-app/package.json` do Mathua. Versões testadas: em Linux x86_64, Node `24.22.3`, Go `1.26.6` e Chromium `158.0.8127.0`; em macOS arm64, Node `24.22.3` na compilação da interface, Node `24.14.1` na execução, Go `1.26.6` e Chromium `151.0.7922.34`. A versão testada não é a versão mínima.

Há três conceitos introdutórios, uma família por conceito. A geração automática de novas famílias a partir do feedback continua pendente. Hoje, o feedback permite registrar, revisar e resolver problemas com participação humana. A calibração pedagógica com alunos reais não foi verificada. As páginas fora do percurso de estudo continuam em inglês.

## Origem

- Projeto-base: [chuma-beep/mathua](https://github.com/chuma-beep/mathua).
- Commit-base: [`2bd4a4e0e160653e274521f6de3df2e61e29c7f7`](https://github.com/chuma-beep/mathua/tree/2bd4a4e0e160653e274521f6de3df2e61e29c7f7).
- O conteúdo e o corretor TypeScript são uma adaptação própria deste piloto. Não são conteúdo oficial do Math Academy nem um currículo oficial do Mathua.
