/**
 * Created by achais on 15/10/12.
 */

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

var csrftoken = getCookie('csrftoken');

jQuery(document).ready(function () {
    jQuery("body").on("click", "#delProLink", function () {
        var app_id = jQuery(this).attr("data-id");
        if (app_id != "") {
            jQuery.ajax({
                url: location.href,
                type: "POST",
                data: {app_id: app_id, action: "del"},
                error: function (e) {
                    console.log("error");
                },
                success: function (response) {
                    response = jQuery.parseJSON(response);
                    console.log(response);
                    if (response.code == 10000) {
                        location.href = "/product/list";
                    }
                },
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            })
        }

    })
});