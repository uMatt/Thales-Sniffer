<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="utf-8">
        <title>Sniffer Ethernet</title>
        <link rel="shortcut icon" href="assets/favicon.png" type="image/x-icon">
        <link rel="stylesheet" href="index.css">
    </head>
    <body>
        <div id="topBar">
            <div id="topBartransparent">
                <a href="index.php">
                    <img class="logo-top-bar" src="assets/thales-logo.png" alt="logo sniffer">
                </a>
            </div>
            <div>
                <img src="assets/banner-search.png" id="banner-img" alt="Image d'un satelite">
                <h1 id="searchTitle">Recherche</h1>
            </div>
        </div>

        <div id="search">
            <form action="result.php" method="get">
                <div id="search-bar">
                    <label for="name" id="textTestName">Nom du test : </label>
                    <select name="name" id="testName">
                        <option value="">--Choisir un test--</option>
                        <?php
                            try {
                                $bdd = new PDO('sqlite:MALISTE.db');
                            } catch (PDOException $e) {
                                echo "Erreur : " . $e->getMessage();
                                die();
                            }
                            $requete = "SELECT DISTINCT bench_3 FROM TRAME";
                            $result = $bdd->query($requete);
                            while ($row = $result->fetch()) {
                                echo "<option value='" . $row['bench_3'] . "'>" . $row['bench_3'] . "</option>";
                            }
                            
                        ?>

                    </select>

                    <label for="date" id="textTestDate">Date du test :</label>
                    <select name="date" id="testDate">
                        <option value="">--Choisir une date--</option>
                        <?php
                            try {
                                $bdd = new PDO('sqlite:MALISTE.db');
                            } catch (PDOException $e) {
                                echo "Erreur : " . $e->getMessage();
                                die();
                            }
                            $requete = "SELECT DISTINCT date FROM TRAME";
                            $result = $bdd->query($requete);
                            while ($row = $result->fetch()) {
                                echo "<option value='" . $row['date'] . "'>" . $row['date'] . "</option>";
                            }
                        ?>
                    </select>
                    <input type="submit" disabled value="Exécuter">
                    <!-- si la valeur des select ne sont pas "" alors on active les boutons -->
                    <script>
                        var testName = document.getElementById("testName");
                        var testDate = document.getElementById("testDate");
                        var btn = document.querySelector("input[type='submit']");
                        testName.addEventListener("change", function() {
                            if (testName.value != "" && testDate.value != "") {
                                btn.disabled = false;
                            }
                        });
                        testDate.addEventListener("change", function() {
                            if (testName.value != "" && testDate.value != "") {
                                btn.disabled = false;
                            }
                        });
                    </script>
                </div>
            </form>
        </div>
    </body>
</html>

