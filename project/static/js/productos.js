var materias = [];
var detalles = [];
var producto = new Object;

function agregarProducto(){
    $("#modalProductos").modal("show");
    $("#modalProductosLabel").html("Agregar Producto");
    $("#txtNombre").val("");
    $("#txtPrecio").val(0);
    $("#txtCantidad").val(0);
    $("#txtDescripcion").val("");
}

function siguienteProductos(){
    var nombre = $("#txtNombre").val();
    var precio = parseInt($("#txtPrecio").val());
    var descripcion = $("#txtDescripcion").val();
    if(nombre != "" && precio > 0 && descripcion != ""){
        producto = {
            "nombre" : nombre,
            "precio" : precio,
            "descripcion" : descripcion,
            "cantidad" : 0,
            "detalles" : []
        }
        mostrarModalProductos2();
    }
    else{
        Swal.fire({
            icon: 'error',
            title: 'Campos invalidos',
            text: 'Debes llenar todos los campos'
        })
    }
}

function mostrarModalProductos2(){
    $("#modalProductos").modal("hide");
    $("#modalProductos2").modal("show");
    $("#modalProductosLabel2").html("Agregar Producto");
    $("#txtCantidadM").val(0);
    $("#tblDetalleProducto").html("");
    llenarListaMateria();
}

function agregarMateriaP(){
    var pos=$("#lstMateriaP").val();
    var cantidad=$("#txtCantidadM").val();

    var materia = JSON.parse(materias[pos]);
    var detalle = {
        "materia" : materia,
        "cantidad" : cantidad
    }
    detalles.push(detalle);
    var str = "";

    for(var i = 0; i < detalles.length; i++){
        detalle = detalles[i];
        str+="<tr>";
        str+="<td>"+detalle.materia.nombre+"</td>";
        str+="<td>"+detalle.cantidad+" "+detalle.materia.unidad+"</td>";
        str+="</tr>";
    }

    $("#tblDetalleProducto").html(str);
}

function guardarProducto(){
    producto.detalles=detalles;
    console.log(producto);
    $("#modalProductos2").modal("hide");
    insertarProducto();
}

function llenarListaMateria(){
    $.ajax({
            type: "GET",
            url: "http://127.0.0.1:5000/materias/getAll",
            async: true,
            success: function (data) {
                materias = JSON.parse(data);
                var str = "";
                for(var i = 0; i < materias.length; i++){
                    var materia = JSON.parse(materias[i]);
                    str+="<option value="+i+">";
                    str+= materia.nombre;
                    str+="</option>";
                }
                $("#lstMateriaP").html(str);
            }
    });
}

function insertarProducto(){
    data={
        "txtId" : "",
        "txtNombre" : producto.nombre,
        "txtDescripcion" : producto.descripcion,
        "txtPrecio" : producto.precio,
        "detalles" : producto.detalles
    }
    $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/productos/guardar",
            async: true,
            data:data,
            success: function (data) {
                json_data = JSON.parse(data);
                if(json_data.result=="OK"){
                    Swal.fire({
                        icon: 'success',
                        title: 'Producto agregado correctamente',
                        showDenyButton: false,
                        confirmButtonText: `Ok`
                      }).then((result) => {
                        if (result.isConfirmed) {
                            window.location.replace("http://127.0.0.1:5000/productos/");
                        }
                      })
                }
                else{
                    Swal.fire({
                        icon: 'error',
                        title: 'Algo salió mal...',
                        text: 'Intentelo de nuevo más tarde'
                    })
                }
            }
    });
}