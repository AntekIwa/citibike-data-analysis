import requests
import pandas as pd
import os

# Konfiguracja dla Nowego Jorku i lat 2019-2022
LATITUDE = 40.7128
LONGITUDE = -74.0060
START_DATE = "2019-01-01"
END_DATE = "2022-12-31"

# Budowanie adresu URL do API Open-Meteo
url = (
    f"https://archive-api.open-meteo.com/v1/archive?"
    f"latitude={LATITUDE}&longitude={LONGITUDE}&"
    f"start_date={START_DATE}&end_date={END_DATE}&"
    f"daily=temperature_2m_max,temperature_2m_min,precipitation_sum&"
    f"timezone=America/New_York"
)

print(f"Pobieranie danych pogodowych dla Nowego Jorku z API Open-Meteo...")
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    # Wyciągamy dane dzienne (daily) z odpowiedzi JSON
    daily_data = data['daily']

    df_weather = pd.DataFrame({
        'date': pd.to_datetime(pd.Series(daily_data['time'])).dt.date,
        'temp_max_C': daily_data['temperature_2m_max'],
        'temp_min_C': daily_data['temperature_2m_min'],
        'precipitation_mm': daily_data['precipitation_sum']
    })
    # Zapisujemy do folderu processed
    output_path = 'data/processed/nyc_weather.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_weather.to_csv(output_path, index=False)

    print(f"Sukces! Zapisano dane pogodowe w: {output_path}")
    print("\nPierwsze kilka wierszy pogody:")
    print(df_weather.head())
else:
    print(f"Błąd podczas pobierania danych. Kod HTTP: {response.status_code}")