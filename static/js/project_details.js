document.getElementById('edit-project-btn').addEventListener('click', function() {
    // Effectuer une requête AJAX pour récupérer le formulaire de modification
    var xhr = new XMLHttpRequest();
    var editUrl = this.getAttribute('data-edit-url');
    xhr.open('GET', editUrl, true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.onload = function() {
        if (xhr.status === 200) {
            // Afficher le formulaire dans le conteneur approprié
            document.getElementById('edit-project-form-container').innerHTML = xhr.responseText;
        } else {
            // Afficher un message d'erreur en cas d'échec du chargement du formulaire
            console.error('Failed to load edit project form');
        }
    };
    xhr.send();
});

function toggleFormVisibility() {
            var manager = document.getElementById("manager_use").getAttribute("manager");
            var user = document.getElementById("manager_use").getAttribute("username");
            var container_manager = document.getElementById("manager_use");
            if (user === manager) {
                container_manager.style.display = "block";  // Afficher le formulaire
            } else {
                container_manager.style.display = "none";   // Masquer le formulaire
            }
        }
        window.onload = toggleFormVisibility;