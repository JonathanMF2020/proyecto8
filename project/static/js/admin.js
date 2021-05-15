var ip = "http://984e801b4218.ngrok.io"
function mostrarModalAdminAgregar(){
    llenarListaRoles();
    $("#modalAdmin").modal("show");
    $("#txtNombre").val("");
    $("#txtEmail").val("");
    $("#txtPassword").val("");
    $("#txtId").val("");
    $("#modalAdminLabel").html("Agregar Usuario");
}

function mostrarModalAdminModificar(usuario){
    console.log(usuario.rol);
    rol = JSON.parse(usuario.rol);
    llenarListaRoles2(rol.id);
    $("#modalAdmin").modal("show");
    $("#txtNombre").val(usuario.name);
    $("#txtEmail").val(usuario.email);
    $("#txtPassword").val("");
    $("#txtId").val(usuario.id);
    $("#modalAdminLabel").html("Editar Usuario");
}

function llenarListaRoles(){
    var roles = [];
    $.ajax({
            type: "GET",
            url: ip+"/admin/getRoles",
            async: true,
            success: function (data) {
                roles = JSON.parse(data);
                var str = "";
                for(var i = 0; i < roles.length; i++){
                    str+="<option value="+roles[i].name+">";
                    str+= roles[i].name;
                    str+="</option>";
                }
                $("#slctRol").html(str);
            }
    });
}

function llenarListaRoles2(id){
    var roles = [];
    $.ajax({
            type: "GET",
            url: ip+"/admin/getRoles",
            async: true,
            success: function (data) {
                roles = JSON.parse(data);
                var str = "";
                for(var i = 0; i < roles.length; i++){
                    if(roles[i].id == id)
                    {
                        str+="<option value="+roles[i].name+" selected>";
                        str+= roles[i].name;
                        str+="</option>";
                    }else{
                        str+="<option value="+roles[i].name+">";
                        str+= roles[i].name;
                        str+="</option>";
                    }
                    
                }
                $("#slctRol").html(str);
            }
    });
}

function confirmarAdmin(id, nombre){
    Swal.fire({
        icon: 'question',
        title: '¿Esta seguro que quiere eliminar este usuario: '+nombre+"?",
        showDenyButton: true,
        confirmButtonText: `Cancelar`,
        denyButtonText: `Eliminar`,
      }).then((result) => {
        if (result.isDenied) 
        {
            eliminarAdmin(id);
        }
      });
}

function eliminarAdmin(id){
    args = {
        txtId: id
    };
    $.ajax({
            type: "POST",
            url: ip+"/admin/eliminar",
            async: true,
            data: args,
            success: function (data) {
                json_data = JSON.parse(data);
                console.log(json_data);
                if(json_data.result=="OK"){
                    Swal.fire({
                        icon: 'success',
                        title: 'Usuario eliminada correctamente',
                        showDenyButton: false,
                        confirmButtonText: `Ok`
                      }).then((result) => {
                        if (result.isConfirmed) {
                            window.location.replace(ip+"/admin/");
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