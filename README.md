# DeltaF1

Projeto em Python para coleta e análise de dados históricos da Fórmula 1.

A ideia do DeltaF1 é explorar uma pergunta que parece simples:

> Como comparar o desempenho de carros de Fórmula 1 de épocas diferentes?

Comparar apenas tempos de pole ou melhores voltas pode ser enganoso, já que fatores como regulamento, pneus, combustível, condições da pista e alterações no circuito mudam ao longo dos anos.

O projeto está sendo desenvolvido para coletar e organizar esses dados antes de realizar as comparações.

## O que já foi implementado

Atualmente, o projeto possui uma primeira etapa de ingestão de dados utilizando a API pública Jolpica-F1

O código:

* consulta o calendário de uma temporada
* identifica uma corrida através do circuito
* utiliza o número da etapa para buscar os dados de volta
* acessa os tempos individuais retornados pela API
* converte tempos no formato `minutos:segundos.milissegundos` para um inteiro em milissegundos

## Fonte dos dados

O projeto utiliza a [Jolpica-F1](https://api.jolpi.ca/ergast/f1/).

A proposta é realizar a ingestão dos dados separadamente e armazená-los localmente, evitando depender da API externa durante futuras consultas da aplicação.

## Tecnologias

* Python
* HTTPX
* Git
* APIs REST / JSON

## Estrutura atual

```text
deltaf1/
├── src/
│   └── deltaf1/
│       ├── __init__.py
│       └── ingestion.py
├── .gitignore
├── .env.example
├── pyproject.toml
└── README.md
```

## Próximos passos

* implementar paginação da API
* coletar todas as voltas de uma corrida
* separar a lógica de ingestão em funções
* persistir os dados localmente
* adicionar testes
* criar métricas para comparação entre temporadas

## Objetivo de longo prazo

Construir uma aplicação capaz de comparar dados de desempenho entre diferentes temporadas da Fórmula 1, deixando explícitas as limitações estatísticas de cada comparação.
