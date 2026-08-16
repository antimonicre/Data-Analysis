from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_excel("/Users/keni/Desktop/datasets/filtrado.xlsx")


mapa_meses = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12,
}

df['num_mes'] = df["Month"].map(mapa_meses)
df['total_personas'] = df["Total Number of Individuals migrants"]

evolucion = (
    df.groupby(['Year', 'num_mes'])['total_personas'].sum().reset_index()
)
evolucion['fecha'] = pd.to_datetime(
    evolucion['Year'].astype(str)
    + '-'
    + evolucion['num_mes'].astype(str)
    + '-01'
)
evolucion = evolucion.sort_values('fecha')

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    evolucion['fecha'],
    evolucion['total_personas'],
    marker='o',
    linewidth=2.5,
    color='#1f77b4',
    label='Entradas registradas',
)

date_lahj = pd.to_datetime('2023-08-01')
date_taiz = pd.to_datetime('2024-10-01')


ax.axvline(
    x=date_lahj,
    color='#d62728',
    linestyle='--',
    linewidth=2,
    label='Ago 2023: Operación en Lahj',
)
ax.axvline(
    x=date_taiz,
    color='#2ca02c',
    linestyle='--',
    linewidth=2,
    label='Oct 2024: Acceso OIM a Ta\'iz',
)
ax.axvspan(
    date_lahj,
    date_taiz,
    color='gray',
    alpha=0.15,
    label='Período de sesgo por falta de acceso',
)

ax.annotate(
    'Operación antitráfico\nen Lahj (Desvío de rutas)',
    xy=(
        date_lahj,
        4176,
    ),
    xytext=(
        pd.to_datetime('2024-05-01'),
        16000,
    ),
    ha='right',
    arrowprops=dict(
        facecolor='#d62728',
        edgecolor='#d62728',
        shrink=0.05,
        width=1.5,
        headwidth=7,
    ),
    fontsize=9.5,
    fontweight='bold',
    color='#d62728',
)

ax.annotate(
    'Monitoreo en Ta\'iz\n(Fin del punto ciego)',
    xy=(date_taiz, 6364),
    xytext=(pd.to_datetime('2024-01-01'), 9500),
    arrowprops=dict(
        facecolor='#2ca02c', shrink=0.08, width=1.5, headwidth=7
    ),
    fontsize=10,
    fontweight='bold',
    color='#2ca02c',
)

ax.set_title(
    'Entradas Migratorias a Yemen (2023 - 2026)\n',
    fontsize=13,
    fontweight='bold',
    pad=15,
)
ax.set_xlabel('Año y Mes', fontsize=11)
ax.set_ylabel('Total de migrantes registrados', fontsize=11)
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9)

ax.legend(
    loc='upper center',
    bbox_to_anchor=(0.75, -0.18),
    ncol=2,
    frameon=True,
    facecolor='white',
    framealpha=0.95,
    fontsize=9.5,
)

# Guardar la imagen en tu carpeta
plt.tight_layout()
ruta_imagen = "/Users/keni/Desktop/results/grafico_yemen.png"
plt.savefig(ruta_imagen, dpi=300)
plt.show()