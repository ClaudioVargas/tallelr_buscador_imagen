import os
import requests
from dotenv import load_dotenv
import streamlit as st

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Reemplaza con tu Access Key de Unsplash Developers
ACCESS_KEY = os.getenv("ACCESS_KEY")
BASE_URL = "https://api.unsplash.com/search/photos"

def buscar_imagenes(query, cantidad=5):
    """
    Busca imágenes en Unsplash según el término ingresado.
    :param query: Texto de búsqueda (ej: 'naturaleza', 'tecnología')
    :param cantidad: Número de resultados a mostrar
    :return: Lista de diccionarios con info de imágenes
    """
    params = {
        "query": query,
        "per_page": cantidad,
        "client_id": ACCESS_KEY
    }
    # response = requests.get(BASE_URL, params=params)
    response = requests.get(f"{BASE_URL}?client_id={ACCESS_KEY}&query={query}&per_page={cantidad}")

    if response.status_code == 200:
        data = response.json()
        resultados = []
        for foto in data["results"]:
            resultados.append({
                "url": foto["urls"]["regular"],
                "autor": foto["user"]["name"],
                "perfil": foto["user"]["links"]["html"]
            })
        return resultados
    else:
        st.error(f"Error en la búsqueda: {response.status_code}")
        return []

def main():
    st.title("📸 Buscador de Imágenes para Redes Sociales")
    st.write("Aplicación integrada con la API de Unsplash")

    tema = st.text_input("Ingrese el tema de la imagen:", "")
    cantidad = st.slider("Cantidad de imágenes a mostrar:", 1, 15, 5)

    if st.button("Buscar"):
        if tema.strip() == "":
            st.warning("Por favor ingrese un tema de búsqueda.")
        else:
            resultados = buscar_imagenes(tema, cantidad)
            if resultados:
                st.subheader("Resultados encontrados:")
                for idx, foto in enumerate(resultados, start=1):
                    st.image(foto["url"], caption=f"{idx}. Autor: {foto['autor']}")
                    st.markdown(f"[Perfil del autor]({foto['perfil']})")
            else:
                st.info("No se encontraron imágenes.")

if __name__ == "__main__":
    main()
