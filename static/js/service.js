document.addEventListener('DOMContentLoaded', function () {
    // Listener pour la modale de suppression de service
    var confirmDeleteServiceModal = document.getElementById('confirmDeleteServiceModal');
    if (confirmDeleteServiceModal) {
        confirmDeleteServiceModal.addEventListener('show.bs.modal', function (event) {
            var button = event.relatedTarget;
            var serviceId = button.getAttribute('data-service-id');
            var serviceIdToDelete = confirmDeleteServiceModal.querySelector('#serviceIdToDelete');
            serviceIdToDelete.value = serviceId;
            console.log("Service ID à supprimer: " + serviceId);
        });
    }
});

function filtrerService() {
    document.getElementById('service-recherche').addEventListener('submit', filtrerService);

    const entreRecherche = document.getElementById('service-recherche').value.toLowerCase();
    const servicePosters = document.querySelectorAll('.service-post');

    let aucunResultat = true;

    servicePosters.forEach(servicePoste => {
        const nomUtilisateur = servicePoste.getAttribute('data-nomUtilisateur');
        const prix = servicePoste.getAttribute('data-prix');
        const titre = servicePoste.getAttribute('data-titre');
        const description = servicePoste.getAttribute('data-description');
        const horaire = servicePoste.getAttribute('data-horaire');

        if ((nomUtilisateur.includes(entreRecherche) ||
            prix === entreRecherche ||
            titre.toLowerCase().includes(entreRecherche) ||
            description.toLowerCase().includes(entreRecherche) ||
            horaire.toLowerCase().includes(entreRecherche))) {
            servicePoste.classList.remove('fade-out');
            servicePoste.style.display = 'block';
            aucunResultat = false;
        } else {
            servicePoste.classList.add('fade-out');
            setTimeout(() => {
                servicePoste.style.display = 'none';
            }, 300);
        }
    });

    const messageAucunResultat = document.getElementById('aucun-resultat-service');
    if (aucunResultat) {
        messageAucunResultat.style.display = 'block';
    } else {
        messageAucunResultat.style.display = 'none';
    }
}