import os
from groq import Groq
from mastodon import Mastodon
from dotenv import load_dotenv

# Charge les variables d'environnement (.env en local)
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TS_EMAIL = os.getenv("TRUTH_SOCIAL_EMAIL")
TS_PASSWORD = os.getenv("TRUTH_SOCIAL_PASSWORD")
TRUTH_SOCIAL_URL = "https://truthsocial.com"

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
        
        # Sécurité pour ne pas dépasser la limite
        if len(texte) > 400:
            texte = texte[:397] + "..."
            
        return texte
        
    except Exception as e:
        print(f"Erreur avec l'API Groq : {e}")
        return None

def publier_sur_truth_social(texte):
    try:
        print("Connexion à Truth Social en cours...")
        
        # 1. Enregistrement d'une application temporaire
        Mastodon.create_app(
            'KeliaBot',
            api_base_url=TRUTH_SOCIAL_URL,
            to_file='kelia_clientcred.secret'
        )
        
        # 2. Initialisation
        truth = Mastodon(
            client_id='kelia_clientcred.secret',
            api_base_url=TRUTH_SOCIAL_URL
        )
        
        # 3. Connexion au compte Kelo Social
        truth.log_in(
            TS_EMAIL,
            TS_PASSWORD
        )
        
        # 4. Publication
        truth.status_post(texte)
        print("✅ KELIA a publié avec succès sous le nom de Kelo Social !")
        
    except Exception as e:
        print(f"Erreur lors de la publication sur Truth Social : {e}")
    finally:
        # Nettoyage du fichier secret généré lors de l'exécution
        if os.path.exists('kelia_clientcred.secret'):
            os.remove('kelia_clientcred.secret')

if __name__ == "__main__":
    print("Éveil de KELIA sur Groq (modèle openai/gpt-oss-120b)...")
    publication = generer_publication_kelia()
    
    if publication:
        print(f"\nTexte généré ({len(publication)} caractères) :\n{publication}\n")
        publier_sur_truth_social(publication)
