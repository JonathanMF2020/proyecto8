var ip = "http://984e801b4218.ngrok.io"
function mostrarModalMateriaAgregar(){
    $("#modalMateria").modal("show");
    $("#txtNombre").val("");
    $("#txtPrecio").val("");
    $("#txtCantidad").val(0.0);
    $("#lstUnidad").val("dm");
    $("#txtId").val("");
    $("#modalMateriaLabel").html("Agregar Materia Prima");
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

function confirmarMateria(id, nombre){
    Swal.fire({
        icon: 'question',
        title: '¿Esta seguro que quiere eliminar la materia '+nombre+"?",
        showDenyButton: true,
        confirmButtonText: `Cancelar`,
        denyButtonText: `Eliminar`,
      }).then((result) => {
        if (result.isDenied) {
            eliminarMateria(id);
        }
      })
}

function eliminarMateria(id){
    args = {
        txtId: id
    }
    $.ajax({
            type: "POST",
            url: ip+"/materias/eliminar",
            async: true,
            data: args,
            success: function (data) {
                json_data = JSON.parse(data);
                if(json_data.result=="OK"){
                    Swal.fire({
                        icon: 'success',
                        title: 'Materia prima eliminada correctamente',
                        showDenyButton: false,
                        confirmButtonText: `Ok`
                      }).then((result) => {
                        if (result.isConfirmed) {
                            window.location.replace(ip+"/materias/");
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