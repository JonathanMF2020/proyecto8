function mostrarModalAgregarProductos(){
    $("#modalProductos").modal("show");
    $("#txtNombre").val("");
    $("#txtPrecio").val("");
    $("#txtCantidad").val(0.0);
    $("#txtDescripcion").val(0.0);
    $("#txtId").val("");
}
function mostrarModalModificarProducto(producto){
    //alert(JSON.stringify(producto))
    $("#modalProductos").modal("show");
    $("#txtNombre").val(producto.nombre);
    $("#txtPrecio").val(producto.precio);
    $("#txtDescripcion").val(producto.descripcion);
    $("#txtId").val(producto.id);
}

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
        }
      })
}

function eliminarProducto(id){
    args = {
        txtId: id
    }
    $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/productos/eliminar",
            async: true,
            data: args,
            success: function (data) {
                json_data = JSON.parse(data);
                if(json_data.result=="OK"){
                    Swal.fire({
                        icon: 'success',
                        title: 'El producto se eliminó',
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