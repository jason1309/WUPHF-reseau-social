from .app_database import Database
import uuid
import os
import random
from werkzeug.utils import secure_filename
import pytz
from datetime import datetime
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    g,
    session,
    jsonify
)

app = Flask(__name__, static_url_path="", static_folder="static")

app.config['SECRET_KEY'] = "cetteClefEstTresSecreteWUPHF"

DOSSIER_SAVE = 'static/img/Post_reseau'
DOSSIER_UPLOAD = 'img/Post_reseau'
app.config['DOSSIER_SAVE'] = DOSSIER_SAVE
app.config['DOSSIER_UPLOAD'] = DOSSIER_UPLOAD

DOSSIER_SAVE_ARTICLE = 'static/img/article'
DOSSIER_UPLOAD_ARTICLE = 'img/article'
app.config['DOSSIER_SAVE_ARTICLE'] = DOSSIER_SAVE_ARTICLE
app.config['DOSSIER_UPLOAD_ARTICLE'] = DOSSIER_UPLOAD_ARTICLE

error_msg = {
    "404": "La page que vous tentez de rejoindre n'existe pas...",
    "400": "Erreur dans la requête"
}

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.disconnect()

@app.context_processor
def inject_user():
    if 'user' in session:
        utilisateur_infos = get_db().get_utilisateur_info(session['user'])
        return {'utilisateur': utilisateur_infos}
    return {'utilisateur': None}

## HOME ##
@app.route("/", methods=["GET", "POST"])
def index():
    if 'user' in session:
        nom_utilisateur = session['user']
        utilisateur_infos = get_db().get_utilisateur_info(nom_utilisateur)
        
        search_query = request.args.get('search', '').lower()
        if search_query:
            posts_reseau = get_db().search_posts_reseau(search_query)
        else:
            posts_reseau = get_db().get_posts_reseau_abonnement(nom_utilisateur)
            
        posts_reseau = preparer_posts(posts_reseau)
        return render_template("reseau/index.html", utilisateur=utilisateur_infos, posts_reseau=posts_reseau, active_page='accueil')
    return redirect(url_for('connexion'))

## ROUTES ##

@app.route("/connexion", methods=["GET", "POST"])
def connexion():
    if request.method == "POST":
        nom_utilisateur = request.form["nom_utilisateur"]
        mot_de_passe = request.form["mot_de_passe"]
        utilisateur_infos = get_db().get_utilisateur_login_info(nom_utilisateur)
        if utilisateur_infos and utilisateur_infos["Password"] == mot_de_passe:
            session_id = str(uuid.uuid4()) 
            session['user'] = nom_utilisateur
            session['sid'] = session_id
            get_db().save_session(session_id, nom_utilisateur)
            return redirect(url_for('index'))
        return render_template("auth.html", error="Nom d'utilisateur ou mot de passe incorrect")
    return render_template("auth.html")


@app.route("/deconnexion")
def deconnexion():
    if 'user' in session:
        get_db().delete_session(session["sid"])
        session.pop('user', None)
    return redirect(url_for('connexion'))


@app.route("/forum")
def forum():
    posts = get_db().get_all_posts_forum(session['user'])
    for post in posts:
        post['horodatage'] = calculer_temps(post['horodatage'])
        post['nombre_commentaire'] = get_db().get_nb_commentaire_post_forum(post['id_post'])
    return render_template("forum/forum.html", posts=posts)


@app.route('/conversation/', defaults={'recepteur_nom': None})
@app.route('/conversation/<recepteur_nom>')
def afficher_conversation_avec_utilisateur(recepteur_nom):
    utilisateur_actuel = session['user']
    db = get_db()
    recepteur = db.get_utilisateur_info(recepteur_nom)
    abonnes = db.get_conversation(utilisateur_actuel)
    if recepteur_nom is None:
        messages = []
        error_message = "Aucun utilisateur sélectionné."
    else:
        messages = db.get_conversation_messages(utilisateur_actuel, recepteur_nom)
        error_message = None
    current_datetime = datetime.now()
    return render_template('inbox.html', messages=messages, utilisateur_actuel=utilisateur_actuel, abonnes=abonnes, current_datetime=current_datetime, recepteur=recepteur, error_message=error_message)


