import pandas as pd
import streamlit as st
import requests
from io import BytesIO
import bcrypt
import yaml

# Función para cargar las credenciales desde un archivo YAML
def load_credentials(file_path):
    with open(file_path) as file:
        return yaml.safe_load(file)

# Función para verificar la contraseña hasheada
def check_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Cargar las credenciales desde el archivo YAML
credentials = load_credentials('credentials.yml')  # Asegúrate de que este archivo esté en el mismo directorio

# Inicializar el estado de sesión si no existe
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Autenticación del usuario
st.title("Autenticación")
username = st.text_input("Usuario", key="username")
password = st.text_input("Contraseña", type="password", key="password")

if st.button("Iniciar sesión", key="login_button"):
    if username in credentials['credentials']['usernames']:
        hashed_password = credentials['credentials']['usernames'][username]['password']
        if check_password(password, hashed_password):
            st.success(f'Bienvenido, {username}!')
            st.session_state.authenticated = True  # Establecer autenticación como verdadera
        else:
            st.error("Contraseña incorrecta.")
            st.session_state.authenticated = False
    else:
        st.error("Usuario no encontrado.")
        st.session_state.authenticated = False

# Si el usuario está autenticado, continuar con la aplicación
if st.session_state.authenticated:
    # URL del archivo Excel en GitHub (asegúrate de usar la versión RAW)
    file_url = "https://raw.githubusercontent.com/afgv9345/Ayuda-preguntas-examen-banco/main/preguntas.xlsx"

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
    query = st.text_input("Ingrese parte de la pregunta:", key="question_input")

    if st.button("Buscar", key="search_button"):
        if query:
            results = df[df['Pregunta'].str.contains(query, case=False, na=False, regex=False)]  # Cambiado a regex=False

            if not results.empty:
                st.session_state.results = []  # Store results in session state
                for index, response in results.iterrows():
                    st.session_state.results.append({"Tema": response['Tema'], "Respuesta": response['Respuesta']})  # Append results

                # Display Results
                for result in st.session_state.results:
                    st.success(f"Tema: {result['Tema']}", icon="📚")
                    st.success(f"Respuesta: {result['Respuesta']}", icon="✅")
            else:
                st.warning("No se encontraron resultados para la pregunta ingresada.", icon="⚠️")
        else:
            st.error("Por favor ingrese una pregunta.", icon="🚨")

    # Botón para limpiar la pregunta y los resultados
    if st.button("Limpiar", key="clear_button"):
        st.session_state.query = ""  # Limpiar la entrada de la pregunta
        if 'results' in st.session_state:
            del st.session_state.results  # Clear the results

    # Botón para cerrar sesión
    if st.button("Cerrar sesión", key="logout_button"):
        st.session_state.authenticated = False  # Restablecer el estado de autenticación
        st.success("Has cerrado sesión exitosamente.", icon="🚪")
