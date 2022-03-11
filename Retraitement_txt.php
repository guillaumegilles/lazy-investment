<html>
<head>
<meta http-equiv = "X-UA-Compatible" content = "IE = 9; IE = 8; IE = 7; IE = edge" /> 
<meta content="text/html;charset=utf-8" http-equiv="Content-Type">
<meta content="utf-8" http-equiv="encoding">
<title>BNA</title>
</head>
<body>


<?php
ini_set('display_errors',1);
ini_set('display_startup_errors',1);
error_reporting(-1);

//retraitement du fichier TXT -- supression ponctuation, supression des lignes avec plus de 4 nombres...
$nom_dossier = 'Fichiers_TXT_brut';
$dossier = opendir($nom_dossier);

while($fichier = readdir($dossier))
{
	
if($fichier != '.' && $fichier != '..')
{
	$texte="";
	foreach(file("Fichiers_TXT_brut/".$fichier) as $line) {
		print($line);
		$compteur_numeric=0;
		$nb_mots=0;
		$nb_petits_mots=0;
		$line=utf8_decode($line);
		
		$line =str_replace( array( '?', ',', '.', ':', '!', '-', '/', '•', "'", ';', "\t"), ' ', $line ); 
		
		$liste_mots=(explode(" ",$line ));
		$nb_mots=(count($liste_mots));
		
		foreach ($liste_mots as $mot) {
			if(is_numeric($mot)){
				$compteur_numeric=$compteur_numeric+1;
				$nb_mots=$nb_mots-1;
			}
			if(strlen($mot)>0 and strlen($mot)<2){
				
				$nb_mots=$nb_mots-1;
				$nb_petits_mots=$nb_petits_mots+1;
			}
			
		}		
		if(($compteur_numeric<4) and (($nb_mots)>5) and (($nb_petits_mots)<10))  {
	
			$texte=$texte.$line;	
			
		}
		
	}
print($texte);
	$fichier_text2 = fopen("Fichiers_TXT_traités/".$fichier, 'c+b');
	fwrite($fichier_text2, $texte);
	//file_put_contents($fichier_text2, utf8_encode(file_get_contents($texte)));

	fclose($fichier_text2);
	

	if(filesize("Fichiers_TXT_traités/".$fichier)<=1000){
		

		rename("Fichiers_TXT_traités/".$fichier,"TXT_erreurs/".$fichier) ;
	}else{
		rename("Fichiers_TXT_brut/".$fichier,"Fichiers_tmp/".$fichier) ;
	}
}
}
closedir($dossier);

/*reclassement des fichiers vide ou partiellement complet
$nom_dossier = 'Fichiers_TXT_traités';
$dossier = opendir($nom_dossier); 

while($fichier_txt = readdir($dossier)){


	if(filesize("Fichiers_TXT_traités/".$fichier_txt)<=1000){
		
		rename("Fichiers_TXT_traités/".$fichier_txt,"TXT_erreurs/".$fichier_txt) ;
	}

}
*/
	
function split_words($string){ 
    $retour = array(); 
    $delimiteurs = ' .!?, :;(){}[]%/-'; 
    $tok = strtok($string, " "); 
	while (strlen(join(" ", $retour)) != strlen($string)) { 

		array_push($retour, $tok); 
		$tok = strtok($delimiteurs); 
	  
    } 
    return $retour; 
}

function nbr_pages($pdf){
   if (false !== ($fichier = file_get_contents($pdf))){
      $pages = preg_match_all("/\/Page\W/", $fichier, $matches);
      return $pages;
   }
}



/*
$output = shell_exec("python Comparaison.cgi");
echo $output;
// on se connecte à MySQL 
//$db = mysql_connect('zulhfnptrimbuj.mysql.db', 'zulhfnptrimbuj', 'JaJa1503'); 
$servername = "zulhfnptrimbuj.mysql.db";
$username = "zulhfnptrimbuj";
$password = "JaJa1503";
$dbname = "zulhfnptrimbuj";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
} 

$sql = "SELECT * FROM cac40";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
  // output data of each row
  while($row = $result->fetch_assoc()) {
    echo "id: " . $row["Nom_fichier_PDF"]. " - Name: " . $row[Nom_Entreprise]. " " . $row[2]. "<br>";
  }
} else {
  echo "0 results";
}
$conn->close();
/*
$source_pdf="http://trimbtech.fr/CAC40_lazy_price/Fichiers_PDF/2001_renault.pdf";
$source_pdf="http://webmedicalt/Trajectoire_TEST/2001_renault.pdf";
$source_pdf="2001_renault.pdf";
$output_folder="http://trimbtech.fr/CAC40_lazy_price/Fichiers_TXT";*/


?>