@app.route("/forum/<id_post>")
def forum_publication(id_post):
    nom_utilisateur = session['user']
    db = get_db()
    post_forum = db.get_post_forum(id_post, nom_utilisateur)
    post_forum['horodatage'] = calculer_temps(post_forum['horodatage'])
    
    commentaires = db.get_commentaires_forum(id_post, nom_utilisateur)
    for commentaire in commentaires:
        commentaire['horodatage'] = calculer_temps(commentaire['horodatage'])
    
    return render_template("forum/postforum.html", post_forum=post_forum, commentaires=commentaires)


@app.route("/marketplace", methods=["GET"])
def marketplace():
    articles = get_db().get_all_articles()
    return render_template("marketplace/market.html", articles = articles)

@app.route("/article/<id_article>", methods=["GET"])
def article(id_article):
    articlePrimaire = get_db().get_article(id_article)
    articles = get_db().get_all_user_articles(articlePrimaire.vendeur.nom_utilisateur)
    return render_template("marketplace/article.html", articlePrimaire=articlePrimaire, articles=articles)

@app.route("/mise-en-vente", methods=["GET", "POST"])
def mise_en_vente():
    if request.method == 'POST':
        nom_vendeur = session['user']
        titre_article = request.form['titre_article']
        prix_article = request.form['prix_article']
        description_article = request.form['description_article']        
        if 'photo' not in request.files:
            return redirect(request.url)
        file = request.files['photo']
        if file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['DOSSIER_SAVE_ARTICLE'], filename))
            image_article = os.path.join(app.config['DOSSIER_UPLOAD_ARTICLE'], filename)
        id_article = get_db().add_article(titre_article, prix_article, description_article, image_article, nom_vendeur)
        return redirect(url_for("article", id_article=id_article))
    return render_template("marketplace/addarticle.html")

@app.route("/modifier-article/<id_article>", methods=["POST"])
def modifier_article(id_article):
    db = get_db()
    if "form-mod-article" in request.form:
        print("Form 'form-mod-article' detected")
        titre_article = request.form['titre_article']
        prix_article = request.form['prix_article']
        description_article = request.form['description_article']
        if 'photo' not in request.files:
            print("No photo in request.files")
            return redirect(request.url)
        image = request.files['photo']
        if image.filename:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['DOSSIER_SAVE_ARTICLE'], filename))
            image_path = os.path.join(app.config['DOSSIER_UPLOAD_ARTICLE'], filename)
        else:
            image_path = request.form["img_path"]
        db.update_article(titre_article, prix_article, description_article, image_path, id_article)
        articlePrimaire = db.get_article(id_article)
        articles = db.get_all_user_articles(articlePrimaire.vendeur.nom_utilisateur)
        return render_template("marketplace/article.html", articlePrimaire=articlePrimaire, articles=articles)
    article = db.get_article(id_article)
    return render_template("marketplace/modifierarticle.html", article=article)

@app.route("/article-en-vente", methods=["GET"])
def article_en_vente():
    articles = get_db().get_all_user_articles(session['user'])
    return render_template("marketplace/myarticles.html", articles = articles)

@app.route("/service", methods=["GET"])
def service():
    services = get_db().get_all_services()
    random.shuffle(services)
    
    return render_template("service/service.html", services = services)

@app.route("/utilisateur-service", methods=["GET"])
def utilisateur_service():
    nom_utilisateur = session['user']
    services = get_db().get_utilisateur_services(nom_utilisateur)
    return render_template("service/serviceutilisateur.html", services = services)

