<?php
include("sesion.php");
include("conexion.php");
$obj=new conexion();
include("listas.php"); 
error_reporting(E_ALL ^ E_NOTICE);
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8" />
    <title>Sistema de Registro y Control de Alumnos - Núcleo Quíbor</title>
    <link rel="shortcut icon" tyoe="image/x-icon" href="../clavedo.ico" />
    <link rel="author" ref="../humans.txt" />
    <link rel="stylesheet" href="../css/estilos.css" />
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
    <script>
        !window.jQuery && document.write("<script src='../js/jquery.min.js'><\/script>");
    </script>
    <script src="../js/ajax.js"></script>
    <script>
        var ver=false;
        window.onload = function(){
            var lista = document.getElementById("actividad");
            lista.onchange = codigoAsignaciones;

            function codigoAsignaciones(){
                var cod = lista.value;
                document.impirmir_reporte.codigoActividad.value = cod;
                cargarContenido('ver_actividad_datagrid.php','contenido',cod);
                // alert(cod);
            }
        }
    </script>
</head>
<body>
    <header>
        <?php include("header.php"); ?>
    </header>
    <nav>
        <?php include("nav.php"); ?>
    </nav>
    <article id="contenedor-principal">
        <section id="contenedor-actividad">
            <div id="contenedor-buscar">
                <form class="buscar_form form" name="form_Buscar" action="" method="post">
                    <fieldset>
                      <legend>Selecione una Actividad</legend>
                        <select id="actividad" class="list large" name="lstActivida" required>
                            <option value="">Seleccionar</option>
                            <?php $cod=""; listaActividad($cod); ?>
                        </select>
                    </fieldset>
                    <input type="hidden" name="hbtnFuncion" />
                </form>
            </div>
            <div id="contenedor-datagrid">
                <div id="contenido">
                </div>
                <div>
                    <form id"reporte_form"class="center" name="impirmir_reporte" method="post"  target="_blank" action="reporte_actividad.php">
                        <input type="hidden" name="codigoActividad">
                        <button class="boton_1" id="btnImprimir" type="submit" value="">Imprimir</button>
                    </form>
                </div>
            </div>
        </section>
    </article>
    <footer class="fijo">
        <?php include("footer.php"); ?>
    </footer>
</body>
</html>