

// Use global variable for status so we know if we need to send ajax if change
var button_pressed = '';

$(document).ready(function() {
// define handlers
$('#direc_1_1').mousedown(function(){dirButtonClicked('1_1')});
$('#direc_2_1').mousedown(function(){dirButtonClicked('2_1')});
//$('#direc_2_1').ontouchstart(function(){preventDefault();dirButtonClicked('2_1');});
$('#direc_3_1').mousedown(function(){dirButtonClicked('3_1')});
$('#direc_1_2').mousedown(function(){dirButtonClicked('1_2')});
$('#direc_2_2').mousedown(function(){dirButtonClicked('2_2')});
$('#direc_3_2').mousedown(function(){dirButtonClicked('3_2')});
$('#direc_1_3').mousedown(function(){dirButtonClicked('1_3')});
$('#direc_2_3').mousedown(function(){dirButtonClicked('2_3')});
//$('#direc_2_3').ontouchstart(function(){preventDefault();dirButtonClicked('2_3');});

$('#direc_3_3').mousedown(function(){dirButtonClicked('3_3')});


// If we wanted to have click to start and stop instead of release to stop then
// disable remaining handlers and just handle the clicks
// add handler for each button, but only do anything with it if that button is active
$('#direc_1_1').mouseleave(function(){dirButtonMouseLeft('1_1')});

// Do mouseup at the document level as whenever mouse button is released we send appropriate stop
$('#direction').mouseup(function(){mouseRelease()});

$('#status').html("<p>Status unknown</p>");


}); // end ready


// convert button position to motor values
function buttonToMotor (button) {
    // array m1 values
    var m1 = {"1_1": 1, "2_1": 1, "3_1": 0, "1_2": 1, "2_2": 0, "3_2": 2, "1_3": 2, "2_3": 2, "3_3": 0};  
    // array m2 values
    var m2 = {"1_1": 0, "2_1": 1, "3_1": 1, "1_2": 2, "2_2": 0, "3_2": 1, "1_3": 0, "2_3": 2, "3_3": 2};
    
    return ([m1[button], m2[button]]);
}


// handle motor direction button being clicked 
// only when clicked over button do we send status - we cancel on either release or move position
function dirButtonClicked (button) {
    // Update global variable to track what button is pressed
    // special case if button 2_2 - that is same as stop so set button_pressed to stop
    if (button == '2_2') {button_pressed = '';}
    else {button_pressed = button;}
    
    motors = buttonToMotor (button);    
    sendAjax ('control', 'cmd=motor&m1='+motors[0]+'&m2='+motors[1]);
}


// mouse button released if we are in press to move mode then cancel
function mouseRelease () {
    //alert ('mouse released');
    // Do we have a button up? 
    if (button_pressed != '') {
        //alert ('send mouse release update');
        // If so use dirButtonClicked to stop motor (2_2 is center stop button)
        dirButtonClicked ('2_2');
    }
}



function dirButtonMouseLeft () {
}

// generic request - simplify process of generating code
// type can be status (ask for status) or control (change motor / speed)
function sendAjax (type, params) {
    // control ie change a parameter
    if (type == 'control') {
        href = "/control";
    }
    // status
    else if (type == 'status') {
        href = "/status";
    }
    // invalid
    else { return; }
    
    // 3rd value - updateStatus is the name of the callback function
    $.get(href, params, updateStatus);
    
}

// call back function from ajax code
function updateStatus (data) {
    // Update screen with new status
    $('#status').html(data);
    
}


//$.get(url, data, callback);
// $.get('rateMovie.php','rating=5&setting2=1');
// 
// 
// $('#message a').click(function() {
// var href=$(this).attr('href');
// var querystring=href.slice(href.indexOf('?')+1);
// get('rate.php', querystring, processResponse);
// return false; // stop the link
// });


// function processResponse(data) {
// var newHTML;
// newHTML = '<h2>Your vote is counted</h2>';
// newHTML += '<p>The average rating for this movie is ';
// newHTML += data + '.</p>';
// $('#message').html(newHTML);
// }
