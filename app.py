
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
