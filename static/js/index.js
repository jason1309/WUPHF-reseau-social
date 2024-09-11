document.addEventListener('DOMContentLoaded', function () {
    // Listener pour les boutons Afficher les commentaires
    document.querySelectorAll('.btn-affiche-commentaire').forEach(button => {
        button.addEventListener('click', afficherCommentairePostReseau);
    });

    // Listener pour les boutons Cacher les commentaires
    document.querySelectorAll('.btn-affiche-moins-commentaire').forEach(button => {
        button.addEventListener('click', enleverCommentairePostReseau);
    });

    // Listener pour la modale de suppression de post
    var confirmDeleteModal = document.getElementById('confirmDeleteModal');
    if (confirmDeleteModal) {
        confirmDeleteModal.addEventListener('show.bs.modal', function (event) {
            var button = event.relatedTarget;
            var postId = button.getAttribute('data-post-id');
            var postIdToDelete = confirmDeleteModal.querySelector('#postIdToDelete');
            postIdToDelete.value = postId;
            console.log("Post ID à supprimer: " + postId);
        });
    }

    // Listener pour les boutons like des posts
    document.querySelectorAll('.like-button-post').forEach(button => {
        button.addEventListener('click', function () {
            activerBoutonLike(this);
        });
    });

    // Listener pour les boutons like des commentaires
    document.querySelectorAll('.like-button-commentaire').forEach(button => {
        button.addEventListener('click', function () {
            activerBoutonLikeCommentaireReseau(this);
        });
    });
});

function activerBoutonLike(buttonLike) {
    var id_post = buttonLike.id.split('-')[1];
    var boutonLikePost = document.getElementById('likePostIcon-' + id_post);
    var requete = boutonLikePost.classList.contains('liked') ? '/api/retirer-like-post-reseau' : '/api/ajouter-like-post-reseau';

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.status === 200) {
            if (boutonLikePost.classList.contains('liked')) {
                boutonLikePost.classList.add('not-like-button');
                boutonLikePost.classList.remove('liked');
                retirerLikePost(id_post);
            } else {
                boutonLikePost.classList.add('liked');
                boutonLikePost.classList.remove('not-like-button');
                ajouterLikePost(id_post);
            }
        }
    };

    xhr.open("POST", requete, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({ id_post: id_post }));
}


function ajouterLikePost(id_post) {
    var affichageNbLikes = document.getElementById('nb-likes-' + id_post);
    var nbLikes = parseInt(affichageNbLikes.innerHTML.split(' ')[0]);

    if (isNaN(nbLikes)) {
        affichageNbLikes.innerHTML = "1 mention j'aime";
    } else {
        nbLikes++;
        affichageNbLikes.innerHTML = nbLikes + " mentions j'aime";
    }
}

function retirerLikePost(id_post) {
    var affichageNbLikes = document.getElementById('nb-likes-' + id_post);
    var nbLikes = parseInt(affichageNbLikes.innerHTML.split(' ')[0]);

    if (!isNaN(nbLikes) && nbLikes > 2) {
        affichageNbLikes.innerHTML = (nbLikes - 1) + " mentions j'aime";
    } else if (nbLikes == 2) {
        affichageNbLikes.innerHTML = "1 mention j'aime";
    } else {
        affichageNbLikes.innerHTML = "Aucune mention j'aime";
    }
}

function activerBoutonLikeCommentaireReseau(boutonLikeCommentaire) {
    id_commentaire = boutonLikeCommentaire.id.split('-')[1]
    var boutonLikeComent = document.getElementById('likeCommentairePost-' + id_commentaire);
    var requete = boutonLikeComent.classList.contains('liked') ? '/api/retirer-like-commentaire-reseau' : '/api/ajouter-like-commentaire-reseau';

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.status === 200) {
            if (boutonLikeComent.classList.contains('liked')) {
                boutonLikeComent.classList.add('not-like-button');
                boutonLikeComent.classList.remove('liked');
                retirerLikeCommentaire(id_commentaire);
            } else {
                boutonLikeComent.classList.add('liked');
                boutonLikeComent.classList.remove('not-like-button');
                ajouterLikeCommentaire(id_commentaire);
            }
        }
    };

    xhr.open("POST", requete, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({ id_commentaire: id_commentaire }));
}

function ajouterLikeCommentaire(id_commentaire) {
    var affichageNbLikes = document.getElementById('nb-likes-comm-' + id_commentaire);
    var nbLikes = parseInt(affichageNbLikes.innerHTML.split(' ')[0]);
    nbLikes++;
    affichageNbLikes.innerHTML = nbLikes + " J'aime";
}

