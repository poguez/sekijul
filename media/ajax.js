var startIndex = 0;
var endIndex = 6;

function show_event(event_id){
	document.getElementById("event_detail").innerHTML = "Loading...";
	document.getElementById("event_detail").style.visibility = "visible";
	query = "/events/" + event_id;
	$.get(
		query,
		"",
		function(data) {
			document.getElementById("event_detail").innerHTML = data;
		}
		);
}

function login(){
	var $form = $("#loginForm"),
    	csrfmiddlewaretoken_ = $form.find( 'input[name="csrfmiddlewaretoken"]' ).val(),
        username_ = $form.find( 'input[name="username"]' ).val(),
        password_ = $form.find( 'input[name="password"]' ).val(),
        url = $form.attr( 'action' );
        
	$.post(
		url,
		{ csrfmiddlewaretoken: csrfmiddlewaretoken_, username: username_, password: password_ },
		function(data) {
			if(data == "success"){
				window.location.href = "/";
			}
			else{
				document.getElementById("dropdown-id").innerHTML = data + "<p>invalid username or password</p>";
			}
		}
		);
}

function register(){
	var $form = $("#registerForm"),
    	csrfmiddlewaretoken_ = $form.find( 'input[name="csrfmiddlewaretoken"]' ).val(),
        username_ = $form.find( 'input[name="username"]' ).val(),
        email_ = $form.find( 'input[name="email"]' ).val(),
        password1_ = $form.find( 'input[name="password1"]' ).val(),
        password2_ = $form.find( 'input[name="password2"]' ).val(),
        url = $form.attr( 'action' );
        
	$.post(
		url,
		{ csrfmiddlewaretoken: csrfmiddlewaretoken_, username: username_, email: email_, password1: password1_, password2: password2_ },
		function(data) {
			document.getElementById("dropdown-id").innerHTML = data;
		}
		);
}

function postComment(){

	var $form = $("#postForm"),
    	csrfmiddlewaretoken_ = $form.find( 'input[name="csrfmiddlewaretoken"]' ).val(),
        object_pk_ = $form.find( 'input[name="object_pk"]' ).val(),
        content_type_ = $form.find( 'input[name="content_type"]' ).val(),
        timestamp_ = $form.find( 'input[name="timestamp"]' ).val(),
        security_hash_ = $form.find( 'input[name="security_hash"]' ).val(),
        comment_ = $form.find( 'textarea[name="comment"]' ).val(),
        url = $form.attr( 'action' );

	$.post(
		url,
		{ csrfmiddlewaretoken: csrfmiddlewaretoken_, object_pk: object_pk_, content_type: content_type_, timestamp: timestamp_, security_hash: security_hash_, comment: comment_ },
		function(data) {
			show_event(object_pk_);
		}
		);
}

function postComment(){

	var $form = $("#postForm"),
    	csrfmiddlewaretoken_ = $form.find( 'input[name="csrfmiddlewaretoken"]' ).val(),
        object_pk_ = $form.find( 'input[name="object_pk"]' ).val(),
        content_type_ = $form.find( 'input[name="content_type"]' ).val(),
        timestamp_ = $form.find( 'input[name="timestamp"]' ).val(),
        security_hash_ = $form.find( 'input[name="security_hash"]' ).val(),
        comment_ = $form.find( 'textarea[name="comment"]' ).val(),
        url = $form.attr( 'action' );

	$.post(
		url,
		{ csrfmiddlewaretoken: csrfmiddlewaretoken_, object_pk: object_pk_, content_type: content_type_, timestamp: timestamp_, security_hash: security_hash_, comment: comment_ },
		function(data) {
			show_event(object_pk_);
		}
		);
}
    
function more(index){
	startIndex = endIndex + 1;
	endIndex = startIndex + 5;
	query = "/events/query/?b="+ startIndex +"&e=" + endIndex;

	document.getElementById("more_button").value = "Loading...";

	$.get(
		query,
		"",
		function(data) {
			document.getElementById("more_events").innerHTML += data;
			document.getElementById("more_button").value = "more events";
		}
		);
}

function proj_detail(proj_id){
	query = "&proj_id=" + proj_id;
	sendRequest(show_the_proj_info, query, "POST", "x_detail.jsp", true);
}

function show_the_proj_info(oj){
	var res = oj.responseText;	
	//alert(res);
	$("layer_for_proj_detail").style.visibility = "visible";
	$("layer_for_proj_detail").innerHTML = "<div align = 'right'><img src = '/img/x.bmp' style = 'cursor:hand' onclick = \"$('layer_for_proj_detail').style.visibility = 'hidden';\"'/></div>";
	$("layer_for_proj_detail").innerHTML += res;	
}

function get_selected_proj_id(){
	for(var i = 0; ; i++){
		try{
			if($("proj" + i).checked){
				return $("proj" + i).value;
			}
		}
		catch(e){	
			return null;
		}
	}
}

function try_proj_login(proj_id){
	//alert(proj_id);
	query = "&proj_id=" + proj_id;
	sendRequest(receive_proj_login_result, query, "POST", "x_try_login.jsp", true);
}

function receive_proj_login_result(oj){
	var res = oj.responseText;	
	//alert(res);
	if(res.substring(0, 1) == "T")
		location.replace("/main/main.jsp");
	else
		alert("error");	
}

$(document).ajaxSend(function(event, xhr, settings) {
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
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});