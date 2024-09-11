document.addEventListener("DOMContentLoaded", function () {
    // Listener pour la suppression de post forum //
    var confirmDeleteForumModal = document.getElementById(
        "confirmDeleteForumModal"
    );
    if (confirmDeleteForumModal) {
        confirmDeleteForumModal.addEventListener("show.bs.modal", function (event) {
            var button = event.relatedTarget;
            var postId = button.getAttribute("data-forum-id");
            var forumIdToDelete =
                confirmDeleteForumModal.querySelector("#forumIdToDelete");
            forumIdToDelete.value = postId;
            console.log("Post ID à supprimer: " + postId);
        });
    }
    // Listener pour afficher le bouton publier commentaire si du texte est entré
    document.querySelectorAll("textarea").forEach((textarea) => {
        textarea.addEventListener("input", function () {
            if (!textarea.id.includes("textarea-commentaire-forum")) {
                activerBoutonPublier(this);
            }
        });
        textarea.addEventListener("focus", function () {
            if (textarea.id.includes("textarea-commentaire-forum")) {
                activerBoutonPublierForum(this);
            }
        });
    });
    // Supprimer commentaire sur forum
    document.querySelectorAll(".btn-supprimer-commentaire").forEach((button) => {
        button.addEventListener("click", function () {
            let commentaireId = this.getAttribute("data-commentaire-id");
            let formData = new FormData();
            formData.append("id_commentaire", commentaireId);

            fetch("/supprimer-commentaire-forum", {
                method: "POST",
                body: formData,
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        document
                            .getElementById("commentaire-" + data.commentaire_id)
                            .remove();
                    } else {
                        alert("Erreur suppression commentaire forum");
                    }
                });
        });
    });

    document.querySelectorAll(".bouton-forum-up").forEach((button) => {
        button.addEventListener("click", function () {
            activerBoutonLikePostForum(this);
        });
    });

    document.querySelectorAll(".bouton-forum-down").forEach((button) => {
        button.addEventListener("click", function () {
            activerBoutonNotLikePostForum(this);
        });
    });

    document
        .querySelectorAll(".like-button-commentaire-forum")
        .forEach((button) => {
            button.addEventListener("click", function () {
                activerBoutonLikeCommentaireForum(this);
            });
        });

    document
        .querySelectorAll(".not-like-button-commentaire")
        .forEach((button) => {
            button.addEventListener("click", function () {
                activerBoutonNotLikeCommentaireForum(this);
            });
        });

    document
        .querySelectorAll(
            ".signaler-forum, .signaler-post-forum, .signaler-commentaire-forum"
        )
        .forEach((button) => {
            button.addEventListener("click", function (event) {
                event.preventDefault();
                showSignalToast();
            });
        });

    var quill = new Quill("#editor-container", {
        theme: "snow",
    });

    document.getElementById("form-add-post-forum").onsubmit = function () {
        var contenuPublicationForum = document.getElementById("contenu-post-forum");
        contenuPublicationForum.value = quill.root.innerHTML;
        console.log(quill.root.innerHTML);
    };

    document.getElementById("form-modifier-forum").onsubmit = function () {
        var contenuPublicationForum = document.getElementById(
            "contenu-modifier-post-forum"
        );
        contenuPublicationForum.value = quillEdit.root.innerHTML;
        console.log(quillEdit.root.innerHTML);
    };
});

// Listener pour trier post forum //
document.getElementById("trier-aimes").addEventListener("click", function () {
    trierPosts("avec-aimes");
});
document.getElementById("trier-recent").addEventListener("click", function () {
    trierPosts("avec-recent");
});
document.getElementById("trier-ancien").addEventListener("click", function () {
    trierPosts("avec-ancien");
});
document
    .getElementById("trier-commentaires")
    .addEventListener("click", function () {
        trierPosts("avec-commentaires");
    });