function retirerLikeCommentaire(id_commentaire) {
    var affichageNbLikes = document.getElementById('nb-likes-comm-' + id_commentaire);
    var nbLikes = parseInt(affichageNbLikes.innerHTML.split(' ')[0]);

    nbLikes--;
    affichageNbLikes.innerHTML = nbLikes + " J'aime";
}

function afficherBoutonPublier(id_post, container, textarea) {
    if (!document.getElementById('boutonPublierCommentaire-' + id_post)) {
        var boutonPublier = document.createElement('button');
        boutonPublier.classList.add('btn', 'btn-primary', 'mt-2');
        boutonPublier.id = 'boutonPublierCommentaire-' + id_post;
        boutonPublier.textContent = 'Publier';

        boutonPublier.addEventListener('click', function () {
            publierCommentaire(id_post);
        });

        container.appendChild(boutonPublier);
    }
}

function cacherBoutonPublier(id_post, container) {
    var boutonPublier = document.getElementById('boutonPublierCommentaire-' + id_post);
    if (boutonPublier) {
        boutonPublier.remove();
    }
}

function publierCommentaire(id_post) {
    var textarea = document.getElementById('newCommentText-' + id_post)
    var contenu = textarea.value;

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                textarea.value = "";
                cacherBoutonPublier(id_post, document.getElementById('publierCommentaireContainer-' + id_post));
                ajouterCommentaire(id_post, response.commentaire)
            }
        }
    };

    xhr.open("POST", "/api/publier-commentaire", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({ id_post: id_post, contenu: contenu }));
}

function afficherCommentairePostReseau(event) {
    event.preventDefault();
    var post_id = event.target.getAttribute('data-post-id');

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                gererCommentaire(JSON.parse(xhr.responseText), post_id);
            }
        }
    };

    xhr.open("GET", "/api/commentaires/" + post_id, true);
    xhr.send();
}

function gererCommentaire(commentaires, post_id) {
    var sectionCommentaire = document.getElementById('section-commentaire-' + post_id);
    var btnAfficherCommentaire = document.getElementById('btn-plus-' + post_id);
    var btnAfficherMoins = document.getElementById('btn-moins-' + post_id);

    btnAfficherCommentaire.style.display = 'none';
    sectionCommentaire.innerHTML = '';

    commentaires.forEach(commentaire => {
        var commentaireDiv = document.createElement('div');
        commentaireDiv.classList.add('section-un-commentaire');

        var utilisateur = document.createElement('strong');
        utilisateur.textContent = commentaire.auteur.nom_utilisateur + ': ';

        var contenu = document.createElement('span');
        contenu.textContent = commentaire.contenu;

        var infoDiv = document.createElement('div');
        infoDiv.classList.add('info-commentaire');

        var nbAimes = document.createElement('span');
        nbAimes.textContent = commentaire.nombre_total_aime + " J'aime";
        nbAimes.id = 'nb-likes-comm-' + commentaire.id_commentaire;

        var horodatage = document.createElement('span');
        horodatage.textContent = calculerTempsDepuis(commentaire.horodatage);

        var likeIcon = document.createElement('i');
        likeIcon.classList.add('far', 'fa-heart');
        if (commentaire.liked) {
            likeIcon.classList.add('liked');
        } else {
            likeIcon.classList.add('not-like-button');
        }
        likeIcon.id = 'likeCommentairePost-' + commentaire.id_commentaire;
        likeIcon.onclick = function () { activerBoutonLikeCommentaireReseau(this) };
        likeIcon.style.marginLeft = '5px';

        commentaireDiv.appendChild(utilisateur);
        commentaireDiv.appendChild(contenu);
        infoDiv.append(horodatage);
        infoDiv.append(nbAimes);
        infoDiv.appendChild(likeIcon);
        infoDiv.style.marginBottom = '5px';
        sectionCommentaire.appendChild(commentaireDiv);
        sectionCommentaire.appendChild(infoDiv);
    });

    sectionCommentaire.style.display = 'block';
    btnAfficherMoins.style.display = 'block';
}

