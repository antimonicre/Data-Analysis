import pandas as pd
import scipy
import matplotlib

df = pd.read_excel("/Users/keni/Desktop/datasets/filtrado.xlsx")

col_total = "Total Number of Individuals migrants"
col_hombres = "Men"
col_mujeres = "Women"
col_ninos = "Boys"
col_ninas = "Girls"
col_mes = "Month"
col_year = "Year"
col_origen = "Departure (admin0)"
col_destino = "[[Destination ] (admin0)"

total = df[col_total].sum()
total_h = df[col_hombres].sum()
total_m = df[col_mujeres].sum()
df["total_kids"] = df[col_ninos] + df[col_ninas]
total_kids = df["total_kids"].sum()


print("==================================================")
print("1. PERFIL DEMOGRÁFICO GENERAL")
print("==================================================")
print(f"Total entradas registradas: {total:,.0f}")
print(f"• Hombres: {total_h:,.0f} ({(total_h/total)*100:.1f}%)")
print(f"• Mujeres: {total_m:,.0f} ({(total_m/total)*100:.1f}%)")
print(
    f"• Menores frente a adultos: {total_kids:,.0f} ({(total_kids/total)*100:.1f}%)\n"
)


# -------------------------------------------------------------
# PREGUNTA 2: EVOLUCIÓN TEMPORAL (Serie del tiempo)
# -------------------------------------------------------------
print("==================================================")
print("2. EVOLUCIÓN DE ENTRADAS POR PERIODO")
print("==================================================")
evolucion = (
    df.groupby([col_year, col_mes])["Total Number of Individuals migrants"]
    .sum()
    .reset_index()
)
print(evolucion.to_string(index=False))
print("\n")


# -------------------------------------------------------------
# PREGUNTA 3: RUTAS Y PAÍSES DE ORIGEN
# -------------------------------------------------------------
print("==================================================")
print("3. RUTAS MIGRATORIAS MÁS FRECUENTADAS")
print("==================================================")
rutas = (
    df.groupby([col_origen, col_destino])["Total Number of Individuals migrants"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)
print(rutas)
print("\n")


# -------------------------------------------------------------
# PREGUNTA 4: GEOGRAFÍA DE VULNERABILIDAD DE MENORES
# -------------------------------------------------------------
print("==================================================")
print("4. TOP 5 DESTINOS CON MAYOR LLEGADA DE MENORES")
print("==================================================")
destinos_menores = (
    df.groupby(col_destino)["total_kids"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)
print(destinos_menores)