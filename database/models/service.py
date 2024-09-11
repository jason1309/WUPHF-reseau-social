class Service:
    def __init__(self, id_service, titre, description, prix, horaire, evaluation, vendeur):
        self.id_service = id_service
        self.titre = titre
        self.description = description
        self.prix = prix
        self.horaire = horaire
        self.evaluation = evaluation
        self.vendeur = vendeur

    def asDictionary(self):
        return {
            "id_service": self.id_service,
            "titre": self.titre,
            "description": self.description,
            "prix": self.prix,
            "horaire": self.horaire,
            "evaluation": self.evaluation,
            "vendeur": self.vendeur.asDictionary()
        }