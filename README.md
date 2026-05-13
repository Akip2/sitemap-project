# Description

Une application web de collecte et de visualisation d'informations sous forme de nuage de mots, construite à partir de titres d'actualités. Elle permet de s'abonner à des sources d'actualités via leurs sitemaps et de stocker les articles dans une base de données MongoDB.

## Prérequis

- Python 3.8 ou supérieur
- MongoDB en cours d'exécution sur `localhost:27017`

## Installation des dépendances

```bash
pip install -r requirements.txt
```

## Lancement de l'application

```bash
cd src
python main.py
```

3. Ouvrir un navigateur et accéder à `http://localhost:5000`

## Utilisation

### Mode Administration
Accessible via l'onglet **Administration**, il permet de :
- Ajouter une source d'actualités en renseignant l'URL de son sitemap Google News
- Supprimer une source existante
- Configurer la fréquence de récupération automatique des articles

### Mode Consultation
Accessible via l'onglet **Consultation**, il propose deux vues :
- **Liste** : parcourir et filtrer les articles par source, date ou mot-clé. Cliquer sur un titre ouvre l'article dans un nouvel onglet.
- **Nuage de mots** : générer un nuage de mots SVG à partir des titres sur une période donnée, avec possibilité de télécharger le fichier SVG.