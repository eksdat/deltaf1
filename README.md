# DeltaF1

Projeto em Python para coleta e análise de dados históricos da Fórmula 1.

A ideia do DeltaF1 é explorar uma pergunta que parece simples:

> Como comparar o desempenho de carros de Fórmula 1 de épocas diferentes?

Comparar apenas tempos de pole ou melhores voltas pode ser enganoso, já que fatores como regulamento, pneus, combustível, condições da pista e alterações no circuito mudam ao longo dos anos.

O projeto está sendo desenvolvido para coletar e organizar esses dados antes de realizar as comparações.

## O que já foi implementado

Atualmente, o projeto possui uma primeira etapa de ingestão de dados utilizando a API pública Jolpica-F1.

O código:

* consulta o calendário de uma temporada e encontra o `round` de um circuito
* busca uma página de voltas da corrida (a API devolve os dados em páginas)
* trata a página vazia que a API devolve quando o offset passa do total
* converte tempos no formato `minutos:segundos.milissegundos` para um inteiro em milissegundos, rejeitando formatos inesperados
* tem testes automatizados com pytest, que não dependem da internet

## Fonte dos dados

O projeto utiliza a [Jolpica-F1](https://api.jolpi.ca/ergast/f1/), que não exige chave de acesso.

A proposta é realizar a ingestão dos dados separadamente e armazená-los localmente, evitando depender da API externa durante futuras consultas da aplicação.

## O que descobri sobre a API

Testes feitos com o GP de São Paulo de 2025 (Interlagos, round 21):

* cada registro de `laps.json` é o tempo de **um piloto em uma volta**, não uma volta inteira
* por isso, uma mesma volta pode ficar dividida entre duas páginas (a página 1 termina na volta 2 e a página 2 começa na volta 2)
* o limite máximo por página é 100, mesmo pedindo mais
* a corrida tem 1249 registros, menos que 71 voltas × 20 pilotos (1420), por causa de abandonos e retardatários
* para conferir se a coleta está completa, a soma dos tempos coletados deve ser igual ao `total` informado pela API

## Tecnologias

* Python
* HTTPX
* pytest
* Git
* APIs REST / JSON

## Como rodar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

pytest                            # testes, sem acesso à internet
python src/deltaf1/ingestion.py   # busca dados reais de Interlagos 2025
```

## Estrutura atual

```text
deltaf1/
├── src/
│   └── deltaf1/
│       ├── __init__.py
│       └── ingestion.py
├── tests/
│   └── test_ingestion.py
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
```

## Limitações atuais

* funciona para uma corrida por vez (Interlagos 2025, no exemplo)
* a paginação ainda não é automática: o código busca páginas específicas
* os dados ainda não são salvos localmente

## Próximos passos

* automatizar a paginação e coletar todas as voltas de uma corrida
* persistir os dados localmente (SQLite)
* integrar o OpenF1 nas corridas a partir de 2023 (pneus, clima e safety car)
* criar métricas para comparação entre temporadas

## Objetivo de longo prazo

Construir uma aplicação capaz de comparar dados de desempenho entre diferentes temporadas da Fórmula 1, deixando explícitas as limitações estatísticas de cada comparação.

## Licença

O código está sob a licença MIT (veja o arquivo `LICENSE`).

Os dados de Fórmula 1 vêm da Jolpica-F1 e seguem os termos dessa fonte. Eles não são versionados neste repositório.
