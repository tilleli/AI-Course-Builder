
# 📚 Tilla Document Builder

Une application web conçue pour résoudre un vrai problème du quotidien : **la création de documents structurés et esthétiques à partir de notes manuscrites**, le tout en un temps record grâce à l'Intelligence Artificielle.

## 💡 Le vrai problème

Créer un document propre (cours, fiche, guide...) demande énormément de temps :

1. On écrit nos idées à la main sur des feuilles.
2. On doit tout retaper sur ordinateur.
3. On doit passer des heures à faire de la mise en page (Word, Canva...) pour que ce soit joli.
4. On doit refaire ce travail si on veut une version imprimable (PDF) et une version web (HTML).

**Tilla Document Builder** automatise tout ce processus. Vous prenez vos notes en photo, l'IA fait le reste.

## ✨ Fonctionnalités

- **Lecture multi-images** : Importez 6 à 7 photos de vos notes manuscrites. L'IA analyse les images, remet les pages dans l'ordre (grâce aux numéros de page cerclés) et extrait le texte avec précision.
- **Style 100 % personnalisable** : L'application ne se contente pas de générer du texte. Elle applique un modèle de style (couleurs, polices, encadrés) que **vous avez défini vous-même**.
- **Double export** :
  - **HTML** : Version web interactive (idéale pour partager en ligne ou ajouter des corrections cachées).
  - **PDF** : Version imprimable optimisée (marges compressées, prête à être imprimée).

## 🚀 Une polyvalence infinie (exemples d'utilisation)

Bien que l'application ait été créée au départ pour des cours, son fonctionnement (Photos de notes + Style personnalisé = PDF/HTML) est **universel**. Le modèle de style peut être modifié pour s'adapter à n'importe quel projet.

Voici quelques exemples de ce que vous pouvez créer :

- **📚 Fiches de révision** : Prenez vos notes de cours en photo, appliquez un style coloré pour les surlignages et les définitions importantes.
- **🛠️ Guides d'utilisation** : Photographiez vos schémas ou notes techniques, appliquez un style sobre et professionnel avec des encadrés pour les avertissements.
- **🍲 Recueils de recettes** : Prenez en photo vos recettes de famille manuscrites, appliquez un style chaleureux avec des polices manuscrites, et générez un PDF pour la cuisine.
- **📝 Comptes-rendus de réunion** : Photographiez vos notes prises rapidement, appliquez un style corporate (bleu/gris) pour générer un PDF propre à envoyer à vos collègues.
- **📖 Manuels ou eBooks** : Rédigez des chapitres sur papier, prenez-les en photo, et laissez l'IA générer un format HTML prêt à être publié sur le web.

## 🛠️ Prérequis

- **Python 3.10+**
- **Une clé API OpenRouter** (Gratuite). Vous pouvez en créer une sur [OpenRouter](https://openrouter.ai/).

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/tilleli/AI-Course-Builder.git
cd AI-Course-Builder
```

### 2. Installer les dépendances

*Si vous utilisez `uv` (recommandé) :*

```bash
uv pip install -r requirements.txt
```

*Sinon, avec `pip` :*

```bash
pip install streamlit openai python-dotenv weasyprint pymupdf
```

### 3. Configurer la clé API

Créez un fichier `.env` à la racine du projet et ajoutez-y votre clé :

```env
OPENROUTER_API_KEY=votre_cle_api_ici
```

### 4. Lancer l'application

```bash
streamlit run app.py
```

## 📂 Structure du projet

- `app.py` : Le cœur de l'application (interface Streamlit et logique IA).
- `templates/modele_tilla.html` : Le fichier modèle (HTML/CSS) qui contient le design du document. **Modifiez ce fichier pour changer de style !**
- `logo.png` : L'icône de l'application.
- `lancer_app.sh` : Script utilitaire pour lancer l'application facilement sur Linux.

## 👩‍🏫 Auteur

**Tilla** – Passionnée de transmission et de pédagogie.

*"Petit pas, grands progrès."*
