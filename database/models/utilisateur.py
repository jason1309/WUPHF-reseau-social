class Utilisateur:
    def __init__(self, nom_utilisateur, nom=None, prenom=None, mot_de_passe=None, salt=None, email=None, boite_messagerie=None, photo_profil='/static/img/profil/default.png'):
        self.nom_utilisateur = nom_utilisateur
        self.nom = nom
        self.prenom = prenom
        self.mot_de_passe = mot_de_passe
        self.salt = salt
        self.email = email
        self.boite_messagerie = None
        self.photo_profil = photo_profil
        self.posts = []
        self.services = []
        self.articles = []
        self.abonnements = []
        self.abonnes = []
        self.posts_reseau_aime = []
        self.commentaires_reseau_aime = []

    def asDictionaryPost(self):
        return {
            "nom_utilisateur": self.nom_utilisateur,
            "nom": self.nom,
            "prenom": self.prenom,
            "photo_profil": self.photo_profil
        }

    def asDictionary(self):
        return {
            "nom_utilisateur": self.nom_utilisateur,
            "nom": self.nom,
            "prenom": self.prenom,
            "mot_de_passe": self.mot_de_passe,
            "salt": self.salt,
            "email": self.email,
            "boite_messagerie": self.boite_messagerie,
            "photo_profil": self.photo_profil,
            "posts": [post.asDictionary() for post in self.posts],
            "services": [service.asDictionary() for service in self.services],
            "articles": [article.asDictionary() for article in self.articles],
            "abonnements": [abonnement.asDictionary() for abonnement in self.abonnements],
            "abonnes": [abonne.asDictionary() for abonne in self.abonnes],
            "posts_reseau_aime": [post_reseau_aime.asDictionary() for post_reseau_aime in self.posts_reseau_aime],
            "commentaires_reseau_aime": [commentaire_reseau_aime.asDictionary() for commentaire_reseau_aime in self.commentaires_reseau_aime]
        }
