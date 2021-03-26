// Socket
var loc = window.location
var wsStart = 'ws://'
if(loc.protocol == 'https:'){
    wsStart = 'wss://'
}
var endpoint = wsStart + loc.host + '/user/' + create_UUID()
ssbtSocket = new ReconnectingWebSocket(endpoint)

// Teacher
var signup_verify_process_teacher = 0
var signup_create_process_teacher = 0
var username_status_teacher = false
var password_status_teacher = false
var userdata_teacher = null


var visible_password_teacher = false
//Socket
ssbtSocket.onopen = function(e) {
    // Teacher
    if($("#loading_signup-teacher").length){
        $("#loading_signup-teacher").remove()
    }

    if($("#signup_verify-teacher").length == 0 && signup_verify_process_teacher == 0){
        var signup_verify_form = `
            <div id="signup_verify-teacher">
                <h4>Join As Teacher</h4>
                <hr>
                <div class="text-center">
                    <form class="text-center" method="post" action="" id="signup-verify-form-teacher">
                        <p class="text-left text-danger" id="verify-message-teacher"></p>
                        <div class="form-group input-group">
                            <input type="text" class="form-control" name="id" id="id-teacher" placeholder="ID" autocomplete="off" required>
                            <div class="input-group-append">
                                <div class="input-group-text">
                                  <span class="fas fa-user"></span>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                          <div class="col-8">
                              <div class="text-right">
                                <span id="loading-animation-verify-teacher" class="fas fa-spinner fa-pulse d-none"></span>
                              </div>
                          </div>
                          <div class="col-4">
                            <button type="submit" id="submit-verify-teacher" class="btn btn-primary btn-block">Verify</button>
                          </div>
                        </div>
                    </form>
                </div>
            </div>`
        $("#teacher").append(signup_verify_form)
    }

    if($("#signup_create-teacher").length == 0 && signup_create_process_teacher == 0 && signup_verify_process_teacher == 1){
        if($("#signup_verify-teacher").length == 1){
            $("#signup_verify-teacher").remove()
        }
        var signup_create_form = `
            <div id="signup_create-teacher">
                <h4>Fill Form As Teacher</h4>
                <hr>
                <div class="text-center">
                    <form class="text-center" method="post" action="/accounts/signup/teacher" id="signup-create-form-teacher">`
                        +token+
                        `<div class="form-group input-group">
                            <input type="text" class="form-control" name="id" id="id-teacher" readonly required>
                        </div>
                        <div class="d-none form-group input-group">
                            <input type="text" class="form-control" name="name" id="name-teacher" readonly required>
                            <div class="input-group-append">
                                <div class="input-group-text">
                                  <span class="fas fa-user"></span>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-sm form-group input-group">
                                <input type="text" class="form-control" name="first_name" id="first_name-teacher" placeholder="First Name" autocomplete="off" required>
                            </div>
                            <div class="col-sm form-group input-group">
                                <input type="text" class="form-control" name="last_name" id="last_name-teacher" placeholder="Last Name" autocomplete="off" required>
                            </div>
                        </div>
                        <div class="form-group input-group">
                            <input type="email" class="form-control" name="email" id="set_email-teacher" placeholder="Enter Email" autocomplete="off" required>
                            <div class="input-group-append">
                                <div class="input-group-text">
                                  <span class="fas fa-envelope"></span>
                                </div>
                            </div>
                        </div>
                        <div class="form-group input-group">
                            <input type="text" class="form-control" name="username" id="set_username-teacher" placeholder="Set Username" autocomplete="off" required>
                            <div class="input-group-append">
                                <div class="input-group-text">
                                  <span class="fas fa-user"></span>
                                </div>
                            </div>
                        </div>
                        <div class="alert d-none" role="alert" id="create-message-username-teacher" ></div>
                        <div class="form-group input-group">
                            <input type="password" class="form-control" name="password" id="set_password-teacher" placeholder="Set Password" required>
                            <div class="input-group-append">
                                <button type="button" class="input-group-text border"  id="visible-password-teacher">
                                    <span id="password-eye-teacher" class="fas fa-eye"></span>
                                </button>
                            </div>
                        </div>
                        <div class="alert d-none" role="alert" id="create-message-password-teacher"></div>
                        <div class="form-group input-group">
                            <input type="password" class="form-control" name="retype_password" id="retype_password-teacher" placeholder="Retype Password" required>
                            <div class="input-group-append">
                                <div class="input-group-text">
                                  <span class="fas fa-lock"></span>
                                </div>
                            </div>
                        </div>

                        <div class="row">
                          <div class="col-8">

                          </div>
                          <div class="col-4">
                            <button type="button" id="submit-create-form-teacher" class="btn btn-primary btn-block">Signup</button>
                          </div>
                        </div>
                    </form>
                </div>
            </div>`
        $("#teacher").append(signup_create_form);
        $("#id-teacher").val(userdata_teacher['id']);
        $("#set_email-teacher").val(userdata_teacher['email']);
        $("#first_name-teacher").val(userdata_teacher['first_name']);
        $("#last_name-teacher").val(userdata_teacher['last_name']);
    }

};

