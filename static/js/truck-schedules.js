"use strict";

// function initMyMap(latt, longi, start_time, end_time, truck_name) {
    
//     console.log(latt, longi);
//     var mapDiv = document.getElementById('map');

    
//     var map = new google.maps.Map(mapDiv, {
//         center: {lat: latt, lng: longi},
//         zoom: 15,
//         mapTypeControl: true,
//         zoomControl: true,
//         scaleControl: false,
//         streetViewControl: true,
//         rotateControl: true
        
//     });

//     console.log(end_time);
//     if (end_time > 12:00:00){
//         console.log("in the if loop");
//         end_time = end_time - 12:00:00;
//     }
//     console.log(end_time);


//     var marker = new google.maps.Marker({
//         position: {lat: latt, lng: longi},
//         map: map,
//         title: 'Hours: ' + start_time + " - "+ end_time,
//         icon: 'http://imageshack.com/a/img924/7348/BZGR4q.png'
        
//         });
    
//     console.log(map);
// }

        
// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.

function initMyMap(latt, longi, start_time, end_time, truck_name){
  var map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: latt, lng: longi},
    zoom: 9,
    mapTypeControl: true,
    zoomControl: true,
    scaleControl: false,
    streetViewControl: true,
    rotateControl: true

  });
  var marker = new google.maps.Marker({
        position: {lat: latt, lng: longi},
        map: map,
        title: 'Hours: ' + start_time + " - "+ end_time,
        icon: 'http://imageshack.com/a/img924/7348/BZGR4q.png'
        
        });

  var infoWindow = new google.maps.InfoWindow({map: map});

  // Try HTML5 geolocation.
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };

      infoWindow.setPosition(pos);
      infoWindow.setContent('Location found.');
      map.setCenter(pos);
    }, function() {
      handleLocationError(true, infoWindow, map.getCenter());
    });
  } else {
    // Browser doesn't support Geolocation
    handleLocationError(false, infoWindow, map.getCenter());
  }
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(browserHasGeolocation ?
                        'Error: The Geolocation service failed.' :
                        'Error: Your browser doesn\'t support geolocation.');
}


// send the event to function for evaluation
function submitSchedule(evt) {
    //stop the default event
    evt.preventDefault();

    var formInputs = {
        "day": $("#day").val(),
        "truck_id": $("#truck-id").val()
    };
    console.log(formInputs);
    // TO DO: Comment out before career day
    debugger;
    
    $.get("/truck_schedule", 
    	   formInputs, function (myScheduleDict)
           {
            //Immediately check to see if the object is empty
            if(jQuery.isEmptyObject(myScheduleDict))
                {
                    // Styling for the map div when there is no map to render.  
                    // This overwrites the big blank box or other messages already in
                    // the div and done in javascript not jQuery just because it
                    // is good to know both methods 6/20/2016
                    document.getElementById('map').style.backgroundColor="#151515";                    
                    document.getElementById('map').innerHTML = "";
                    document.getElementById('map').style.color="#32CD32"; 
                    document.getElementById('map').style.font = "26px Rancho";
                    document.getElementById('map').innerHTML += '<br>No schedule available for date selected. Please pick another date.';
                    
                }
            else 
                {
                    initMyMap(myScheduleDict.lattitude, myScheduleDict.longitude, myScheduleDict.start_time, myScheduleDict.end_time, myScheduleDict.truck_name);
                }
           });
}// End of anonymous success function from AJAX call


///////////////////////////////////
// Click event button for truck.html
// 
$("#display-schedule").on("submit", submitSchedule);




