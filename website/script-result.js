// Si l'ulisateur essaye de fermer la page, on lui demande confirmation
window.onbeforeunload = function() {
    return "Etes-vous sûr de vouloir quitter ?";
}

// Path: script-result.js