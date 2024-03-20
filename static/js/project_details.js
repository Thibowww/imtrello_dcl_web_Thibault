document.getElementById('edit-project-btn').addEventListener('click', function() {
    // Effectuer une requête AJAX pour récupérer le formulaire de modification
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '{{ url_for("edit_project_form", project_id=project.id) }}', true);
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