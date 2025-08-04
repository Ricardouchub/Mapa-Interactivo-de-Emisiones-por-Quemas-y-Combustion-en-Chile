import streamlit as st
import pandas as pd
import plotly.express as px
import os
import json

# --- Configuración de la página ---
st.set_page_config(page_title="Atlas de Emisiones - Chile", page_icon="💨", layout="wide")

# --- Carga de Datos Optimizada ---
@st.cache_data
def cargar_datos():
    ruta_archivo = os.path.join('data', 'emisiones_consolidadas_limpias.parquet')
    if not os.path.exists(ruta_archivo):
        st.error(f"Error: No se encontró el archivo de datos en la ruta: {ruta_archivo}")
        return None
    columnas_necesarias = ['ano', 'region', 'comuna', 'id_comuna', 'tipo_fuente', 'contaminantes', 'cantidad_toneladas']
    tipos_de_datos = {'region': 'category', 'comuna': 'category', 'tipo_fuente': 'category', 'contaminantes': 'category', 'ano': 'int16', 'id_comuna': 'int32', 'cantidad_toneladas': 'float32'}
    try:
        df = pd.read_parquet(ruta_archivo, columns=columnas_necesarias)
        df = df.astype(tipos_de_datos)
        return df
    except Exception as e:
        st.error(f"Error al leer u optimizar el archivo Parquet: {e}")
        return None

@st.cache_data
def cargar_geojson():
    ruta_geojson = os.path.join('data', 'comunas.geojson')
    try:
        with open(ruta_geojson, 'r', encoding='utf-8') as f:
            geojson = json.load(f)
        CLAVE_CODIGO = 'cod_comuna'
        CLAVE_NOMBRE = 'Comuna'
        comuna_names = {str(feature['properties'][CLAVE_CODIGO]): feature['properties'][CLAVE_NOMBRE] for feature in geojson['features']}
        return geojson, comuna_names, CLAVE_CODIGO
    except Exception as e:
        st.error(f"Error al cargar o procesar el archivo GeoJSON local: {e}")
        return None, None, None

df = cargar_datos()
geojson_chile, comuna_nombres, CLAVE_GEOJSON_ID = cargar_geojson()

if df is None or geojson_chile is None:
    st.warning("No se pudieron cargar los datos necesarios para la aplicación.")
    st.stop()

# --- Título y Filtros ---
st.title('Atlas Interactivo de Emisiones de fuentes difusas en Chile (2019-2023)')
st.markdown("""
> Este panel interactivo presenta un análisis de las emisiones de fuentes difusas en Chile para el período 2019-2023. 
>
> Los datos revelan que la **combustión de leña residencial** es una de las fuentes de emisión más constantes y extendidas, con una alta concentración en las regiones del **centro-sur del país**.
> Destaca un **evento anómalo en el año 2023**, donde las emisiones por **incendios forestales** se dispararon a niveles históricos, reflejando la severidad de la temporada de incendios de ese verano y convirtiéndose en la principal fuente de contaminación de todo el período analizado.
>
> Te invitamos a utilizar los filtros para explorar estos patrones en detalle.
>
>**Fuente de datos:** **[Registro de Emisiones y Transferencia de Contaminantes (RETC)](https://datosretc.mma.gob.cl/dataset/emisiones-al-aire)**
""")
st.sidebar.header('Filtros de Búsqueda')
selected_years = st.sidebar.slider('Selecciona un rango de años:', min_value=int(df['ano'].min()), max_value=int(df['ano'].max()), value=(int(df['ano'].min()), int(df['ano'].max())))
regiones_disponibles = sorted(df['region'].unique())
opciones_region = ['Todas'] + regiones_disponibles
selected_regions = st.sidebar.multiselect('Regiones:', options=opciones_region, default=['Todas'])
fuentes_disponibles = sorted(df['tipo_fuente'].unique())
selected_source = st.sidebar.selectbox('Tipo de fuente:', options=['Todas'] + fuentes_disponibles)
contaminantes_disponibles = sorted(df['contaminantes'].unique())
selected_pollutant = st.sidebar.selectbox('Contaminante:', options=['Todos'] + contaminantes_disponibles)

# --- Lógica de Filtrado ---
df_filtrado = df[(df['ano'] >= selected_years[0]) & (df['ano'] <= selected_years[1])]
if selected_regions:
    if 'Todas' not in selected_regions:
        df_filtrado = df_filtrado[df_filtrado['region'].isin(selected_regions)]
if selected_source != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['tipo_fuente'] == selected_source]
if selected_pollutant != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['contaminantes'] == selected_pollutant]

# --- Pestañas ---
tab1, tab2, tab3 = st.tabs(["Mapa de Emisiones", "Análisis por Zona", "Tendencias Anuales"])

