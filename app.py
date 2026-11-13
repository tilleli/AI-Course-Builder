import os
from openai import OpenAI
from dotenv import load_dotenv

# Charger la clé OpenRouter depuis le fichier .env
load_dotenv()
cle = os.getenv("OPENROUTER_API_KEY")
print("Clé lue :", repr(cle[:12]) if cle else None, "| longueur :", len(cle) if cle else 0)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Test de connexion
try:
    response = client.chat.completions.create(
        model="inclusionai/ling-3.2-flash:free",
        messages=[
            {
                "role": "user",
                "content": "Dis juste 'Bonjour Tilla, la connexion avec OpenRouter fonctionne !'"
            }
        ],
    )
    print(response.choices[0].message.content)
except Exception as e:
    print("Erreur :", e)
import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="AI Course Builder",
    page_icon="📚",
    layout="centered"
)

# Titre de l'application
st.title("📚 AI Course Builder")

st.write("Transformez vos documents en un cours complet.")

# Importation des documents
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

image = st.file_uploader(
    "Ajouter une image complémentaire",
    type=["jpg", "jpeg", "png"]
)

# Bouton de génération
if st.button("Générer mon cours"):
    st.info("La génération du cours sera ajoutée à la prochaine étape.")
