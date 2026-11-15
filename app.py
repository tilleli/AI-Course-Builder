import streamlit as st
import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

# Charger la clé
load_dotenv()

def lire_image_avec_ia(image_bytes):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )
    
    # Encoder l'image en base64
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    # Demander à l'IA de lire
    response = client.chat.completions.create(
        model="nvidia/nemotron-3.5-super-vl:free",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Transcris tout le texte que tu vois sur cette image. Sois précis."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                ]
            }
        ]
    )
    return response.choices[0].message.content


# --- Interface Streamlit ---
st.set_page_config(page_title="AI Course Builder", page_icon="📚")
st.title("📚 AI Course Builder")
st.write("Transformez vos documents en un cours complet.")

st.subheader("Importer vos documents")

photos = st.file_uploader(
    "Ajouter vos photos de cours",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

pdf = st.file_uploader(
    "Ajouter votre document PDF",
    type=["pdf"]
)

if st.button("Générer mon cours"):
    if not photos and not pdf:
        st.warning("Ajoute au moins un fichier.")
    else:
        with st.spinner("L'IA lit vos documents... (cela peut prendre 30 secondes)"):
            if photos:
                image_bytes = photos[0].read()
                texte_extrait = lire_image_avec_ia(image_bytes)
                st.success("Texte extrait par l'IA :")
                # --- MEMOIRE CACHE ---
                # On range le texte dans la boîte "texte_cours" pour s'en souvenir plus tard
                st.session_state.texte_cours = texte_extrait