function activerBoutonLikePostForum(buttonLike) {
    var idPost = buttonLike.id.split("-")[1];
    var boutonLike = document.getElementById("likePostForum-" + idPost);
    var boutonNotLike = document.getElementById("notlikePostForum-" + idPost);
    var requete = boutonLike.classList.contains("fa-arrow-up-not-activate")
        ? "/api/upvote-post-forum"
        : "/api/retirer-upvote-post";

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            if (boutonLike.classList.contains("fa-arrow-up-not-activate")) {
                if (boutonNotLike.classList.contains("fa-arrow-down-activate")) {
                    boutonNotLike.classList.remove("fa-arrow-down-activate");
                    boutonNotLike.classList.add("fa-arrow-down-not-activate");
                    ajusterNbLikesPost(idPost, 1);
                }
                boutonLike.classList.add("fa-arrow-up-activate");
                boutonLike.classList.remove("fa-arrow-up-not-activate");
                ajusterNbLikesPost(idPost, 1);
            } else {
                boutonLike.classList.add("fa-arrow-up-not-activate");
                boutonLike.classList.remove("fa-arrow-up-activate");
                ajusterNbLikesPost(idPost, -1);
            }
        }
    };

    xhr.open("POST", requete, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({ id_post: idPost }));
}

function activerBoutonNotLikePostForum(buttonNotLike) {
    var idPost = buttonNotLike.id.split("-")[1];
    var boutonLike = document.getElementById("likePostForum-" + idPost);
    var boutonNotLike = document.getElementById("notlikePostForum-" + idPost);
    var requete = boutonNotLike.classList.contains("fa-arrow-down-not-activate")
        ? "/api/downvote-post-forum"
        : "/api/retirer-downvote-post";

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            if (boutonNotLike.classList.contains("fa-arrow-down-not-activate")) {
                if (boutonLike.classList.contains("fa-arrow-up-activate")) {
                    boutonLike.classList.remove("fa-arrow-up-activate");
                    boutonLike.classList.add("fa-arrow-up-not-activate");
                    ajusterNbLikesPost(idPost, -1);
                }
                boutonNotLike.classList.add("fa-arrow-down-activate");
                boutonNotLike.classList.remove("fa-arrow-down-not-activate");
                ajusterNbLikesPost(idPost, -1);
            } else {
                boutonNotLike.classList.add("fa-arrow-down-not-activate");
                boutonNotLike.classList.remove("fa-arrow-down-activate");
                ajusterNbLikesPost(idPost, 1);
            }
        }
    };

    xhr.open("POST", requete, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({ id_post: idPost }));
}

function activerBoutonLikeCommentaireForum(buttonLike) {
    var idCommentaire = buttonLike.id.split("-")[1];
    var boutonLike = document.getElementById(
        "likeCommentaireForum-" + idCommentaire
    );
    var boutonNotLike = document.getElementById(
        "notlikeCommentaireForum-" + idCommentaire
    );
    var requete = boutonLike.classList.contains("far-arrow-up-not-activate")
        ? "/api/upvote-commentaire-forum"
        : "/api/retirer-upvote-commentaire";

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            if (boutonLike.classList.contains("far-arrow-up-not-activate")) {
                if (boutonNotLike.classList.contains("far-arrow-down-activate")) {
                    boutonNotLike.classList.remove("far-arrow-down-activate");
                    boutonNotLike.classList.add("far-arrow-down-not-activate");
                    ajusterNbLikes(idCommentaire, 1);
                }
                boutonLike.classList.add("far-arrow-up-activate");
                boutonLike.classList.remove("far-arrow-up-not-activate");
                ajusterNbLikes(idCommentaire, 1);
            } else {
                boutonLike.classList.add("far-arrow-up-not-activate");
                boutonLike.classList.remove("far-arrow-up-activate");
                ajusterNbLikes(idCommentaire, -1);
            }
        }
    };

    xhr.open("POST", requete, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({ id_commentaire: idCommentaire }));
}

