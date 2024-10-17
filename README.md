# QualiTube

QualiTube est un outil permettant de rechercher et d'analyser des vidéos YouTube pertinentes en fonction des intérêts de l'utilisateur. Il utilise l'API Gemini pour générer des requêtes de recherche et analyser le contenu des vidéos.

## Fonctionnalités

- **Génération de requêtes de recherche :** Basée sur l'entrée utilisateur, QualiTube génère des requêtes de recherche pertinentes et concises.
- **Recherche et extraction de métadonnées :** Recherche des vidéos sur YouTube et extrait des informations telles que le titre, la description, la durée, la date de publication, etc.
- **Analyse de contenu :** Utilise l'API Gemini pour analyser le contenu des vidéos et attribuer un score de pertinence.
- **Suggestions automatiques :** Fournit des suggestions de recherche basées sur une entrée partielle de l'utilisateur.
- **Filtrage avancé :** Permet de filtrer les vidéos par durée et date de publication.

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/flambis/qualitube.git
cd qualitube

2. Créer un environnement virtuel

Il est recommandé d'utiliser un environnement virtuel pour gérer les dépendances du projet.

bash

python3 -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate

3. Installer les dépendances

Installez toutes les bibliothèques nécessaires listées dans requirements.txt.

bash

pip install -r requirements.txt

4. Configurer les variables d'environnement

Créez un fichier .env à la racine du projet et ajoutez vos clés API ainsi que la clé secrète de Flask.

env

FLASK_SECRET_KEY=your_secret_key
GEMINI_API_KEY=your_gemini_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

Remarque : Assurez-vous de ne jamais partager ce fichier ou de le commettre dans votre dépôt public.
5. Lancer l'application

Démarrez le serveur Flask en exécutant le script run.py.

bash

python run.py

L'application sera accessible sur http://localhost:4000.
Utilisation

    Page de Recherche : Accédez à la page principale pour entrer votre requête de recherche. Vous pouvez affiner vos recherches en utilisant les filtres de durée et de date de publication.
    Résultats : Les vidéos correspondant à vos critères seront affichées avec des scores de pertinence et des explications personnalisées.
    Suggestions : En tapant dans la barre de recherche, des suggestions automatiques vous aideront à affiner votre requête.

Contribution

Les contributions sont les bienvenues ! Voici comment vous pouvez aider à améliorer QualiTube :

    Forker le dépôt : Créez un fork du projet sur GitHub.
    Créer une branche : Créez une branche pour votre fonctionnalité ou correction de bug (git checkout -b feature/nom-de-la-fonctionnalité).
    Commiter vos changements : Commitez vos modifications avec un message clair (git commit -m "Ajoute une nouvelle fonctionnalité X").
    Pousser vers le fork : Poussez votre branche vers votre fork (git push origin feature/nom-de-la-fonctionnalité).
    Créer une Pull Request : Ouvrez une Pull Request sur le dépôt principal en décrivant vos changements.

Veuillez vous assurer que vos contributions respectent les standards de code et que le projet reste fonctionnel après vos modifications.
Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
Remerciements

    Merci à Scrapetube pour leur outil de scraping YouTube.
    Merci à Pytube pour l'extraction des métadonnées des vidéos.
    Merci à l'équipe de Supabase pour leurs services backend.
    Merci à OpenAI pour l'API Gemini utilisée dans ce projet.

Contact

Pour toute question ou suggestion, veuillez ouvrir une issue sur le dépôt GitHub ou contacter benjamin.koensgen@gmail.com.
