import httpx


JOLPICA_BASE_URL = "https://api.jolpi.ca/ergast/f1"

# Busca do calendário de 2025 para checar o 'round' de Interlagos
response = httpx.get(f"{JOLPICA_BASE_URL}/2025.json")
response.raise_for_status()

data = response.json()

races = data["MRData"]["RaceTable"]["Races"]

# Busco Interlagos nas corridas da temporada
for race in races:
    if race["Circuit"]["circuitId"] == "interlagos":
        round_number = race["round"]

        print(f"O round de Interlagos é {round_number}")

        # Offset separado para depois poder automatizar a paginação
        offset = 30

        # Agora que tenho o 'round', posso buscar os tempos de volta
        laps_url = (
            f"{JOLPICA_BASE_URL}/2025/{round_number}/laps.json"
            f"?limit=30&offset={offset}"
        )

        laps_response = httpx.get(laps_url)
        laps_response.raise_for_status()

        laps_data = laps_response.json()

        # Check se o Jolpica realmente recebeu o offset
        print(f"URL chamada: {laps_response.request.url}")
        print(f"Offset retornado: {laps_data['MRData']['offset']}")

        # Guardo os dados que vou precisar para entender a paginação
        total = laps_data["MRData"]["total"]
        limit = laps_data["MRData"]["limit"]

        print(f"Total de registros: {total}")
        print(f"Limite por resposta: {limit}")

        # Busco até chegar nas voltas da corrida
        laps = laps_data["MRData"]["RaceTable"]["Races"][0]["Laps"]

        timings = laps[0]["Timings"]

        lap_time = timings[0]["time"]

        # Formato recebido: minutos:segundos.milissegundos
        minutes, seconds = lap_time.split(":")
        whole_seconds, milliseconds = seconds.split(".")

        # Conversão para ms
        minutes_ms = int(minutes) * 60_000
        seconds_ms = int(whole_seconds) * 1_000
        milliseconds_ms = int(milliseconds)

        lap_time_ms = minutes_ms + seconds_ms + milliseconds_ms

        print(f"Tempo original: {lap_time}")
        print(f"Tempo em milissegundos: {lap_time_ms}")

        break