function ajouterCommentaire(post_id, commentaire) {
    var sectionCommentaire = document.getElementById('section-commentaire-' + post_id);

    var commentaireDiv = document.createElement('div');
    commentaireDiv.classList.add('section-un-commentaire');

    var utilisateur = document.createElement('strong');
    utilisateur.textContent = commentaire.auteur.nom_utilisateur + ': ';

    var contenu = document.createElement('span');
    contenu.textContent = commentaire.contenu;

    var infoDiv = document.createElement('div');
    infoDiv.classList.add('info-commentaire');

    var nbAimes = document.createElement('span');
    nbAimes.textContent = commentaire.nombre_total_aime + " J'aime";
    nbAimes.id = 'nb-likes-comm-' + commentaire.id_commentaire;

    var horodatage = document.createElement('span');
    horodatage.textContent = calculerTempsDepuis(commentaire.horodatage);

    // Bouton like
    var likeButton = document.createElement('button');
    likeButton.classList.add('btn', 'btn-link');
    var likeIcon = document.createElement('i');
    likeIcon.classList.add('far', 'fa-heart', 'not-like-button');
    likeIcon.id = 'likeCommentairePost-' + commentaire.id_commentaire;
    likeIcon.onclick = function () { activerBoutonLikeCommentaireReseau(this) };
    likeButton.appendChild(likeIcon);
    likeButton.style.marginLeft = '10px';

    commentaireDiv.appendChild(utilisateur);
    commentaireDiv.appendChild(contenu);
    infoDiv.append(horodatage);
    infoDiv.append(nbAimes);
    infoDiv.appendChild(likeButton);
    infoDiv.style.marginBottom = '5px';
    sectionCommentaire.appendChild(commentaireDiv);
    sectionCommentaire.appendChild(infoDiv);
    sectionCommentaire.style.display = 'block';
    var buttonCacherCommentaire = document.getElementById('btn-moins-' + post_id);
    buttonCacherCommentaire.style.display = 'block';
    var buttonAfficheCommentaire = document.getElementById('btn-plus-' + post_id);
    buttonAfficheCommentaire.style.display = 'none';

}

function boutonAbonnement(nomUtilisateur, abonner) {
    var url = abonner ? "/api/abonner" : "/api/desabonner";
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                var bouton = document.getElementById("bouton-abonnement");
                var nbAbonnesElement = document.getElementById("nb-abonnes");
                var nbAbonnes = response.nb_abonnes;

                nbAbonnesElement.textContent = nbAbonnes;

                if (abonner) {
                    bouton.textContent = "Se désabonner";
                    bouton.onclick = function () { boutonAbonnement(nomUtilisateur, false); };
                } else {
                    bouton.textContent = "S'abonner";
                    bouton.onclick = function () { boutonAbonnement(nomUtilisateur, true); };
                }
            }
        }
    };

    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({ abonnement_nom_utilisateur: nomUtilisateur }));
}


function enleverCommentairePostReseau(event) {
    event.preventDefault();

    var post_id = event.target.getAttribute('data-post-id');
    var sectionCommentaire = document.getElementById('section-commentaire-' + post_id);
    var btnAfficherCommentaire = document.getElementById('btn-plus-' + post_id);
    var btnAfficherMoins = document.getElementById('btn-moins-' + post_id);

    sectionCommentaire.style.display = 'none';
    btnAfficherMoins.style.display = 'none';
    btnAfficherCommentaire.style.display = 'block';
}


function activerBoutonPublier(textarea) {
    var id_post = textarea.id.split('-')[1];
    var boutonCommentaireContainer = document.getElementById('publierCommentaireContainer-' + id_post);

    if (textarea.value.trim() !== "") {
        afficherBoutonPublier(id_post, boutonCommentaireContainer, textarea);
    } else {
        cacherBoutonPublier(id_post, boutonCommentaireContainer);
    }
}

function suggestionProfils() {
    var input = document.getElementById('entre-recherche').value;
    var URLstatic = document.getElementById('url-static').value;
  
    if (input.length < 1) {
      document.getElementById('liste-suggestion').innerHTML = '';
      return;
    }
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
        var suggestions = JSON.parse(xhr.responseText);
        var listeSuggestions = document.getElementById('liste-suggestion');
        listeSuggestions.innerHTML = '';
        suggestions.forEach(function (utilisateur) {
          var suggestionItem = document.createElement('a');
          suggestionItem.href = '/profile?user=' + utilisateur.nom_utilisateur;
          suggestionItem.className = 'list-group-item list-group-item-action';
          suggestionItem.innerHTML = `
                    <img src="${URLstatic}${utilisateur.photo_profil}" class="rounded-circle" width="30" height="30">
                    ${utilisateur.prenom} ${utilisateur.nom} (@${utilisateur.nom_utilisateur})
                `;
          listeSuggestions.appendChild(suggestionItem);
        });
      }
    };
    xhr.open('GET', '/api/rechercher-utilisateur?query=' + encodeURIComponent(input), true);
    xhr.send();
  }