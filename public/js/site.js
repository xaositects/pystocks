function checkSession() {
    $.ajax({
        url: '/Login/checkSession',
        global: false,
        error: function (r) {
            Materialize.toast('You are being logged out due to inactivity');
            signOut();
        }
    });
}
function geo_decode(anchor) {
    var href = anchor.getAttribute('href');
    var address = href.replace(/.*contact\/([a-z0-9._%-]+)+([a-z0-9._%-]+)+([a-z.]+)/i, '$1' + '@' + '$2' + '.' + '$3');
    if (href != address) {
        anchor.setAttribute('href', 'mailto:' + address);
    }
}


function keepAlive() {
    var chk = /.*(Login|Logout).*/;
    if(!chk.exec(window.location.pathname)) {
        setTimeout(function () {
            checkSession();
            keepAlive();
        }, 20000);
    }
}
keepAlive();
var links = document.getElementsByTagName('a');
for (var l = 0; l < links.length; l++) {
    links[l].click(function () {
        geo_decode(this);
    });
}

function remainingDays(id_to_notify, end) {
    $.ajax({
        url: '/lib/datediff.php', 
        global: false, 
        data: {end: end}, 
        success: function (r) {
            var secs = r;
            var mins = secs/60;
            var hours = mins/60;
            var days = Math.round((hours/24) * 100) /100;
            var rem;
            if(days > 1) {
                rem = days + ' Days';
            }else{
                rem = hours + ':' + mins + ':' + secs;
            }
            $('#' + id_to_notify).html(rem);
        }, 
        type: 'POST'});
    setTimeout(function () {
        remainingDays(id_to_notify, end);
    }, 60000);
}