ssbtSocket.onclose = function(e) {
    // Teacher
    if($("#signup_verify-teacher").length){
        $("#signup_verify-teacher").remove()
    }

    if($("#signup_create-teacher").length){
        $("#signup_create-teacher").remove()
    }

    if($("#loading_signup-teacher").length == 0){
        $("#teacher").append('<p class="text-danger text-center py-3" id="loading_signup-teacher">Wait for connecting to Server</p>')
    }
};

ssbtSocket.onerror = function(e){
}

ssbtSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    //Teacher
    if(data['process'] === 'signup-verify-teacher'){
        if(data['status'] == false){
            $("#verify-message-teacher").text(data['error']);
            $("#submit-verify-teacher").text('Verify')
            $("#loading-animation-verify-teacher").addClass('d-none')
            $("#submit-verify-teacher").prop('disabled', false)
        }
        else{
            signup_verify_process_teacher = 1

            if($("#signup_verify-teacher").length){
                $("#signup_verify-teacher").remove()
            }

            var signup_create_form = `
                <div id="signup_create-teacher">
                    <h4>Fill Form As Teacher</h4>
                    <hr>
                    <div class="text-center">
                        <form class="text-center" method="post" action="/accounts/signup/teacher" id="signup-create-form-teacher">`
                            +token+
                            `<div class="form-group input-group">
                                <input type="text" class="form-control" name="id" id="id-teacher" readonly required>
                            </div>
                            <div class="d-none form-group input-group">
                                <input type="text" class="form-control" name="name" id="name-teacher" readonly required>
                                <div class="input-group-append">
                                    <div class="input-group-text">
                                      <span class="fas fa-user"></span>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm form-group input-group">
                                    <input type="text" class="form-control" name="first_name" id="first_name-teacher" placeholder="First Name" autocomplete="off" required>
                                </div>
                                <div class="col-sm form-group input-group">
                                    <input type="text" class="form-control" name="last_name" id="last_name-teacher" placeholder="Last Name" autocomplete="off" required>
                                </div>
                            </div>
                            <div class="form-group input-group">
                                <input type="email" class="form-control" name="email" id="set_email-teacher" placeholder="Enter Email" autocomplete="off" required>
                                <div class="input-group-append">
                                    <div class="input-group-text">
                                      <span class="fas fa-envelope"></span>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group input-group">
                                <input type="text" class="form-control" name="username" id="set_username-teacher" placeholder="Set Username" autocomplete="off" required>
                                <div class="input-group-append">
                                    <div class="input-group-text">
                                      <span class="fas fa-user"></span>
                                    </div>
                                </div>
                            </div>
                            <div class="alert d-none" role="alert" id="create-message-username-teacher" ></div>
                            <div class="form-group input-group">
                                <input type="password" class="form-control" name="password" id="set_password-teacher" placeholder="Set Password" required>
                                <div class="input-group-append">
                                    <button type="button" class="input-group-text border"  id="visible-password-teacher">
                                        <span id="password-eye-teacher" class="fas fa-eye"></span>
                                    </button>
                                </div>
                            </div>
                            <div class="alert d-none" role="alert" id="create-message-password-teacher"></div>
                            <div class="form-group input-group">
                                <input type="password" class="form-control" name="retype_password" id="retype_password-teacher" placeholder="Retype Password" required>
                                <div class="input-group-append">
                                    <div class="input-group-text">
                                      <span class="fas fa-lock"></span>
                                    </div>
                                </div>
                            </div>

                            <div class="row">
                              <div class="col-8">

                              </div>
                              <div class="col-4">
                                <button type="button" id="submit-create-form-teacher" class="btn btn-primary btn-block">Signup</button>
                              </div>
                            </div>
                        </form>
                    </div>
                </div>`
            $("#teacher").append(signup_create_form);
            userdata_teacher = data['data']
            $("#id-teacher").val(userdata_teacher['id']);
            $("#set_email-teacher").val(userdata_teacher['email']);
            $("#first_name-teacher").val(userdata_teacher['first_name']);
            $("#last_name-teacher").val(userdata_teacher['last_name']);
        }
    }
    else if(data['process'] === 'username-availability-teacher'){
        $("#create-message-username-teacher").removeClass('d-none');
        if(data['status'] == false){
            $("#create-message-username-teacher").text('Username Not Available');
            $("#create-message-username-teacher").removeClass('alert-success');
            $("#create-message-username-teacher").addClass('alert-danger');
            $("#set_username-teacher").removeClass('border border-success is-valid');
            $("#set_username-teacher").addClass('border border-danger is-invalid');
            username_status_teacher = false;
        }
        else{
            $("#create-message-username-teacher").text('');
            $("#create-message-username-teacher").removeClass('alert-danger');
            $("#create-message-username-teacher").addClass('d-none');
            $("#set_username-teacher").removeClass('border border-danger is-invalid');
            $("#set_username-teacher").addClass('border border-success is-valid');
            username_status_teacher = true;
        }
    }
    else if(data['process'] === 'password-availability-teacher'){
        $("#create-message-password-teacher").removeClass('d-none');
        if(data['status'] == false){
            $("#create-message-password-teacher").text(data['error']);
            $("#create-message-password-teacher").removeClass('alert-success');
            $("#create-message-password-teacher").addClass('alert-danger');
            password_status_teacher = false;
        }
        else{
            $("#create-message-password-teacher").text(data['data']);
            $("#create-message-password-teacher").removeClass('alert-danger');
            $("#create-message-password-teacher").addClass('d-none');
            password_status_teacher = true;
        }
    }
};

