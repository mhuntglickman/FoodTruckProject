"use strict";



function initMyMap(latt, longi) {
    console.log("yo we be here");
    var mapDiv = document.getElementById('map');

    var map = new google.maps.Map(mapDiv, {
        center: {lat: latt, lng: longi},
        zoom: 15,
        mapTypeControl: true,
        zoomControl: true,
        scaleControl: false,
        streetViewControl: true,
        rotateControl: true
   
    });
    var marker = new google.maps.Marker({
        position: {lat: latt, lng: longi},
        map: map,
        title: 'Change Me'
        });
    
    console.log(map);
}
    


// send the event to function for evaluation
function submitSchedule(evt) {
    //stop the default event
    evt.preventDefault();

    var formInputs = {
        "day": $("#day").val(),
        "truck_id": $("#truck-id").val()
    };
    console.log('form inputs created');
    $.get("/truck_schedule", 
    	   formInputs, function (myScheduleDict){
            console.log(myScheduleDict);
            console.log(myScheduleDict.lattitude, myScheduleDict.longitude);
            initMyMap(myScheduleDict.lattitude, myScheduleDict.longitude);
            // Still need to create the info box with start and end times for the 
            // date user selected
           });
}

$("#display-schedule").on("submit", submitSchedule);