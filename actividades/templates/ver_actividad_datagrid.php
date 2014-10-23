<?php
header('Content-Type: text/html; charset=UTF-8');
error_reporting(E_ALL ^ E_NOTICE);
$cod = $_POST['cedula'];
require 'DataGrid.php';
include("funciones.php");


$con=mysql_connect("localhost","root","") or die("No se pudo conectar con el servidorde BD");
mysql_select_db("bd_orquesta", $con) or die("No se pudo conectar con la BD");
mysql_set_charset('utf8');

$sentencia = "SELECT CONCAT(a.nombres,' ',a.apellidos) AS nombre, a.cedula_alumno, date_format(a.fecha_nacimiento,'%d-%m-%Y') AS fecha,	a.sexo, (i.nombre) AS instrumento,  date_format(a.fecha_nacimiento,'%Y') AS ano FROM alumno a, instrumento i, alumno_actividad aa WHERE a.cedula_alumno=aa.cedula_alumno AND aa.cod_instru=i.cod_instru	AND aa.cod_activ='$cod' ORDER BY i.orden, ano DESC";

$users = array();
$result = mysql_query($sentencia, $con);
while ($row = mysql_fetch_assoc($result))
{
    $users[] = $row;
}
mysql_free_result($result);
?>
<html><head>
<style>
.fdg_sortable {cursor:pointer;text-decoration:underline;color:#00f}
.fila {background-color:#E0F8F7;}
.filaAlterna {background-color:#BCF5A9}
</style></head><body>
<?php
Fete_ViewControl_DataGrid::getInstance($users)
->setGridAttributes(array('cellspacing' => '5', 'cellpadding' => '5', 'border' => '9'))
// ->enableSorting(true)
->removeColumn('ano')
->setup(array(
	'nombre' => array('header' => 'Nombres y Apellios'),
    'cedula_alumno' => array('header' => 'Cedula'),
    'fecha' => array('header' => 'F. Nacimiento'),
    // 'edad' => array('header' => 'Edad'),
    'sexo' => array('header' => 'Sexo'),
    'instrumento' => array('header' => 'Instumento')
))

->addColumnBefore('counter', '%counter%.', 'Nro.', array('align' => 'right'))
->setStartingCounter(1)
->setRowClass('fila')
->setAlterRowClass('filaAlterna')
->render();
?>
</body>
</html>