@app.route("/profile", methods=["GET"])
def profile():
    db = get_db()
    username = request.args.get('user')
    
    if not username:
        return redirect(url_for('index')) 

    utilisateur_courrant = session.get('user')
    
    user = db.get_utilisateur_info(username)
    if not user:
        return redirect(url_for('index'))

    posts_reseau = db.get_posts_reseau_user(username)
    posts_reseau = preparer_posts(posts_reseau)

    abonnements = db.get_abonnements(username)
    abonnes = db.get_abonnes(username)

    est_abonne = False
    if utilisateur_courrant:
        est_abonne = db.est_abonne(utilisateur_courrant, username)

    return render_template("profile.html", user=user, posts_reseau=posts_reseau, abonnements=abonnements, abonnes=abonnes, est_abonne=est_abonne)

@app.route("/publication", methods=["GET"])
def publication():
    return render_template("post.html")

@app.route("/ajouter-publication", methods=["GET", "POST"])
def ajouter_publication():
    if request.method == 'POST':
        nom_auteur = session['user']
        description = request.form['description']
        if 'photo' not in request.files:
            return redirect(request.url)
        file = request.files['photo']
        if file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['DOSSIER_SAVE'], filename))
            photo_path = os.path.join(app.config['DOSSIER_UPLOAD'], filename)
            get_db().add_post_reseau(nom_auteur, description, photo_path)
            return redirect(url_for("index"))
    return render_template("reseau/addpost.html")

@app.route("/modifier-publication", methods=["POST"])
def modifier_publication():
    db = get_db()
    if "form-mod-pub" in request.form: 
        id_post = request.form["id_post"]
        description = request.form["description"]
        if 'photo' not in request.files:
            return redirect(request.url)
        image = request.files['photo']
        if image.filename:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['DOSSIER_SAVE'], filename))
            image_path = os.path.join(app.config['DOSSIER_UPLOAD'], filename)
        else:
            image_path = request.form["img_path"]
        db.update_post_reseau(id_post, description, image_path)        
        return redirect(url_for("index"))
    id_post = request.form["id_post"]
    post = db.get_post_reseau_par_id(id_post)
    return render_template("reseau/modpost.html", post = post)

@app.route("/ajouter-service", methods=["GET", "POST"])
def ajouter_service():
    if request.method == 'POST':
        nom_vendeur = session['user']
        titre_service = request.form['titre_service']
        description_service = request.form['description']
        cout_service = request.form['cout_service']
        disponibilite_service = request.form['disponibilite_service']
        get_db().add_service(nom_vendeur, titre_service, description_service, cout_service, disponibilite_service)
        return redirect(url_for("utilisateur_service"))
    return render_template("service/addservice.html")

@app.route("/modifier-service", methods=["GET", "POST"])
def modifier_service():
    if request.method == 'POST':
        id_service = request.form.get('id_service')
        titre = request.form.get('titre_service')
        description = request.form.get('description')
        prix = request.form.get('cout_service')
        horaire = request.form.get('disponibilite_service')

        get_db().update_service(id_service, titre, description, prix, horaire)
        return redirect(url_for("utilisateur_service"))
    
    id_service = request.args.get('id_service')
    if id_service:
        service = get_db().get_service(id_service)
        if service:
            return render_template("service/modifierservice.html", service=service)
    return render_template("service/modifierservice.html")

@app.route("/parametre", methods=["GET"])
def parametre():
    return render_template("options.html")


## A DEPLACER DANS LAPI
@app.route("/modifier-profil", methods=["POST"])
def modifier_profil():
    if 'user' in session:
        nom_utilisateur = session['user']
        prenom = request.form['prenom']
        nom = request.form['nom']
        biographie = request.form['biographie']
        
        db = get_db()
        db.modifier_utilisateur(nom_utilisateur, prenom, nom, biographie)
        
        return redirect(url_for('profile', user=nom_utilisateur))
    return redirect(url_for('connexion'))

@app.route("/ajouter-post-forum", methods=["GET", "POST"])
def ajouter_post_forum():
    if request.method == "POST":
        nom_auteur = session['user']
        titre = request.form['titre-publication']
        description = request.form['contenu-post-forum']
        id_post = get_db().add_post_forum(nom_auteur, titre, description)
        return redirect(url_for('forum_publication', id_post=id_post))
        
    return render_template('forum/addpostforum.html')

