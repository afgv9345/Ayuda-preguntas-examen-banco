import pandas as pd
import streamlit as st
import requests  # Para descargar el archivo desde la URL
from io import BytesIO  # Para manejar el archivo en memoria

# URL del archivo Excel en GitHub (asegúrate de usar la versión RAW)
file_url = "https://raw.githubusercontent.com/afgv9345/Ayuda-preguntas-examen-banco/main/preguntas.xlsx"  # Reemplaza con tu URL cruda

# Descargar el archivo Excel desde la URL
try:
    response = requests.get(file_url)
    response.raise_for_status()  # Verifica si hubo algún error en la descarga
    excel_data = BytesIO(response.content)  # Cargar el contenido en memoria
    df = pd.read_excel(excel_data)  # Leer el archivo Excel en un DataFrame
except Exception as e:
    st.error(f"Error al cargar el archivo: {e}")
    st.stop()  # Detener la ejecución si ocurre un error

# Título de la aplicación
st.title("Buscador de Preguntas")

# Campo de entrada para la pregunta
query = st.text_input("Ingrese parte de la pregunta:")

if st.button("Buscar"):
    if query:
        results = df[df['Pregunta'].str.contains(query, case=False, na=False)]
        
        if not results.empty:
            response = results.iloc[0]
            st.success(f"Tema: {response['Tema']}")
            st.success(f"Respuesta: {response['Respuesta']}")
        else:
            st.warning("No se encontraron resultados para la pregunta ingresada.")
    else:
        st.error("Por favor ingrese una pregunta.")
