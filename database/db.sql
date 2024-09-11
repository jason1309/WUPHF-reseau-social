/* NETTOYAGE DE LA BD */
DROP TABLE IF EXISTS Utilisateur_Groupe;
DROP TABLE IF EXISTS Article;
DROP TABLE IF EXISTS Service;
DROP TABLE IF EXISTS Groupe;
DROP TABLE IF EXISTS CommentaireReseau;
DROP TABLE IF EXISTS CommentaireForum;
DROP TABLE IF EXISTS PostForum;
DROP TABLE IF EXISTS PostReseau;
DROP TABLE IF EXISTS Message;
DROP TABLE IF EXISTS Message_BoiteMessagerie;
DROP TABLE IF EXISTS BoiteMessagerie;
DROP TABLE IF EXISTS Utilisateur;
DROP TABLE IF EXISTS Abonnement;
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS PostReseauLike;
DROP TABLE IF EXISTS CommentaireReseauLike;
DROP TABLE IF EXISTS PostForumLike;
DROP TABLE IF EXISTS CommentaireForumLike;

/* CREATION DES TABLES */
CREATE TABLE IF NOT EXISTS Utilisateur(
    nom_utilisateur VARCHAR(20) PRIMARY KEY,
    password VARCHAR(20) NOT NULL,
    salt VARCHAR(250) NOT NULL,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    photo_profil VARCHAR(250) DEFAULT '/img/profil/default.png',
    biographie TEXT
);

CREATE TABLE IF NOT EXISTS Article(
    id_article INTEGER PRIMARY KEY AUTOINCREMENT,
    titre VARCHAR(100) NOT NULL,
    prix NUMERIC(8,2) NOT NULL
        CHECK(prix >= 0),
    description TEXT,
    image VARCHAR(250) NOT NULL,
    nom_vendeur VARCHAR(50),
    FOREIGN KEY(nom_vendeur) REFERENCES Utilisateur(nom_utilisateur)
);

CREATE TABLE IF NOT EXISTS Service(
    id_service INTEGER PRIMARY KEY AUTOINCREMENT,
    titre VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    prix NUMERIC(8,2) NOT NULL
        CHECK(prix >= 0),
    horaire VARCHAR(100),
    evaluation INTEGER DEFAULT 0
        CHECK(evaluation >= 0),
    nom_vendeur VARCHAR(50),
    FOREIGN KEY(nom_vendeur) REFERENCES Utilisateur(nom_utilisateur)
);

CREATE TABLE IF NOT EXISTS PostForum (
    id_post INTEGER PRIMARY KEY AUTOINCREMENT,
    titre VARCHAR(50) NOT NULL,
    nom_auteur VARCHAR(50),
    horodatage TEXT NOT NULL,
    description TEXT NOT NULL,
    nombre_total_aime INTEGER DEFAULT 0,
    FOREIGN KEY(nom_auteur) REFERENCES Utilisateur(nom_utilisateur)
);

CREATE TABLE IF NOT EXISTS PostReseau (
    id_post INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_auteur VARCHAR(50),
    horodatage TEXT NOT NULL,
    description TEXT,
    nombre_total_aime INTEGER DEFAULT 0
        CHECK(nombre_total_aime >= 0),
    image VARCHAR(250) NOT NULL,
    FOREIGN KEY(nom_auteur) REFERENCES Utilisateur(nom_utilisateur)
);

