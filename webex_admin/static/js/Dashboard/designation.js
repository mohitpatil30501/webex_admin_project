// Function
$(function () {
    $('[data-mask]').inputmask()
})
// Socket
var loc = window.location
var wsStart = 'ws://'
if(loc.protocol == 'https:'){
    wsStart = 'wss://'
}
var endpoint = wsStart + loc.host + '/designation/' + data.designation.id
ssbtSocket = new ReconnectingWebSocket(endpoint)



// Socket Functions
ssbtSocket.onopen = function(e) {
    $("#loading").text('').addClass('d-none');
    $("#designation-div-form").removeClass('d-none');

    $("#designation").prop('readonly', false);
    $("#department").prop('readonly', false);
    $("#institute").prop('readonly', false);
};

ssbtSocket.onclose = function(e) {
    $("#designation-div-form").addClass('d-none')
    $("#loading").text('Wait for connecting to Server').removeClass('d-none');

    $("#designation").prop('readonly', true);
    $("#department").prop('readonly', true);
    $("#institute").prop('readonly', true);
};

ssbtSocket.onerror = function(e){
}

ssbtSocket.onmessage = function(e) {
    const data_received = JSON.parse(e.data);
    if(data_received['process'] === 'designation-form-submission'){
        if(data_received['status']){
            data.designation.designation = data_received['data']['designation']
            data.designation.department = data_received['data']['department']
            data.designation.institute = data_received['data']['institute']

            alert('Saving Successful')
        }
        else{
            alert('Saving Failed, Try again..!')
        }
        $('#loading-animation-designation').addClass('d-none')
        $("#designation-form-submit").prop('disabled', false).text('Save');
    }
};

// Function
$(document).on('click', '#designation-form-submit', function(){
    $('#loading-animation-designation').removeClass('d-none')
    $("#designation-form-submit").prop('disabled', true).text('Saving...');

    if($("#designation").val() !== data.designation.designation || $("#department").val() !== data.designation.department || $("#institute").val() !== data.designation.institute){
        ssbtSocket.send(JSON.stringify({
            'process': 'designation-form-submission',
            'data':{
                'id': data.designation.id,
                'teacher': data.designation.teacher,
                'designation': $("#designation").val(),
                'department': $("#department").val(),
                'institute': $("#institute").val(),
            }
        }))
    }
    else{
        alert('Nothing is Changed to Save..!')
        $('#loading-animation-designation').addClass('d-none')
        $("#designation-form-submit").prop('disabled', false).text('Save');
    }
})

// Scroll Down table
function scrollToBottom(box, table) {
   box.scrollTop(table.height());
}