function activerBoutonNotLikeCommentaireForum(buttonNotLike) {
    var idCommentaire = buttonNotLike.id.split("-")[1];
    var boutonNotLike = document.getElementById(
        "notlikeCommentaireForum-" + idCommentaire
    );
    var boutonLike = document.getElementById(
        "likeCommentaireForum-" + idCommentaire
    );
    var requete = boutonNotLike.classList.contains("far-arrow-down-not-activate")
        ? "/api/downvote-commentaire-forum"
        : "/api/retirer-downvote-commentaire";

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            if (boutonNotLike.classList.contains("far-arrow-down-not-activate")) {
                if (boutonLike.classList.contains("far-arrow-up-activate")) {
                    boutonLike.classList.remove("far-arrow-up-activate");
                    boutonLike.classList.add("far-arrow-up-not-activate");
                    ajusterNbLikes(idCommentaire, -1);
                }
                boutonNotLike.classList.add("far-arrow-down-activate");
                boutonNotLike.classList.remove("far-arrow-down-not-activate");
                ajusterNbLikes(idCommentaire, -1);
            } else {
                boutonNotLike.classList.add("far-arrow-down-not-activate");
                boutonNotLike.classList.remove("far-arrow-down-activate");
                ajusterNbLikes(idCommentaire, 1);
            }
        }
    };

    xhr.open("POST", requete, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({ id_commentaire: idCommentaire }));
}

function ajusterNbLikesPost(idPost, valeur) {
    var affichageNbLikes = document.getElementById(
        "nb-likes-forum-post-" + idPost
    );
    var nbLikes = parseInt(affichageNbLikes.innerHTML);
    if (!isNaN(nbLikes)) {
        nbLikes += valeur;
        affichageNbLikes.innerHTML = nbLikes;
    } else {
        console.error("La valeur des likes n'est pas un nombre valide.");
    }
}

function ajusterNbLikes(idCommentaire, valeur) {
    var affichageNbLikes = document.getElementById(
        "nb-likes-forum-commentaire-" + idCommentaire
    );
    var nbLikes = parseInt(affichageNbLikes.innerHTML);
    if (!isNaN(nbLikes)) {
        nbLikes += valeur;
        affichageNbLikes.innerHTML = nbLikes;
    } else {
        console.error("La valeur des likes n'est pas un nombre valide.");
    }
}

