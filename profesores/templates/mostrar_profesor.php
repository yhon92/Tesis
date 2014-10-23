<?php 
include("conexion.php");
$obj=new conexion();
include("listas.php");
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8" />
    <title>Sistema de Registro y Control de Alumnos - Núcleo Quíbor</title>
    <link rel="shortcut icon" tyoe="image/x-icon" href="../clavedo.ico" />
    <link rel="author" ref="../humans.txt" />
    <link rel="stylesheet" href="../css/estilos.css" />
    <script>
        function soloLetras(e){
            key = e.keyCode || e.which;
            tecla = String.fromCharCode(key).toLowerCase();
            letras = " áéíóúüabcdefghijklmnñopqrstuvwxyz";
            especiales = [8,37,39,46];

            tecla_especial = false
                for(var i in especiales){
                    if(key == especiales[i]){
                        tecla_especial = true;
                    break;
                }
            }

            if(letras.indexOf(tecla)==-1 && !tecla_especial){
            return false;
            }
        }

        function soloNum(e){
            key = e.keyCode || e.which;
            tecla = String.fromCharCode(key).toLowerCase();
            num = "0123456789";
            especiales = [8,37,39,46];

            tecla_especial = false
                for(var i in especiales){
                    if(key == especiales[i]){
                        tecla_especial = true;
                    break;
                }
            }

            if(num.indexOf(tecla)==-1 && !tecla_especial){
            return false;
            }
        }

        function operacion(){
            document.form_Registrar.hbtnFuncion.value="eliminarProfesor";
            document.submit();
        }

        var ver=false;
        window.onload = function(){
            if (ver) {
                document.getElementById("mostrar_form").style.visibility="visibile";
            } else
                document.getElementById("mostrar_form").style.visibility="hidden";
            var lista = document.getElementById("profesor");
            lista.onchange = cedulaProfesor;

            function cedulaProfesor(){
                window.location = "?p="+lista.value
            }

            document.getElementById("btnEliminar").onclick = operacion;
            document.getElementById("btnCancelar").onclick = salir;
        }
    </script>
    <?
        if (isset($_POST["hbtnFuncion"])) {
            $obj->vCedula = $_POST["txtCedula"];
            $obj->funSaberOperacion();
        }
        if ($_POST["hbtnFuncion"]=="eliminarProfesor") {
                ?><script>
                    location.href="mostrar_profesor.php";
                </script><?
            }
    ?>
</head>
<body>
    <header>
        <?php include("header.php"); ?>
    </header>
    <nav>
        <?php include("nav.php"); ?>
    </nav>
    <article id="contenedor-principal">
        <section >
            <div id="contenedor-buscar">
                <form class="buscar_form form" name="form_Buscar" action="" method="post">
                    <fieldset>
                      <legend>Selecione un Profesor</legend>
                        <select id="profesor" class="list large" name="lstProfesor" required>
                            <option value="">Seleccionar</option>
                            <?php $cod = $_GET["p"]; listaProfesor($cod); ?>
                        </select>
                        <?php 
                            if ($_GET["p"]!=null) {
                                // echo $codigo;
                                if ($obj->buscarProfesor($cod)) {
                                    ?><script>
                                        ver = true;
                                    </script><?
                                }
                            }
                        ?>
                    </fieldset>
                    <input type="hidden" name="hbtnFuncion" />
                </form>
            </div>
            <div id="contenedor-registar">
                <form id="mostrar_form" class="registrar_form form" name="form_Registrar" action="#" method="post">
                    <h3>Mostrar Datos</h3><br>
                    <fieldset>
                        <legend>Datos Personales</legend>
                        <div>
                            <label for="nombres">Nombres: <h2><?echo $obj->vNombres;?></h2></label>
                            
                        </div>
                        <div>
                            <label for="apellidos">Apellidos: <h2><?echo $obj->vApellidos;?></h2></label>
                        </div>
                        <div>
                            <label for="cedula">Cédula: <h2><?echo $obj->vCedula;?></h2></label>
                        </div>
                        <div>
                            <label for="estado" name="lblEstado">Estado: 
                                <h2><?echo $obj->vEstado;?></h2>
                            </label>
                        </div>
                    </fieldset>
                    <div>
                        <button id="btnEliminar"class="boton_2" type="submit" >Eliminar</button>
                        <button id="btnCancelar" class="boton_1" type="button" onclick("salir();")>Cancelar</button>
                    </div>
                        <input type="hidden" name="txtCedula" value="<?echo $obj->vCedula?>" />
                        <input type="hidden" name="hbtnFuncion" />
                    </div>
                </form>                 
            </div>
        </section>
    </article>
    <footer class="fijo">
        <?php include("footer.php"); ?>
    </footer>
    <script>
        function salir(){
            location.href="home.php";
        }
    </script>
</body>
</html>