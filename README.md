# Atlas Interactivo de Emisiones de fuentes difusas en Chile (2019-2023)

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.2-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.22-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

Este repositorio contiene el código y los datos para un dashboard interactivo que analiza las emisiones de fuentes difusas en Chile.

---

###  [Ver Proyecto en Vivo](https://atlas-interactivo-de-emisiones-en-chile-2019-2023.streamlit.app/) 

<img width="757" height="375" alt="image" src="https://github.com/user-attachments/assets/6eedb848-de04-48fc-92cf-31440ea05e75" />



---

## Contexto

Este proyecto realiza un análisis de datos de extremo a extremo, desde la recopilación y limpieza de datos públicos hasta el despliegue de una aplicación web. El objetivo es visualizar y analizar las emisiones al aire provenientes de fuentes difusas (quemas agrícolas, incendios forestales, combustión de leña, etc.) en Chile, para el período 2019-2023.

La fuente de datos es el **Registro de Emisiones y Transferencia de Contaminantes (RETC)** del Ministerio del Medio Ambiente de Chile.

---

## Desarrollo del Proyecto

El flujo de trabajo siguió las etapas estándar de un proyecto de ciencia de datos:

1.  **Recopilación y Limpieza de Datos:**
    * Se consolidaron 5 datasets anuales (2019-2023) en un único DataFrame.
    * Se realizaron tareas de limpieza como la estandarización de nombres de columnas y regiones.
    * Se corrigieron los tipos de datos para permitir el análisis numérico, manejando inconsistencias como el uso de comas en lugar de puntos decimales.

2.  **Análisis Exploratorio de Datos (EDA):**
    * Se identificaron las principales fuentes de emisión y los contaminantes más relevantes a nivel nacional.
    * Se analizaron las tendencias temporales, descubriendo un **pico anómalo de emisiones en 2023**, el cual se correlacionó directamente con los mega-incendios forestales ocurridos ese año.
    * Se determinaron las regiones y comunas con mayores niveles de emisión.

3.  **Visualización y Desarrollo del Dashboard:**
    * Se utilizó **Streamlit** para construir la aplicación web interactiva.
    * Se implementó un mapa coroplético de Chile usando **Plotly Express** y un archivo GeoJSON para visualizar la distribución geográfica de las emisiones por comuna.
    * Se añadieron filtros dinámicos por año, región, fuente y tipo de contaminante.
    * El contenido se organizó en pestañas para una navegación clara e intuitiva.

4.  **Despliegue:**
    * El proyecto se configuró para su despliegue, incluyendo la creación de un archivo `requirements.txt` para gestionar las dependencias.
    * La aplicación final fue desplegada en **Streamlit Community Cloud**, haciéndola accesible a través de un enlace público.

---

## Herramientas

* **Lenguaje:** Python
* **Análisis de Datos:** Pandas
* **Visualización Interactiva:** Plotly Express
* **Aplicación Web:** Streamlit
* **Manejo de Datos Geoespaciales:** GeoJSON, JSON
* **Almacenamiento Eficiente:** PyArrow (formato Parquet)

---

## Cómo ejecutar este proyecto localmente

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/Ricardouchub/Atlas-Interactivo-de-Emisiones-por-Quemas-y-Combustion-en-Chile.git](https://github.com/Ricardouchub/Atlas-Interactivo-de-Emisiones-por-Quemas-y-Combustion-en-Chile.git)
    cd Atlas-Interactivo-de-Emisiones-por-Quemas-y-Combustion-en-Chile
    ```

2.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ejecutar la aplicación:**
    ```bash
    streamlit run app.py
    ```

## Estructura del Repositorio

* `analisis_exploratorio.ipynb` Notebook con la limpieza y el EDA
* `app.py` El script de la aplicación web Streamlit
* `requirements.txt` Las librerías de Python necesarias para ejecutar el proyecto
* `/data`: Carpeta que contiene los archivos de datos:
        `2019.csv 2020.csv 2021.csv 2022.csv 2023.csv`
        `comunas.geojson`
        `emisiones_consolidadas_limpias.parquet`

---

## Autor

**Ricardo Urdaneta**

* [GitHub](https://github.com/Ricardouchub)
* [LinkedIn](https://www.linkedin.com/in/ricardourdanetacastro)
