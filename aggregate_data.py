import pandas as pd
import os
import glob

# sciezka do danych
raw_data_path = 'data/raw'

# Wyszukiwanie wszystkich plików CSV we wszystkich podfolderach
all_files = glob.glob(os.path.join(raw_data_path, "**", "*.csv"), recursive=True)

if not all_files:
    print("Nie znaleziono żadnych plików .csv! Sprawdź strukturę folderów.")
    exit()

daily_aggregates = []

print(f"Znaleziono {len(all_files)} plików do przetworzenia. Zaczynamy...\n")

for file in all_files:
    print(f"Przetwarzam plik: {os.path.basename(file)}...")

    # Wczytujemy plik
    df = pd.read_csv(file, low_memory=False)

    # Rozpoznawanie kolumny z data
    if 'starttime' in df.columns:
        date_col = 'starttime'
    elif 'started_at' in df.columns:
        date_col = 'started_at'
    else:
        print(f" -> Pomijam plik (brak znanej kolumny z datą): {os.path.basename(file)}")
        continue

    # Wyciągnięcie samej daty (bez godziny) do nowej kolumny
    df['date'] = pd.to_datetime(df[date_col]).dt.date

    # Agregacja: zliczamy liczbę przejazdów każdego dnia
    daily_summary = df.groupby('date').size().reset_index(name='total_rides')

    daily_aggregates.append(daily_summary)

print("\nŁączenie wszystkich miesięcy w jeden główny zbiór...")
final_daily_data = pd.concat(daily_aggregates, ignore_index=True)

# Sumujemy jeszcze raz dla pewności (gdyby przejazdy nocne nachodziły na dwa pliki)
final_daily_data = final_daily_data.groupby('date')['total_rides'].sum().reset_index()

# Sortowanie po dacie rosnąco
final_daily_data = final_daily_data.sort_values('date')

# Zapis do pliku wynikowego
output_path = 'data/processed/citi_bike_daily.csv'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
final_daily_data.to_csv(output_path, index=False)

print(f"Gotowe! Zagregowane dane zapisano w: {output_path}")