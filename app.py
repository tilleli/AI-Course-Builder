import streamlit as st
import os
import base64
import fitz  # L'outil pour lire les PDF
from openai import OpenAI
from dotenv import load_dotenv
from weasyprint import HTML

# Charger la clé
load_dotenv()

# --- FONCTION 1 : LIRE L'IMAGE ---
def lire_image_avec_ia(liste_photos):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        timeout=180.0,
        max_retries=3
    )
    
    contenu = [
        {"type": "text", "text": "Voici les photos de mon cours. Regarde attentivement en bas à droite de chaque image : il y a un petit numéro de page entouré d'un cercle. Utilise CE numéro pour organiser le texte. Transcris tout le texte de chaque image sans rien sauter, et sépare chaque page par '--- Page [numéro du cercle] ---'. Si un mot est difficile à lire, écris-le entre crochets comme ceci : [mot incertain]."}
    ]
    
    for photo in liste_photos:
        image_bytes = photo.read()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        contenu.append({
            "type": "image_url", 
            "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
        })
    
    response = client.chat.completions.create(
        model="nvidia/nemotron-3.5-super-vl:free",
        messages=[{"role": "user", "content": contenu}]
    )
    return response.choices[0].message.content

# --- FONCTION 2 : LIRE LE PDF ---
def lire_pdf(fichier_pdf):
    texte = ""
    # On ouvre le PDF depuis la mémoire
    with fitz.open(stream=fichier_pdf.read(), filetype="pdf") as doc:
        for page in doc:
            texte += page.get_text()
    return texte

# --- FONCTION 3 : APPLIQUER LE STYLE TILLA (COURS + EXOS) ---
def generer_style_tilla(texte_cours, texte_exercices):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        timeout=180.0,
        max_retries=3
    )
    
    with open("templates/modele_tilla.html", "r", encoding="utf-8") as f:
        modele_html = f.read()
    
    consigne = f"""
    Tu es un professeur de français. Voici deux textes :
    
    1. LE COURS (extrait des photos) :
    {texte_cours}
    
    2. LES EXERCICES (extraits du PDF) :
    {texte_exercices}
    
    Voici le code HTML de mon cours (le Style Tilla). Tu dois ABSOLUMENT garder exactement le même style, les mêmes classes CSS, les mêmes couleurs et la même structure.
    
    {modele_html}
    
    Ta mission : Remplis ce code HTML avec le contenu du cours ET les exercices.
    - Mets le cours dans les sections normales (.sec).
    - Ajoute les exercices à la fin, en utilisant la classe .exh pour les titres des exercices (ex: "Exercice 1"), et .exo pour les listes de questions.
    - IMPORTANT : Tu dois créer les corrections et les mettre dans des balises <details><summary>Voir la correction</summary>...</details>.
    - Utilise UNIQUEMENT les balises et les classes CSS présentes dans mon modèle.
    - Ne rajoute pas de texte inutile. Sois concis. Le cours doit tenir sur un maximum de 4 pages.
    
    Renvoie UNIQUEMENT le code HTML final, sans aucune explication autour.
    """
    
    response = client.chat.completions.create(
        model="nvidia/nemotron-3.5-super-vl:free",
        messages=[{"role": "user", "content": consigne}],
        temperature=0.2 
    )
    return response.choices[0].message.content

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="Cours Facile avec tilla", page_icon="logo.png", layout="wide")

