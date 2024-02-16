function confirmar_exclusao(id,url)  {
    Swal.fire({
        "title": "Confirma Exclusão",
        "text": "Tem certeza ?",
        "showCancelButton": true,
        "cancelButtonText": "Cancelar",
        "confirmButtonText": "Confirmar",
        "reverseButtons": true,
    })
    .then(function(result){
        if (result.isConfirmed) {
            window.location.href = url+id;
        }
    })
}