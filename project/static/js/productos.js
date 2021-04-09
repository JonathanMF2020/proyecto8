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
    $("#btnSiguiente1").removeAttr("hidden");
    $("#btnSiguiente2").prop("hidden", "true");
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

function siguienteProductos2(){
    data = {
        "txtId" : producto.id
    }
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/productos/getDetalles",
        data : data,
        async: true,
        success: function (data) {
            detalles = JSON.parse(data);
            mostrarModalProductos3();
        }
});
}

function mostrarModalProductos2(){
    $("#modalProductos").modal("hide");
    $("#modalProductosLabel2").html("Agregar Producto");
    $("#txtCantidadM").val(0);
    $("#tblDetalleProducto").html("");
    $("#btnAgregarMateriaP").removeProp("hidden");
    $("#btnAgregarMateriaP2").prop("hidden", "true");
    $("#btnGuardarProducto").removeProp("hidden");
    $("#btnGuardarProducto2").prop("hidden", "true");
    llenarListaMateria();
    $("#modalProductos2").modal("show");
}

function mostrarModalProductos3(){
    $("#modalProductos").modal("hide");
    $("#modalProductosLabel2").html("Modificar Producto");
    $("#txtCantidadM").val(0);
    $("#tblDetalleProducto").html("");
    $("#btnAgregarMateriaP2").removeProp("hidden");
    $("#btnAgregarMateriaP").prop("hidden", "true");
    $("#btnGuardarProducto2").removeProp("hidden");
    $("#btnGuardarProducto").prop("hidden", "true");
    llenarListaMateria();
    actualizarDetalleProducto(1);
    $("#modalProductos2").modal("show");
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
    actualizarDetalleProducto(0);
}

function actualizarDetalleProducto(des){
    var str = "";

    for(var i = 0; i < detalles.length; i++){
        detalle = detalles[i];
        str+="<tr>";
        str+="<td>"+detalle.materia.nombre+"</td>";
        str+="<td>"+detalle.cantidad+" "+detalle.materia.unidad+"</td>";
        if(des==0)
            str+="<td><button class='btn btn-smal btn-danger' onclick='eliminarMateriaP("+i+")'><i class='fas fa-trash'></i></button></td>";
        else
            str+="<td><button class='btn btn-smal btn-danger' onclick='eliminarMateriaP2("+i+")'><i class='fas fa-trash'></i></button></td>";
        str+="</tr>";
    }

    $("#tblDetalleProducto").html(str);
}

function guardarProducto(){
    $("#modalProductos2").modal("hide");
    insertarProducto();
}

function guardarProducto2(){
    $("#modalProductos2").modal("hide");
    window.location.replace("http://127.0.0.1:5000/productos/");
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
        "detalles" : JSON.stringify(producto.detalles)
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
<<<<<<< HEAD

function editarProducto(){
    var nombre = $("#txtNombre").val();
    var precio = parseInt($("#txtPrecio").val());
    var descripcion = $("#txtDescripcion").val();
    data={
        "txtId" : producto.id,
        "txtNombre" : nombre,
        "txtDescripcion" : descripcion,
        "txtPrecio" : precio
    }
    $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/productos/guardar",
            async: true,
            data:data,
            success: function (data) {
                json_data = JSON.parse(data);
                if(json_data.result=="OK"){
                    siguienteProductos2();
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

function eliminarProducto(id, nombre){
    Swal.fire({
        icon: 'question',
        title: '¿Esta seguro que quiere eliminar el producto '+nombre,
        showDenyButton: true,
        confirmButtonText: `Cancelar`,
        denyButtonText: `Eliminar`
      }).then((result) => {
        if (result.isDenied) {
            borrarProducto(id);
=======
function confirmarProducto(id){
    alert(id)
    Swal.fire({
        icon: 'question',
        title: '¿Esta seguro que quiere eliminar el producto ?',
        showDenyButton: true,
        confirmButtonText: `Cancelar`,
        denyButtonText: `Eliminar`,
      }).then((result) => {
        if (result.isDenied) {
            eliminarProducto(id);
>>>>>>> bad844a1bfab393be3fd633d3af3b2b136b6f0b2
        }
      })
}

<<<<<<< HEAD
function borrarProducto(id){
    data={
        "txtId" : id
=======
function eliminarProducto(id){
    args = {
        txtId: id
>>>>>>> bad844a1bfab393be3fd633d3af3b2b136b6f0b2
    }
    $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/productos/eliminar",
            async: true,
<<<<<<< HEAD
            data:data,
=======
            data: args,
>>>>>>> bad844a1bfab393be3fd633d3af3b2b136b6f0b2
            success: function (data) {
                json_data = JSON.parse(data);
                if(json_data.result=="OK"){
                    Swal.fire({
                        icon: 'success',
<<<<<<< HEAD
                        title: 'Producto eliminado correctamente',
=======
                        title: 'El producto se eliminó',
>>>>>>> bad844a1bfab393be3fd633d3af3b2b136b6f0b2
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
<<<<<<< HEAD
}

function eliminarMateriaP(pos){
    detalles.splice(pos, 1);
    actualizarDetalleProducto();
}

function modificarProducto(prod){
    producto = prod;
    $("#modalProductos").modal("show");
    $("#modalProductosLabel").html("Modificar Producto");
    $("#txtNombre").val(producto.nombre);
    $("#txtPrecio").val(producto.precio);
    $("#txtCantidad").val(producto.cantidad);
    $("#txtDescripcion").val(producto.descripcion);
    $("#btnSiguiente2").removeAttr("hidden");
    $("#btnSiguiente1").prop("hidden", "true");
}

function agregarMateriaP2(pos){
    var pos=$("#lstMateriaP").val();
    var cantidad=$("#txtCantidadM").val();

    var materia = JSON.parse(materias[pos]);
    var detalle = {
        "materia" : materia,
        "cantidad" : cantidad
    }
    data={
        "txtIdProducto" : producto.id,
        "txtIdMateria" : detalle.materia.id,
        "txtCantidad" : detalle.cantidad
    }
    $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/productos/agregar_detalle",
            async: true,
            data:data,
            success: function (data) {
                var json_data = JSON.parse(data);
                detalle.id = json_data.result;
                detalles.push(detalle);
                actualizarDetalleProducto(1);
            }
    });
}

function eliminarMateriaP2(pos){
    var detalle = detalles[pos];
    data={
        "txtId" : detalle.id
    }
    $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/productos/eliminar_detalle",
            async: true,
            data:data,
            success: function (data) {
                detalles.splice(pos, 1);
                actualizarDetalleProducto(1);
            }
    });
=======
>>>>>>> bad844a1bfab393be3fd633d3af3b2b136b6f0b2
}