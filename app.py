import pandas as pd
import streamlit as st

# Leer el archivo Excel
file_path = "C:\\Users\\AndrésFelipeGiraldoV\\OneDrive - Perceptio S.A.S\\Clientes\\Doc's_BANCO\\Python\\App respuestas examen banco\\Data\\preguntas.xlsx"
df = pd.read_excel(file_path)

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
