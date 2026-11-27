# Anki TypeScript

Material e experimentos para aprender TypeScript por conceitos, com variação de exercícios após erros e feedback sobre a qualidade das perguntas.

## Piloto disponível: Mathua

O piloto integra três conceitos ao motor existente do Mathua: literal numérico, tipo `number` e declaração `const` com valor numérico.

**Estado validado em 26/11/2026:** 29 cenários do piloto e 180 testes existentes selecionados passaram. A validação cobriu a API, a persistência, os pré-requisitos, a correção TypeScript e o ciclo de feedback com revisão humana. Os resultados são das execuções registradas nos arquivos de evidência, anteriores a este envio ao GitHub.

| Material | Conteúdo |
| --- | --- |
| [Relatório e reprodução](pilotos/mathua/LEIA-ME.md) | Caso concreto, critérios, resultados, limites e comandos para reproduzir |
| [Patch completo](pilotos/mathua/mathua-typescript-pilot.patch) | Os seis arquivos novos do piloto e a correção de uma linha na API original |
| [Resultados estruturados](pilotos/mathua/resultados.json) | Versões, contagens, comandos e escopo dos testes |
| [Evidências](pilotos/mathua/evidencias/) | Registros das execuções, falha anterior à correção e teste de reinício do executável |
| [Licença do Mathua](pilotos/mathua/LICENSE-Mathua.txt) | Licença do projeto usado como base |

## Como retomar

Leia o [relatório](pilotos/mathua/LEIA-ME.md) e siga a seção de reprodução a partir de `pilotos/mathua/`. O patch contém o código completo da adaptação e deve ser aplicado ao commit-base indicado do Mathua. O piloto depende desse projeto para compilar e executar.

As próximas partes pendentes são a integração visual e a geração automática de novas famílias de exercícios a partir do feedback. Hoje, o feedback permite registrar, revisar e resolver problemas com participação humana.

## Origem

- Projeto-base: [chuma-beep/mathua](https://github.com/chuma-beep/mathua).
- Commit-base: [`2bd4a4e0e160653e274521f6de3df2e61e29c7f7`](https://github.com/chuma-beep/mathua/tree/2bd4a4e0e160653e274521f6de3df2e61e29c7f7).
- O conteúdo e o corretor TypeScript são uma adaptação própria deste piloto. Não são conteúdo oficial do Math Academy nem um currículo oficial do Mathua.