function activerBoutonPublierForum(textarea) {
    var button = document.getElementById("commentaire-bouton-forum");

    if (button.getAttribute("data-event-attached") !== "true") {
        button.style.display = "flex";
        button.addEventListener("click", function () {
            var id_post = textarea.id.split("-")[3];
            var contenu = textarea.value;

            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function () {
                if (xhr.readyState === XMLHttpRequest.DONE) {
                    if (xhr.status === 200) {
                        var response = JSON.parse(xhr.responseText);
                        textarea.value = "";
                        button.classList.add("fade-out-hidden");
                        ajouterCommentaireForum(response.commentaire);
                        button.setAttribute("data-event-attached", "false");
                    }
                }
            };
            xhr.open("POST", "/api/publier-commentaire-forum", true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.send(JSON.stringify({ id_post: id_post, contenu: contenu }));
        });
    }

    button.setAttribute("data-event-attached", "true");
}

function ajouterCommentaireForum(commentaire) {
    var sectionCommentaire = document.getElementById("section-commentaire-forum");

    var commentaireDiv = document.createElement("div");
    commentaireDiv.classList.add("card", "commentaire-card", "mb-3");
    commentaireDiv.id = "commentaire-" + commentaire.id_commentaire;

    var bodyDiv = document.createElement("div");
    bodyDiv.classList.add("card-body", "d-flex", "align-items-start");
    commentaireDiv.appendChild(bodyDiv);

    var img = document.createElement("img");
    img.src = commentairePhotoProfil + commentaire.photo_profil;
    img.alt = "Photo de profil";
    img.classList.add("rounded-circle");
    img.width = 50;
    img.height = 50;
    bodyDiv.appendChild(img);

    var commentaireContenu = document.createElement("div");
    commentaireContenu.classList.add(
        "ml-3",
        "d-flex",
        "flex-column",
        "align-items-start",
        "affichage-profil-forum"
    );
    bodyDiv.appendChild(commentaireContenu);

    var commentaireInfo = document.createElement("p");
    commentaireInfo.classList.add("text-muted", "mb-1");
    var horodatage = calculerTempsDepuis(commentaire.horodatage);
    if (horodatage.endsWith("- ")) {
        horodatage = horodatage.slice(0, -2).trim();
    }
    commentaireInfo.innerHTML =
        `<strong>${commentaire.nom_auteur}</strong> • ` + horodatage;
    commentaireContenu.appendChild(commentaireInfo);

    var commentaireText = document.createElement("p");
    commentaireText.classList.add("mb-0");
    commentaireText.textContent = commentaire.contenu;
    commentaireContenu.appendChild(commentaireText);

    var commentaireOptions = document.createElement("div");
    commentaireOptions.classList.add("mt-2");
    commentaireContenu.appendChild(commentaireOptions);

    var btnUpvote = document.createElement("button");
    btnUpvote.classList.add(
        "btn",
        "btn-link",
        "p-0",
        "mr-3",
        "commentaire-options-button",
        "far-arrow-up-not-activate",
        "like-button-commentaire-forum"
    );
    btnUpvote.id = "likeCommentaireForum-" + commentaire.id_commentaire;
    var upvoteIcon = document.createElement("i");
    upvoteIcon.classList.add("far", "fa-arrow-alt-circle-up");
    btnUpvote.appendChild(upvoteIcon);
    commentaireOptions.appendChild(btnUpvote);

    var commentaireAime = document.createElement("span");
    commentaireAime.classList.add("commentaire-aime");
    commentaireAime.id =
        "nb-likes-forum-commentaire-" + commentaire.id_commentaire;
    commentaireAime.textContent = commentaire["commentaire_nombre_aime"];
    commentaireOptions.appendChild(commentaireAime);
    commentaireAime.style.marginLeft = "3px";

    var btnDownvote = document.createElement("button");
    btnDownvote.classList.add(
        "btn",
        "btn-link",
        "p-0",
        "mr-3",
        "commentaire-options-button",
        "far-arrow-down-not-activate",
        "not-like-button-commentaire"
    );
    btnDownvote.id = "notlikeCommentaireForum-" + commentaire.id_commentaire;
    var downvoteIcon = document.createElement("i");
    downvoteIcon.classList.add("far", "fa-arrow-alt-circle-down");
    btnDownvote.appendChild(downvoteIcon);
    btnDownvote.style.marginLeft = "3px";
    commentaireOptions.appendChild(btnDownvote);

    var btnModifier = document.createElement("button");
    btnModifier.classList.add(
        "btn",
        "btn-link",
        "p-0",
        "mr-3",
        "commentaire-options-button"
    );
    var modifierLink = document.createElement("a");
    modifierLink.href = `/modifier-commentaire-forum?id_commentaire=${commentaire.id_commentaire}`;
    btnModifier.appendChild(modifierLink);
    var modifierIcon = document.createElement("i");
    modifierIcon.classList.add("fas", "fa-edit");
    modifierLink.appendChild(modifierIcon);
    modifierLink.appendChild(document.createTextNode(" MODIFIER"));
    commentaireOptions.appendChild(modifierLink);

    var btnSupprimer = document.createElement("button");
    btnSupprimer.classList.add(
        "btn",
        "btn-link",
        "p-0",
        "mr-3",
        "commentaire-options-button",
        "btn-supprimer-commentaire"
    );
    btnSupprimer.setAttribute("data-commentaire-id", commentaire.id_commentaire);
    var supprimerIcon = document.createElement("i");
    supprimerIcon.classList.add("fas", "fa-trash");
    btnSupprimer.appendChild(supprimerIcon);
    btnSupprimer.appendChild(document.createTextNode(" Supprimer"));
    commentaireOptions.appendChild(btnSupprimer);

    var btnRepondre = document.createElement("button");
    btnRepondre.classList.add(
        "btn",
        "btn-link",
        "p-0",
        "mr-3",
        "commentaire-options-button"
    );
    var repondreIcon = document.createElement("i");
    repondreIcon.classList.add("fas", "fa-reply");
    btnRepondre.appendChild(repondreIcon);
    btnRepondre.appendChild(document.createTextNode(" Répondre"));
    btnRepondre.style.marginLeft = "3px";
    commentaireOptions.appendChild(btnRepondre);

    var btnSignaler = document.createElement("button");
    btnSignaler.classList.add(
        "btn",
        "btn-link",
        "p-0",
        "mr-3",
        "commentaire-options-button"
    );
    var signalerIcon = document.createElement("i");
    signalerIcon.classList.add("fas", "fa-flag");
    btnSignaler.appendChild(signalerIcon);
    btnSignaler.appendChild(document.createTextNode(" Signaler"));
    btnSignaler.style.marginLeft = "3px";
    commentaireOptions.appendChild(btnSignaler);

    sectionCommentaire.insertBefore(
        commentaireDiv,
        sectionCommentaire.childNodes[6]
    );

    btnUpvote.addEventListener("click", function () {
        activerBoutonLikeCommentaireForum(this);
    });

    btnDownvote.addEventListener("click", function () {
        activerBoutonNotLikeCommentaireForum(this);
    });

    btnSupprimer.addEventListener("click", function () {
        let commentaireId = this.getAttribute("data-commentaire-id");
        let formData = new FormData();
        formData.append("id_commentaire", commentaireId);

        fetch("/supprimer-commentaire-forum", {
            method: "POST",
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    document
                        .getElementById("commentaire-" + data.commentaire_id)
                        .remove();
                } else {
                    alert("Erreur suppression commentaire forum");
                }
            });
    });

    document.getElementById("first-to-comment-h3").style.display = "none";
}

