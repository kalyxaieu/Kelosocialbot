# KELIA - Bot Truth Social pour Kelo Social

Ce bot génère des publications promotionnelles pour KeloSocial.eu et Kelo-ID.eu grâce à l'intelligence artificielle (Groq / Llama 3) et les publie automatiquement sur Truth Social.

## Déploiement sur Render
Ce bot est conçu pour tourner via un "Cron Job" sur Render.com.

Variables d'environnement requises sur Render :
- `GROQ_API_KEY` : Clé API de la console Groq.
- `TRUTH_SOCIAL_EMAIL` : Email du compte Kelo Social.
- `TRUTH_SOCIAL_PASSWORD` : Mot de passe du compte.
