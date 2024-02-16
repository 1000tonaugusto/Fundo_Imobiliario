function confirmar_inclusao()  {
    Swal.fire({
        "title": "Confirma Inclusao",
        "text": "Tem certeza ?",
        "showCancelButton": true,
        "cancelButtonText": "Cancelar",
        "confirmButtonText": "Confirmar",
        "reverseButtons": true,
    })
    .then(function(result){
        if (result.isConfirmed) {
            document.getElementById('formInclui').submit();
        }
    })
}