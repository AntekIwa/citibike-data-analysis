import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

print("=== START ===")

# --- ZMIENNA STERUJĄCA LICZBĄ KLASTRÓW ---
N_CLUSTERS = 7
# ----------------------------------------

data_path = 'data/processed/citi_bike_ml_ready.csv'

print("Wczytywanie danych...")
df_ml = pd.read_csv(data_path)

# Usunięcie weekendów (soboty i niedziele)
print("Filtrowanie danych: Usuwanie weekendów...")
df_ml = df_ml[df_ml['day_of_week'] < 5].copy()
print(f"Liczba wierszy po usunięciu weekendów: {len(df_ml)}")

features = ['hour', 'day_of_week', 'duration_min', 'temp_max_C', 'precipitation_mm']
X = df_ml[features]

print("Skalowanie cech...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"Trenowanie algorytmu K-Means dla {N_CLUSTERS} klastrów...")
kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=42, n_init=10)
df_ml['cluster'] = kmeans.fit_predict(X_scaled)

plt.style.use('dark_background')
color_palette = 'tab10'

os.makedirs('data/processed', exist_ok=True)

# --- WYKRES 1: Profile Godzinowe i Czasowe ---
print("Generowanie wykresu 1: Profile godzinowe i czas podróży...")
plt.figure(figsize=(16, 6))

plt.subplot(1, 2, 1)
sns.kdeplot(data=df_ml, x='hour', hue='cluster', fill=True, palette=color_palette, common_norm=False, alpha=0.4)
plt.title(f'Profil Godzinowy ({N_CLUSTERS} Klastrów - Dni Robocze)', fontsize=13, fontweight='bold')
plt.xlabel('Godzina w ciągu dnia')
plt.xticks(range(0, 24, 2))

plt.subplot(1, 2, 2)
sns.boxplot(data=df_ml, x='cluster', y='duration_min', palette=color_palette, showfliers=False)
plt.title(f'Czas podróży ({N_CLUSTERS} Klastrów)', fontsize=13, fontweight='bold')
plt.xlabel('Wyznaczony Klaster (Grupa)')
plt.ylabel('Czas trwania podróży (minuty)')
plt.tight_layout()

plot1_path = f'data/processed/klastry_{N_CLUSTERS}k_godzina.png'
plt.savefig(plot1_path, dpi=300, bbox_inches='tight')
print(f"-> Zapisano: {plot1_path}")
plt.show()

# --- WYKRES 2: Pogoda (Temperatura vs Godzina) ---
print("Generowanie wykresu 2: Zależność od temperatury i pory dnia...")
plt.figure(figsize=(12, 6))
df_sample = df_ml.sample(n=min(20000, len(df_ml)), random_state=42)

sns.scatterplot(
    data=df_sample, x='hour', y='temp_max_C', hue='cluster',
    palette=color_palette, alpha=0.7, s=40
)
plt.title(f'Zależność pory dnia od temp. ({N_CLUSTERS} Klastrów - Dni Robocze)', fontsize=14, fontweight='bold')
plt.xlabel('Godzina w ciągu dnia')
plt.ylabel('Maksymalna temperatura dnia (°C)')
plt.xticks(range(0, 24, 2))
plt.grid(True, alpha=0.2)
plt.legend(title='Klaster', loc='lower right', ncol=2)
plt.tight_layout()

plot2_path = f'data/processed/klastry_{N_CLUSTERS}k_pogoda.png'
plt.savefig(plot2_path, dpi=300, bbox_inches='tight')
print(f"-> Zapisano: {plot2_path}")
plt.show()

# --- WYKRES 3: Ewolucja Pandemiczna ---
print("Generowanie wykresu 3: Ewolucja profili użytkowników w czasie...")
cluster_evolution = df_ml.groupby(['year', 'cluster']).size().unstack()
cluster_evolution_pct = cluster_evolution.apply(lambda x: x / x.sum() * 100, axis=1)

# Dynamiczne generowanie etykiet legendy na podstawie liczby klastrów
legend_labels = [f"Profil {i}" for i in range(N_CLUSTERS)]

plt.figure(figsize=(12, 6))
cluster_evolution_pct.plot(kind='bar', stacked=True, figsize=(11, 6), cmap=color_palette, edgecolor='black', linewidth=1)

plt.title(f'Ewolucja profili użytkowników ({N_CLUSTERS} Klastrów, Dni robocze, 2019-2022)', fontsize=14, fontweight='bold')
plt.xlabel('Rok')
plt.ylabel('Udział w całkowitym ruchu (%)')
plt.legend(title='Profile Behawioralne', labels=legend_labels, bbox_to_anchor=(1.02, 1), loc='upper left')
plt.xticks(rotation=0)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()

plot3_path = f'data/processed/klastry_{N_CLUSTERS}k_rok.png'
plt.savefig(plot3_path, dpi=300, bbox_inches='tight')
print(f"-> Zapisano: {plot3_path}")
plt.show()

print("\n=== gotowe ===")