class Compte:
    def __init__(self, id_compte, nom_utilisateur, mot_de_passe, email):
        self.id_compte = id_compte
        self.nom_utilisateur = nom_utilisateur
        self.mot_de_passe = mot_de_passe
        self.email = email

    def asDictionary(self):
        return {
            "id_compte": self.id_compte,
            "nom_utilisateur": self.nom_utilisateur,
            "mot_de_passe": self.mot_de_passe,
            "email": self.email
        }
