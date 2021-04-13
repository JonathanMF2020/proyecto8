function mostrarModalCompraAgregar(){
    $("#modalCompra").modal("show");
    $("#txtId").val("");
    $("#modalCompraLabel").html("Agregar Compra");
}

function mostrarModalCompraDetalleAgregar(){
    $("#modalCompra").modal("show");
    $("#modalCompraLabel").html("Agregar Detalle Compra");
}

function mostrarModalCompraModificar(compra){
    $("#modalCompra").modal("show");
    $("#txtId").val(compra.id);
    $("#txtPrecio").val(compra.precio);
    $("#txtComentario").val(compra.comentarios)
    $("#slcProveedor").val(compra.proveedor);
    $("#modalCompraLabel").html("Modificar Compra");
}

function mostrarModalCompraDetalleModificar(){
    $("#modalCompra").modal("show");
    
    $("#modalCompraLabel").html("Modificar Detalle Compra");
}


function confirmarCompra(id, nombre){
    Swal.fire({
        icon: 'question',
        title: '¿Esta seguro que quiere eliminar la Compra hacia el proveedor '+nombre+"?",
        showDenyButton: true,
        confirmButtonText: `Cancelar`,
        denyButtonText: `Eliminar`,
      }).then((result) => {
        if (result.isDenied) {
            eliminarCompra(id);
        }
      })
}

function eliminarCompra(id){
    args = {
        txtId: id
    }
    $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/compras/eliminar",
            async: true,
            data: args,
            success: function (data) {
                json_data = JSON.parse(data);
                if(json_data.result=="OK"){
                    Swal.fire({
                        icon: 'success',
                        title: 'Proveedor eliminado correctamente',
                        showDenyButton: false,
                        confirmButtonText: `Ok`
                      }).then((result) => {
                        if (result.isConfirmed) {
                            window.location.replace("http://127.0.0.1:5000/compras/");
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