with tab1:
    st.header("Mapa de Emisiones por Comuna")
    if not df_filtrado.empty:
        emisiones_mapa = df_filtrado.groupby('id_comuna')['cantidad_toneladas'].sum().reset_index()
        emisiones_mapa['id_comuna'] = emisiones_mapa['id_comuna'].astype(str)
        emisiones_mapa['nombre_comuna'] = emisiones_mapa['id_comuna'].map(comuna_nombres)

        # --- CAMBIO: Se usa la nueva función px.choropleth ---
        # Nota: He quitado 'mapbox_style' ya que la nueva función usa un estilo por defecto.
        fig_map = px.choropleth(
            emisiones_mapa,
            geojson=geojson_chile,
            locations='id_comuna',
            featureidkey=f"properties.{CLAVE_GEOJSON_ID}", 
            color='cantidad_toneladas',
            color_continuous_scale="YlOrRd",
            scope="world", # Se define el alcance del mapa
            labels={'cantidad_toneladas': 'Toneladas Emitidas', 'nombre_comuna': 'Comuna'},
            hover_name='nombre_comuna',
            hover_data={'cantidad_toneladas': ':.2f', 'id_comuna': False}
        )
        # Se ajusta la vista del mapa para centrarse en Chile
        fig_map.update_geos(
            fitbounds="locations", 
            visible=False
        )
        fig_map.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            height=800
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("No hay datos para mostrar con los filtros seleccionados.")

with tab2:
    st.header("Resumen y Desglose por Zona Geográfica")
    if not df_filtrado.empty:
        total_toneladas = df_filtrado['cantidad_toneladas'].sum()
        num_registros = len(df_filtrado)
        col1, col2 = st.columns(2)
        col1.metric("Total de Emisiones (Ton)", f"{total_toneladas:,.0f}")
        col2.metric("Nº de Registros", f"{num_registros:,.0f}")
        st.subheader("Emisiones por Región")
        emisiones_region = df_filtrado.groupby('region')['cantidad_toneladas'].sum().sort_values(ascending=False)
        fig_bar_region = px.bar(emisiones_region, y=emisiones_region.index, x='cantidad_toneladas', orientation='h', labels={'y': 'Región'})
        fig_bar_region.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar_region, use_container_width=True)
        st.subheader("Top 15 Comunas")
        emisiones_comuna_top = df_filtrado.groupby('comuna')['cantidad_toneladas'].sum().nlargest(15)
        fig_bar_comuna = px.bar(emisiones_comuna_top, y=emisiones_comuna_top.index, x='cantidad_toneladas', orientation='h', labels={'y': 'Comuna'})
        fig_bar_comuna.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar_comuna, use_container_width=True)
    else:
        st.warning("No hay datos para mostrar con los filtros seleccionados.")
with tab3:
    st.header("Evolución Anual de Emisiones por Fuente")
    if not df_filtrado.empty:
        emisiones_anual_fuente = df_filtrado.groupby(['ano', 'tipo_fuente'])['cantidad_toneladas'].sum().reset_index()
        fig_line_anual = px.line(emisiones_anual_fuente,x='ano',y='cantidad_toneladas',color='tipo_fuente',title='Evolución de Emisiones por Fuente',markers=True)
        fig_line_anual.update_xaxes(dtick=1)
        st.plotly_chart(fig_line_anual, use_container_width=True)
    else:
        st.warning("No hay datos para mostrar con los filtros seleccionados.")

# --- Pie de Página y CSS (sin cambios) ---
st.markdown("---")
st.markdown("""<div style="text-align: center;"><p>Autor: Ricardo Urdaneta</p><a href="https://github.com/Ricardouchub" target="_blank"><button class="footer-btn">Github</button></a><a href="https://www.linkedin.com/in/ricardourdanetacastro" target="_blank"><button class="footer-btn">Linkedin</button></a></div>""", unsafe_allow_html=True)
st.markdown("""<style>.stApp {background-color: #ffffff;}.st-emotion-cache-16txtl3 {padding: 2rem 1rem 1rem;}.st-emotion-cache-z5fcl4 {padding-top: 3rem;}h1 {color: #1A5276;font-family: 'sans-serif';}h2, h3, .st-emotion-cache-l99vhe {color: #1F618D;font-family: 'sans-serif';}.st-emotion-cache-1y4p8pa {max-width: 95%;}.footer-btn {background-color: transparent;color: #1F618D;padding: 8px 20px;border-radius: 8px;border: 2px solid #1F618D;text-align: center;text-decoration: none;display: inline-block;font-size: 16px;margin: 4px 2px;cursor: pointer;transition-duration: 0.4s;}.footer-btn:hover {background-color: #1F618D;color: white;}</style>""", unsafe_allow_html=True)
