function confirmar_alteracao(id)  {
    Swal.fire({
        "title": "Confirma Alteração",
        "text": "Tem certeza ?",
        "showCancelButton": true,
        "cancelButtonText": "Cancelar",
        "confirmButtonText": "Confirmar",
        "reverseButtons": true,
    })
    .then(function(result){
        if (result.isConfirmed) {
            document.getElementById('formAltera').submit(id);
        }
    })
}