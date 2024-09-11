class Post:
    def __init__(self, id_post, auteur, horodatage, description, commentaires=None):
        self.id_post = id_post
        self.auteur = auteur 
        self.horodatage = horodatage
        self.description = description
        self.commentaires = commentaires if commentaires is not None else []

        
    def asDictionary(self):
        return {
            "id_post": self.id_post,
            "auteur": self.auteur.asDictionary(),
            "horodatage": self.horodatage,
            "description": self.description,
            "commentaires": [commentaire.asDictionary() for commentaire in self.commentaires]
        }

class PostForum(Post):
    def __init__(self, id_post, auteur, horodatage, description, nombre_total_aime=0, image=None, commentaires=None):
        super().__init__(id_post, auteur, horodatage, description, commentaires)
        self.image = image
        self.nombre_total_aime = nombre_total_aime

    def asDictionary(self):
        post_dict = super().asDictionary()
        post_dict.update({
            "image": self.image,
            "nombre_total_aime": self.nombre_total_aime
        })
        return post_dict

class PostReseau(Post):
    def __init__(self, id_post, auteur, horodatage, description=None, nombre_total_aime=0, image=None, commentaires=None, liked=False, contient_commentaire=False):
        super().__init__(id_post, auteur, horodatage, description, commentaires)
        self.nombre_total_aime = nombre_total_aime
        self.image = image
        self.liked = liked
        self.contient_commentaire = contient_commentaire

    def asDictionary(self):
        post_reseau_dict = super().asDictionary()
        post_reseau_dict.update({
            "nombre_total_aime": self.nombre_total_aime,
            "image": self.image,
            "liked": self.liked,
            "contient_commentaire": self.contient_commentaire
        })
        return post_reseau_dict
