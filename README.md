# Anki TypeScript

Material e experimentos para aprender TypeScript por conceitos, com variação de exercícios após erros e feedback sobre a qualidade das perguntas.

## Piloto disponível: Mathua

O piloto integra três conceitos ao motor existente do Mathua: literal numérico, tipo `number` e declaração `const` com valor numérico.

**Estado validado em 26/11/2026:** a interface existente do Mathua funciona com o piloto. O teste em Chromium percorreu os três conceitos, os links de continuação, a liberação por pré-requisitos, o ciclo errar → variante → acertar e o envio de feedback. Os 29 cenários do piloto passaram novamente e o programa de reinício real está incluído.

**Ressalva da suíte geral:** `go test -json ./... -count=1` terminou com 59 pacotes aprovados, um reprovado e cinco sem testes. A falha de `TestWave23QuestionVariety` também apareceu no commit-base sem o patch, em uma repetição de 500 execuções. Os comandos, as saídas e os limites estão registrados abaixo.

| Material | Conteúdo |
| --- | --- |
| [Relatório e reprodução](pilotos/mathua/LEIA-ME.md) | Caso concreto, critérios, resultados, limites e comandos para reproduzir |
| [Comandos e saídas desta rodada](pilotos/mathua/COMANDOS-E-SAIDAS.md) | Ambiente medido, teste no navegador, reinício, contrato `ungraded` e falha da suíte geral |
| [Patch completo](pilotos/mathua/mathua-typescript-pilot.patch) | Piloto, aulas, servidor da interface existente, uma linha na API e duas propriedades no botão de feedback |
| [Resultados estruturados](pilotos/mathua/resultados.json) | Versões, contagens, comandos e escopo dos testes |
| [Evidências](pilotos/mathua/evidencias/) | Registros das execuções, falha anterior à correção e teste de reinício do executável |
| [Programas de verificação](pilotos/mathua/scripts/) | Reinício de processos e fluxo no navegador, ambos contra a API real |
| [Licença do Mathua](pilotos/mathua/LICENSE-Mathua.txt) | Licença do projeto usado como base |

## Como retomar

Leia o [relatório](pilotos/mathua/LEIA-ME.md) e siga a seção de reprodução a partir de `pilotos/mathua/`. O patch contém o código completo da adaptação e deve ser aplicado ao commit-base indicado do Mathua. O piloto depende desse projeto para compilar e executar.

A instalação compila a interface e o executável. Depois de iniciá-lo, abra `http://127.0.0.1:8081`. O ambiente testado foi Linux x86_64 com Node `24.22.3`, Go `1.26.6` e Chromium `158.0.8127.0`. A exigência de Node da interface vem do `package.json` do Mathua. As versões `24.14.1` e `26.7.0` não satisfazem essa exigência.

Há três conceitos introdutórios, uma família por conceito. A geração automática de novas famílias a partir do feedback continua pendente. Hoje, o feedback permite registrar, revisar e resolver problemas com participação humana. A calibração pedagógica com alunos reais e a instalação no computador do usuário não foram verificadas.

## Origem

- Projeto-base: [chuma-beep/mathua](https://github.com/chuma-beep/mathua).
- Commit-base: [`2bd4a4e0e160653e274521f6de3df2e61e29c7f7`](https://github.com/chuma-beep/mathua/tree/2bd4a4e0e160653e274521f6de3df2e61e29c7f7).
- O conteúdo e o corretor TypeScript são uma adaptação própria deste piloto. Não são conteúdo oficial do Math Academy nem um currículo oficial do Mathua.
