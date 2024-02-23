function mascara_decimal(){
    $(document).ready(function(){
        $("#numeroDecimal").inputmask({
            alias:"decimal",
            integerDigits:6,
            digits:3,
            allowMinus:false,        
            digitsOptional: false,
            placeholder: "0"
        });
    });
}