//Teacher

$(document).on('click', "#visible-password-teacher", function(e){
    if(!visible_password_teacher){
        $('#set_password-teacher').get(0).type = 'text';
        $('#password-eye-teacher').removeClass('fa-eye').addClass('fa-eye-slash');
        visible_password_teacher = true
    }
    else{
        $('#set_password-teacher').get(0).type = 'password';
        $('#password-eye-teacher').removeClass('fa-eye-slash').addClass('fa-eye');
        visible_password_teacher = false
    }
})

$(document).on('click', "#submit-create-form-teacher", function(e){
    e.preventDefault();
    if($("#first_name-teacher").val() === '' || $("#last_name-teacher").val() === '' || $("#set_email-teacher").val() === '' || $("#set_username-teacher").val() === '' || $("#set_password-teacher").val() === '' || $("#retype_password-teacher").val() === '' ){
        alert("All fields are Compulsory to Fill...!");
    }
    else{
        if($("#set_email-teacher").val() !== ''){
            var password_teacher = $("#set_password-teacher").val()
            var retype_password_teacher = $("#retype_password-teacher").val()
            if(username_status_teacher){
                if(password_status_teacher){
                    if(password_teacher === retype_password_teacher){
                        $("#signup-create-form-teacher").submit();
                    }
                    else{
                        alert("Password and Retype password are Not Matching...!");
                    }
                }
                else{
                    alert("Choosen Password not Satisfying requirements...!");
                }
            }
            else{
                alert("Choosen Username not Satisfying requirements...!");
            }
        }
        else{
            alert("Wrong Email...!");
        }
    }
    return false;
})

