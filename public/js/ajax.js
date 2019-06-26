$(document).ajaxStart(function(){
    startLoading();
});
$(document).ajaxStop(function(){
    stopLoading();
});
function startLoading() {
    $('#sb').show();
}
function stopLoading() {
    $('#sb').hide();
}

