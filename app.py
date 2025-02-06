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

# Estilo CSS personalizado para los botones
st.markdown(
    """
    <style>
    div.stButton > button:first-child {
        background-color: #007ACC;
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 5px; /* Espacio entre el icono y el texto */
    }
    div.stButton > button:first-child:hover {
        background-color: #005EA2; /* Un tono más oscuro al pasar el mouse */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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

    # Diccionario de colores para los temas
    tema_colores = {
        "Tema 1": "blue",
        "Tema 2": "green",
        "Tema 3": "orange",
        # Agrega más temas y colores aquí
    }

    if st.button("Buscar \U0001F50D", key="search_button"):  # Icono de lupa
        if query:
            results = df[df['Pregunta'].str.contains(query, case=False, na=False, regex=False)]

            if not results.empty:
                st.session_state.results = []  # Store results in session state
                for index, response in results.iterrows():
                    tema = response['Tema']
                    respuesta = response['Respuesta']

                    # Obtener el color del tema o usar un color predeterminado
                    color = tema_colores.get(tema, "black")  # "black" como color por defecto

                    # Crear el HTML para el texto coloreado
                    tema_html = f"<p style='color:{color}; font-weight: bold;'>Tema: {tema}</p>"
                    respuesta_html = f"<p style='color:{color};'>Respuesta: {respuesta}</p>"

                    # Agrega los resultados al estado de la sesión para que persistan
                    st.session_state.results.append({"Tema": tema_html, "Respuesta": respuesta_html})

                # Mostrar los resultados
                for result in st.session_state.results:
                    st.markdown(result['Tema'], unsafe_allow_html=True)
                    st.markdown(result['Respuesta'], unsafe_allow_html=True)
            else:
                st.warning("No se encontraron resultados para la pregunta ingresada.", icon="⚠️")
        else:
            st.error("Por favor ingrese una pregunta.", icon="🚨")

    # Botón para nueva pregunta (limpia campo de búsqueda y resultados)
    if st.button("Nueva Pregunta \U0001F5D1", key="new_question_button"):  # Icono de borrador
        st.session_state.query = ""  # Limpiar la entrada de la pregunta

        if 'results' in st.session_state:
            del st.session_state.results  # Limpiar los resultados

    # Botón para cerrar sesión
    if st.button("Cerrar sesión \U0001F512", key="logout_button"):  # Icono de candado
        st.session_state.authenticated = False  # Restablecer el estado de autenticación
        st.success("Has cerrado sesión exitosamente.", icon="🚪")
