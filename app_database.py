from datetime import datetime
import sqlite3
from .builders import (
    build_abonnes,
    build_article,
    build_commentaire,
    build_message,
    build_postforum,
    build_postreseau,
    build_service,
    build_utilisateur
)

class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect("database/interfaceWUPHF.db")
            self.connection.row_factory = sqlite3.Row
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    ## Methode pour utilisateurs
    def creer_utilisateur(self, nom_utilisateur, mot_de_passe, salt, nom, prenom, email):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute(
            "INSERT INTO Utilisateur (nom_utilisateur, mot_de_passe, salt, nom, prenom, email) VALUES (?, ?, ?, ?, ?, ?);",
            (nom_utilisateur, mot_de_passe, salt, nom, prenom, email),
        )
        connexion.commit()

    def get_utilisateur_login_info(self, nom_utilisateur):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        utilisateur_infos = connexion.execute(
            "SELECT * FROM Utilisateur WHERE nom_utilisateur = ?;", (nom_utilisateur,)
        ).fetchone()
        return utilisateur_infos

    def get_utilisateurs(self):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        utilisateur_list = connexion.execute("SELECT * FROM Utilisateur").fetchall()
        return utilisateur_list

    def get_utilisateur_info(self, nom_utilisateur):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        utilisateur_infos = connexion.execute("SELECT * FROM Utilisateur WHERE nom_utilisateur = ?;", (nom_utilisateur,)).fetchone()
        return utilisateur_infos

    def update_utilisateur_photo_profil(self, nom_utilisateur, chemin_photo):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute(
            "UPDATE Utilisateur SET photo_profil = ? WHERE nom_utilisateur = ?;", (chemin_photo, nom_utilisateur,)
        )
        connexion.commit()
    
    ## Méthode pour post réseau
    def add_post_reseau(self, nom_auteur, description, image):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute(
            "INSERT INTO PostReseau (nom_auteur, horodatage, description, nombre_total_aime, image) VALUES (?, datetime('now'), ?, 0, ?);",
            (nom_auteur, description, image)
        )
        connexion.commit()
    
    def add_commentaire_post_reseau(self, id_post, nom_auteur, contenu, horodatage):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute(
            "INSERT INTO CommentaireReseau (contenu, nom_auteur, id_post, horodatage, nombre_total_aime) VALUES (?, ?, ?, ?, 0);",
            (contenu, nom_auteur, id_post, horodatage)
        )
        connexion.commit()
    
    def get_utilisateur_posts_reseau(self, nom_utilisateur):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        posts_reseau = connexion.execute(
            "SELECT * FROM PostReseau WHERE nom_auteur = ?;", (nom_utilisateur,)
        ).fetchall()
        return [build_postreseau(post) for post in posts_reseau]

    def get_commentaires_post_reseau(self, nom_utilisateur, id_post):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        query = """
        SELECT cr.id_commentaire, cr.contenu, cr.horodatage, cr.nombre_total_aime, u.nom_utilisateur, u.nom, u.prenom, u.photo_profil,
           EXISTS(SELECT 1 FROM CommentaireReseauLike crl WHERE crl.id_commentaire = cr.id_commentaire AND crl.nom_utilisateur = ?) AS liked
        FROM CommentaireReseau cr
        JOIN Utilisateur u ON cr.nom_auteur = u.nom_utilisateur
        WHERE cr.id_post = ?
        ORDER BY cr.horodatage ASC;
        """
        commentaires = connexion.execute(query, (nom_utilisateur, id_post,)).fetchall()
        return [build_commentaire(commentaire) for commentaire in commentaires]

    def add_post_reseau_aime(self, nom_utilisateur, id_post):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO PostReseauLike (nom_utilisateur, id_post) VALUES (?, ?);", (nom_utilisateur, id_post)
        )
        cursor.execute(
            "UPDATE PostReseau SET nombre_total_aime = nombre_total_aime + 1 WHERE id_post = ?;", (id_post,)
        )
        connexion.commit()
    
    def remove_post_reseau_aime(self, nom_utilisateur, id_post):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute(
            "DELETE FROM PostReseauLike WHERE nom_utilisateur = ? AND id_post = ?;", (nom_utilisateur, id_post)
        )
        cursor.execute(
            "UPDATE PostReseau SET nombre_total_aime = nombre_total_aime - 1 WHERE id_post = ?;", (id_post,)
        )
        connexion.commit()
    
    def get_posts_reseau_abonnement(self, nom_utilisateur):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        ## On va chercher les informations nécessaires sur le posts et sur son auteur
        ## On va chercher tout les nom utilisateurs des posts ou nom_utilisateur passé 
        ## en paramètre est abonné.
        query = """
        SELECT p.*, u.nom_utilisateur, u.nom, u.prenom, u.photo_profil,
           EXISTS(SELECT 1 FROM PostReseauLike pl WHERE pl.id_post = p.id_post AND pl.nom_utilisateur = ?) AS liked,
           EXISTS(SELECT 1 FROM CommentaireReseau cr WHERE cr.id_post = p.id_post) AS contient_commentaire
        FROM PostReseau p
        JOIN Utilisateur u ON p.nom_auteur = u.nom_utilisateur
        LEFT JOIN Abonnement a ON p.nom_auteur = a.abonnement_nom_utilisateur
        WHERE a.nom_utilisateur = ? OR p.nom_auteur = ?
        ORDER BY p.horodatage DESC;
        """
        posts_reseau = connexion.execute(query, (nom_utilisateur, nom_utilisateur, nom_utilisateur)).fetchall()
        return [build_postreseau(post) for post in posts_reseau]

    
    def remove_post_reseau(self, id_post):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute("DELETE FROM PostReseau WHERE id_post = ?;", (id_post,))
        connexion.commit()

    def update_post_reseau(self, id_post, description, image_path):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute("UPDATE PostReseau SET description = ?, image = ? WHERE id_post = ?;", (description, image_path, id_post,))
        connexion.commit()
        cursor.close()

    def get_post_reseau_par_id(self, id_post):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        post_reseau = cursor.execute("SELECT * FROM PostReseau WHERE id_post = ?;", (id_post,)).fetchone()
        return post_reseau
    
    ## Méthode commentaire réseau
    def add_commentaire_reseau_aime(self, nom_utilisateur, id_commentaire):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO CommentaireReseauLike (nom_utilisateur, id_commentaire) VALUES (?, ?);", (nom_utilisateur, id_commentaire)
        )
        cursor.execute(
            "UPDATE CommentaireReseau SET nombre_total_aime = nombre_total_aime + 1 WHERE id_commentaire = ?;", (id_commentaire,)
        )
        connexion.commit()
    
    def remove_commentaire_reseau_aime(self, nom_utilisateur, id_commentaire):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute(
            "DELETE FROM CommentaireReseauLike WHERE nom_utilisateur = ? AND id_commentaire = ?;", (nom_utilisateur, id_commentaire)
        )
        cursor.execute(
            "UPDATE CommentaireReseau SET nombre_total_aime = nombre_total_aime - 1 WHERE id_commentaire = ?;", (id_commentaire,)
        )
        connexion.commit()

    def remove_commentaire_post_reseau(self, id_commentaire):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute("DELETE FROM CommentaireReseau WHERE id_commentaire = ?;", (id_commentaire,))
        connexion.commit()
    
    def get_dernier_commentaire(self, id_post, nom_auteur, contenu):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        query = """
        SELECT cr.id_commentaire, cr.contenu, cr.horodatage, u.nom_utilisateur, u.nom, u.prenom, u.photo_profil
        FROM CommentaireReseau cr
        JOIN Utilisateur u ON cr.nom_auteur = u.nom_utilisateur
        WHERE cr.id_post = ? AND cr.nom_auteur = ? AND cr.contenu = ?
        ORDER BY cr.horodatage DESC
        LIMIT 1;
        """
        commentaire = connexion.execute(query, (id_post, nom_auteur, contenu)).fetchone()
        if commentaire:
            commentaire = dict(commentaire)
            commentaire['liked'] = False
            commentaire['nombre_total_aime'] = 0
        return build_commentaire(commentaire) if commentaire else None
    
    # Méthode pour session
    def save_session(self, session_id, nom_utilisateur):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute(
            "INSERT INTO sessions (session_id, nom_utilisateur) VALUES (?, ?);",
            (session_id, nom_utilisateur)
        )
        connexion.commit()

    def delete_session(self, session_id):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute(
            "DELETE FROM sessions WHERE session_id = ?;", (session_id,)
        )
        connexion.commit()

    def get_session(self, session_id):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        session = connexion.execute(
            "SELECT nom_utilisateur FROM sessions WHERE session_id = ?;", (session_id,)
        ).fetchone()
        return session["nom_utilisateur"] if session else None
    
    def search_posts_reseau(self, search_query):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        cursor = connexion.cursor()
        cursor.execute("""
            SELECT PostReseau.*, Utilisateur.photo_profil
            FROM PostReseau
            JOIN Utilisateur ON PostReseau.nom_auteur = Utilisateur.nom_utilisateur
            WHERE LOWER(PostReseau.nom_auteur) LIKE ?
        """, ('%' + search_query + '%',))
        posts_reseau = cursor.fetchall()
        return [build_postreseau(post) for post in posts_reseau]
    

    ## METHODES MARKETPLACE ##

    def get_all_articles(self):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        cursor = connexion.cursor()
        cursor.execute("""
            SELECT a.id_article, a.titre, a.prix, a.description, a.image, 
                   u.nom_utilisateur, u.nom, u.prenom, u.photo_profil
            FROM Article a
            JOIN Utilisateur u ON a.nom_vendeur = u.nom_utilisateur
        """)
        articles = cursor.fetchall()
        return [build_article(article) for article in articles]
    
    def get_all_user_articles(self, nom_utilisateur):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        cursor = connexion.cursor()
        query = ("""
            SELECT a.id_article, a.titre, a.prix, a.description, a.image, 
                   u.nom_utilisateur, u.nom, u.prenom, u.photo_profil
            FROM Article a
            JOIN Utilisateur u ON a.nom_vendeur = u.nom_utilisateur
            WHERE u.nom_utilisateur = ?;
        """)
        cursor.execute(query, (nom_utilisateur,))
        articles = cursor.fetchall()
        return [build_article(article) for article in articles]
    
    ## METHODES PAGE PROFIL ##
    
    def get_abonnements(self, nom_utilisateur):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        abonnements = connexion.execute(
        "SELECT abonnement_nom_utilisateur FROM Abonnement WHERE nom_utilisateur = ?;", (nom_utilisateur,)
    ).fetchall()
        return [abonnement["abonnement_nom_utilisateur"] for abonnement in abonnements]

    def get_abonnes(self, nom_utilisateur):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        abonnes = connexion.execute(
        "SELECT nom_utilisateur FROM Abonnement WHERE abonnement_nom_utilisateur = ?;", (nom_utilisateur,)
    ).fetchall()
        return [abonne["nom_utilisateur"] for abonne in abonnes]        
    
    def get_article(self, id_article):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        cursor = connexion.cursor()
        cursor.execute("""
            SELECT a.id_article, a.titre, a.prix, a.description, a.image, 
                   u.nom_utilisateur, u.nom, u.prenom, u.photo_profil
            FROM Article a
            JOIN Utilisateur u ON a.nom_vendeur = u.nom_utilisateur
            WHERE a.id_article = ?
        """, (id_article,))
        article = cursor.fetchone()
        return build_article(article) if article else None
    
    def add_article(self, titre, prix, description, image, nom_vendeur):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        cursor = connexion.cursor()
        query = ("INSERT INTO Article (titre, prix, description, image, nom_vendeur) VALUES (?, ?, ?, ?, ?);")
        cursor.execute(query, (titre, prix, description, image, nom_vendeur,))
        connexion.commit()
        article_id = cursor.lastrowid
        return article_id
    
    def supprimer_article(self, id_article):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        cursor = connexion.cursor()
        cursor.execute("DELETE FROM Article WHERE id_article = ?;", (id_article,))
        connexion.commit()
    
    def update_article(self, titre, prix, description, image, id_article):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        cursor = connexion.cursor()
        query = ("UPDATE Article SET titre = ?, prix = ?, description = ?, image = ? WHERE id_article = ?")
        cursor.execute(query, (titre, prix, description, image, id_article,))
        connexion.commit()
    
    ## METHODES SERVICES ##
    def get_all_services(self):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        cursor = connexion.cursor()
        query = """
        SELECT s.id_service, s.titre, s.description, s.prix, s.horaire, s.evaluation,
            u.nom_utilisateur, u.nom, u.prenom, u.photo_profil
        FROM Service s
        JOIN Utilisateur u ON s.nom_vendeur = u.nom_utilisateur;
        """
        cursor.execute(query)
        services = cursor.fetchall()
        return [build_service(service) for service in services]
    
    def add_service(self, nom_vendeur, titre, description, cout, disponibilite):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute(
            "INSERT INTO Service (nom_vendeur, titre, description, prix, horaire) VALUES (?, ?, ?, ?, ?);",
            (nom_vendeur, titre, description, cout, disponibilite)
        )
        connexion.commit()
        
    def get_utilisateur_services(self, nom_utilisateur):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        cursor = connexion.cursor()
        query = """
        SELECT s.id_service, s.titre, s.description, s.prix, s.horaire, s.evaluation,
            u.nom_utilisateur, u.nom, u.prenom, u.photo_profil
        FROM Service s
        JOIN Utilisateur u ON s.nom_vendeur = u.nom_utilisateur
        WHERE s.nom_vendeur = ?
        ORDER BY s.id_service DESC;
        """
        cursor.execute(query, (nom_utilisateur,))
        services = cursor.fetchall()
        return [build_service(service) for service in services]
    
    def supprimer_service(self, id_service):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute("DELETE FROM Service WHERE id_service = ?;", (id_service,))
        connexion.commit()
    
    def get_service(self, id_service):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        cursor = connexion.cursor()
        query = """
        SELECT s.id_service, s.titre, s.description, s.prix, s.horaire, s.evaluation,
            u.nom_utilisateur, u.nom, u.prenom, u.photo_profil
        FROM Service s
        JOIN Utilisateur u ON s.nom_vendeur = u.nom_utilisateur
        WHERE s.id_service = ?;
        """
        cursor.execute(query, (id_service,))
        service = cursor.fetchone()
        return build_service(service) if service else None
    
    def update_service(self, id_service, titre, description, prix, horaire):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute("UPDATE Service SET titre = ?, description = ?, prix = ?, horaire = ? WHERE id_service = ?; ", 
                       (titre, description, prix, horaire, id_service))
        connexion.commit()
    
    ## METHOIDES PROFIL ##
    def get_posts_reseau_user(self, nom_utilisateur):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        query = """
        SELECT p.*, u.nom_utilisateur, u.nom, u.prenom, u.photo_profil,
               EXISTS(SELECT 1 FROM PostReseauLike pl WHERE pl.id_post = p.id_post AND pl.nom_utilisateur = ?) AS liked,
               EXISTS(SELECT 1 FROM CommentaireReseau cr WHERE cr.id_post = p.id_post) AS contient_commentaire
        FROM PostReseau p
        JOIN Utilisateur u ON p.nom_auteur = u.nom_utilisateur
        WHERE p.nom_auteur = ?
        ORDER BY p.horodatage DESC;
        """
        posts_reseau = connexion.execute(query, (nom_utilisateur, nom_utilisateur)).fetchall()
        return [build_postreseau(post) for post in posts_reseau]
    
    def ajouter_abonnement(self, nom_utilisateur, abonnement_nom_utilisateur):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO Abonnement (nom_utilisateur, abonnement_nom_utilisateur) VALUES (?, ?);", 
            (nom_utilisateur, abonnement_nom_utilisateur)
        )
        connexion.commit()

    def supprimer_abonnement(self, nom_utilisateur, abonnement_nom_utilisateur):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute(
            "DELETE FROM Abonnement WHERE nom_utilisateur = ? AND abonnement_nom_utilisateur = ?;", 
            (nom_utilisateur, abonnement_nom_utilisateur)
        )
        connexion.commit()
    
    def est_abonne(self, utilisateur_courant, utilisateur_visite):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM Abonnement WHERE nom_utilisateur = ? AND abonnement_nom_utilisateur = ?", (utilisateur_courant, utilisateur_visite))
        result = cursor.fetchone()
        return result[0] > 0
    
    def get_conversation(self, nom_utilisateur):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        query = """
            SELECT U.nom_utilisateur, U.password, U.salt, U.nom, U.prenom, U.email, U.photo_profil, U.biographie
            FROM Abonnement A
            JOIN Utilisateur U ON A.abonnement_nom_utilisateur = U.nom_utilisateur
            WHERE A.nom_utilisateur = ?
        """
        cursor.execute(query, (nom_utilisateur,))
        result_set = cursor.fetchall()
        abonnes = [build_abonnes(result_set_item) for result_set_item in result_set]
        return abonnes

    def rechercher_utilisateurs(self, search_query):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        utilisateurs = connexion.execute(
            "SELECT nom_utilisateur, prenom, nom, photo_profil FROM Utilisateur WHERE LOWER(nom_utilisateur) LIKE ? OR LOWER(prenom) LIKE ? OR LOWER(nom) LIKE ?",
            ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%')
        ).fetchall()
        return [dict(utilisateur) for utilisateur in utilisateurs]

    def modifier_utilisateur(self, nom_utilisateur, prenom, nom, biographie):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute(
            "UPDATE Utilisateur SET prenom = ?, nom = ?, biographie = ? WHERE nom_utilisateur = ?",
            (prenom, nom, biographie, nom_utilisateur)
        )
        connexion.commit()
    
    ## METHODE FORUM ##
    def get_all_posts_forum(self, nom_utilisateur):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        query = """
        SELECT p.id_post, p.titre, p.nom_auteur, p.horodatage, p.description, p.nombre_total_aime, 
               u.photo_profil,
               COALESCE(l.aime, 0) AS aime, 
               COALESCE(l.aime_pas, 0) AS aime_pas
        FROM PostForum p
        JOIN Utilisateur u ON p.nom_auteur = u.nom_utilisateur
        LEFT JOIN PostForumLike l ON p.id_post = l.id_post AND l.nom_utilisateur = ?
        ORDER BY p.horodatage DESC;
        """
        cursor = connexion.cursor()
        cursor.execute(query, (nom_utilisateur,))
        posts = cursor.fetchall()
        return [dict(post) for post in posts]
    
    def add_post_forum(self, nom_auteur, titre, description):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute(
            """
            INSERT INTO PostForum (nom_auteur, titre, description, horodatage, nombre_total_aime)
            VALUES (?, ?, ?, datetime('now'), 0)
            """, (nom_auteur, titre, description)
        )
        connexion.commit()
        return cursor.lastrowid
    
    def get_post_forum(self, id_post, nom_utilisateur):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        cursor = connexion.cursor()
        query = """
        SELECT p.id_post, p.titre, p.nom_auteur, p.horodatage, p.description, p.nombre_total_aime, u.photo_profil,
            COALESCE(l.aime, 0) AS aime, COALESCE(l.aime_pas, 0) AS aime_pas
        FROM PostForum p
        JOIN Utilisateur u ON p.nom_auteur = u.nom_utilisateur
        LEFT JOIN PostForumLike l ON p.id_post = l.id_post AND l.nom_utilisateur = ?
        WHERE p.id_post = ?;
        """
        cursor.execute(query, (nom_utilisateur, id_post))
        post_forum = cursor.fetchone()
        return dict(post_forum)

    
    def get_commentaires_forum(self, id_post, nom_utilisateur):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        cursor = connexion.cursor()
        query = """
        SELECT c.id_commentaire, c.nom_auteur, c.horodatage, c.contenu, u.photo_profil, 
           c.commentaire_nombre_aime, 
           COALESCE(l.aime, 0) AS aime, 
           COALESCE(l.aime_pas, 0) AS aime_pas
        FROM CommentaireForum c
        JOIN Utilisateur u ON c.nom_auteur = u.nom_utilisateur
        LEFT JOIN CommentaireForumLike l ON c.id_commentaire = l.id_commentaire AND l.nom_utilisateur = ?
        WHERE c.id_post = ?
        ORDER BY c.horodatage ASC;
        """
        cursor.execute(query, (nom_utilisateur, id_post,))
        commentaires = cursor.fetchall()
        return [dict(commentaire) for commentaire in commentaires]

    def add_commentaire_post_forum(self, id_post, nom_auteur, contenu, horodatage):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute(
            "INSERT INTO CommentaireForum (id_post, nom_auteur, contenu, horodatage) VALUES (?, ?, ?, ?)",
            (id_post, nom_auteur, contenu, horodatage)
        )
        connexion.commit()
        dernier_id = cursor.lastrowid
        cursor.execute("""
        SELECT c.*, u.photo_profil 
        FROM CommentaireForum c
        JOIN Utilisateur u ON c.nom_auteur = u.nom_utilisateur
        WHERE c.id_commentaire = ?
        """, (dernier_id,))
        commentaire = cursor.fetchone()
        
        return dict(commentaire)
    
    def get_nb_commentaire_post_forum(self, id_post):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM CommentaireForum WHERE id_post = ?", (id_post,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return 0
    
    def upvote_commentaire_forum(self, id_commentaire, nom_utilisateur):
        connexion = self.get_connection()
        cursor = connexion.cursor()

        cursor.execute("""
            SELECT aime, aime_pas FROM CommentaireForumLike 
            WHERE id_commentaire = ? AND nom_utilisateur = ?
        """, (id_commentaire, nom_utilisateur))
        result = cursor.fetchone()

        if result:
            current_aime, current_aime_pas = result
            if current_aime_pas:
                cursor.execute("""
                    UPDATE CommentaireForum
                    SET commentaire_nombre_aime = commentaire_nombre_aime + 2
                    WHERE id_commentaire = ?
                """, (id_commentaire,))
            elif not current_aime:
                cursor.execute("""
                    UPDATE CommentaireForum
                    SET commentaire_nombre_aime = commentaire_nombre_aime + 1
                    WHERE id_commentaire = ?
                """, (id_commentaire,))
        else:
            cursor.execute("""
                UPDATE CommentaireForum
                SET commentaire_nombre_aime = commentaire_nombre_aime + 1
                WHERE id_commentaire = ?
            """, (id_commentaire,))

        cursor.execute("""
            INSERT INTO CommentaireForumLike (id_commentaire, nom_utilisateur, aime, aime_pas)
            VALUES (?, ?, TRUE, FALSE)
            ON CONFLICT(id_commentaire, nom_utilisateur)
            DO UPDATE SET aime = TRUE, aime_pas = FALSE
        """, (id_commentaire, nom_utilisateur))
        
        connexion.commit()

    def retirer_upvote_commentaire(self, id_commentaire, nom_utilisateur):
        connexion = self.get_connection()
        cursor = connexion.cursor()

        cursor.execute("""
            UPDATE CommentaireForum
            SET commentaire_nombre_aime = commentaire_nombre_aime - 1
            WHERE id_commentaire = ?
        """, (id_commentaire,))
        
        cursor.execute("""
            UPDATE CommentaireForumLike
            SET aime = FALSE
            WHERE id_commentaire = ? AND nom_utilisateur = ?
        """, (id_commentaire, nom_utilisateur))
        connexion.commit()
    
    def downvote_commentaire_forum(self, id_commentaire, nom_utilisateur):
        connexion = self.get_connection()
        cursor = connexion.cursor()

        cursor.execute("""
            SELECT aime, aime_pas FROM CommentaireForumLike 
            WHERE id_commentaire = ? AND nom_utilisateur = ?
        """, (id_commentaire, nom_utilisateur))
        result = cursor.fetchone()

        if result:
            current_aime, current_aime_pas = result
            if current_aime:
                cursor.execute("""
                    UPDATE CommentaireForum
                    SET commentaire_nombre_aime = commentaire_nombre_aime - 2
                    WHERE id_commentaire = ?
                """, (id_commentaire,))
            elif not current_aime_pas:
                cursor.execute("""
                    UPDATE CommentaireForum
                    SET commentaire_nombre_aime = commentaire_nombre_aime - 1
                    WHERE id_commentaire = ?
                """, (id_commentaire,))
        else:
            cursor.execute("""
                UPDATE CommentaireForum
                SET commentaire_nombre_aime = commentaire_nombre_aime - 1
                WHERE id_commentaire = ?
            """, (id_commentaire,))

        cursor.execute("""
            INSERT INTO CommentaireForumLike (id_commentaire, nom_utilisateur, aime, aime_pas)
            VALUES (?, ?, FALSE, TRUE)
            ON CONFLICT(id_commentaire, nom_utilisateur)
            DO UPDATE SET aime = FALSE, aime_pas = TRUE
        """, (id_commentaire, nom_utilisateur))
        
        connexion.commit()

    def retirer_downvote_commentaire(self, id_commentaire, nom_utilisateur):
        connexion = self.get_connection()
        cursor = connexion.cursor()

        cursor.execute("""
            UPDATE CommentaireForum
            SET commentaire_nombre_aime = commentaire_nombre_aime + 1
            WHERE id_commentaire = ?
        """, (id_commentaire,))
        
        cursor.execute("""
            UPDATE CommentaireForumLike
            SET aime_pas = FALSE
            WHERE id_commentaire = ? AND nom_utilisateur = ?
        """, (id_commentaire, nom_utilisateur))
        
        connexion.commit()

    def upvote_post_forum(self, id_post, nom_utilisateur):
        connexion = self.get_connection()
        cursor = connexion.cursor()

        cursor.execute("""
            SELECT aime, aime_pas FROM PostForumLike 
            WHERE id_post = ? AND nom_utilisateur = ?
        """, (id_post, nom_utilisateur))
        result = cursor.fetchone()

        if result:
            current_aime, current_aime_pas = result
            if current_aime_pas:
                cursor.execute("""
                    UPDATE PostForum
                    SET nombre_total_aime = nombre_total_aime + 2
                    WHERE id_post = ?
                """, (id_post,))
            elif not current_aime:
                cursor.execute("""
                    UPDATE PostForum
                    SET nombre_total_aime = nombre_total_aime + 1
                    WHERE id_post = ?
                """, (id_post,))
        else:
            cursor.execute("""
                UPDATE PostForum
                SET nombre_total_aime = nombre_total_aime + 1
                WHERE id_post = ?
            """, (id_post,))

        cursor.execute("""
            INSERT INTO PostForumLike (id_post, nom_utilisateur, aime, aime_pas)
            VALUES (?, ?, TRUE, FALSE)
            ON CONFLICT(id_post, nom_utilisateur)
            DO UPDATE SET aime = TRUE, aime_pas = FALSE
        """, (id_post, nom_utilisateur))
        
        connexion.commit()

    def retirer_upvote_post_forum(self, id_post, nom_utilisateur):
        connexion = self.get_connection()
        cursor = connexion.cursor()

        cursor.execute("""
            UPDATE PostForum
            SET nombre_total_aime = nombre_total_aime - 1
            WHERE id_post = ?
        """, (id_post,))
        
        cursor.execute("""
            UPDATE PostForumLike
            SET aime = FALSE
            WHERE id_post = ? AND nom_utilisateur = ?
        """, (id_post, nom_utilisateur))
        connexion.commit()
    
    def downvote_post_forum(self, id_post, nom_utilisateur):
        connexion = self.get_connection()
        cursor = connexion.cursor()

        cursor.execute("""
            SELECT aime, aime_pas FROM PostForumLike 
            WHERE id_post = ? AND nom_utilisateur = ?
        """, (id_post, nom_utilisateur))
        result = cursor.fetchone()

        if result:
            current_aime, current_aime_pas = result
            if current_aime:
                cursor.execute("""
                    UPDATE PostForum
                    SET nombre_total_aime = nombre_total_aime - 2
                    WHERE id_post = ?
                """, (id_post,))
            elif not current_aime_pas:
                cursor.execute("""
                    UPDATE PostForum
                    SET nombre_total_aime = nombre_total_aime - 1
                    WHERE id_post = ?
                """, (id_post,))
        else:
            cursor.execute("""
                UPDATE PostForum
                SET nombre_total_aime = nombre_total_aime - 1
                WHERE id_post = ?
            """, (id_post,))

        cursor.execute("""
            INSERT INTO PostForumLike (id_post, nom_utilisateur, aime, aime_pas)
            VALUES (?, ?, FALSE, TRUE)
            ON CONFLICT(id_post, nom_utilisateur)
            DO UPDATE SET aime = FALSE, aime_pas = TRUE
        """, (id_post, nom_utilisateur))
        
        connexion.commit()

    def retirer_downvote_post_forum(self, id_post, nom_utilisateur):
        connexion = self.get_connection()
        cursor = connexion.cursor()

        cursor.execute("""
            UPDATE PostForum
            SET nombre_total_aime = nombre_total_aime + 1
            WHERE id_post = ?
        """, (id_post,))
        
        cursor.execute("""
            UPDATE PostForumLike
            SET aime_pas = FALSE
            WHERE id_post = ? AND nom_utilisateur = ?
        """, (id_post, nom_utilisateur))
        
        connexion.commit()
    
    def supprimer_post_forum(self, post_id):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute("DELETE FROM PostForum WHERE id_post = ?", (post_id,))
        connexion.commit()

    def update_post_forum(self, post_id, titre, description):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute("UPDATE PostForum SET titre = ?, description = ? WHERE id_post = ?", (titre, description, post_id))
        connexion.commit()

    def get_commentaire_forum(self, commentaire_id):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute("SELECT * FROM CommentaireForum WHERE id_commentaire = ?", (commentaire_id,))
        commentaire = cursor.fetchone()
        return commentaire

    def update_commentaire_forum(self, commentaire_id, contenu):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute("UPDATE CommentaireForum SET contenu = ? WHERE id_commentaire = ?", (contenu, commentaire_id))
        connexion.commit()

    def supprimer_commentaire_forum(self, commentaire_id):
       connexion = self.get_connection()
       cursor = connexion.cursor()
       cursor.execute("DELETE FROM CommentaireForum WHERE id_commentaire = ?", (commentaire_id,))
       connexion.commit()
    
    ## MESSAGERIE
   
    def get_boite_messagerie_id(self, connexion, nom_utilisateur):
        connexion = self.get_connection()
        connexion.row_factory = sqlite3.Row
        cursor = connexion.cursor()
        cursor.execute("SELECT id_boite_messagerie FROM BoiteMessagerie WHERE nom_utilisateur = ?", (nom_utilisateur,))
        return cursor.fetchone()[0]

    def get_conversation_messages(self, utilisateur_nom, recepteur_nom):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        query = """
        SELECT m.id_message, m.contenu, m.recepteur_nom, m.emetteur_nom, m.horodatage,
            r.nom_utilisateur AS recepteur_nom_utilisateur, r.nom AS recepteur_nom, r.prenom AS recepteur_prenom, r.photo_profil AS recepteur_photo_profil,
            e.nom_utilisateur AS emetteur_nom_utilisateur, e.nom AS emetteur_nom, e.prenom AS emetteur_prenom, e.photo_profil AS emetteur_photo_profil
        FROM Message m
        JOIN Utilisateur r ON m.recepteur_nom = r.nom_utilisateur
        JOIN Utilisateur e ON m.emetteur_nom = e.nom_utilisateur
        WHERE (m.emetteur_nom = ? AND m.recepteur_nom = ?) OR (m.emetteur_nom = ? AND m.recepteur_nom = ?)
        ORDER BY m.horodatage ASC
        """
        cursor.execute(query, (utilisateur_nom, recepteur_nom, recepteur_nom, utilisateur_nom))
        result_set = cursor.fetchall()
        return [build_message(item) for item in result_set]
    
    def ajouter_message(self, emetteur_nom, recepteur_nom, contenu):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        
        query_message = """
        INSERT INTO Message(contenu, recepteur_nom, emetteur_nom, horodatage)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(query_message, (contenu, recepteur_nom, emetteur_nom, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        message_id = cursor.lastrowid

        query_boite_emetteur = """
        INSERT INTO Message_BoiteMessagerie(id_message, id_boite_messagerie)
        VALUES (?, (SELECT id_boite_messagerie FROM BoiteMessagerie WHERE nom_utilisateur = ?))
        """
        cursor.execute(query_boite_emetteur, (message_id, emetteur_nom))

        query_boite_recepteur = """
        INSERT INTO Message_BoiteMessagerie(id_message, id_boite_messagerie)
        VALUES (?, (SELECT id_boite_messagerie FROM BoiteMessagerie WHERE nom_utilisateur = ?))
        """
        cursor.execute(query_boite_recepteur, (message_id, recepteur_nom))

        connexion.commit()