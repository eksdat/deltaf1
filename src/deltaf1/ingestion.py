import httpx

JOLPICA_BASE_URL = "https://api.jolpi.ca/ergast/f1"

# Primeiro eu busco todas as corridas de 2025
response = httpx.get(f"{JOLPICA_BASE_URL}/2025.json")
response.raise_for_status()

# Transformo a resposta da API em um dicionário Python
data = response.json()

# acesso a lista de corridas que veio dentro do JSON
races = data["MRData"]["RaceTable"]["Races"]

# Percorro as corridas até encontrar Interlagos
for race in races:
    if race["Circuit"]["circuitId"] == "interlagos":
        # Salvo o número do round porque vou precisar dele para buscar as voltas
        round_number = race["round"]

        print(f"O round de Interlagos é {round_number}")

        # URL que retorna os tempos de volta
        laps_url = f"{JOLPICA_BASE_URL}/2025/{round_number}/laps.json"

        # Faço uma nova requisição, agora buscando os dados das voltas
        laps_response = httpx.get(laps_url)
        laps_response.raise_for_status()

        # Converto a resposta das voltas para um dicionário do Python
        laps_data = laps_response.json()

        # acesso a lista de voltas da corrida
        laps = laps_data["MRData"]["RaceTable"]["Races"][0]["Laps"]

        # Por enquanto estou usando somente a primeira volta para entender os dados
        timings = laps[0]["Timings"]

        # Pego o tempo do primeiro piloto da lista
        lap_time = timings[0]["time"]

        # O tempo vem como texto no formato "1:18.067"
        # primeiro separo os minutos dos segundos
        minutes, seconds = lap_time.split(":")

        #depois separo os segundos inteiros dos milissegundos
        whole_seconds, milliseconds = seconds.split(".")

        # Converto cada parte diretamente para milissegundos
        # sem usar float, porque quero evitar problemas de precisão
        minutes_ms = int(minutes) * 60_000
        seconds_ms = int(whole_seconds) * 1_000
        milliseconds_ms = int(milliseconds)

        # Somo tudo para guardar o tempo como um inteiro
        lap_time_ms = minutes_ms + seconds_ms + milliseconds_ms

        print(f"Tempo original: {lap_time}")
        print(f"Tempo em milissegundos: {lap_time_ms}")

        break