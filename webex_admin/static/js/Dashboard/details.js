// Functions
$(function () {
    $('[data-mask]').inputmask()
})
// Socket
var loc = window.location
var wsStart = 'ws://'
if(loc.protocol == 'https:'){
    wsStart = 'wss://'
}
var endpoint = wsStart + loc.host + '/details/' + data.id
ssbtSocket = new ReconnectingWebSocket(endpoint)
// Socket Functions

ssbtSocket.onopen = function(e) {
    $("#loading").text('').addClass('d-none');
    $("#details-form").removeClass('d-none');

    $("#name").prop('readonly', false);
    $("#website").prop('readonly', false);
    $("#email").prop('readonly', false);
    $("#phone").prop('readonly', false);
    $("#mobile").prop('readonly', false);
    $("#address").prop('readonly', false);
    $("#date_of_birth").prop('readonly', false);
};

ssbtSocket.onclose = function(e) {
    $("#details-form").addClass('d-none')
    $("#loading").text('Wait for connecting to Server').removeClass('d-none');

    $("#name").prop('readonly', true);
    $("#website").prop('readonly', true);
    $("#email").prop('readonly', true);
    $("#phone").prop('readonly', true);
    $("#mobile").prop('readonly', true);
    $("#address").prop('readonly', true);
    $("#date_of_birth").prop('readonly', true);
};

ssbtSocket.onerror = function(e){
}

ssbtSocket.onmessage = function(e) {
    const data_received = JSON.parse(e.data);

    if(data_received['process'] === 'details-form-submission'){
        if(data_received['status']){
            data.name = data_received["name"],
            data.website = data_received["website"]
            data.email = data_received["email"]
            data.phone = data_received["phone"]
            data.mobile = data_received["mobile"]
            data.address = data_received["address"]
            data.date_of_birth = data_received["date_of_birth"]

            alert('Saving Successful')
            $('#loading-animation').addClass('d-none')
            $("#details-form-submit").prop('disabled', false).text('Save');
        }
        else{
            alert('Saving Failed, Try again..!')
            $('#loading-animation').addClass('d-none')
            $("#details-form-submit").prop('disabled', false).text('Save');
        }
    }
};

$(document).on('click', '#details-form-submit', function(){
    $('#loading-animation').removeClass('d-none')
    $("#details-form-submit").prop('disabled', true).text('Saving...');

    if($("#name").val() !== '' && $("#email").val() !== ''){
        if($("#name").val() !== data.name || $("#website").val() !== data.website || $("#email").val() !== data.email || $("#phone").val() !== data.phone || $("#mobile").val() !== data.mobile || $("#address").val() !== data.address || $("#date_of_birth").val() !== data.date_of_birth){
            if(isEmail($('#email').val())){
                ssbtSocket.send(JSON.stringify({
                    'process': 'details-form-submission',
                    'data':{
                        'id': data.id,
                        'teacher': data.teacher,
                        'name': $("#name").val(),
                        'website': $("#website").val(),
                        'email': $("#email").val(),
                        'phone': $("#phone").val(),
                        'mobile': $("#mobile").val(),
                        'address': $("#address").val(),
                        'date_of_birth': $("#date_of_birth").val(),
                    }
                }))
            }
            else{
                alert('Wrong Email Format..!')
                $('#loading-animation').addClass('d-none')
                $("#details-form-submit").prop('disabled', false).text('Save');
            }
        }
        else{
            alert('Nothing is Changed to Save..!')
            $('#loading-animation').addClass('d-none')
            $("#details-form-submit").prop('disabled', false).text('Save');
        }
    }
    else{
        alert('Name and Email is Compulsory Fields, Fill Them..!')
        $('#loading-animation').addClass('d-none')
        $("#details-form-submit").prop('disabled', false).text('Save');
    }
})

function isEmail(email) {
  var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9.]{2,8})+$/;
  return regex.test(email);
}

// DropZone
Dropzone.autoDiscover = false;
var profileDropzone = new Dropzone("#profile-dropzone", {
    url: "/dashboard/edit/profile",
    maxFiles: 1,
    maxFilesize: 3,
    acceptedFiles: 'image/*',
    addRemoveLinks: true,
    capture: true,
});

profileDropzone.on("success", function(file){
  $(".dz-success-mark svg").css("background", "green");
  $(".dz-error-mark").css("display", "none");
  $("#profile-dropzone-message").text("Profile Picture Successfully Uploaded...").css("color", "green");
  location.reload();
});

profileDropzone.on("error", function(file, response) {
  $(".dz-error-mark svg").css("background", "red");
  $(".dz-success-mark").css("display", "none");
  $("#profile-dropzone-message").text(response).css("color", "red");
});