@app.route("/modifier-forum", methods=["GET", "POST"])
def modifier_post():
    if request.method == "POST":
        post_id = request.form.get('id_post')
        titre = request.form['titre']
        description = request.form['description']

        get_db().update_post_forum(post_id, titre, description)
        return redirect(url_for("forum_publication", id_post=post_id))

    post_id = request.args.get('id_post')
    if post_id:
        postforum = get_db().get_post_forum(post_id, session['user'])
        if postforum:
            return render_template("forum/modifierforum.html", postforum=postforum)
    return render_template("forum/modifierforum.html")

@app.route("/modifier-commentaire-forum", methods=["GET", "POST"])
def modifier_commentaire_forum():
    if request.method == "POST":
        commentaire_id = request.form.get('id_commentaire')
        contenu = request.form['contenu']

        get_db().update_commentaire_forum(commentaire_id, contenu)
        post_id = request.form.get('id_post')
        return redirect(url_for("forum_publication", id_post=post_id))
    
    commentaire_id = request.args.get('id_commentaire')
    if commentaire_id:
        commentaire = get_db().get_commentaire_forum(commentaire_id)
        if commentaire:
            return render_template("forum/modifiercommentaire.html", commentaire=commentaire)
    return render_template("forum/modifiercommentaire.html")

@app.route("/supprimer-commentaire-forum", methods=["POST"])
def supprimer_commentaire_forum():
    commentaire_id = request.form["id_commentaire"]
    get_db().supprimer_commentaire_forum(commentaire_id)
    return jsonify({'success': True, 'commentaire_id': commentaire_id})

## REST API SERVICES ##

@app.route("/api/commentaires/<post_id>", methods=['GET'])
def get_commentaires(post_id):
    if 'user' in session:
        nom_utilisateur = session['user']
        commentaires = get_db().get_commentaires_post_reseau(nom_utilisateur, post_id)
        list_commentaires = [commentaire.asDictionary() for commentaire in commentaires]
    return jsonify(list_commentaires)


@app.route("/api/publier-commentaire", methods=['POST'])
def publier_commentaire():
    if 'user' in session:
        nom_utilisateur = session['user']
        data = request.get_json()
        id_post = data['id_post']
        contenu = data['contenu']

        if not id_post or not contenu:
            return jsonify({'error': 'Invalid input'}), 400
        
        edt = pytz.timezone('America/Toronto')
        now = datetime.now(edt)
        horodatage = now.strftime('%Y-%m-%d %H:%M:%S')
        
        get_db().add_commentaire_post_reseau(id_post, nom_utilisateur, contenu, horodatage)
        commentaire = get_db().get_dernier_commentaire(id_post, nom_utilisateur, contenu)
        return jsonify({'success': True, 'commentaire': commentaire.asDictionary()}), 200


@app.route("/api/supprimer-publication", methods=["POST"])
def supprimer_publication():
    post_id = request.form["id_post"]
    get_db().remove_post_reseau(post_id)
    return redirect(url_for("index"))


@app.route("/api/ajouter-like-post-reseau", methods=['POST'])
def ajouter_like_post_reseau():
    if 'user' in session:
        nom_utilisateur = session['user']
        data = request.get_json()
        id_post = data['id_post']
        get_db().add_post_reseau_aime(nom_utilisateur, id_post)
        return jsonify({'success': True}), 200
    
@app.route("/api/ajouter-like-commentaire-reseau", methods=['POST'])
def ajouter_like_commentaire_reseau():
    if 'user' in session:
        nom_utilisateur = session['user']
        data = request.get_json()
        id_commentaire = data['id_commentaire']
        get_db().add_commentaire_reseau_aime(nom_utilisateur, id_commentaire)
        return jsonify({'success': True}), 200


@app.route("/api/retirer-like-commentaire-reseau", methods=['POST'])
def retirer_like_commentaire_reseau():
    if 'user' in session:
        nom_utilisateur = session['user']
        data = request.get_json()
        id_commentaire = data['id_commentaire']

        get_db().remove_commentaire_reseau_aime(nom_utilisateur, id_commentaire)
        return jsonify({'success': True}), 200


