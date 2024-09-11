class Article:
    def __init__(self, id_article, vendeur, titre, prix, description, image):
        self.id_article = id_article
        self.vendeur = vendeur
        self.titre = titre
        self.prix = prix
        self.description = description
        self.image = image

    def asDictionary(self):
        return {
            "id_article": self.id_article,
            "vendeur": self.vendeur.asDictionary(),
            "titre": self.titre,
            "prix": self.prix,
            "description": self.description,
            "image": self.image
        }
