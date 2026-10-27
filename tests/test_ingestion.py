import pytest

from deltaf1.ingestion import get_laps, parse_lap_time


def test_tempo_comum():
    assert parse_lap_time("1:23.456") == 83_456


def test_tempo_acima_de_dois_minutos():
    assert parse_lap_time("2:03.001") == 123_001


def test_texto_invalido():
    with pytest.raises(ValueError):
        parse_lap_time("abc")


def test_milissegundos_incompletos():
    # "1:23.4" não pode virar 83004 ms em silêncio
    with pytest.raises(ValueError):
        parse_lap_time("1:23.4")


def test_pagina_vazia():
    # offset maior que o total: a API devolve a lista de corridas vazia
    page = {"RaceTable": {"Races": []}}
    assert get_laps(page) == []
