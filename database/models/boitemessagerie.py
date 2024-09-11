class BoiteMessagerie:
    def __init__(self, id_boite_messagerie, utilisateur):
        self.id_boite_messagerie = id_boite_messagerie
        self.utilisateur = utilisateur
        self.messages = []

    def asDictionary(self):
        return {
            "id_boite_messagerie": self.id_boite_messagerie,
            "utilisateur": self.utilisateur.asDictionary(),
            "messages": [message.asDictionary() for message in self.messages]
        }
