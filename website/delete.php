<?php
try {
    $bdd = new PDO('sqlite:MALISTE.db');
} catch (PDOException $e) {
    echo "Erreur : " . $e->getMessage();
    die();
}
$requete = "DELETE FROM TRAME";
$result = $bdd->prepare($requete);
$result->execute();

header('Location: index.php');

?>