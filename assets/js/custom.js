
/* P.E.A.K.A. */

// rand Function
function rand(min , max){
    return Math.floor(Math.random() * (max - min + 1) ) + min;
}
// passWord Shower
document.getElementById('shpw').onclick = function () {

    var x = document.getElementsByTagName('input')[3]
    var y = document.getElementById('eye');
    var yy = document.getElementById('eye2');

    if (x.type === "password") {
        x.type = "text";
        y.classList.remove('fa-eye');
        y.classList.add('fa-eye-slash');
        yy.classList.remove('fa-eye');
        yy.classList.add('fa-eye-slash');
    } else {
        x.type = "password";
        y.classList.add('fa-eye');
        y.classList.remove('fa-eye-slash');
        yy.classList.add('fa-eye');
        yy.classList.remove('fa-eye-slash');
    }
}
// change filter price
function changeprice(){
    document.getElementById('priceshower').innerHTML = document.getElementById('rangeprice').value;
}

// JQuery Codes
$(document).ready(function(){
    $('.imgSlideShow').click(function(){
        $('#mainImageInslideShow').attr("src", $(this).attr('src'));
    });

});
