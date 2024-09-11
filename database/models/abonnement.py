class Abonnement:
    def __init__(self, nom_utilisateur, abonnement_nom_utilisateur):
        self.nom_utilisateur = nom_utilisateur
        self.abonnement_nom_utilisateur = abonnement_nom_utilisateur

    def asDictionary(self):
        return {
            "nom_utilisateur": self.nom_utilisateur.asDictionary(),
            "abonnement_nom_utilisateur": self.abonnement_nom_utilisateur.asDictionary()
        }