@app.route("/api/retirer-like-post-reseau", methods=['POST'])
def retirer_like_post_reseau():
    if 'user' in session:
        nom_utilisateur = session['user']
        data = request.get_json()
        id_post = data['id_post']

        get_db().remove_post_reseau_aime(nom_utilisateur, id_post)
        return jsonify({'success': True}), 200
    

@app.route("/api/rechercher-utilisateur", methods=["GET"])
def rechercher_utilisateur():
    search_query = request.args.get('query', '').lower()
    utilisateurs = get_db().rechercher_utilisateurs(search_query)
    return jsonify(utilisateurs)

@app.route("/api/supprimer-service", methods=['POST'])
def supprimer_service():
    service_id = request.form["id_service"]
    get_db().supprimer_service(service_id)
    return redirect(url_for("utilisateur_service"))


@app.route("/api/supprimer-article", methods=['POST'])
def supprimer_article():
    article_id = request.form["article_id"]
    get_db().supprimer_article(article_id)
    return redirect(url_for("marketplace"))

@app.route("/api/abonner", methods=["POST"])
def abonner():
    if 'user' in session:
        nom_utilisateur = session['user']
        data = request.get_json()
        abonnement_nom_utilisateur = data['abonnement_nom_utilisateur']
        get_db().ajouter_abonnement(nom_utilisateur, abonnement_nom_utilisateur)
        nb_abonnes = len(get_db().get_abonnes(abonnement_nom_utilisateur))
        return jsonify({'success': True, 'nb_abonnes': nb_abonnes}), 200
    return jsonify({'error': 'Unauthorized'}), 401

@app.route("/api/desabonner", methods=["POST"])
def desabonner():
    if 'user' in session:
        nom_utilisateur = session['user']
        data = request.get_json()
        abonnement_nom_utilisateur = data['abonnement_nom_utilisateur']
        get_db().supprimer_abonnement(nom_utilisateur, abonnement_nom_utilisateur)
        nb_abonnes = len(get_db().get_abonnes(abonnement_nom_utilisateur))
        return jsonify({'success': True, 'nb_abonnes': nb_abonnes}), 200
    return jsonify({'error': 'Unauthorized'}), 401

@app.route('/api/envoyer_message', methods=['POST'])
def envoyer_message():    
    utilisateur_actuel = session['user']
    data = request.json
    recepteur_nom = data.get('recepteur_nom')
    contenu = data.get('contenu')
    
    if not recepteur_nom or not contenu:
        return jsonify({"error": "Erreur"}), 400
    
    db = get_db()
    db.ajouter_message(utilisateur_actuel, recepteur_nom, contenu)
    
    return jsonify({"success": True}), 201

@app.route("/api/publier-commentaire-forum", methods=['POST'])
def publier_commentaire_forum():
    if 'user' in session:
        nom_utilisateur = session['user']
        data = request.get_json()
        id_post = data['id_post']
        contenu = data['contenu']

        if not id_post or not contenu:
            return jsonify({'error': 'Invalid input'}), 400
        
        edt = pytz.timezone('America/Toronto')
        now = datetime.now(edt)
        horodatage = now.strftime('%Y-%m-%d %H:%M:%S')
        
        commentaire = get_db().add_commentaire_post_forum(id_post, nom_utilisateur, contenu, horodatage)
        return jsonify({'success': True, 'commentaire': commentaire}), 200

@app.route('/api/upvote-commentaire-forum', methods=['POST'])
def upvote_commentaire_forum():
    data = request.json
    id_commentaire = data['id_commentaire']
    nom_utilisateur = session['user']
    get_db().upvote_commentaire_forum(id_commentaire, nom_utilisateur)
    return jsonify(success=True)

@app.route('/api/retirer-upvote-commentaire', methods=['POST'])
def retirer_upvote_commentaire():
    data = request.json
    id_commentaire = data['id_commentaire']
    nom_utilisateur = session['user']
    get_db().retirer_upvote_commentaire(id_commentaire, nom_utilisateur)
    return jsonify(success=True)

