
function getCookie(name, document, jQuery) {
    "use strict";
    var cookievalue = null, cookies = null;
    if (document.cookie && document.cookie !== '') {
        cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookievalue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookievalue;
}

var csrftoken = getCookie('csrftoken', document, jQuery);

function csrfSafeMethod(method) {
    "use strict";
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