$(document).on('input', "#retype_password-teacher", function(e){
    var password_teacher = $("#set_password-teacher").val()
    var retype_password_teacher = $("#retype_password-teacher").val()
    if(password_teacher === retype_password_teacher){
        $("#retype_password-teacher").removeClass('border border-danger is-invalid');
        $("#set_password-teacher").removeClass('border border-danger is-invalid');
        $("#retype_password-teacher").addClass('border border-success is-valid');
        $("#set_password-teacher").addClass('border border-success is-valid');
    }
    else if(retype_password_teacher === ''){
        $("#retype_password-teacher").removeClass('border border-danger is-invalid');
        $("#set_password-teacher").removeClass('border border-danger is-invalid');
        $("#retype_password-teacher").removeClass('border border-success is-valid');
        $("#set_password-teacher").removeClass('border border-success is-valid');
    }
    else{
        $("#retype_password-teacher").removeClass('border border-success is-valid');
        $("#set_password-teacher").removeClass('border border-success is-valid');
        $("#retype_password-teacher").addClass('border border-danger is-invalid');
        $("#set_password-teacher").addClass('border border-danger is-invalid');
    }
    return false;
})

$(document).on('input', "#set_password-teacher", function(e){
    var password_teacher = $("#set_password-teacher").val()
    var username_teacher = $("#set_username-teacher").val()
    if(password_teacher === '' || password_teacher.length <= 2){
        $("#set_password-teacher").val(password_teacher)
        $("#create-message-password-teacher").text('');
        $("#create-message-password-teacher").addClass('d-none');
        password_status_teacher = false;
    }
    else{
        ssbtSocket.send(JSON.stringify({
                    'process': 'password-availability-teacher',
                    'username': username_teacher,
                    'password': password_teacher
                }))
    }

    if($("#retype_password-teacher").val() !== '')
    {
        var retype_password_teacher = $("#retype_password-teacher").val()
        if(password_teacher === retype_password_teacher){
            $("#retype_password-teacher").removeClass('border border-danger is-invalid');
            $("#set_password-teacher").removeClass('border border-danger is-invalid');
            $("#retype_password-teacher").addClass('border border-success is-valid');
            $("#set_password-teacher").addClass('border border-success is-valid');
        }
        else{
            $("#retype_password-teacher").removeClass('border border-success is-valid');
            $("#set_password-teacher").removeClass('border border-success is-valid');
            $("#retype_password-teacher").addClass('border border-danger is-invalid');
            $("#set_password-teacher").addClass('border border-danger is-invalid');
        }
    }
    return false;
})

$(document).on('input', "#set_username-teacher", function(e){
    var username_teacher = $("#set_username-teacher").val()
    if(username_teacher === '' || username_teacher.length <= 3){
        $("#set_username-teacher").val(username_teacher)
        $("#create-message-username-teacher").text('');
        $("#create-message-username-teacher").addClass('d-none');
        $("#set_username-teacher").removeClass('is-invalid is-valid');
        username_status_teacher = false;
    }
    else{
        ssbtSocket.send(JSON.stringify({
                    'process': 'username-availability-teacher',
                    'username': username_teacher
                }))
    }
    return false;
})

$(document).on('submit', "#signup-verify-form-teacher", function(e){
    e.preventDefault();

    $("#submit-verify-teacher").text('Loading')
    $("#loading-animation-verify-teacher").removeClass('d-none')
    $("#submit-verify-teacher").prop('disabled', true)

    var id = $("#id-teacher").val()
    ssbtSocket.send(JSON.stringify({
                'process': 'signup-verify-teacher',
                'data':{'id': id}
            }))
    return false;
})

// Functions
function create_UUID(){
    var dt = new Date().getTime();
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (dt + Math.random()*16)%16 | 0;
        dt = Math.floor(dt/16);
        return (c=='x' ? r :(r&0x3|0x8)).toString(16);
    });
    return uuid;
}

function isEmail(email) {
  var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9.]{2,8})+$/;
  return regex.test(email);
}
