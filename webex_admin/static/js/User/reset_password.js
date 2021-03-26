// Socket
var loc = window.location
var wsStart = 'ws://'
if(loc.protocol == 'https:'){
    wsStart = 'wss://'
}
var endpoint = wsStart + loc.host + '/user/reset_password/' + id;
chatSocket = new ReconnectingWebSocket(endpoint)

var password_status = false
var visible_password = false

$(document).on('click', "#reset-form-submit", function(e){
    e.preventDefault();
    $("#loading-animation-verify").removeClass('d-none')
    $("#reset-form-verify").prop('disabled', true)
    if($("#id").val() === '' || $("#password").val() === '' || $("#retype_password").val() === '' ){
        alert("All fields are Compulsory to Fill...!");
        $("#loading-animation-verify").addClass('d-none')
        $("#reset-form-verify").prop('disabled', false)
    }
    else{
        if(password_status){
            var password = $("#set_password").val()
            var retype_password = $("#retype_password").val()
            if(password === retype_password){
                $("#reset-form").submit();
            }
            else{
                alert("Password and Retype password are Not Matching...!");
                $("#loading-animation-verify").addClass('d-none')
                $("#reset-form-verify").prop('disabled', false)
            }
        }
        else{
            alert("Choosen Password not Satisfying requirements...!");
            $("#loading-animation-verify").addClass('d-none')
            $("#reset-form-verify").prop('disabled', false)
        }
    return false;
}
})


$(document).on('click', "#visible-password", function(e){
    if(!visible_password){
        $('#set_password').get(0).type = 'text';
        $('#password-eye').removeClass('fa-eye').addClass('fa-eye-slash');
        visible_password = true
    }
    else{
        $('#set_password').get(0).type = 'password';
        $('#password-eye').removeClass('fa-eye-slash').addClass('fa-eye');
        visible_password = false
    }
})

$(document).on('input', "#retype_password", function(e){
    var password = $("#set_password").val()
    var retype_password = $("#retype_password").val()
    if(password === retype_password){
        $("#retype_password").removeClass('border border-danger is-invalid');
        $("#set_password").removeClass('border border-danger is-invalid');
        $("#retype_password").addClass('border border-success is-valid');
        $("#set_password").addClass('border border-success is-valid');
    }
    else if(retype_password === ''){
        $("#retype_password").removeClass('border border-danger is-invalid');
        $("#set_password").removeClass('border border-danger is-invalid');
        $("#retype_password").removeClass('border border-success is-valid');
        $("#set_password").removeClass('border border-success is-valid');
    }
    else{
        $("#retype_password").removeClass('border border-success is-valid');
        $("#set_password").removeClass('border border-success is-valid');
        $("#retype_password").addClass('border border-danger is-invalid');
        $("#set_password").addClass('border border-danger is-invalid');
    }
    return false;
})

$(document).on('input', "#set_password", function(e){
    var password = $("#set_password").val()
    var username = $("#set_username").val()
    if(password === '' || password.length <= 2){
        $("#set_password").val(password)
        $("#create-message-password").text('');
        $("#create-message-password").addClass('d-none');
        password_status = false;
    }
    else{
        chatSocket.send(JSON.stringify({
                    'process': 'password-availability',
                    'id': id,
                    'password': password
                }))
    }

    if($("#retype_password").val() !== '')
    {
        var retype_password = $("#retype_password").val()
        if(password === retype_password){
            $("#retype_password").removeClass('border border-danger is-invalid');
            $("#set_password").removeClass('border border-danger is-invalid');
            $("#retype_password").addClass('border border-success is-valid');
            $("#set_password").addClass('border border-success is-valid');
        }
        else{
            $("#retype_password").removeClass('border border-success is-valid');
            $("#set_password").removeClass('border border-success is-valid');
            $("#retype_password").addClass('border border-danger is-invalid');
            $("#set_password").addClass('border border-danger is-invalid');
        }
    }
    return false;
})

chatSocket.onopen = function(e) {
    if($("#loading_signup").length){
        $("#loading_signup").remove()
    }

    if($("#reset-form").length == 0){
        var reset_form = `
            <form action="/accounts/reset_password" method="post" id="reset-form">`
        + token +
        `<div class="form-group input-group d-none">
            <input type="text" class="form-control" name="id" id="id" placeholder="ID" readonly>
        </div>
        <div class="form-group input-group">
            <input type="password" class="form-control" name="password" id="set_password" placeholder="Set Password" required>
            <div class="input-group-append">
                <button type="button" class="input-group-text border"  id="visible-password">
                    <span id="password-eye" class="fas fa-eye"></span>
                </button>
            </div>
        </div>
        <div class="alert d-none" role="alert" id="create-message-password"></div>
        <div class="form-group input-group">
            <input type="password" class="form-control" name="retype_password" id="retype_password" placeholder="Retype Password" required>
            <div class="input-group-append">
                <div class="input-group-text">
                  <span class="fas fa-lock"></span>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-7">
                <div class="text-right">
                  <span id="loading-animation-verify" class="fas fa-spinner fa-pulse d-none"></span>
                </div>
            </div>
          <div class="col-5">
            <button type="button" id="reset-form-submit" class="btn btn-primary btn-block">Reset</button>
          </div>
          <!-- /.col -->
        </div>
      </form>`
      $("#form").append(reset_form);
      $("#id").val(id);
    }
};

chatSocket.onclose = function(e) {
    if($("#reset-form").length){
        $("#reset-form").remove()
    }

    if($("#loading_signup").length == 0){
        $("#form").append('<p class="text-danger text-center py-3" id="loading_signup">Wait for connecting to Server</p>')
    }
};

chatSocket.onerror = function(e){
}

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if(data['process'] === 'password-availability'){
        $("#create-message-password").removeClass('d-none');
        if(data['status'] == false){
            $("#create-message-password").text(data['error']);
            $("#create-message-password").removeClass('alert-success');
            $("#create-message-password").addClass('alert-danger');
            password_status = false;
        }
        else{
            $("#create-message-password").text(data['data']);
            $("#create-message-password").removeClass('alert-danger');
            $("#create-message-password").addClass('d-none');
            password_status = true;
        }
    }
};
