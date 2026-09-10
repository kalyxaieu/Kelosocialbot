import os
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from groq import Groq
from mastodon import Mastodon
from dotenv import load_dotenv

# Charge les variables d'environnement
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TS_EMAIL = os.getenv("TRUTH_SOCIAL_EMAIL")
TS_PASSWORD = os.getenv("TRUTH_SOCIAL_PASSWORD")
TRUTH_SOCIAL_URL = "https://truthsocial.com"

# Création du mini-serveur Web pour Render
app = Flask(__name__)

def generer_publication_kelia():
    client = Groq(api_key=GROQ_API_KEY)
    
    prompt = """
    Tu es KELIA. Ta seule mission est de faire la promotion de :
    1. KeloSocial.eu : Réseau social basé sur AT Protocol.
    2. Kelo-ID.eu : Plateforme de vérification d'identité.
    
    Rédige une publication pour les réseaux sociaux. 
    CONTRAINTES STRICTES :
    - MAXIMUM 400 caractères au total (espaces et hashtags compris).
    - Ne mets AUCUN guillemet autour de ton texte.
    - Ajoute 1 ou 2 emojis et les hashtags #KeloSocial #KeloID.
    - Sois directe et percutante.
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Tu gères la promotion exclusive de KeloSocial.eu et Kelo-ID.eu."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="openai/gpt-oss-120b", 
            temperature=0.7,
            max_tokens=150
        )
        
        texte = chat_completion.choices[0].message.content.strip()
        
        if len(texte) > 400:
            texte = texte[:397] + "..."
            
        return texte
        
    except Exception as e:
        print(f"Erreur avec l'API Groq : {e}")
        return None

def publier_sur_truth_social(texte):
    try:
        print("Connexion à Truth Social en cours...")
        Mastodon.create_app(
            'KeliaBot',
            api_base_url=TRUTH_SOCIAL_URL,
            to_file='kelia_clientcred.secret'
        )
        truth = Mastodon(
            client_id='kelia_clientcred.secret',
            api_base_url=TRUTH_SOCIAL_URL
        )
        truth.log_in(TS_EMAIL, TS_PASSWORD)
        truth.status_post(texte)
        print("✅ KELIA a publié avec succès sous le nom de Kelo Social !")
    except Exception as e:
        print(f"Erreur lors de la publication sur Truth Social : {e}")
    finally:
        if os.path.exists('kelia_clientcred.secret'):
            os.remove('kelia_clientcred.secret')

# C'est la fonction que l'horloge va déclencher
def tache_de_publication():
    print("⏰ L'horloge interne déclenche une publication...")
    publication = generer_publication_kelia()
    if publication:
        print(f"\nTexte généré ({len(publication)} caractères) :\n{publication}\n")
        publier_sur_truth_social(publication)

# Page d'accueil du Web Service pour que Render sache que le bot va bien
@app.route('/')
def home():
    return "🤖 KELIA Bot est en ligne et actif !"

if __name__ == "__main__":
    print("Éveil de KELIA sur Groq (modèle openai/gpt-oss-120b)...")
    
    # 1. Configuration de l'horloge interne (déclenchement toutes les 6 heures)
    scheduler = BackgroundScheduler()
    scheduler.add_job(tache_de_publication, 'interval', hours=6)
    
    # Déclenche une première publication immédiate au démarrage du serveur
    scheduler.add_job(tache_de_publication) 
    
    scheduler.start()
    
    # 2. Lancement du serveur Web demandé par Render
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
