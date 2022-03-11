<?php
ini_set('display_errors',1);
ini_set('display_startup_errors',1);
error_reporting(-1);
include 'vendor/autoload.php';

// Initialize and load PDF Parser library 
$parser = new \Smalot\PdfParser\Parser(); 
$nom_dossier = 'PDF_original';
//$nom_dossier = glob(dirname(__FILE__) .'/Fichiers_PDF/*.pdf');
//$nb_pages_pdf= nbr_pages("Fichiers_PDF/2002_renault.pdf");

$dossier = scandir($nom_dossier); 

foreach($dossier as $fichierpdf){
	if ($fichierpdf != '.' && $fichierpdf != '..'){
	$nb_pages_pdf= nbr_pages("PDF_original/".$fichierpdf);

	// Parse pdf file using Parser library 
	
	$pdf = $parser->parseFile("PDF_original/".$fichierpdf); 
	$pages = $pdf->getPages();
	// Extract text from PDF 
	//$textContent = $pdf->getText();
	//$pdfText  =   ( $textContent ); 

	$read=strtok($fichierpdf,".");
	$testfile = "$read.txt";

	$numPage=1;
	//créer et écrire le contenu du pdf dans le fichier texte
	//$fichier_text = fopen($testfile, 'c+b');
	//fwrite($fichier_text, $textContent);
	$text = "";
	$text_final="";

	foreach ($pages as $page) {
		$compteur_numeric=0;
		$nb_mots=0;
		if(($numPage>1) and ($numPage<$nb_pages_pdf)){
			
			$text = $page->getText();
			$text=str_replace( array( '?', ',', '.', ':', '!', '-', '/', '•' , ';'), ' ', $text );  
			$liste_mots=split_words($text);
			$nb_mots=(count($liste_mots));
			foreach ($liste_mots as $mot) {
			
				if(is_numeric($mot)){
					$compteur_numeric=$compteur_numeric+1;
					$nb_mots=$nb_mots-1;
				}
				if(strlen($mot)>=0 and strlen($mot)<2){
					
					$nb_mots=$nb_mots-1;
					
				}
			}	
		}	
		$numPage=$numPage+1;
		if((($nb_mots))>5)  {
			$text_final=$text_final.$text;
			//print_r($liste_mots);echo '</br>';
		}
	}
	//print_r($text_final);
	//$fichier_text = fopen($testfile, 'c+b');
	$fichier_text = fopen('Fichiers_TXT_brut/'.$testfile, 'c+b');
	fwrite($fichier_text, $text_final);
	fclose($fichier_text);
	rename("PDF_original/".$fichierpdf,"Fichiers_tmp/".$fichierpdf) ;
	
	
	/*
	//code nécessaire pour identifier et placer les fichiers pdf encrypté pour les placer dans le fichier pdf_erreurs pour retraitement et desencryptage
	$fichier_text = 'Fichiers_TXT/'.$testfile;
	if(filesize($fichier_text)<=0){
		
		rename("Fichiers_PDF/".$fichierpdf,"PDF_erreurs/".$fichierpdf) ;
	}else{
		
		rename("Fichiers_PDF/".$fichierpdf,"PDF_traités/".$fichierpdf) ;
	}
	*/
	

	}
} 

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



?>