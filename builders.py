from .database.models.article import Article
from .database.models.commentaire import Commentaire
from .database.models.message import Message
from .database.models.post import PostForum, PostReseau
from .database.models.service import Service
from .database.models.utilisateur import Utilisateur
from .database.models.abonnement import Abonnement

def build_article(result_set_item):
        vendeur = Utilisateur(
        nom_utilisateur=result_set_item['nom_utilisateur'],
        nom=result_set_item['nom'],
        prenom=result_set_item['prenom'],
        photo_profil=result_set_item['photo_profil']
        )
        return Article(
        id_article = result_set_item["id_article"],
        vendeur = vendeur, 
        titre=result_set_item["titre"], 
        prix=result_set_item["prix"], 
        description=result_set_item["description"], 
        image=result_set_item["image"]
        )

def build_message(result_set_item):
    recepteur = Utilisateur(
        nom_utilisateur=result_set_item['recepteur_nom_utilisateur'],
        nom=result_set_item['recepteur_nom'],
        prenom=result_set_item['recepteur_prenom'],
        photo_profil=result_set_item['recepteur_photo_profil']
    )
    emetteur = Utilisateur(
        nom_utilisateur=result_set_item['emetteur_nom_utilisateur'],
        nom=result_set_item['emetteur_nom'],
        prenom=result_set_item['emetteur_prenom'],
        photo_profil=result_set_item['emetteur_photo_profil']
    )
    return Message(
        id_message=result_set_item['id_message'], 
        contenu=result_set_item['contenu'], 
        recepteur=recepteur,
        emetteur=emetteur,
        horodatage=result_set_item['horodatage']
    )

def build_postforum(row):
    return PostForum(
        id_post=row['id_post'],
        nom_auteur=row['nom_auteur'],
        titre=row['titre'],
        description=row['description'],
        horodatage=row['horodatage'],
        photo_profil=row['photo_profil']
    )

def build_utilisateur(result_set_item):
    return Utilisateur(
        nom_utilisateur=result_set_item['nom_utilisateur'],
        password=result_set_item['password'],
        salt=result_set_item['salt'],
        nom=result_set_item['nom'],
        prenom=result_set_item['prenom'],
        email=result_set_item['email'],
        photo_profil=result_set_item['photo_profil'],
        biographie=result_set_item['biographie']
    )

def build_postreseau(result_set_item):
    ## Créer Utilisateur avec seulement les informations nécessaires sur le post
    auteur = Utilisateur(
        nom_utilisateur=result_set_item['nom_utilisateur'],
        nom=result_set_item['nom'],
        prenom=result_set_item['prenom'],
        photo_profil=result_set_item['photo_profil']
    )
    return PostReseau(
        id_post=result_set_item['id_post'],
        auteur=auteur,
        horodatage=result_set_item['horodatage'],
        description=result_set_item['description'],
        nombre_total_aime=result_set_item['nombre_total_aime'],
        image=result_set_item['image'],
        liked=bool(result_set_item['liked']),
        contient_commentaire=bool(result_set_item['contient_commentaire'])
    )
    
def build_commentaire(result_set_item):
    ## Créer Utilisateur avec seulement les informations nécessaires sur le commentaire
    auteur = Utilisateur(
        nom_utilisateur=result_set_item['nom_utilisateur'],
        nom=result_set_item['nom'],
        prenom=result_set_item['prenom'],
        photo_profil=result_set_item['photo_profil']
    )
    return Commentaire(
        id_commentaire=result_set_item['id_commentaire'],
        contenu=result_set_item['contenu'],
        auteur=auteur,
        horodatage=result_set_item['horodatage'],
        liked=bool(result_set_item['liked']),
        nombre_total_aime=result_set_item['nombre_total_aime'] 
    )
    
def build_service(result_set_item):
    ## Créer Utilisateur avec seulement les informations nécessaires sur le service
    vendeur = Utilisateur(
        nom_utilisateur=result_set_item['nom_utilisateur'],
        nom=result_set_item['nom'],
        prenom=result_set_item['prenom'],
        photo_profil=result_set_item['photo_profil']
    )
    return Service(
        id_service=result_set_item['id_service'],
        titre=result_set_item['titre'],
        description=result_set_item['description'],
        prix=result_set_item['prix'],
        horaire=result_set_item['horaire'],
        evaluation=result_set_item['evaluation'],
        vendeur=vendeur
    )

def build_abonnes(result_set_item):
    abonnement_utilisateur = Utilisateur(
        nom_utilisateur=result_set_item['nom_utilisateur'],
        nom=result_set_item['nom'],
        prenom=result_set_item['prenom'],
        photo_profil=result_set_item['photo_profil']
    )
    return Abonnement(
        nom_utilisateur=result_set_item['nom_utilisateur'],
        abonnement_nom_utilisateur = abonnement_utilisateur
    )

