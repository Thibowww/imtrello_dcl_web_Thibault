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