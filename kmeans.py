import pandas as pd
import glob
import os
import random

print("=== ROZPOCZYNAMY PRZYGOTOWANIE DANYCH DO UCZENIA MASZYNOWEGO ===")

# 1. Wczytanie danych pogodowych
print("Wczytywanie historii pogody...")
df_weather = pd.read_csv('data/processed/nyc_weather.csv')
df_weather['date'] = pd.to_datetime(df_weather['date'])

# 2. Skanowanie surowych gigabajtów
raw_files = glob.glob('data/raw/**/*.csv', recursive=True)
df_list = []

print(f"Znaleziono {len(raw_files)} plików surowych. Losowanie 1% próbki...")
for f in raw_files:
    try:
        header = pd.read_csv(f, nrows=0).columns

        if 'starttime' in header and 'stoptime' in header:
            use_cols = ['starttime', 'stoptime']
        elif 'started_at' in header and 'ended_at' in header:
            use_cols = ['started_at', 'ended_at']
        else:
            continue

        # Sprytne czytanie 1% wierszy bez zapychania RAMu
        df_temp = pd.read_csv(f, usecols=use_cols, skiprows=lambda i: i > 0 and random.random() > 0.01)
        df_temp.columns = ['start', 'end']
        df_list.append(df_temp)
        print(f"-> Pomyślnie pobrano próbkę z: {os.path.basename(f)}")
    except Exception as e:
        print(f" Błąd podczas przetwarzania pliku {os.path.basename(f)}: {e}")
        continue

# 3. Łączenie próbek w jedną bazę
print("\nŁączenie próbek i wyciąganie cech...")
df_raw = pd.concat(df_list, ignore_index=True)

df_raw['start'] = pd.to_datetime(df_raw['start'])
df_raw['end'] = pd.to_datetime(df_raw['end'])

# Ekstrakcja cech behawioralnych
df_raw['year'] = df_raw['start'].dt.year
df_raw['hour'] = df_raw['start'].dt.hour
df_raw['day_of_week'] = df_raw['start'].dt.dayofweek
df_raw['duration_min'] = (df_raw['end'] - df_raw['start']).dt.total_seconds() / 60.0
df_raw['date'] = df_raw['start'].dt.normalize()

# Czyszczenie anomalii czasowych (błędy stacji)
df_raw = df_raw[(df_raw['duration_min'] >= 2) & (df_raw['duration_min'] <= 180)]

# 4. Mariaż z danymi pogodowymi
print("Łączenie danych o przejazdach z historią pogody...")
df_ml = pd.merge(df_raw, df_weather, on='date', how='inner')
df_ml = df_ml.dropna(subset=['temp_max_C', 'precipitation_mm'])

# 5. Zapis finalnego, lekkiego zestawu danych do uczenia
output_file = 'data/processed/citi_bike_ml_ready.csv'
os.makedirs(os.path.dirname(output_file), exist_ok=True)
df_ml[['year', 'hour', 'day_of_week', 'duration_min', 'temp_max_C', 'precipitation_mm']].to_csv(output_file,
                                                                                                index=False)

print(f"\n SUKCES! Plik zintegrowany dla ML został zapisany w: {output_file}")
print(f"Łączna liczba rekordów do analizy: {len(df_ml)}")