class Message:
    def __init__(self, id_message, contenu, recepteur, emetteur, horodatage):
        self.id_message = id_message
        self.contenu = contenu
        self.recepteur = recepteur
        self.emetteur = emetteur
        self.horodatage = horodatage 

def asDictionary(self):
        return {
            "id_message": self.id_message,
            "contenu": self.contenu,
            "recepteur": self.recepteur.asDictionary(),
            "emetteur": self.emetteur.asDictionary(),
            "horodatage": self.horodatage
        }