var clientes = [];
var productos = [];
var detalles = [];
var venta = new Object;


function agregarVenta(){
    llenarListaClientes();
    $("#modalVentas").modal("show");
    $("#modalVentasLabel").html("Agregar Venta");
    $("#txtFecha").val("");
    $("#txtComentarios").val(0);
    $("#txtId").val("");

    $("#btnSiguiente1").removeAttr("hidden");
    $("#btnSiguiente2").prop("hidden", "true");
}

function llenarListaClientes(){
$.ajax({
    type: "GET",
    url: "http://127.0.0.1:5000/clientes/getAll",
    async: true,
    success: function (data) {
        clientes = JSON.parse(data);
        var str = "";
        for(var i = 0; i < clientes.length; i++){

            var cliente = JSON.parse(clientes[i]);
            str+="<option value="+cliente.id+">";
            str+= cliente.nombre_empresa;
            str+="</option>";
        }
        $("#lstCliente").html(str);
    }
});
}

function siguienteClientes(){
    var pos = $("#lstCliente").val();
    var fecha = $("#txtFecha").val();
    var comentarios = $("#txtComentarios").val();

    if(fecha != "" && comentarios != "" && pos >= 0){
        venta = {
            "fecha" : fecha,
            "idC": pos,
            "comentarios" : comentarios,
            "detallesVenta" : []
        }
        mostrarModalVentas2();
    }
    else{
        Swal.fire({
            icon: 'error',
            title: 'Campos invalidos',
            text: 'Debes llenar todos los campos'
        })
    }
}

function mostrarModalVentas2(){
    $("#modalVentas").modal("hide");
    $("#modalVentasLabel2").html("Agregar Producto");
    llenarListaProductosVenta();
    $("#txtTalla").val(0);
    $("#txtCantidadV").val(0);
    $("#txtPrecio").val(0);
    $("#tblDetalleVenta").html("");
    $("#btnAgregarVentasP").removeProp("hidden");
    $("#btnAgregarVentasP2").prop("hidden", "true");
    $("#btnGuardarVenta").removeProp("hidden");
    $("#btnGuardarVenta2").prop("hidden", "true");
    
    $("#modalVentas2").modal("show");
}

function llenarListaProductosVenta(){
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/productos/getAll",
        async: true,
        success: function (data) {
            productos = JSON.parse(data);
            var str = "";
            for(var i = 0; i < productos.length; i++){
                var producto = JSON.parse(productos[i]);
                str+="<option value="+i+">";
                str+= producto.nombre;
                str+="</option>";
            }
            $("#lstProductosP").html(str);
        }
    });
    }
function eliminarProductoVemtaP(pos){
        detalles.splice(pos, 1);
        actualizarDetalleProductoVentas();
    }
    
function agregarProductoVentaP(){
        var pos=$("#lstProductosP").val();
        var cantidad=$("#txtCantidadV").val();
        var talla=$("#txtTalla").val();
        var color=$("#lstColores").val();
        var precio_unitario=$("#txtPrecio").val();
        var producto = JSON.parse(productos[pos]);
        var detalle = {
            "producto" : producto,
            "talla" : talla,
            "color" : color,
            "precio_unitario" : precio_unitario,
            "cantidad" : cantidad,

        }
        detalles.push(detalle);
        actualizarDetalleProductoVentas(0);
    }

    function agregarProductoVentaP2(pos){
        var poss=$("#lstProductosP").val();
        var cantidad=$("#txtCantidadV").val();
        var talla=$("#txtTalla").val();
        var color=$("#lstColores").val();
        var producto = JSON.parse(productos[poss]);
        var dett =detalles;
        data={
            "txtProducto" : producto.id,
            "txtPrecioProducto" : producto.precio,
            "txtTalla" : talla,
            "txtColor" : color,
            "txtCantidad" : cantidad,
            "txtIdVenta" : venta.id,
            "txtIdProducto" : producto.id,
        }
        $.ajax({
                type: "POST",
                url: "http://127.0.0.1:5000/ventas/agregar_detalle",
                async: true,
                data:data,
                success: function (data) {
                    var json_data = JSON.parse(data);
                    detalle.id = json_data.result;
                    detalles.push(detalle);
                    actualizarDetalleProductoVentas(1);
                }
        });
    }

    function actualizarDetalleProductoVentas(des){
        var str = "";    
        for(var i = 0; i < detalles.length; i++){
            detalle = detalles[i];
            str+="<tr>";
            str+="<td>"+detalle.producto.nombre+"</td>";
            str+="<td>"+detalle.cantidad+"</td>";
            if(des==0)
                str+="<td><button class='btn btn-smal btn-danger' onclick='eliminarProductoVemtaP("+i+")'><i class='fas fa-trash'></i></button></td>";
            else
                str+="<td><button class='btn btn-smal btn-danger' onclick='eliminarProductoVentaP2("+i+")'><i class='fas fa-trash'></i></button></td>";
            str+="</tr>";
        }
    
        $("#tblDetalleVenta").html(str);
    }

