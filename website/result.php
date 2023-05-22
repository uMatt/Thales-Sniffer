<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="utf-8">
        <title>Sniffer Ethernet - Résultats</title>
        <link rel="shortcut icon" href="assets/favicon.png" type="image/x-icon">
        <link rel="stylesheet" type="text/css" href="result.css">
    </head>
    <body>
        <div id="topBar">
            <div id="topBartransparent">
                <a href="index.php">
                    <img class="logo-top-bar" src="assets/thales-logo.png" alt="logo sniffer">
                </a>
            </div>
            <div>
                <img src="assets/banner-results.png" id="banner-img" alt="Image d'un satelite">
                <h1 id="resultTitle">Résultats</h1>
            </div>
        </div>
        <div>
            <form action="delete.php" method="post">
                <?php
                    echo '<input type="hidden" name="name" value="' . $_GET["name"] . '">';
                    echo '<input type="submit" value="supprimer" id="btn-delete">';
                ?>
            </form>
        </div>
        <div id="results-table">
            <?php
            // récupération du nom des entêtes
            $filename = file("result_name.txt");
            // Connexion à la base de données
            try {
                $bdd = new PDO('sqlite:MALISTE.db');
            } catch (PDOException $e) {
                echo "Erreur : " . $e->getMessage();
                die();
            }

            
            $elements_par_page = 50;
            $page = isset($_GET['page']) ? $_GET['page'] : 1;
            $indice_depart = ($page - 1) * $elements_par_page;

            //! ATTENTION CHANGER LE BENCH_3 EN LE NOM DANS LA BASE DE DONNEES DU TEST !!!
            $requete = "SELECT * FROM TRAME WHERE bench_3 = '" . $_GET['name'] . "' AND date = '" . $_GET['date'] . "' LIMIT " . $elements_par_page . " OFFSET " . $indice_depart;
            $result = $bdd->query($requete);

            // Affichage du tableau
            echo "<table>";
            echo "<tr>";
            echo "<form>";
            
            foreach ($filename as $value) {
                echo '<th><input type="text" id="' . $value . '" value="' . $value . '"></th>';
            }
            echo "</form>";
            echo "</tr>";
            while ($row = $result->fetch()) {
                echo "<tr>";
                echo "<td>" . $row['numero'] . "</td>";
                echo "<td>" . $row['numero_trame'] . "</td>";
                echo "<td>" . $row['date'] . "</td>";
                echo "<td>" . $row['PMID'] . "</td>";
                echo "<td>" . $row['bench_3'] . "</td>";
                echo "<td>" . $row['bench_5'] . "</td>";
                echo "<td>" . $row['Taille'] . "</td>";
                echo "<td>" . $row['Mac_Src'] . "</td>";
                echo "<td>" . $row['Mac_Dst'] . "</td>";
                echo "<td>" . $row['type'] . "</td>";
                echo "<td>" . $row['Field_2'] . "</td>";
                echo "<td>" . $row['Field_3'] . "</td>";
                echo "<td>" . $row['Field_4'] . "</td>";
                echo "<td>" . $row['Field_5'] . "</td>";
                echo "<td>" . $row['Field_6'] . "</td>";
                echo "<td>" . $row['Field_7'] . "</td>";
                echo "<td>" . $row['MAC_Sender'] . "</td>";
                echo "<td>" . $row['Source_IP'] . "</td>";
                echo "<td>" . $row['Sender_IP'] . "</td>";
                echo "<td>" . $row['Dest_IP'] . "</td>";
                echo "<td>" . $row['MAC_Target'] . "</td>";
                echo "<td>" . $row['Field_9'] . "</td>";
                echo "<td>" . $row['Target_IP'] . "</td>";
                echo "<td>" . $row['Field_10'] . "</td>";
                echo "<td>" . $row['Field_11'] . "</td>";
                echo "<td>" . $row['Field_14'] . "</td>";
                echo "<td>" . $row['Field_16'] . "</td>";
                echo "<td>" . $row['Field_17'] . "</td>";
                echo "<td>" . $row['Field_18'] . "</td>";
                echo "<td>" . $row['Field_20'] . "</td>";
                echo "<td>" . $row['Field_21'] . "</td>";
                echo "<td>" . $row['Field_23'] . "</td>";
                echo "<td>" . $row['Field_25'] . "</td>";
                echo "<td>" . $row['Field_26'] . "</td>";
                echo "<td>" . $row['Field_28'] . "</td>";
                echo "<td>" . $row['Field_29'] . "</td>";
                echo "<td>" . $row['Field_30'] . "</td>";
                echo "<td>" . $row['Field_32'] . "</td>";
                echo "<td>" . $row['Field_33_34_35'] . "</td>";
                echo "<td>" . $row['Packet'] . "</td>";
                echo "</tr>";
            }
            echo "</table>";
            $bdd = null;
            /*
            $requete_count = "SELECT COUNT(*) AS total FROM TRAME";
            $resultat_count = $connexion->query($requete_count);
            $ligne_count = $resultat_count->fetch();
            $total_elements = $ligne_count['total'];
            $nombre_pages = ceil($total_elements / $elements_par_page);
            for ($i = 1; $i <= $nombre_pages; $i++) {
                echo "<a href=\"?page=$i\">$i</a> ";
            }*/
            ?>
        </div>
    </body>
    <script src="script-result.js"></script>
</html>
