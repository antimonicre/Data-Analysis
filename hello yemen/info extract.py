from pathlib import Path
import pandas as pd

# 1. CARGA DE DATOS
ruta_entrada = Path("/Users/keni/Desktop/datasets/yemen/filtrado.xlsx")
df = pd.read_excel(ruta_entrada)

# Definición de columnas
col_total = "Total Number of Individuals migrants"
col_hombres = "Men"
col_mujeres = "Women"
col_ninos = "Boys"
col_ninas = "Girls"
col_mes = "Month"
col_year = "Year"
col_origen = "Departure (admin0)"
col_destino = "[[Destination ] (admin0)"
col_transport = "Mean of Transport"

# Cálculos generales
total = df[col_total].sum()
total_h = df[col_hombres].sum()
total_m = df[col_mujeres].sum()
df["total_kids"] = df[col_ninos] + df[col_ninas]
total_kids = df["total_kids"].sum()

# -------------------------------------------------------------
# ESTRUCTURACIÓN DE RESULTADOS PARA EXCEL
# -------------------------------------------------------------

# Tabla 1: Perfil Demográfico
df_perfil = pd.DataFrame(
    [
        {
            "Categoría": "Total entradas registradas",
            "Cantidad": total,
            "Porcentaje": "100.0%",
        },
        {
            "Categoría": "Hombres",
            "Cantidad": total_h,
            "Porcentaje": f"{(total_h/total)*100:.1f}%",
        },
        {
            "Categoría": "Mujeres",
            "Cantidad": total_m,
            "Porcentaje": f"{(total_m/total)*100:.1f}%",
        },
        {
            "Categoría": "Menores",
            "Cantidad": total_kids,
            "Porcentaje": f"{(total_kids/total)*100:.1f}%",
        },
    ]
)

# Tabla 2: Evolución Temporal
df_evolucion = (
    df.groupby([col_year, col_mes])[col_total].sum().reset_index()
)

# Tabla 3: Top Rutas Migratorias
df_rutas = (
    df.groupby([col_origen, col_destino])[col_total]
    .sum()
    .reset_index()
    .sort_values(by=col_total, ascending=False)
    .head(5)
)

# Tabla 4: Top Destinos con Menores
df_destinos_menores = (
    df.groupby(col_destino)["total_kids"]
    .sum()
    .reset_index()
    .sort_values(by="total_kids", ascending=False)
    .head(5)
)

# Tabla 5: Medios más frecuentes

df_transport= (
    df.groupby(col_transport)[col_total]
    .sum()
    .reset_index()
    .sort_values(by=col_total, ascending=False)
)

df_transport["porcentaje"] = (
    df_transport[col_total] / df_transport[col_total].sum() * 100
).round(2)

# -------------------------------------------------------------
# EXPORTACIÓN A HOJA DE EXCEL
# -------------------------------------------------------------
ruta_salida = Path("/Users/keni/Desktop/results/resultados_extraidos.xlsx")

with pd.ExcelWriter(ruta_salida, engine="openpyxl") as writer:
    df_perfil.to_excel(writer, sheet_name="Perfil Demográfico", index=False)
    df_evolucion.to_excel(writer, sheet_name="Evolución Temporal", index=False)
    df_rutas.to_excel(writer, sheet_name="Rutas", index=False)
    df_destinos_menores.to_excel(
        writer, sheet_name="Destinos Menores", index=False
    )
    df_transport.to_excel(writer, sheet_name="Medios de Transporte", index=False)

print(
    f"¡Archivo generado con éxito! Puedes abrirlo en: {ruta_salida}"
)