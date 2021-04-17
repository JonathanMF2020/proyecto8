var ip = "http://e23f8d156612.ngrok.io"
var productos = [];
var queryString = window.location.search;
var urlParams = new URLSearchParams(queryString);
var idP = urlParams.get('txtIdP');;

function agregarEjemplar(){
    $("#modalEjemplares").modal("show");
    $("#lstTalla").val("22");
    $("#txtColor").val("");
    $("#txtCantidad").val(0);
    $("#txtId").val("");
    $("#txtIdP").val(idP);
    $("#modalEjemplaresLabel").html("Agregar Ejemplar");
}

function modificarEjemplar(ejemplar){
    $("#modalEjemplares").modal("show");
    $("#lstTalla").val(ejemplar.talla);
    $("#txtColor").val(ejemplar.color);
    $("#txtCantidad").val(ejemplar.cantidad);
    $("#txtId").val(ejemplar.id);
    $("#txtIdP").val(idP);
    $("#modalEjemplaresLabel").html("Modificar Ejemplar");
}

function confirmarEjemplar(id){
    Swal.fire({
        icon: 'question',
        title: '¿Esta seguro que quiere eliminar el ejemplar?',
        showDenyButton: true,
        confirmButtonText: `Cancelar`,
        denyButtonText: `Eliminar`,
      }).then((result) => {
        if (result.isDenied) {
            eliminarEjemplar(id);
        }
      })
}

function eliminarEjemplar(id){
    data = {
        txtId: id
    }
    $.ajax({
            type: "POST",
            url: ip+"/ejemplares/eliminar",
            async: true,
            data:data,
            success: function (data) {
                json_data = JSON.parse(data);
                if(json_data.result>0){
                    Swal.fire({
                        icon: 'success',
                        title: 'Ejemplar eliminado correctamente',
                        showDenyButton: false,
                        confirmButtonText: `Ok`
                      }).then((result) => {
                        if (result.isConfirmed) {
                            window.location.replace(ip+"/ejemplares/getByProducto?txtIdP="+json_data.result);
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