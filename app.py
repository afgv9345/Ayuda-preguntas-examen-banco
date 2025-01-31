import pandas as pd
import streamlit as st

# Leer el archivo Excel desde GitHub
file_url = "https://github.com/afgv9345/Ayuda-preguntas-examen-banco/blob/main/preguntas.xlsx"  # Reemplaza con tu URL cruda
df = pd.read_excel(file_url)

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
