import httpx

JOLPICA_BASE_URL = "https://api.jolpi.ca/ergast/f1"


def fetch_round(season, circuit_id):
    # Busca o calendário da temporada para descobrir o 'round' do circuito
    response = httpx.get(f"{JOLPICA_BASE_URL}/{season}.json")
    response.raise_for_status()

    races = response.json()["MRData"]["RaceTable"]["Races"]

    for race in races:
        if race["Circuit"]["circuitId"] == circuit_id:
            return race["round"]

    # o circuito não fez parte do calendário dessa temporada
    return None


def fetch_laps_page(season, round_number, limit=30, offset=0):
    # Busca uma página de voltas; o Jolpica devolve os dados em páginas
    laps_url = (
        f"{JOLPICA_BASE_URL}/{season}/{round_number}/laps.json"
        f"?limit={limit}&offset={offset}"
    )

    response = httpx.get(laps_url)
    response.raise_for_status()

    # MRData guarda total, limit e offset, que servem para paginar
    return response.json()["MRData"]


def get_laps(page):
    # Se o offset passar do total, a lista de corridas vem vazia
    races = page["RaceTable"]["Races"]

    if not races:
        return []

    return races[0]["Laps"]


def parse_lap_time(lap_time):
    # Formato recebido: minutos:segundos.milissegundos
    minutes, seconds = lap_time.split(":")
    whole_seconds, milliseconds = seconds.split(".")

    # Sem 3 dígitos, "1:23.4" viraria 4 ms em vez de 400
    if len(milliseconds) != 3:
        raise ValueError(f"Tempo em formato inesperado: {lap_time}")

    # Conversão para ms
    minutes_ms = int(minutes) * 60_000
    seconds_ms = int(whole_seconds) * 1_000
    milliseconds_ms = int(milliseconds)

    return minutes_ms + seconds_ms + milliseconds_ms


if __name__ == "__main__":
    # Só roda quando o arquivo é executado direto, não quando é importado
    season = 2025
    round_number = fetch_round(season, "interlagos")

    if round_number is None:
        raise SystemExit(f"Interlagos não está no calendário de {season}")

    print(f"O round de Interlagos é {round_number}")

    first_page = fetch_laps_page(season, round_number, offset=0)
    second_page = fetch_laps_page(season, round_number, offset=30)

    print(f"Total de registros: {first_page['total']}")
    print(f"Limite por resposta: {first_page['limit']}")

    first_laps = get_laps(first_page)
    second_laps = get_laps(second_page)

    # Experimento 1: cada registro é uma volta ou um piloto numa volta?
    timings_count = sum(len(lap["Timings"]) for lap in first_laps)
    print(f"Página 1: {timings_count} tempos em {len(first_laps)} voltas")

    # Experimento 2: uma volta fica dividida entre duas páginas?
    if first_laps and second_laps:
        print(f"Última volta da página 1: {first_laps[-1]['number']}")
        print(f"Primeira volta da página 2: {second_laps[0]['number']}")

    # Experimento 3: qual o limite máximo que o Jolpica aceita?
    big_page = fetch_laps_page(season, round_number, limit=1000)
    print(f"Pedi limit=1000, o Jolpica devolveu limit={big_page['limit']}")

    # Conversão do primeiro tempo encontrado
    if first_laps:
        lap_time = first_laps[0]["Timings"][0]["time"]
        print(f"Tempo original: {lap_time}")
        print(f"Tempo em milissegundos: {parse_lap_time(lap_time)}")
