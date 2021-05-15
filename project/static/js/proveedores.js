var ip = "http://984e801b4218.ngrok.io"
function mostrarModalProveedorAgregar(){
    $("#modalProveedor").modal("show");
    $("#txtNombreEmpresa").val("");
    $("#txtEmail").val("");
    $("#txtTelefono").val("");
    $("#txtDireccion").val("");
    $("#txtContacto").val("");
    $("#txtRFC").val("");    
    $("#modalProvedoresLabel").html("Agregar Proveedor");
}


function mostrarModalProveedorModificar(proveedor){
    console.log(proveedor);
    $("#modalProveedor").modal("show");
    $("#txtNombreEmpresa").val(proveedor.nombre_empresa);
    $("#txtEmail").val(proveedor.email);
    $("#txtTelefono").val(proveedor.telefono);
    $("#txtDireccion").val(proveedor.direccion);
    $("#txtContacto").val(proveedor.contacto);
    $("#txtRFC").val(proveedor.RFC);
    $("#txtId").val(proveedor.id_proveedor);
    $("#modalProveedoresLabel").html("Modificar Proveedor");
}

function confirmarProveedor(id, nombre){
    Swal.fire({
        icon: 'question',
        title: '¿Esta seguro que quiere eliminar el proveedor '+nombre+"?",
        showDenyButton: true,
        confirmButtonText: `Cancelar`,
        denyButtonText: `Eliminar`,
      }).then((result) => {
        if (result.isDenied) {
            eliminarProveedor(id);
        }
      })
}

function eliminarProveedor(id){
    args = {
        txtId: id
    }
    $.ajax({
            type: "POST",
            url: ip+"/proveedores/eliminar",
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
                            window.location.replace(ip+"/proveedores/");
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