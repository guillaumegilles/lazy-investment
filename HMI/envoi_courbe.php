<html>
<head>

<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"> 

</head>
<body>
<?php
$servername = 'localhost';
$username = 'root';
$password = '';
$db='cac40';
$port='3308';
            
//On établit la connexion
$conn = new mysqli($servername, $username, $password, $db, $port);
            
//On vérifie la connexion
if($conn->connect_error){
    die('Erreur : ' .$conn->connect_error);
}
if(isset($_POST['entreprise_brut'])){
	$nom_entreprise_brut = ($_POST['entreprise_brut']);

}

if(isset($_POST['entreprise'])){
	$nom_entreprise = ($_POST['entreprise']);
	//echo "Entreprise séléctionnée : ".$nom_entreprise;

	//$query_date="SELECT LEFT(Date_Mois,4), Close FROM $nom_entreprise WHERE (RIGHT(Date_Mois,2) like '12') ORDER BY Date_Mois ASC";
	$query_date="SELECT Date_Mois, Close FROM $nom_entreprise  ORDER BY Date_Mois ASC";

$result = mysqli_query($conn, $query_date);
$liste_dates= array();
$liste_cot_close= array();
if($result){
	while($row = mysqli_fetch_array($result)){
		$liste_dates[] = $row[0];
		$liste_cot_close[] = $row[1];
	}
}

/*
print_r($liste_dates)	;
echo '</br>';echo '</br>';

print_r($liste_cot_close)	;
*/
}
?>
<div id='courbe'>



</div>

<canvas id="plots" style="width:100%;max-width:700px"></canvas>


</body>
<script type="text/javascript" src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.min.js"></script>

<script>


// Get the HTML canvas by its id 
plots = document.getElementById("plots");
// Example datasets for X and Y-axes 
var date_mois = <?php echo json_encode($liste_dates); ?>;//Stays on the X-axis 
var cotations = <?php echo json_encode($liste_cot_close); ?>; //Stays on the Y-axis 
var label_concat = 'Cotations '+<?php echo json_encode($nom_entreprise_brut); ?>;
// Create an instance of Chart object:
new Chart(plots, {
	type: 'line', //Declare the chart type 
	data: {
		
		labels: date_mois, //X-axis data 
		
		datasets: [{
			label: label_concat,
			data: cotations, //Y-axis data 
			backgroundColor: 'blue',
			borderColor: 'darkblue',
			fill: false, //Fills the curve under the line with the babckground color. It's true by default 
		}]
	},
});

</script>

</html>