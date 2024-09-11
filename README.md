# WUPHF - Plateforme pour Maîtres de Chiens
Bienvenue dans le dépôt Git de WUPHF, une plateforme centralisée conçue pour les maîtres de chiens, intégrant des fonctionnalités de réseau social, marketplace, forum de discussion, et plus encore.

Ce projet a été réalisé lors du cours INM5151 - Projet d'analyse et de modélisation (Été 2024). Le but était de produire un prototype du logiciel pour démontrer les fonctionnalités du projet, généralement les plus complexes ou les plus risquées. C'est pourquoi certaines vérifications nécessaires ou un design responsive n'ont pas été implémenté. Une approche incrémentale était requise sous forme de 3 itérations de 3 semaines.

## Table des matières
- [Description](#description)
- [Fonctionnalités](#fonctionnalités)
- [Technologies Utilisées](#technologies-utilisées)
- [Installation](#installation)
- [Contributeur](#contributeur)

## Description
WUPHF vise à simplifier la vie des maîtres de chiens en centralisant les ressources et services canins en un seul endroit. Cette plateforme permet aux utilisateurs de partager des photos de leurs chiens, de rechercher et d'offrir des services, de vendre et acheter des produits, et de participer à des discussions dans des forums dédiés.

## Fonctionnalités
- **Réseau social** : Partage de photos et d'expériences, commentaires et mentions "j'aime".
- **Services entre utilisateurs** : Recherche et offre de services pour chiens.
- **Marketplace** : Achat et vente d'articles pour chiens.
- **Forum de discussion** : Discussion sur divers sujets liés aux chiens, commentaires, mentions "j'aime" et "je n'aime pas".
- **Messagerie privée** : Communication entre utilisateurs. (à finaliser)

## Technologies Utilisées
- **Backend** : Flask, Python
- **Frontend** : HTML, CSS, Bootstrap, JavaScript, Jinja
- **Base de Données** : SQLite3

## Installation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/jason1309/WUPHF-reseau-social
   cd WUPHF-reseau-social
   ```

2. **Créer un environnement virtuel, l'activer et installer les dépendances**
   ##### macOS et Linux
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
   ##### Windows
   ```bash
   python -m venv venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Démarrer l'application**
    ```bash
    make run
    ```

Pour accéder à l'application, allez sur http://127.0.0.1:5000

## Contributeur
- [Gagné, Jason](https://www.linkedin.com/in/jason-gagn%C3%A9-839032246/)
- [Ricard, Gabriel](https://www.linkedin.com/in/gabriel-ricard-17a4a1206/)
- Gagné, Jeffrey