st.markdown("""
<style>
    /* 1. Le fond bleu du PPT */
    .stApp {
        background-color: #2F3C7E; 
    }
    
    /* 2. On force les titres et les labels au-dessus des uploads en blanc */
    h1, h2, h3, h4, h5, h6, label[data-testid="stWidgetLabel"] p {
        color: white !important;
    }
    
    /* 3. On rend la boîte d'upload BLANCHE avec une bordure jaune pointillée */
    div[data-testid="stFileUploaderDropzone"] {
        background-color: #FFFFFF !important;
        border: 2px dashed #F9E795 !important;
        border-radius: 10px !important;
    }
    
    /* 4. Le texte à l'intérieur de la boîte blanche doit être bleu foncé */
    div[data-testid="stFileUploaderDropzone"] span, 
    div[data-testid="stFileUploaderDropzone"] small {
        color: #2F3C7E !important;
    }
    
    /* 5. Le bouton "Upload" à l'intérieur de la boîte prend la couleur corail */
    div[data-testid="stFileUploaderDropzone"] button {
        background-color: #F96167 !important;
        color: white !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGO TILLA ---
st.markdown("""
<div style="display: flex; align-items: center; gap: 15px; margin-bottom: 30px;">
    <svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <style>
          @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@700&amp;display=swap');
        </style>
      </defs>
      <circle cx="24" cy="24" r="22" fill="#F9E795" />
      <text x="24" y="25" font-family="'Fredoka', sans-serif" font-weight="700" font-size="16" fill="#2F3C7E" text-anchor="middle" dominant-baseline="central">
        tilla
      </text>
    </svg>
    <h1 style="margin: 0; color: white; font-family: 'Fredoka', sans-serif; font-size: 32px;">
        AI Course Builder
    </h1>
</div>
""", unsafe_allow_html=True)

# Mémoire
if "html_final" not in st.session_state:
    st.session_state.html_final = None
if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None

# Les zones d'importation
photos = st.file_uploader("Photos du cours", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
pdf_input = st.file_uploader("Document PDF (Exercices)", type=["pdf"])

st.write("") # Un peu d'espace

# --- BOUTON PRINCIPAL ---
if st.button("Générer le cours", type="primary"):
    if not photos and not pdf_input:
        st.error("Veuillez ajouter au moins une photo.")
    else:
        with st.spinner("Lecture des documents..."):
            texte_cours = ""
            texte_exercices = ""
            
            # 1. Lecture des photos
            if photos:
                texte_cours = lire_image_avec_ia(photos)
                
            # 2. Lecture du PDF
            if pdf_input:
                texte_exercices = lire_pdf(pdf_input)
                
            with st.spinner("Génération du Style Tilla..."):
                # 3. Envoi à l'IA
                html_final = generer_style_tilla(texte_cours, texte_exercices)
                st.session_state.html_final = html_final
                
                # 4. Création du PDF
                css_pdf = """
                <style>
                    @page { size: A4; margin: 8mm 10mm !important; }
                    .nav, details { display: none !important; } 
                    .pb, .page-break, br[style*="page-break"] { display: none !important; }
                    * { page-break-before: auto !important; page-break-after: auto !important; page-break-inside: auto !important; }
                    .hero { padding: 10px 0 !important; margin-bottom: 5px !important; }
                    .hero h1 { font-size: 22px !important; margin: 0 !important; }
                    .hero p { font-size: 12px !important; margin: 2px 0 !important; }
                    .badge { width: 40px !important; height: 40px !important; line-height: 40px !important; font-size: 16px !important; }
                    body { font-size: 12px !important; line-height: 1.25 !important; }
                    p { margin: 3px 0 !important; }
                    h2 { font-size: 16px !important; margin: 8px 0 4px !important; padding-bottom: 2px !important; }
                    .sec { margin: 8px 0 0 0 !important; }
                    .rule, .ex, .warn, .ret { padding: 4px 8px !important; margin: 4px 0 !important; }
                    .exh { margin: 6px 0 3px !important; padding: 3px 6px !important; font-size: 14px !important; }
                    table { margin: 4px 0 !important; }
                    table.t td, table.t th { padding: 3px !important; font-size: 11px !important; }
                </style>
                """
                html_optimise = html_final.replace("</head>", css_pdf + "</head>")
                pdf_doc = HTML(string=html_optimise).render()
                st.session_state.pdf_bytes = pdf_doc.write_pdf()

# --- AFFICHAGE CÔTE À CÔTE ---
if st.session_state.html_final and st.session_state.pdf_bytes:
    st.write("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Version HTML")
        st.components.v1.html(st.session_state.html_final, height=600, scrolling=True)
        
        st.download_button(
            label="Télécharger le HTML",
            data=st.session_state.html_final,
            file_name="cours_style_tilla.html",
            mime="text/html",
            use_container_width=True
        )
        
    with col2:
        st.subheader("Version PDF")
        
        base64_pdf = base64.b64encode(st.session_state.pdf_bytes).decode('utf-8')
        pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}#toolbar=0&navpanes=0&scrollbar=0" width="100%" height="600" type="application/pdf" />'
        st.markdown(pdf_display, unsafe_allow_html=True)
        
        st.download_button(
            label="Télécharger le PDF",
            data=st.session_state.pdf_bytes,
            file_name="cours_style_tilla.pdf",
            mime="application/pdf",
            use_container_width=True
        )