function filtrerPostForum() {
    document
        .getElementById("forum-recherche")
        .addEventListener("submit", filtrerPostForum);
    const entreRecherche = document
        .getElementById("forum-recherche")
        .value.toLowerCase();
    const forumPosters = document.querySelectorAll(".forum-post");

    let aucunResultat = true;

    forumPosters.forEach((forumPoste) => {
        const nomAuteur = forumPoste.getAttribute("data-nomAuteur");
        const titre = forumPoste.getAttribute("data-titre");
        const description = forumPoste.getAttribute("data-description");

        if (
            nomAuteur.includes(entreRecherche) ||
            titre.toLowerCase().includes(entreRecherche) ||
            description.toLowerCase().includes(entreRecherche)
        ) {
            forumPoste.classList.remove("fade-out");
            forumPoste.style.display = "flex";
            aucunResultat = false;
        } else {
            forumPoste.classList.add("fade-out");
            setTimeout(() => {
                forumPoste.style.display = "none";
            }, 300);
        }
    });

    const messageAucunResultat = document.getElementById("aucun-resultat-forum");
    if (aucunResultat) {
        messageAucunResultat.style.display = "block";
    } else {
        messageAucunResultat.style.display = "none";
    }
}

function trierPosts(critere) {
    const posts = Array.from(document.querySelectorAll(".forum-post"));
    let sortedPosts;

    if (critere === "avec-aimes") {
        sortedPosts = posts.sort(
            (a, b) => b.getAttribute("data-likes") - a.getAttribute("data-likes")
        );
    } else if (critere === "avec-recent" || critere === "avec-ancien") {
        sortedPosts = posts.sort((a, b) => {
            const dateA = convertirDateAJour(
                a.querySelector(".forum-details").textContent
            );
            const dateB = convertirDateAJour(
                b.querySelector(".forum-details").textContent
            );
            if (critere === "avec-recent") {
                return dateA - dateB;
            } else {
                return dateB - dateA;
            }
        });
    } else if (critere === "avec-commentaires") {
        sortedPosts = posts.sort(
            (a, b) =>
                b.getAttribute("data-comments") - a.getAttribute("data-comments")
        );
    }

    const container = document.querySelector(".container-forum");
    sortedPosts.forEach((post) => container.appendChild(post));
}

function showSignalToast() {
    var toastEl = document.getElementById('signalToast');
    var toast = new bootstrap.Toast(toastEl);
    toast.show();
  }
  