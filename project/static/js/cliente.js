function mostrarModalClienteAgregar(){
    $("#modalClientes").modal("show");
    $("#txtNombreEmpresa").val("");
    $("#txtEmail").val("");
    $("#txtTelefono").val("");
    $("#txtDireccion").val("");
    $("#txtContacto").val("");
    $("#txtRFC").val("");
    $("#txtId").val("");
    $("#modalClientesLabel").html("Agregar Cliente");
}



function mostrarModalMateriaModificar(materia){
    console.log(materia);
    $("#modalMateria").modal("show");
    $("#txtNombre").val(materia.nombre);
    $("#txtCosto").val(materia.costo);
    $("#lstUnidad").val(materia.unidad);
    $("#txtCantidad").val(materia.cantidad);
    $("#txtId").val(materia.id);
    $("#modalMateriaLabel").html("Modificar Materia Prima");
}

function mostrarModalClienteModificar(cliente){
    console.log(cliente);
    $("#modalClientes").modal("show");
    $("#txtNombreEmpresa").val(cliente.nombre_empresa);
    $("#txtEmail").val(cliente.email);
    $("#txtTelefono").val(cliente.telefono);
    $("#txtDireccion").val(cliente.direccion);
    $("#txtContacto").val(cliente.contacto);
    $("#txtRFC").val(cliente.rfc);
    $("#txtId").val(cliente.id);
    $("#modalClientesLabel").html("Modificar Cliente");
}

function confirmarCliente(id, nombre_empresa){
    Swal.fire({
        icon: 'question',
        title: '¿Esta seguro que quiere eliminar el cliente '+nombre_empresa+'?',
        showDenyButton: true,
        confirmButtonText: `Cancelar`,
        denyButtonText: `Eliminar`,
      }).then((result) => {
        if (result.isDenied) {
            eliminarCliente(id);
        }
      })
}

function eliminarCliente(id){
    args = {
        txtId: id
    }
    $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/clientes/eliminar",
            async: true,
            data: args,
            success: function (data) {
                json_data = JSON.parse(data);
                if(json_data.result=="OK"){
                    Swal.fire({
                        icon: 'success',
                        title: 'Cliente eliminado correctamente',
                        showDenyButton: false,
                        confirmButtonText: `Ok`
                      }).then((result) => {
                        if (result.isConfirmed) {
                            window.location.replace("http://127.0.0.1:5000/clientes/");
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