CREATE TABLE IF NOT EXISTS CommentaireReseau (
    id_commentaire INTEGER PRIMARY KEY AUTOINCREMENT,
    contenu TEXT NOT NULL,
    nom_auteur VARCHAR(50),
    id_post INTEGER,
    horodatage TEXT NOT NULL,
    nombre_total_aime INTEGER DEFAULT 0
        CHECK(nombre_total_aime >= 0),
    FOREIGN KEY(nom_auteur) REFERENCES Utilisateur(nom_utilisateur), 
    FOREIGN KEY(id_post) REFERENCES  PostReseau(id_post) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS CommentaireForum (
    id_commentaire INTEGER PRIMARY KEY AUTOINCREMENT,
    contenu TEXT NOT NULL,
    nom_auteur VARCHAR(50),
    id_post INTEGER,
    horodatage TEXT NOT NULL,
    commentaire_nombre_aime INTEGER DEFAULT 0,
    FOREIGN KEY(nom_auteur) REFERENCES Utilisateur(nom_utilisateur),
    FOREIGN KEY(id_post) REFERENCES  PostForum(id_post)
);

CREATE TABLE IF NOT EXISTS BoiteMessagerie (
    id_boite_messagerie INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_utilisateur VARCHAR(20),
    FOREIGN KEY(nom_utilisateur) REFERENCES Utilisateur(nom_utilisateur)
);

CREATE TABLE IF NOT EXISTS Message (
    id_message INTEGER PRIMARY KEY AUTOINCREMENT,
    contenu TEXT NOT NULL,
    recepteur_nom VARCHAR(20),
    emetteur_nom VARCHAR(20),
    horodatage TEXT NOT NULL,
    FOREIGN KEY(recepteur_nom) REFERENCES Utilisateur(nom_utilisateur),
    FOREIGN KEY(emetteur_nom) REFERENCES Utilisateur(nom_utilisateur)
);

CREATE TABLE IF NOT EXISTS Message_BoiteMessagerie (
    id_message INTEGER,
    id_boite_messagerie INTEGER,
    FOREIGN KEY(id_message) REFERENCES Message(id_message),
    FOREIGN KEY(id_boite_messagerie) REFERENCES BoiteMessagerie(id_boite_messagerie),
    PRIMARY KEY(id_message, id_boite_messagerie)
);

CREATE TABLE IF NOT EXISTS Abonnement (
    nom_utilisateur VARCHAR(20),
    abonnement_nom_utilisateur VARCHAR(20),
    FOREIGN KEY(nom_utilisateur) REFERENCES Utilisateur(nom_utilisateur),
    FOREIGN KEY(abonnement_nom_utilisateur) REFERENCES Utilisateur(nom_utilisateur),
    PRIMARY KEY(nom_utilisateur, abonnement_nom_utilisateur)
);

CREATE TABLE IF NOT EXISTS sessions (
    session_id VARCHAR(250) PRIMARY KEY,
    nom_utilisateur VARCHAR(20),
    FOREIGN KEY(nom_utilisateur) REFERENCES Utilisateur(nom_utilisateur)
);

CREATE TABLE IF NOT EXISTS PostReseauLike (
    id_post INTEGER,
    nom_utilisateur VARCHAR(20),
    PRIMARY KEY(id_post, nom_utilisateur),
    FOREIGN KEY(id_post) REFERENCES PostReseau(id_post),
    FOREIGN KEY(nom_utilisateur) REFERENCES Utilisateur(nom_utilisateur)
);

CREATE TABLE IF NOT EXISTS CommentaireReseauLike (
    id_commentaire INTEGER,
    nom_utilisateur VARCHAR(20),
    PRIMARY KEY(id_commentaire, nom_utilisateur),
    FOREIGN KEY(id_commentaire) REFERENCES CommentaireReseau(id_commentaire),
    FOREIGN KEY(nom_utilisateur) REFERENCES Utilisateur(nom_utilisateur)
);

CREATE TABLE IF NOT EXISTS PostForumLike (
    id_post INTEGER,
    nom_utilisateur VARCHAR(20),
    aime BOOLEAN DEFAULT FALSE,
    aime_pas BOOLEAN DEFAULT FALSE,
    PRIMARY KEY(id_post, nom_utilisateur),
    FOREIGN KEY(id_post) REFERENCES PostReseau(id_post),
    FOREIGN KEY(nom_utilisateur) REFERENCES Utilisateur(nom_utilisateur)
);

CREATE TABLE IF NOT EXISTS CommentaireForumLike (
    id_commentaire INTEGER,
    nom_utilisateur VARCHAR(20),
    aime BOOLEAN DEFAULT FALSE,
    aime_pas BOOLEAN DEFAULT FALSE,
    PRIMARY KEY(id_commentaire, nom_utilisateur),
    FOREIGN KEY(id_commentaire) REFERENCES CommentaireReseau(id_commentaire),
    FOREIGN KEY(nom_utilisateur) REFERENCES Utilisateur(nom_utilisateur)
);

/* INSERTION */

/* UTILISATEURS */

INSERT INTO Utilisateur(nom_utilisateur, password, nom, prenom, email, salt, photo_profil, biographie)
VALUES("JohnTheGoat", "ihatecat", "Gagné", "Jeffréy", "cathater@gmail.com", "111", "img/profil/jeffrey.png", "Je ne vis que pour mon chien!");

INSERT INTO Utilisateur(nom_utilisateur, password, nom, prenom, email, salt, photo_profil, biographie)
VALUES("LittleDog", "chien", "Builder", "Bob", "chien@chien.com", "222", "img/profil/GAB.png", "La vie d'un homme et son chien.");

INSERT INTO Utilisateur(nom_utilisateur, password, nom, prenom, email, salt, photo_profil, biographie)
VALUES("Jimothy", "goodpassword", "Halpert", "Jim", "jim.halpert@dundermifflin.com", "333", "img/profil/Jim.jpg", "Mon chien s'appelle Pam. Ma femme aussi.");

INSERT INTO Utilisateur(nom_utilisateur, password, nom, prenom, email, salt, photo_profil, biographie)
VALUES("Dwight", "BearsBeets", "Shrute", "Dwight", "dwight.k.shrute@dundermifflin.com", "444", "img/profil/dwight.jpg", "Dogs, Beets... Battlestar Galactica!");

INSERT INTO Utilisateur(nom_utilisateur, password, nom, prenom, email, salt, photo_profil, biographie)
VALUES("WhatIsUpdog", "password", "Scott", "Michael", "michael.j.scott@dundermifflin.com", "555", "img/profil/michael.jpg", "La seule chose que j'aime plus que mon chien est le papier!");

INSERT INTO Utilisateur(nom_utilisateur, password, nom, prenom, email, salt, photo_profil, biographie)
VALUES("RyFromWHUPHF", "rywhuphf", "Howard", "Ryan", "ryan.howard@dundermifflin.com", "667", "img/profil/ryan.jpg", "Kelly arrête de regarder mon profil. Merci.");

INSERT INTO Utilisateur(nom_utilisateur, password, nom, prenom, email, salt, photo_profil, biographie)
VALUES("TheNardDog", "nardog123", "Bernard", "Andy", "andy.bernard@dundermifflin.com", "777", "img/profil/andy.jfif", "Survivant d'un séminaire sur le contrôle de la colère." );

/* MESSAGERIES */

INSERT INTO BoiteMessagerie(nom_utilisateur) VALUES("JohnTheGoat");

INSERT INTO BoiteMessagerie(nom_utilisateur) VALUES ("LittleDog");

/* ARTICLES */

INSERT INTO Article(titre, prix, description, image, nom_vendeur)
VALUES("Manteau rose", 5000.0, "Un beau manteau rose! Porter une seule fois.", "img/article/manteau_rose.png", "JohnTheGoat");

INSERT INTO Article(titre, prix, description, image, nom_vendeur)
VALUES("Lit superposé pour grand chien", 5.50, "Très beau lit superposé. Je dois m'en débarrasser puisque mon chien est décédé en tombant du lit", "img/article/lit_chien.png", "JohnTheGoat");

INSERT INTO Article(titre, prix, description, image, nom_vendeur)
VALUES("Laisse", 50.0, "Ça doit partir", "img/article/laisse.png", "LittleDog");

INSERT INTO Article(titre, prix, description, image, nom_vendeur)
VALUES("Bols pour eau et nourriture", 300.0, "Bol en acier innoxidable avec boitier de bois fait à la main avec des arbres de ma ferme. Je vend au plus offrant!", "img/article/bowls.jpg", "Dwight");

INSERT INTO Article(titre, prix, description, image, nom_vendeur)
VALUES("Piscine pour CHIENS (ATTENTION, PAS FAIT POUR LES HUMAINS)", 75.0, "Je croyais que c'étais une piscine pour humain... Utilisé une seule fois.", "img/article/dog-pool2.webp", "WhatIsUpdog");

INSERT INTO Article(titre, prix, description, image, nom_vendeur)
VALUES("Barrière pour chiens", 62.0, "Mon chien est bien élevé maintenant, je n'en ai plus besoin.", "img/article/dog-gate.jpg", "Jimothy");

/* SERVICES */

INSERT INTO Service(titre, description, prix, horaire, evaluation, nom_vendeur)
VALUES("Disponible pour promener vos chiens", "Disponible pour promener vos chiens. Une marche d'environ 20km, j'accepte seulement les chihuahuas.", 50.0, "Lun-Ven 18-22", 0, "JohnTheGoat");

INSERT INTO Service(titre, description, prix, horaire, evaluation, nom_vendeur)
VALUES("Gardiennage", "Disponible pour garder vos chiens. J'accepte seulement les chihuahuas.", 30.0, "Sam-Dim 9-18", 0, "JohnTheGoat");

INSERT INTO Service(titre, description, prix, horaire, evaluation, nom_vendeur)
VALUES("Toilettage", "Je me déplace à votre domicile pour effectuer le nettoyage de vos précieux pitous! Le prix indiqué est le prix de base, il peut y avoir un surplus selon la distance.",60.0, "Lundi-Vendredi 9-17", 0, "TheNardDog");

INSERT INTO Service(titre, description, prix, horaire, evaluation, nom_vendeur)
VALUES("Gardiennage", "Je suis à votre disposition pour garder votre chien. Le prix est par semaine. Veuillez me contacter pour plus d'informations.", 100.0, "Lundi à Dimanche, 24h sur 24", 0, "Jimothy");

INSERT INTO Service(titre, description, prix, horaire, evaluation, nom_vendeur)
VALUES("Musculation", "Service de musculation pour votre chien! Gain assurer!", 500.0, "Sam-Dim 9-18", 0, "Dwight");

/* POSTS RESEAU */

INSERT INTO PostReseau(nom_auteur, horodatage, description, nombre_total_aime, image)
VALUES("LittleDog",'2024-09-05 16:30:00' , "Merlin le chien", 0, '/img/Post_reseau/merlin.jpg');

INSERT INTO PostReseau(nom_auteur, horodatage, description, nombre_total_aime, image)
VALUES("LittleDog",'2024-09-01 14:30:00', "Mon chien", 1, '/img/Post_reseau/merlin2.jpg');

INSERT INTO PostReseau(nom_auteur, horodatage, description, nombre_total_aime, image)
VALUES("JohnTheGoat",'2024-08-22 16:40:11', "So pretty !", 2, '/img/Post_reseau/lilia_sleep.png');

INSERT INTO PostReseau(nom_auteur, horodatage, description, nombre_total_aime, image)
VALUES("Jimothy",'2024-08-22 16:40:11', "Notre chien c'est fait un ami!", 12, '/img/Post_reseau/cute-pugs.webp');

INSERT INTO PostReseau(nom_auteur, horodatage, description, nombre_total_aime, image)
VALUES("Dwight",'2024-08-24 16:40:11', "J'ai acheté un nouveau chien pour ma copine. Il s'appelle Poubelle!", 5, '/img/Post_reseau/funny-bulldog.webp');

INSERT INTO PostReseau(nom_auteur, horodatage, description, nombre_total_aime, image)
VALUES("WhatIsUpdog",'2024-08-25 16:40:11', "Je voulais devenir ami avec ce chien mais il c'est enfuit...", 1, '/img/Post_reseau/run_lab.webp');

INSERT INTO PostReseau(nom_auteur, horodatage, description, nombre_total_aime, image)
VALUES("RyFromWHUPHF",'2024-08-26 12:10:19', "La nouvelle mascotte de WHUPHF!!", 17, '/img/Post_reseau/cute_samoyed.webp');

INSERT INTO PostReseau(nom_auteur, horodatage, description, nombre_total_aime, image)
VALUES("TheNardDog",'2024-08-26 18:30:11', "Le chien du Nard-Dog!", 6, '/img/Post_reseau/cute-bernese.jpg');

INSERT INTO PostReseau(nom_auteur, horodatage, description, nombre_total_aime, image)
VALUES("WhatIsUpdog",'2024-08-28 19:42:48', "J'ai payé un photoshoot à mon chien, seulement 500$!", 2, '/img/Post_reseau/golden-retriever.jpg');

INSERT INTO PostReseau(nom_auteur, horodatage, description, nombre_total_aime, image)
VALUES("JohnTheGoat",'2024-08-29 19:42:48', "Mon chien prend un coup de soleil", 2, '/img/Post_reseau/lilia_soleil.png');

INSERT INTO PostReseau(nom_auteur, horodatage, description, nombre_total_aime, image)
VALUES("JohnTheGoat",'2024-08-30 19:42:48', "Lilia aime bien prendre des selfies!", 6, '/img/Post_reseau/lilia_selfie.png');

INSERT INTO PostReseau(nom_auteur, horodatage, description, nombre_total_aime, image)
VALUES("Dwight",'2024-09-06 19:43:48', "Regarder la nouvelle robe de mon chien!", 5, '/img/Post_reseau/lilia_jupe.png');

/* COMMENTAIRE RESEAU */

INSERT INTO CommentaireReseau(contenu, nom_auteur, id_post, horodatage)
VALUES("Très beau ton chien", "JohnTheGoat", 2, '2024-09-06 14:32:00');

INSERT INTO CommentaireReseau(contenu, nom_auteur, id_post, horodatage)
VALUES("First !!", "JohnTheGoat", 1, '2024-09-06 16:37:00' );

INSERT INTO CommentaireReseau(contenu, nom_auteur, id_post, horodatage)
VALUES("Avec son jouet!!", "LittleDog", 1, '2024-09-06 16:35:00'  );

INSERT INTO CommentaireReseau(contenu, nom_auteur, id_post, horodatage)
VALUES("Non, désolé John..", "LittleDog", 1, '2024-09-06 16:38:00'  );

INSERT INTO CommentaireReseau(contenu, nom_auteur, id_post, horodatage)
VALUES("tb#@*", "JohnTheGoat", 1, '2024-09-06 16:39:00'  );

/* ABONNEMENT */

INSERT INTO Abonnement(nom_utilisateur, abonnement_nom_utilisateur) VALUES("JohnTheGoat", "LittleDog"); 

INSERT INTO Abonnement(nom_utilisateur, abonnement_nom_utilisateur) VALUES("LittleDog", "JohnTheGoat");

INSERT INTO Abonnement(nom_utilisateur, abonnement_nom_utilisateur) VALUES("JohnTheGoat", "WhatIsUpdog");

INSERT INTO Abonnement(nom_utilisateur, abonnement_nom_utilisateur) VALUES("JohnTheGoat", "TheNardDog");

INSERT INTO Abonnement(nom_utilisateur, abonnement_nom_utilisateur) VALUES("JohnTheGoat", "RyFromWHUPHF");

INSERT INTO Abonnement(nom_utilisateur, abonnement_nom_utilisateur) VALUES("JohnTheGoat", "Dwight");

INSERT INTO Abonnement(nom_utilisateur, abonnement_nom_utilisateur) VALUES("JohnTheGoat", "Jimothy");


/* BOITEMESSAGERIE */

INSERT INTO BoiteMessagerie(nom_utilisateur) VALUES ("JohnTheGoat");
INSERT INTO BoiteMessagerie(nom_utilisateur) VALUES ("LittleDog");
INSERT INTO BoiteMessagerie(nom_utilisateur) VALUES ("Dwight");
INSERT INTO BoiteMessagerie(nom_utilisateur) VALUES ("Jimothy");
INSERT INTO BoiteMessagerie(nom_utilisateur) VALUES ("RyFromWHUPHF");

/* MESSAGES */

INSERT INTO Message(contenu, recepteur_nom, emetteur_nom, horodatage) 
VALUES("Salut, comment vas-tu?", "JohnTheGoat", "LittleDog", '2024-07-28 20:39:00');

INSERT INTO Message(contenu, recepteur_nom, emetteur_nom, horodatage) 
VALUES("Salut! Ça va et toi?", "LittleDog", "JohnTheGoat", '2024-07-28 20:39:30');

INSERT INTO Message(contenu, recepteur_nom, emetteur_nom, horodatage) 
VALUES("Bien merci! Je voulais savoir comment tu avais élever ton chiens, il est tellement gentil et docile. Aurais-tu un éleveur à me recommander?", "JohnTheGoat", "LittleDog", '2024-07-28 20:41:00');

INSERT INTO Message(contenu, recepteur_nom, emetteur_nom, horodatage) 
VALUES("Bonjour Dwight, est-ce qu'on se voyait toujours pour écouter Battlestar Galactica ensemble?", "Dwight", "JohnTheGoat", '2024-07-28 20:39:00');

INSERT INTO Message(contenu, recepteur_nom, emetteur_nom, horodatage) 
VALUES("J'aime tellement mieux mon atmosphère de travail à Stanford!", "JohnTheGoat", "Jimothy", '2024-07-28 20:39:30');

INSERT INTO Message(contenu, recepteur_nom, emetteur_nom, horodatage) 
VALUES("Je pense que je vais laisser Kelly... Je pense avoir un chance avec Erin ;P", "RyFromWHUPHF", "JohnTheGoat", '2024-07-28 20:41:00');

/* MESSAGE_BOITEMESSAGERIE */

INSERT INTO Message_BoiteMessagerie(id_message, id_boite_messagerie) VALUES (1, 1); -- JohnTheGoat
INSERT INTO Message_BoiteMessagerie(id_message, id_boite_messagerie) VALUES (1, 2); -- LittleDog

INSERT INTO Message_BoiteMessagerie(id_message, id_boite_messagerie) VALUES (2, 1); -- JohnTheGoat
INSERT INTO Message_BoiteMessagerie(id_message, id_boite_messagerie) VALUES (2, 2); -- LittleDog

INSERT INTO Message_BoiteMessagerie(id_message, id_boite_messagerie) VALUES (3, 1); -- JohnTheGoat
INSERT INTO Message_BoiteMessagerie(id_message, id_boite_messagerie) VALUES (3, 2); -- LittleDog

INSERT INTO Message_BoiteMessagerie(id_message, id_boite_messagerie) VALUES (4, 1); -- JohnTheGoat
INSERT INTO Message_BoiteMessagerie(id_message, id_boite_messagerie) VALUES (4, 3); -- Dwight

INSERT INTO Message_BoiteMessagerie(id_message, id_boite_messagerie) VALUES (5, 1); -- JohnTheGoat
INSERT INTO Message_BoiteMessagerie(id_message, id_boite_messagerie) VALUES (5, 4); -- Jimothy

INSERT INTO Message_BoiteMessagerie(id_message, id_boite_messagerie) VALUES (6, 1); -- JohnTheGoat
INSERT INTO Message_BoiteMessagerie(id_message, id_boite_messagerie) VALUES (6, 5); -- RyFromWHUPHF
/* POSTFORUM */

INSERT INTO PostForum (id_post, titre, nom_auteur, horodatage, description, nombre_total_aime) VALUES
(1, "Besoin d'aide, mon chien a une bosse énorme sur la tête!! Quoi faire??", "JohnTheGoat", "2024-08-02 14:30:00", "Je me suis levé un bon matin et mon chien avait une bosse sur la tête, ça vous est déjà arrivé? Les vétérinaires ne veulent que mon argent... Mais ils n'y toucheront pas!", 6),
(2, "Conseils de dressage, y a-t-il des césars ici?", "LittleDog", "2024-07-06 09:15:00", "Quels sont vos meilleurs conseils pour dresser un chiot ? Mon nouveau chiot est très énergique.", 12),
(3, "Ma femme est jalouse de l'amour que je donne à mon chien HELP!", "Jimothy", "2024-07-27 11:00:00", "Quel est votre parc à chiens préféré en ville ? J'aimerais trouver un nouvel endroit pour promener mon chien.", 4),
(4, "Comment démontrez à mon chien que je l'adore au tant que Starcraft??", "Dwight", "2024-07-08 16:45:00", "Quelle est la meilleure marque de nourriture pour chien selon vous ? Mon chien a des allergies.", 3),
(5, "Dites-moi vos meilleurs blagues sur les chiens", "WhatIsUpdog", "2024-07-09 12:30:00", "Quels sont les meilleurs jeux pour occuper un chien à la maison ?", 7),
(6, "Je vis dans un garde-robe, est-ce trop petit pour un chien?", "RyFromWHUPHF", "2024-08-01 14:00:00", "Je cherche un vétérinaire de confiance dans la région. Avez-vous des recommandations ?", 2),
(7, "Je fais de l'art avec une intelligence artificielle, voici quelques photos de chiens!", "TheNardDog", "2024-07-11 18:20:00", "Partagez vos meilleures photos de chiens ici !", 7),
(8, "Voyager avec un chien, comment vous y prendre selon moi. Je suis un grand connaisseur!", "JohnTheGoat", "2024-07-12 10:10:00", "Des astuces pour voyager avec un chien ? Je prévois un long voyage en voiture.", 4),
(9, "Aider moi à trouver un nom pour mon chien!", "LittleDog", "2024-07-13 17:00:00", "Je pense à adopter un deuxième chien. Des conseils sur comment préparer l'arrivée d'un nouveau chien à la maison ?", 2),
(10, "Entre 20 chihuahua et 1 labrador, qui gagne dans un combat?", "Jimothy", "2024-07-14 13:50:00", "Quels accessoires pour chien sont vraiment utiles et lesquels sont superflus selon vous ?", 10);

/* COMMENTAIRE FORUM */

INSERT INTO CommentaireForum (id_commentaire, contenu, nom_auteur, id_post, horodatage, commentaire_nombre_aime) VALUES
(1,	"Non cela ne m'aie jamais arrivé, peut-être que ton chien va mourir honnêtement", "TheNardDog",	1, "2024-08-02 19:30:00", 50),
(2, "Peut-être que c'est une piqûre d'insecte. Consulte un autre vétérinaire pour un deuxième avis.", "LittleDog", 1, "2024-08-02 15:45:00", 1),
(3, "Il faudrait surveiller ça de près. Si ça empire, retourne voir un vétérinaire.", "Jimothy", 1, "2024-08-02 17:20:00", 3),
(4, "Pour dresser un chiot, la constance est la clé. Utilise des récompenses pour renforcer les bons comportements.", "JohnTheGoat", 2, "2024-07-06 10:30:00", 3),
(5, "Les séances d'entraînement courtes et fréquentes fonctionnent mieux.", "RyFromWHUPHF", 2, "2024-07-06 11:00:00", 2),
(6, "Ma femme est pareille! Essaie de leur accorder du temps individuellement.", "Dwight", 3, "2024-07-27 12:00:00", 1),
(7, "Peut-être organiser des activités où tu inclues les deux.", "WhatIsUpdog", 3, "2024-07-27 12:30:00", 9),
(8, "Pour les allergies, essaie la nourriture hypoallergénique. Ça a bien fonctionné pour mon chien.", "LittleDog", 4, "2024-07-08 17:30:00", 3),
(9, "Il y a des marques spécialisées pour les chiens avec allergies, consulte ton vétérinaire.", "Jimothy", 4, "2024-07-08 18:00:00", 1),
(10, "Pourquoi les chiens n'aiment-ils pas les blagues? Parce qu'ils les trouvent toutoures nulles!", "JohnTheGoat", 5, "2024-07-09 13:00:00", 4),
(11, "Quel est le sport préféré des chiens? Le tennis de chien bien sûr!", "RyFromWHUPHF", 5, "2024-07-09 13:30:00", 2),
(12, "Ça dépend du chien, mais généralement un espace plus grand est préférable.", "TheNardDog", 6, "2024-08-01 14:30:00", 1),
(13, "Essaie de le sortir souvent pour compenser l'espace limité.", "WhatIsUpdog", 6, "2024-08-01 15:00:00", 2),
(14, "Superbes photos! Tu utilises quel logiciel pour créer ces images?", "LittleDog", 7, "2024-07-11 19:00:00", 3),
(15, "C'est incroyable! As-tu d'autres photos à partager?", "Jimothy", 7, "2024-07-11 19:30:00", 2),
(16, "Assure-toi d'avoir beaucoup d'eau et de faire des pauses fréquentes.", "Dwight", 8, "2024-07-12 10:45:00", 2),
(17, "J'utilise un harnais spécial pour la voiture, c'est beaucoup plus sûr.", "RyFromWHUPHF", 8, "2024-07-12 11:00:00", 1),
(18, "Pourquoi pas 'Buddy' ou 'Max' ? Ce sont des noms classiques.", "TheNardDog", 9, "2024-07-13 17:30:00", 1),
(19, "J'aime bien le nom 'Rocky'. Ça sonne bien pour un chien.", "WhatIsUpdog", 9, "2024-07-13 18:00:00", 0),
(20, "Je parie sur le labrador, ils sont plus grands et plus forts.", "JohnTheGoat", 10, "2024-07-14 14:30:00", 3),
(21, "Les chihuahuas pourraient avoir l'avantage du nombre, mais je pense que le labrador gagnerait.", "RyFromWHUPHF", 10, "2024-07-14 15:00:00", 2);

INSERT INTO CommentaireForumLike (id_commentaire, nom_utilisateur, aime, aime_pas) 
VALUES (2, "JohnTheGoat", true, false);


INSERT INTO PostForumLike (id_post, nom_utilisateur, aime, aime_pas) 
VALUES (1, "JohnTheGoat", true, false);

INSERT INTO PostForumLike (id_post, nom_utilisateur, aime, aime_pas) 
VALUES (2, "JohnTheGoat", false, true);
