<html>
<head>
<meta http-equiv = "X-UA-Compatible" content = "IE = 9; IE = 8; IE = 7; IE = edge" /> 
<meta content="text/html;charset=utf-8" http-equiv="Content-Type">
<meta content="utf-8" http-equiv="encoding">


<title>COURBE</title>
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
//$query = "SELECT * FROM $usertable";
$query = "SELECT Nom_Entreprise FROM compositions_cac40 ORDER BY Nom_Entreprise ASC";	
//$query="SHOW TABLES FROM cac40";

$liste_entreprises= array();
$result = mysqli_query($conn,$query);
	
if($result){
	while($row = mysqli_fetch_array($result)){
		$liste_entreprises[] = $row[0];
	}
}

$query_date="SELECT Date_Mois, Close FROM air_liquide ORDER BY Date_Mois ASC";

$result = mysqli_query($conn, $query_date);
$liste_dates= array();
$liste_cot_close= array();
if($result){
	while($row = mysqli_fetch_array($result)){
		$liste_dates[] = $row[0];
		$liste_cot_close[] = $row[1];
	}
}



?>
<select name="choix_entreprise" id='id_choix_entreprise' class="choix_entreprise">
	<option selected="selected" >Sélectionner une valeur</option>
	<?php
	// Parcourir la liste des enterprises
	foreach($liste_entreprises as $value){
	?>
		
		<option value="<?php echo($value); ?>"><?php echo $value; ?></option>

	<?php
	}
	?>
</select>
<div id='courbe'>
<canvas id="plots" style="width:100%;max-width:700px"></canvas>
</div>
</body>
<script type="text/javascript" src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.min.js"></script>
<script>
document.getElementById("id_choix_entreprise").selectedIndex = 1;

$('.choix_entreprise').change(function(){
		var nom_entreprise_brut = document.getElementById('id_choix_entreprise').options[document.getElementById('id_choix_entreprise').selectedIndex].value;
		nom_entreprise=nom_entreprise_brut.replace(" ","_")
		nom_entreprise=nom_entreprise.replace("'","")
		nom_entreprise=(nom_entreprise.replace(".","")).toLowerCase();
		
		//alert(nom_entreprise);
		
							
		var posting=$.post('envoi_courbe.php', { 
		
			entreprise: nom_entreprise,
			entreprise_brut : nom_entreprise_brut,
		}, function(data){			
		$('#courbe').empty().append(data);
				
		});
});		


// Get the HTML canvas by its id 
plots = document.getElementById("plots");
// Example datasets for X and Y-axes 
var date_mois = <?php echo json_encode($liste_dates); ?>;//Stays on the X-axis 
var cotations = <?php echo json_encode($liste_cot_close); ?>; //Stays on the Y-axis 
var label_concat = 'Air Liquide';
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