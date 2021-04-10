function mostrarModalCompraAgregar(){
    $("#modalCompra").modal("show");
    $("#txtId").val("");
    $("#modalCompraLabel").html("Agregar Compra");
}

function mostrarModalCompraDetalleAgregar(){
    $("#modalCompra").modal("show");
    $("#modalCompraLabel").html("Agregar Detalle Compra");
}