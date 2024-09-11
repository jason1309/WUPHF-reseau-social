class Commentaire:
    def __init__(self, id_commentaire, contenu, auteur, horodatage, nombre_total_aime, liked):
        self.id_commentaire = id_commentaire
        self.contenu = contenu
        self.auteur = auteur
        self.horodatage = horodatage
        self.nombre_total_aime = nombre_total_aime
        self.liked = liked

    def asDictionary(self):
        return {
            "id_commentaire": self.id_commentaire,
            "contenu": self.contenu,
            "auteur": self.auteur.asDictionary() if self.auteur else None,
            "horodatage": self.horodatage,
            "nombre_total_aime": self.nombre_total_aime,
            "liked": self.liked
        }
