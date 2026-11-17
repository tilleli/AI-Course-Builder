import streamlit as st
import os
import base64
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
        messages=[
            {
                "role": "user",
                "content": contenu
            }
        ]
    )
    return response.choices[0].message.content


# --- FONCTION 2 : APPLIQUER LE STYLE TILLA ---
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
    
    Voici le code HTML de mon cours (le Style Tilla). Tu dois ABSOLUMENT garder exactement le même style, les mêmes classes CSS, les mêmes couleurs et la même structure.
    
    {modele_html}
    
    Ta mission : Remplis ce code HTML avec le contenu du texte brut. 
    Utilise UNIQUEMENT les balises et les classes CSS présentes dans mon modèle (comme .sec, .rule, .ex, .warn, .exh, .pp, etc.). 
    Ne rajoute pas de texte inutile. Sois concis, fais des phrases courtes. Le cours final doit absolument tenir sur un maximum de 4 pages.
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

# On initialise la mémoire pour le PDF
if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None

# --- BOUTON PRINCIPAL ---
if st.button("Générer mon cours"):
    if not photos and not pdf:
        st.warning("Ajoute au moins un fichier.")
    else:
        with st.spinner("L'IA lit vos documents..."):
            if photos:
                texte_extrait = lire_image_avec_ia(photos)
                st.session_state.texte_cours = texte_extrait
                st.success(f"{len(photos)} pages lues avec succès !")
        
        with st.spinner("Génération du cours avec le Style Tilla... (environ 30 secondes)"):
            html_final = generer_style_tilla(st.session_state.texte_cours)
            st.session_state.html_final = html_final
            st.session_state.pdf_bytes = None # On réinitialise le PDF

# --- AFFICHAGE DU COURS ET DES TÉLÉCHARGEMENTS (Hors du bouton) ---
if "html_final" in st.session_state:
    st.subheader("Aperçu de ton cours :")
    st.components.v1.html(st.session_state.html_final, height=800, scrolling=True)
    
    # Bouton HTML
    st.download_button(
        label="📥 Télécharger le cours (HTML)",
        data=st.session_state.html_final,
        file_name="cours_style_tilla.html",
        mime="text/html"
    )
    
    # Bouton PDF
    if st.button("📄 Générer le PDF (Style Tilla)"):
        with st.spinner("Création du PDF..."):
            try:
                # On cache juste la barre de nav et les corrections pour le PDF
                css_pdf = """
                <style>
                    /* 1. Marges de la page au minimum */
                    @page { 
                        size: A4; 
                        margin: 8mm 10mm !important; 
                    }
                    
                    /* 2. On cache la navigation et les corrections */
                    .nav, details { display: none !important; } 
                    
                    /* 3. ON DÉTRUIT TOUS LES SAUTS DE PAGE FORCÉS */
                    .pb, .page-break, br[style*="page-break"] { 
                        display: none !important; 
                    }
                    * { 
                        page-break-before: auto !important; 
                        page-break-after: auto !important; 
                        page-break-inside: auto !important; 
                    }
                    
                    /* 4. On écrase les espaces de la bannière bleue */
                    .hero { padding: 10px 0 !important; margin-bottom: 5px !important; }
                    .hero h1 { font-size: 22px !important; margin: 0 !important; }
                    .hero p { font-size: 12px !important; margin: 2px 0 !important; }
                    .badge { width: 40px !important; height: 40px !important; line-height: 40px !important; font-size: 16px !important; }
                    
                    /* 5. On tasse le texte */
                    body { font-size: 12px !important; line-height: 1.25 !important; }
                    p { margin: 3px 0 !important; }
                    h2 { font-size: 16px !important; margin: 8px 0 4px !important; padding-bottom: 2px !important; }
                    
                    /* 6. On réduit les sections et les encadrés */
                    .sec { margin: 8px 0 0 0 !important; }
                    .rule, .ex, .warn, .ret { 
                        padding: 4px 8px !important; 
                        margin: 4px 0 !important; 
                    }
                    .exh { 
                        margin: 6px 0 3px !important; 
                        padding: 3px 6px !important; 
                        font-size: 14px !important; 
                    }
                    
                    /* 7. On tasse les tableaux */
                    table { margin: 4px 0 !important; }
                    table.t td, table.t th { padding: 3px !important; font-size: 11px !important; }
                </style>
                """
                
                html_optimise = st.session_state.html_final.replace("</head>", css_pdf + "</head>")
                
                # On génère le PDF
                pdf_doc = HTML(string=html_optimise).render()
                nb_pages = len(pdf_doc.pages)
                
                if nb_pages > 4:
                    st.warning(f"⚠️ Attention : Le PDF fait {nb_pages} pages (max 4). L'IA a peut-être été trop bavarde.")
                else:
                    st.success(f"✅ PDF généré ({nb_pages} pages) !")
                
                st.session_state.pdf_bytes = pdf_doc.write_pdf()
                
            except Exception as e:
                st.error(f"Erreur PDF : {e}")
                
    # Bouton de téléchargement du PDF
    if st.session_state.pdf_bytes:
        st.download_button(
            label="Télécharger le PDF",
            data=st.session_state.pdf_bytes,
            file_name="cours_style_tilla.pdf",
            mime="application/pdf"
        )