@app.route('/api/downvote-commentaire-forum', methods=['POST'])
def downvote_commentaire_forum():
    data = request.json
    id_commentaire = data['id_commentaire']
    nom_utilisateur = session['user']
    get_db().downvote_commentaire_forum(id_commentaire, nom_utilisateur)
    return jsonify(success=True)

@app.route('/api/retirer-downvote-commentaire', methods=['POST'])
def retirer_downvote_commentaire():
    data = request.json
    id_commentaire = data['id_commentaire']
    nom_utilisateur = session['user']
    get_db().retirer_downvote_commentaire(id_commentaire, nom_utilisateur)
    return jsonify(success=True)

@app.route('/api/upvote-post-forum', methods=['POST'])
def upvote_post_forum():
    data = request.json
    id_post = data['id_post']
    nom_utilisateur = session['user']
    get_db().upvote_post_forum(id_post, nom_utilisateur)
    return jsonify(success=True)

@app.route('/api/retirer-upvote-post', methods=['POST'])
def retirer_upvote_post():
    data = request.json
    id_post = data['id_post']
    nom_utilisateur = session['user']
    get_db().retirer_upvote_post_forum(id_post, nom_utilisateur)
    return jsonify(success=True)

@app.route('/api/downvote-post-forum', methods=['POST'])
def downvote_post_forum():
    data = request.json
    id_post = data['id_post']
    nom_utilisateur = session['user']
    get_db().downvote_post_forum(id_post, nom_utilisateur)
    return jsonify(success=True)

@app.route('/api/retirer-downvote-post', methods=['POST'])
def retirer_downvote_post():
    data = request.json
    id_post = data['id_post']
    nom_utilisateur = session['user']
    get_db().retirer_downvote_post_forum(id_post, nom_utilisateur)
    return jsonify(success=True)

@app.route("/api/supprimer-post-forum", methods=["POST"])
def supprimer_post_forum():
    post_id = request.form["id_post"]
    get_db().supprimer_post_forum(post_id)
    return redirect(url_for("forum"))


## ERROR HANDLING ##

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html"), 404

@app.route("/erreur/<code>")
def erreur(code):
    message = error_msg[code]
    error = {
        'code': code,
        'message': message
    }
    return render_template("error.html", error=error), int(code)

## Méthodes utilitaires
def calculer_temps(horodatage):
    utc = pytz.utc
    local_tz = pytz.timezone('America/Toronto')
    

    naive_horodatage = datetime.strptime(horodatage, '%Y-%m-%d %H:%M:%S')
    utc_horodatage = utc.localize(naive_horodatage)
    local_horodatage = utc_horodatage.astimezone(local_tz)
    now_utc = datetime.now(utc)
    now_local = now_utc.astimezone(local_tz)
    
    diff = now_local - local_horodatage
    
    minutes = abs(diff.total_seconds() // 60)
    heures = abs(diff.total_seconds() // 3600)
    jours = abs(heures // 24)
    semaines = abs(jours // 7)

    if semaines >= 1:
        return "Il y a {} semaine{}".format(int(semaines), 's' if semaines > 1 else '')
    elif jours >= 1:
        return "Il y a {} jour{}".format(int(jours), 's' if jours > 1 else '')
    elif heures >= 1:
        return "Il y a {} heure{}".format(int(heures), 's' if heures > 1 else '')
    elif minutes >= 1:
        return "Il y a {} minute{}".format(int(minutes), 's' if minutes > 1 else '')
    else:
        return "Il y a un instant"

def preparer_posts(posts):
    for post in posts:
        post.horodatage = calculer_temps(post.horodatage)
    return posts

def format_horodatage(horodatage, current_datetime):
    message_datetime = datetime.strptime(horodatage, '%Y-%m-%d %H:%M:%S')
    if message_datetime.date() == current_datetime.date():
        return message_datetime.strftime('%H:%M')
    else:
        return message_datetime.strftime('%Y-%m-%d')


app.jinja_env.globals.update(format_horodatage=format_horodatage)