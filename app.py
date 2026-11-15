import streamlit as st
import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

# Charger la clé
load_dotenv()

# --- FONCTION 1 : LIRE L'IMAGE ---
def lire_image_avec_ia(liste_photos):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )
    
    # On prépare la liste des contenus à envoyer
    contenu = [
        {"type": "text", "text": "Voici les photos de mon cours. Transcris TOUT le texte de ces images, dans l'ordre exact des pages. Ne saute aucun mot. Sépare chaque page par '--- Page X ---'."}
    ]
    
    # On ajoute chaque image à la liste
    for photo in liste_photos:
        image_bytes = photo.read()  # <--- C'est ici qu'on lit le fichier
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        contenu.append({
            "type": "image_url", 
            "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
        })
    
    # On envoie tout d'un coup
    response = client.chat.completions.create(
        model="nvidia/nemotron-3.5-super-vl:free",
        messages=[
            {
                "role": "user",
                "content": contenu
            }
        ]
    )
    return response.choices[0].message.content


# --- FONCTION 2 : APPLIQUER LE STYLE TILLA ---
# (C'est ici que tu mets le code que tu viens de me montrer)
def generer_style_tilla(texte_extrait):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )
    
    with open("templates/modele_tilla.html", "r", encoding="utf-8") as f:
        modele_html = f.read()
    
    consigne = f"""
    Tu es un professeur de français. Voici le texte brut d'un cours extrait d'une photo :
    
    {texte_extrait}
    
    Voici le code HTML d'un cours que j'ai fait. Tu dois ABSOLUMENT garder exactement le même style (les couleurs, les polices, les cadres, etc.).
    
    {modele_html}
    
    Ta mission : Remplis ce code HTML avec le contenu du texte brut. 
    Remplace le texte entre les balises par le nouveau cours. 
    Garde les classes CSS, les couleurs, et la structure. 
    Renvoie UNIQUEMENT le code HTML final, sans aucune explication autour.
    """
    
    response = client.chat.completions.create(
        model="nvidia/nemotron-3.5-super-vl:free",
        messages=[
            {"role": "user", "content": consigne}
        ],
        temperature=0.2 
    )
    
    return response.choices[0].message.content


# --- INTERFACE STREAMLIT ---
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
        with st.spinner("L'IA lit vos documents..."):
            if photos:
                # On envoie la liste complète des photos à la fonction
                texte_extrait = lire_image_avec_ia(photos)
                
                st.session_state.texte_cours = texte_extrait
                st.success(f"{len(photos)} pages lues avec succès !")
        
        # --- ÉTAPE 2 : LE STYLE TILLA ---
        with st.spinner("Génération du cours avec le Style Tilla... (environ 30 secondes)"):
            html_final = generer_style_tilla(st.session_state.texte_cours)
            
            st.subheader("Aperçu de ton cours :")
            st.components.v1.html(html_final, height=800, scrolling=True)
            # --- BOUTON DE TÉLÉCHARGEMENT ---
            st.download_button(
                label="📥 Télécharger le cours (HTML)",
                data=html_final,
                file_name="cours_style_tilla.html",
                mime="text/html"
)