function eliminarProductoVentaP2(pos){
        var detalle = detalles[pos];
        data={
            "txtId" : detalle.id
        }
        $.ajax({
                type: "POST",
                url: "http://127.0.0.1:5000/ventas/eliminar_detalle",
                async: true,
                data:data,
                success: function (data) {
                    detalles.splice(pos, 1);
                    actualizarDetalleProductoVentas(1);
                }
        });
    }

    function insertarVenta(){

        data={
            "txtId" : "",
            "txtClienteI" : venta.idC,
            "txtFecha" : venta.fecha,
            "txtComentarios" : venta.comentarios,
            "detallesVenta" : JSON.stringify(detalles)
        }
        $.ajax({
                type: "POST",
                url: "http://127.0.0.1:5000/ventas/guardar",
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
                                window.location.replace("http://127.0.0.1:5000/ventas/");
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
    function guardarVenta(){
        $("#modalVentas2").modal("hide");
        insertarVenta();
    }
    function guardarVenta2(){
        $("#modalVentas2").modal("hide");
        window.location.replace("http://127.0.0.1:5000/ventas/");
    }
    function modificarVentas(vent){
        venta = vent;
        var valor=venta.cliente_id;
        llenarListaClientes();
        console.log(venta.cliente_id);
        $("#lstCliente").val(2).change();

        $("#modalVentas").modal("show");
        $("#modalVentasLabel").html("Modificar Venta");
        $("#txtId").val(venta.id);
        $("#txtPrecio").val(venta.precio);
        $("#txtFecha").val(venta.date);
        $("#txtComentarios").val(venta.comentarios);
        $("#btnSiguiente2").removeAttr("hidden");
        $("#btnSiguiente1").prop("hidden", "true");
    }
    function confirmarVenta(id){
        Swal.fire({
            icon: 'question',
            title: '¿Esta seguro que quiere cancelar la venta ?',
            showDenyButton: true,
            confirmButtonText: `Cancelar`,
            denyButtonText: `Eliminar`,
          }).then((result) => {
            if (result.isDenied) {
                eliminarVenta(id);
            }
          })
    }
    
    function eliminarVenta(id){
        data = {
            txtId: id
        }
        $.ajax({
                type: "POST",
                url: "http://127.0.0.1:5000/ventas/eliminar",
                async: true,
                data:data,
                success: function (data) {
                    json_data = JSON.parse(data);
                    if(json_data.result=="OK"){
                        Swal.fire({
                            icon: 'success',
                            title: 'Venta cancelada correctamente',
                            showDenyButton: false,
                            confirmButtonText: `Ok`
                          }).then((result) => {
                            if (result.isConfirmed) {
                                window.location.replace("http://127.0.0.1:5000/ventas/");
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
    
function editarVenta(){
    var pos = $("#lstCliente").val();
    var fecha = $("#txtFecha").val();
    var comentarios = $("#txtComentarios").val();
    data={
        "txtId" : venta.id,
        "lstCliente" : pos,
        "txtFecha" : fecha,
        "txtComentarios" : comentarios
    }
    $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/ventas/guardar",
            async: true,
            data:data,
            success: function (data) {
                json_data = JSON.parse(data);
                if(json_data.result=="OK"){
                    siguienteVentas2();
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
function siguienteVentas2(){
    data = {
        "txtId" : venta.id
    }
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/ventas/getDetalles",
        data : data,
        async: true,
        success: function (data) {
            detalles = JSON.parse(data);
            mostrarModalVemtas3();
        }
});
}
function guardarProducto2(){
    $("#modalVenta2").modal("hide");
    window.location.replace("http://127.0.0.1:5000/productos/");
}
function mostrarModalVemtas3(){
    $("#modalVentas").modal("hide");
    $("#modalVentasLabel2").html("Modificar Venta");

    $("#txtCantidadM").val(0);
    $("#tblDetalleProducto").html("");
    $("#btnAgregarMateriaP2").removeProp("hidden");
    $("#btnAgregarMateriaP").prop("hidden", "true");
    $("#btnGuardarProducto2").removeProp("hidden");
    $("#btnGuardarProducto").prop("hidden", "true");

    $("#btnGuardarVenta2").removeProp("hidden");
    $("#btnGuardarVenta").prop("hidden", "true");
    $("#btnAgregarVentasP2").removeProp("hidden");
    $("#btnAgregarVentasP").prop("hidden", "true");
    llenarListaProductosVenta();
    actualizarDetalleProductoVentas(1);

    $("#modalVentas2").modal("show");
}
