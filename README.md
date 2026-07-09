# DeltaF1

Comparador de tempos de volta entre carros de F1 em pistas e anos diferentes.

**Status:** em início

## A pergunta

Um carro de 2004 era mais rápido que o de 2014 em Monza?

Resposta ingênua: comparar o tempo de pole. Isso está errado — traçado,
asfalto, pneu, combustível e regulamento mudaram. Este projeto tenta medir
o que dá pra medir.

## Fonte de dados

Jolpica-F1, sucessor do Ergast.
Base: https://api.jolpi.ca/ergast/f1/

Consequência: a API pública deste projeto nunca consulta o Jolpica em
tempo de requisição. Ingestão offline, banco local.

## Perguntas em aberto

- [ ] Qual o limite de requisições por hora sem autenticação? (fonte: ?)
- [ ] Quando exatamente o Ergast foi desligado? (fonte: ?)
- [ ] Desde que ano existem tempos volta a volta?
- [ ] Desde que ano existem pit stops?
- [ ] Desde que ano a classificação vem separada em Q1/Q2/Q3?
- [ ] Qual o `limit` máximo por página? Como funciona o `offset`?
- [ ] O que dizem os termos de uso sobre cache e redistribuição?
- [ ] Quando Monza foi recapeada ou mudou de traçado?

## Decisões

- Tempo de volta em **inteiro de milissegundos**. Nunca float.
- Mediana e MAD, nunca média e desvio-padrão — safety car destrói os dois.
- Nenhum endpoint devolve número sem intervalo.
- Toda resposta carrega `caveats[]`: o que aquela comparação não controla.
  Isso é a implementação do "declarar em voz alta o que não dá".

## Fora de escopo

Telemetria ponto a ponto. Previsão. Login. Front. WEC.

## Como rodar

Ainda não roda.